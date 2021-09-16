import _ctypes
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

base_methods = []
async_methods = []
for field in PyNumberMethods_fields + PyAsyncMethods_fields + PySequenceMethods_fields + PyMappingMethods_fields + PyTypeObject_fields:
    dunders = field[2:]

    if field in PyTypeObject_fields:
        base_methods.extend(dunders)

    if field in PyAsyncMethods_fields:
        async_methods.extend(dunders)

    for dunder in dunders:
        tp_as_name = tp_as_dict.get(field[0][:2])
        if not dunder_dict[tp_as_name].get(dunder):
            dunder_dict[tp_as_name][dunder] = [field[:2]]
        else:
            dunder_dict[tp_as_name][dunder].append(field[:2])


def get_tp_as_name(klass, method):
    if method in async_methods:
        return 'tp_as_async'

    if method in base_methods:
        return None

    if isinstance(klass, type):
        # sequences use mapping getitem method for some reason
        if issubclass(klass, collections.abc.Mapping) or method in ['__getitem__', '__setitem__', '__delitem__']:
            return 'tp_as_mapping'
        if issubclass(klass, numbers.Number):
            return 'tp_as_number'
        if issubclass(klass, collections.abc.Sequence):
            return 'tp_as_sequence'


def dunder_patch(klass, attribute, value):
    tp_as_name = get_tp_as_name(klass, attribute)
    for c_method, c_func_t in dunder_dict[tp_as_name][attribute]:
        copied_value = value
        c_object = PyTypeObject.from_address(id(klass))

        # string copied_value for dunder property
        if c_func_t == ctypes.c_char_p:
            assert type(copied_value) == str
            new_value = copied_value.encode('utf-8')
        # object copied_value for dunder property
        elif c_func_t == ctypes.py_object:
            new_value = copied_value
        # function copied_value for dunder
        else:
            @wraps(copied_value)
            def wrapper(*args, **kwargs):
                # mp_ass_subscript does some funky stuff
                # with the __delitem__ method, it sets the last arg to null, but the last arg cant be null if it's
                # a py_object, so it's set to void_p, which gives the id of the returned obj, with delitem, the id is 0
                if c_method == 'mp_ass_subscript' and issubclass(klass, collections.abc.Sequence):
                    index = _ctypes.PyObj_FromPtr(args[1])
                    value = _ctypes.PyObj_FromPtr(args[2]) if args[2] else ctypes.c_void_p()
                    args = [args[0], index, value]

                return copied_value(*args, **kwargs)

            if tp_as_name:
                tp_as_pointer = getattr(c_object, tp_as_name)
                c_object = tp_as_pointer.contents

            c_func = c_func_t(wrapper)
            # for some weird reason, without this, a segmentation fault happens
            storage[(klass, attribute)] = c_func
            new_value = c_func

        reverse_storage[(klass, attribute, c_method)] = ctypes.cast(getattr(c_object, c_method), c_func_t)
        setattr(c_object, c_method, new_value)


def dunder_unpatch(klass, attribute):
    tp_as_name = get_tp_as_name(klass, attribute)
    for c_method, c_func_t in dunder_dict[tp_as_name][attribute]:
        c_object = PyTypeObject.from_address(id(klass))

        if tp_as_name:
            tp_as_pointer = getattr(c_object, tp_as_name)
            if tp_as_pointer:
                c_object = tp_as_pointer.contents

        setattr(c_object, c_method, reverse_storage[(klass, attribute, c_method)])
        del reverse_storage[(klass, attribute, c_method)]


def patch(klass, attribute, value):
    values = gc.get_referents(klass.__dict__)[0]

    if attribute.startswith('__') and attribute.endswith('__'):
        dunder_patch(klass, attribute, value)
    else:
        reverse_storage[(klass, attribute)] = values.get(attribute, None)

    values[attribute] = value
    # Invalidate the internal lookup cache for the type and all of its subtypes
    ctypes.pythonapi.PyType_Modified(ctypes.py_object(klass))


def unpatch(klass, attribute):
    tp_as_name = get_tp_as_name(klass, attribute)
    for c_method, c_func_t in dunder_dict[tp_as_name][attribute]:
        if (klass, attribute, c_method) not in reverse_storage:
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
