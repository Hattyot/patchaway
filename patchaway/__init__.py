import ctypes
from functools import wraps
import gc

inquiry = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object)
unaryfunc = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object)
binaryfunc = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object)
ternaryfunc = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object, ctypes.py_object)
lenfunc = ctypes.CFUNCTYPE(ctypes.c_ssize_t, ctypes.py_object)
ssizeargfunc = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.c_ssize_t)
ssizeobjargproc = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.c_ssize_t, ctypes.py_object)
objobjproc = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.py_object)
visitproc = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.c_void_p)


class IntStruct (ctypes.Structure):
    # declaration of fields
    _fields_ = [("ob_refcnt", ctypes.c_long),
                ("ob_type", ctypes.c_void_p),
                ("ob_size", ctypes.c_long),
                ("ob_digit", ctypes.c_long)]

    def value(self):
        return self.ob_digit


class PyObject(ctypes.Structure):
    _fields_ = [
        ('ob_refcnt', ctypes.c_ssize_t),
        ('ob_type', ctypes.py_object)
    ]

    def incref(self):
        self.ob_refcnt += 1

    def decref(self):
        self.ob_refcnt -= 1


class PyFile(ctypes.Structure):
    pass


class PyNumberMethods(ctypes.Structure):
    pass


class PySequenceMethods(ctypes.Structure):
    pass


class PyMappingMethods(ctypes.Structure):
    pass


class PyAsyncMethods(ctypes.Structure):
    pass


class Pybuffer(ctypes.Structure):
    _fields_ = [
        ('buf', ctypes.c_void_p),
        ('obj', ctypes.c_void_p),
        ('len', ctypes.c_ssize_t),
        ('readonly', ctypes.c_int),
        ('itemsize', ctypes.c_ssize_t),
        ('format', ctypes.c_char_p),
        ('ndim', ctypes.c_int),
        ('shape', ctypes.c_ssize_t),  # ssize_t pointer?
        ('strides', ctypes.c_ssize_t),  # ssize_t pointer?
        ('suboffsets', ctypes.c_ssize_t),  # ssize_t pointer?
        ('internal', ctypes.c_void_p)
    ]


class PyBufferProcs(ctypes.Structure):
    _fields_ = [
        ('bf_getbuffer', ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, Pybuffer, ctypes.c_int)),
        ('bf_releasebuffer', ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.py_object, Pybuffer)),
    ]


class PyTypeObject(ctypes.Structure):
    pass


PyNumberMethods_fields = [
    ('nb_add', binaryfunc, '__add__', '__radd__'),
    ('nb_subtract', binaryfunc, '__sub__', '__rsub__'),
    ('nb_multiply', binaryfunc, '__mul__', '__rmul__'),
    ('nb_remainder', binaryfunc, '__mod__', '__rmod__'),
    ('nb_divmod', binaryfunc, '__divmod__', '__rdivmod__'),
    ('nb_power', ternaryfunc, '__pow__', '__rpow__'),
    ('nb_negative', unaryfunc, '__neg__'),
    ('nb_positive', unaryfunc, '__pos__'),
    ('nb_absolute', unaryfunc, '__abs__'),
    ('nb_bool', inquiry, '__bool__'),
    ('nb_invert', unaryfunc, '__invert__'),
    ('nb_lshift', binaryfunc, '__lshift__', '__rlshift__'),
    ('nb_rshift', binaryfunc, '__rshift__', '__rrshift__'),
    ('nb_and', binaryfunc, '__and__', '__rand__'),
    ('nb_xor', binaryfunc, '__xor__', '__rxor__'),
    ('nb_or', binaryfunc, '__or__', '__ror__'),
    ('nb_int', unaryfunc, '__int__'),
    ('nb_reserved', ctypes.c_void_p),
    ('nb_float', unaryfunc, '__float__'),

    ('nb_inplace_add', binaryfunc, '__iadd__'),
    ('nb_inplace_subtract', binaryfunc),
    ('nb_inplace_multiply', binaryfunc),
    ('nb_inplace_remainder', binaryfunc),
    ('nb_inplace_power', ternaryfunc),
    ('nb_inplace_lshift', binaryfunc),
    ('nb_inplace_rshift', binaryfunc),
    ('nb_inplace_and', binaryfunc),
    ('nb_inplace_xor', binaryfunc),
    ('nb_inplace_or', binaryfunc),

    ('nb_floor_divide', binaryfunc, '__floordiv__'),
    ('nb_true_divide', binaryfunc, '__truediv__'),
    ('nb_inplace_floor_divide', binaryfunc),
    ('nb_inplace_true_divide', binaryfunc),

    ('nb_index', unaryfunc, '__index__'),

    # ('nb_matrix_multiply', binaryfunc, '__matmul__', '__rmatmul__'),
    # ('nb_inplace_matrix_multiply', binaryfunc),
]

PySequenceMethods_fields = [
    ('sq_length', lenfunc, '__len__'),
    ('sq_concat', binaryfunc, '__add__'),
    # ('sq_concat', binaryfunc),
    ('sq_repeat', ssizeargfunc, '__mul__'),
    ('sq_item', ssizeargfunc, '__getitem__'),
    ('was_sq_slice', ctypes.c_void_p),
    ('sq_ass_item', ssizeobjargproc, '__setitem__', '__delitem__'),
    ('was_sq_ass_slice', ctypes.c_void_p),
    ('sq_contains', objobjproc, '__contains__'),
    ('sq_inplace_concat', binaryfunc, '__iadd__'),
    ('sq_inplace_repeat', ssizeargfunc, '__imul__'),
]

