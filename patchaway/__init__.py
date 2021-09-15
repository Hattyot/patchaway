import ctypes
import numbers
import sys
import collections.abc
import gc
from functools import wraps
from contextlib import contextmanager
from .structures import (
    PyTypeObject_fields,
    PySequenceMethods_fields,
    PyAsyncMethods_fields,
    PyNumberMethods_fields,
    PyMappingMethods_fields,
    PyTypeObject
)

sys.dont_write_bytecode = True
storage = {}
reverse_storage = {}


def get_tp_as_name(klass, method):
    if method in ['__await__', '__aiter__', '__anext__']:
        return 'tp_as_async'

    if isinstance(klass, type):
        if issubclass(klass, numbers.Number):
            return 'tp_as_number'
        if issubclass(klass, collections.abc.Sequence):
            return 'tp_as_sequence'
        if issubclass(klass, collections.abc.Mapping):
            return 'tp_as_mapping'


dunder_dict = {
    'tp_as_number': {},
    'tp_as_async': {},
    'tp_as_sequence': {},
    'tp_as_mapping': {},
    None: {}
}

tp_as_dict = {
    'nb': "tp_as_number",
    'am': "tp_as_async",
    'sq': "tp_as_sequence",
    'mp': "tp_as_mapping"
}

for field in PyNumberMethods_fields + PyAsyncMethods_fields + PySequenceMethods_fields + PyMappingMethods_fields + PyTypeObject_fields:
    dunders = field[2:]
    for dunder in dunders:
        tp_as_name = tp_as_dict.get(field[0][:2])
        dunder_dict[tp_as_name][dunder] = field[:2]


def dunder_patch(klass, attribute, value):
    tp_as_name = get_tp_as_name(klass, attribute)
    c_method, c_func_t = dunder_dict[tp_as_name][attribute]
    c_object = PyTypeObject.from_address(id(klass))

    # string value for dunder property
    if c_func_t == ctypes.c_char_p:
        assert type(value) == str
        new_value = value.encode('utf-8')
    # object value for dunder property
    elif c_func_t == ctypes.py_object:
        new_value = value
    # function value for dunder
    else:
        @wraps(value)
        def wrapper(*args, **kwargs):
            return value(*args, **kwargs)

        if tp_as_name:
            tp_as_pointer = getattr(c_object, tp_as_name)
            c_object = tp_as_pointer.contents

        c_func = c_func_t(wrapper)
        # for some weird reason, without this, a segmentation fault happens
        storage[(klass, attribute)] = c_func
        new_value = c_func

    reverse_storage[(klass, attribute)] = ctypes.cast(getattr(c_object, c_method), c_func_t)
    setattr(c_object, c_method, new_value)


def dunder_unpatch(klass, attribute):
    tp_as_name = get_tp_as_name(klass, attribute)
    c_method, c_func_t = dunder_dict[tp_as_name][attribute]
    c_object = PyTypeObject.from_address(id(klass))

    tp_as_pointer = getattr(c_object, tp_as_name)
    if tp_as_pointer:
        c_object = tp_as_pointer.contents

    setattr(c_object, c_method, reverse_storage[(klass, attribute)])
    del reverse_storage[(klass, attribute)]


def patch(klass, attribute, value):
    if attribute.startswith('__') and attribute.endswith('__'):
        return dunder_patch(klass, attribute, value)

    values = gc.get_referents(klass.__dict__)[0]
    reverse_storage[(klass, attribute)] = values.get(attribute, None)
    values[attribute] = value
    # Invalidate the internal lookup cache for the type and all of its subtypes
    ctypes.pythonapi.PyType_Modified(ctypes.py_object(klass))


def unpatch(klass, attribute):
    if (klass, attribute) not in reverse_storage:
        raise ValueError(f'Method {attribute} for class {klass} was never patched.')

    if attribute.startswith('__') and attribute.endswith('__'):
        return dunder_unpatch(klass, attribute)

    reverse = reverse_storage[(klass, attribute)]
    values = gc.get_referents(klass.__dict__)[0]
    if reverse is None:
        del values[attribute],
    else:
        values[attribute] = reverse_storage[(klass, attribute)]

    # Invalidate the internal lookup cache for the type and all of its subtypes
    ctypes.pythonapi.PyType_Modified(ctypes.py_object(klass))


@contextmanager
def patcher(obj, attr, val):
    patch(obj, attr, val)
    try:
        yield
    finally:
        unpatch(obj, attr)
