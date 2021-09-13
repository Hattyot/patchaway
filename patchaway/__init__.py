import ctypes
from functools import wraps


Inquiry_p = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object)
UnaryFunc_p = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object)
BinaryFunc_p = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object)
TernaryFunc_p = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object, ctypes.py_object)
LenFunc_p = ctypes.CFUNCTYPE(ctypes.c_ssize_t, ctypes.py_object)
SSizeArgFunc_p = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.c_ssize_t)
SSizeObjArgProc_p = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.c_ssize_t, ctypes.py_object)
ObjObjProc_p = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.py_object)
visitproc = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.c_void_p)


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
    ('nb_add', ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object), '__add__', '__radd__'),
    ('nb_subtract', BinaryFunc_p, '__sub__', '__rsub__'),
    ('nb_multiply', BinaryFunc_p, '__mul__', '__rmul__'),
    ('nb_remainder', BinaryFunc_p, '__mod__', '__rmod__'),
    ('nb_divmod', BinaryFunc_p, '__divmod__', '__rdivmod__'),
    ('nb_power', TernaryFunc_p, '__pow__', '__rpow__'),
    ('nb_negative', UnaryFunc_p, '__neg__'),
    ('nb_positive', UnaryFunc_p, '__pos__'),
    ('nb_absolute', UnaryFunc_p, '__abs__'),
    ('nb_bool', Inquiry_p, '__bool__'),
    ('nb_invert', UnaryFunc_p, '__invert__'),
    ('nb_lshift', BinaryFunc_p, '__lshift__', '__rlshift__'),
    ('nb_rshift', BinaryFunc_p, '__rshift__', '__rrshift__'),
    ('nb_and', BinaryFunc_p, '__and__', '__rand__'),
    ('nb_xor', BinaryFunc_p, '__xor__', '__rxor__'),
    ('nb_or', BinaryFunc_p, '__or__', '__ror__'),
    ('nb_int', UnaryFunc_p, '__int__'),
    ('nb_reserved', ctypes.c_void_p),
    ('nb_float', UnaryFunc_p, '__float__'),

    ('nb_inplace_add', BinaryFunc_p, '__iadd__'),
    ('nb_inplace_subtract', BinaryFunc_p),
    ('nb_inplace_multiply', BinaryFunc_p),
    ('nb_inplace_remainder', BinaryFunc_p),
    ('nb_inplace_power', TernaryFunc_p),
    ('nb_inplace_lshift', BinaryFunc_p),
    ('nb_inplace_rshift', BinaryFunc_p),
    ('nb_inplace_and', BinaryFunc_p),
    ('nb_inplace_xor', BinaryFunc_p),
    ('nb_inplace_or', BinaryFunc_p),

    ('nb_floor_divide', BinaryFunc_p, '__floordiv__'),
    ('nb_true_divide', BinaryFunc_p, '__truediv__'),
    ('nb_inplace_floor_divide', BinaryFunc_p),
    ('nb_inplace_true_divide', BinaryFunc_p),

    ('nb_index', UnaryFunc_p, '__index__'),

    # ('nb_matrix_multiply', BinaryFunc_p, '__matmul__', '__rmatmul__'),
    # ('nb_inplace_matrix_multiply', BinaryFunc_p),
]

PySequenceMethods_fields = [
    ('sq_length', LenFunc_p, '__len__'),
    ('sq_concat', BinaryFunc_p, '__add__'),
    # ('sq_concat', BinaryFunc_p),
    ('sq_repeat', SSizeArgFunc_p, '__mul__'),
    ('sq_item', SSizeArgFunc_p, '__getitem__'),
    ('was_sq_slice', ctypes.c_void_p),
    ('sq_ass_item', SSizeObjArgProc_p, '__setitem__', '__delitem__'),
    ('was_sq_ass_slice', ctypes.c_void_p),
    ('sq_contains', ObjObjProc_p, '__contains__'),
    ('sq_inplace_concat', BinaryFunc_p, '__iadd__'),
    ('sq_inplace_repeat', SSizeArgFunc_p, '__imul__'),
]

PyAsyncMethods_fields = [
    ('am_await', UnaryFunc_p, '__await__'),
    ('am_aiter', UnaryFunc_p, '__aiter__'),
    ('am_anext', UnaryFunc_p, '__anext__')
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


class IntStruct (ctypes.Structure):
    # declaration of fields
    _fields_ = [("ob_refcnt", ctypes.c_long),
                ("ob_type", ctypes.c_void_p),
                ("ob_size", ctypes.c_long),
                ("ob_digit", ctypes.c_int)]


def dunder_patch(klass, method, value):
    c_method, c_func_t, tp_as_name = dunder_dict[method]
    c_object = PyTypeObject.from_address(id(klass))

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