PyAsyncMethods_fields = [
    ('am_await', unaryfunc, '__await__'),
    ('am_aiter', unaryfunc, '__aiter__'),
    ('am_anext', unaryfunc, '__anext__')
]

PyTypeObject_fields = [
    # head
    ('ob_base', PyObject),
    ('ob_size', ctypes.c_ssize_t),
    ('tp_name', ctypes.c_char_p, '__name__'),
    ('tp_basicsize', ctypes.c_ssize_t),
    ('tp_itemsize', ctypes.c_ssize_t),
    ('tp_dealloc', ctypes.CFUNCTYPE(None, ctypes.py_object)),
    ('tp_vectorcall_offset', ctypes.c_ssize_t),
    ('tp_getattr', ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object), '__getattr__', '__getattribute__'),
    ('tp_setattr', ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.c_char_p, ctypes.py_object), '__setattr__'),
    ('tp_as_async', ctypes.CFUNCTYPE(PyAsyncMethods)),
    ('tp_repr', ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object), '__repr__'),
    ('tp_as_number', ctypes.POINTER(PyNumberMethods)),
    ('tp_as_sequence', ctypes.POINTER(PySequenceMethods)),
    ('tp_as_mapping', ctypes.POINTER(PyMappingMethods)),
    ('tp_hash', ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.py_object), '__hash__'),
    ('tp_call', ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object, ctypes.py_object), '__call__'),
    ('tp_str', ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object), '__str__'),
    ('tp_getattro', ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object)),
    ('tp_setattro', ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.py_object, ctypes.py_object)),
    ('tp_as_buffer', ctypes.POINTER(PyBufferProcs)),  # undefined
    ('tp_flags', ctypes.c_ulong),
    ('tp_doc', ctypes.c_char_p, '__doc__'),
    ('tp_traverse', ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, visitproc, ctypes.c_void_p)),  # undefined
    ('tp_clear', ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object)),
    ('tp_richcompare', ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object, ctypes.c_int), '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__'),
    ('tp_weaklistoffset', ctypes.c_ssize_t),
    ('tp_iter', ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object), '__iter__'),
    ('tp_iternext', ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object), '__next__'),
    ('tp_methods', ctypes.c_void_p),  # undefined
    ('tp_members', ctypes.c_void_p),  # undefined
    ('tp_getset', ctypes.c_void_p),  # undefined
    ('tp_base', ctypes.POINTER(PyTypeObject), '__base__'),
    ('tp_dict', ctypes.py_object, '__dict__'),
    ('tp_descr_get', ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object, ctypes.py_object), '__get__'),
    ('tp_descr_set', ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.py_object, ctypes.py_object), '__set__', '__delete__'),
    ('tp_dictoffset', ctypes.c_ssize_t),
    ('tp_init', ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.py_object, ctypes.py_object), '__init__'),
    ('tp_alloc', ctypes.CFUNCTYPE(ctypes.py_object, PyTypeObject, ctypes.c_ssize_t)),
    ('tp_new', ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object, ctypes.c_void_p), '__new__'),
    ('tp_free', ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p)),
    ('tp_is_gc', ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object)),
    ('tp_bases', ctypes.py_object, '__bases__'),
    ('tp_mro', ctypes.py_object, '__mro__'),
    ('tp_cache', ctypes.py_object),
    ('tp_subclasses', ctypes.py_object, '__subclasses__'),
    ('tp_weaklist', ctypes.py_object),
    ('tp_del', ctypes.CFUNCTYPE(None, ctypes.py_object)),
    ('tp_version_tag', ctypes.c_uint),
    ('tp_finalize', ctypes.CFUNCTYPE(None, ctypes.py_object), '__del__'),
    ('tp_vectorcall_offset', ctypes.c_ssize_t),
]

PyNumberMethods._fields_ = [field[:2] for field in PyNumberMethods_fields]
PyTypeObject._fields_ = [field[:2] for field in PyTypeObject_fields]
PySequenceMethods._fields_ = [field[:2] for field in PySequenceMethods_fields]
PyAsyncMethods._fields_ = [field[:2] for field in PyAsyncMethods_fields]

tp_as_dict = {
    'nb': "tp_as_number",
    'am': "tp_as_async",
    'sq': "tp_as_sequence"
}

tp_as_struct_dict = {
    'tp_as_number': PyNumberMethods,
    'tp_as_async': PyAsyncMethods,
    'tp_as_sequence': PySequenceMethods
}

storage = {}

dunder_dict = {}
for field in PyAsyncMethods_fields + PySequenceMethods_fields + PyTypeObject_fields:
    dunders = field[2:]
    for dunder in dunders:
        dunder_dict[dunder] = field[:2] + (tp_as_dict.get(field[0][:2]), )


def dunder_patch(klass, method, value):
    c_method, c_func_t, tp_as_name = dunder_dict[method]
    c_object = PyTypeObject.from_address(id(int))

    if c_func_t == ctypes.c_char_p:
        assert type(value) == str
        new_value = value.encode('utf-8')
    elif c_func_t == ctypes.py_object:
        new_value = value
    else:
        @wraps(value)
        def wrapper(*args, **kwargs):
            return value(*args, **kwargs)

        if tp_as_name:
            tp_as_pointer = getattr(c_object, tp_as_name)
            c_object = tp_as_pointer.contents

        c_func = c_func_t(wrapper)
        # for some weird reason, without this, a segmentation fault happens
        storage[(klass, method)] = c_func
        new_value = c_func

    setattr(c_object, c_method, new_value)


def patch(klass, method, value):
    if method.startswith('__') and method.endswith('__'):
        return dunder_patch(klass, method, value)

    gc.get_referents(klass.__dict__)[0][method] = value
