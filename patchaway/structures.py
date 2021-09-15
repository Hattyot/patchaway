import ctypes


class PyObject(ctypes.Structure):
    _fields_ = [
        ('ob_refcnt', ctypes.c_ssize_t),
        ('ob_type', ctypes.py_object)
    ]

    def incref(self):
        self.ob_refcnt += 1

    def decref(self):
        self.ob_refcnt -= 1


inquiry = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object)
unaryfunc = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object)
binaryfunc = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object)
ternaryfunc = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object, ctypes.py_object)
quaternaryfunc = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.py_object, ctypes.py_object, ctypes.py_object, ctypes.py_object)
lenfunc = ctypes.CFUNCTYPE(ctypes.c_ssize_t, ctypes.py_object)
ssizeargfunc = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.c_ssize_t)
ssizeobjargproc = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.c_ssize_t)
objobjproc = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.py_object)
ssizessizeargfunc = ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.c_ssize_t, ctypes.c_ssize_t)
ssizessizeobjargproc = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.c_ssize_t, ctypes.c_ssize_t, ctypes.py_object)
visitproc = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.c_void_p)


class Pybuffer(ctypes.Structure):
    _fields_ = [
        ('buf', ctypes.c_void_p),
        ('obj', ctypes.py_object),
        ('len', ctypes.c_ssize_t),
        ('itemsize', ctypes.c_ssize_t),
        ('readonly', ctypes.c_int),
        ('ndim', ctypes.c_int),
        ('format', ctypes.c_char_p),
        ('shape', ctypes.POINTER(ctypes.c_ssize_t)),  # ssize_t pointer?
        ('strides', ctypes.POINTER(ctypes.c_ssize_t)),  # ssize_t pointer?
        ('suboffsets', ctypes.POINTER(ctypes.c_ssize_t)),  # ssize_t pointer?
        ('smalltable', ctypes.c_ssize_t * 2),
        ('internal', ctypes.c_void_p)
    ]


class PyBufferProcs(ctypes.Structure):
    _fields_ = [
        ('bf_getreadbuffer', ctypes.CFUNCTYPE(ctypes.c_ssize_t, ctypes.py_object, ctypes.c_ssize_t, ctypes.POINTER(ctypes.c_void_p))),
        ('bf_getwritebuffer', ctypes.CFUNCTYPE(ctypes.c_ssize_t, ctypes.py_object, ctypes.c_ssize_t, ctypes.POINTER(ctypes.c_void_p))),
        ('bf_getsegcount', ctypes.CFUNCTYPE(ctypes.c_ssize_t, ctypes.py_object, ctypes.POINTER(ctypes.c_ssize_t))),
        ('bf_getcharbuffer', ctypes.CFUNCTYPE(ctypes.c_ssize_t, ctypes.py_object, ctypes.c_ssize_t, ctypes.POINTER(ctypes.c_void_p))),
        ('bf_getbuffer', ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.POINTER(Pybuffer), ctypes.c_int)),
        ('bf_releasebuffer', ctypes.CFUNCTYPE(None, ctypes.py_object, ctypes.POINTER(Pybuffer))),
    ]


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
    ('nb_inplace_subtract', binaryfunc, '__sub__'),
    ('nb_inplace_multiply', binaryfunc, '__mul__', '__rmul__'),
    ('nb_inplace_remainder', binaryfunc, '__mod__'),
    ('nb_inplace_power', ternaryfunc, '__pow__'),
    ('nb_inplace_lshift', binaryfunc, '__lshift__'),
    ('nb_inplace_rshift', binaryfunc, '__rshift__'),
    ('nb_inplace_and', binaryfunc, '__and__', '__rand__'),
    ('nb_inplace_xor', binaryfunc, '__xor__', '__rxor__'),
    ('nb_inplace_or', binaryfunc, '__or__'),

    ('nb_floor_divide', binaryfunc, '__floordiv__'),
    ('nb_true_divide', binaryfunc, '__truediv__'),
    ('nb_inplace_floor_divide', binaryfunc, '__floordiv__'),
    ('nb_inplace_true_divide', binaryfunc, '__truediv__'),

    ('nb_index', unaryfunc, '__index__'),
]

PySequenceMethods_fields = [
    ('sq_length', lenfunc, '__len__'),
    ('sq_concat', binaryfunc, '__add__'),
    ('sq_repeat', ssizeargfunc, '__mul__'),
    ('sq_item', ssizeargfunc),
    ('was_sq_slice', ssizessizeargfunc),
    ('sq_ass_item', ssizeobjargproc, '__setitem__', '__delitem__'),
    ('was_sq_ass_slice', ssizessizeobjargproc),  # was_sq_ass_slice in python 3
    ('sq_contains', objobjproc, '__contains__'),
    ('sq_inplace_concat', binaryfunc, '__iadd__'),
    ('sq_inplace_repeat', ssizeargfunc, '__imul__'),
]

PyAsyncMethods_fields = [
    ('am_await', unaryfunc, '__await__'),
    ('am_aiter', unaryfunc, '__aiter__'),
    ('am_anext', unaryfunc, '__anext__')
]


PyMappingMethods_fields = [
    ('mp_length', lenfunc, '__len__'),
    ('mp_subscript', binaryfunc, '__getitem__'),
    ('mp_ass_subscript', ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.py_object, ctypes.py_object), '__setitem__', '__delitem__')
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
    ('tp_getattr', ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object)),
    ('tp_setattr', ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.c_char_p, ctypes.py_object)),
    ('tp_as_async', ctypes.POINTER(PyAsyncMethods)),
    ('tp_repr', ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object), '__repr__'),
    ('tp_as_number', ctypes.POINTER(PyNumberMethods)),
    ('tp_as_sequence', ctypes.POINTER(PySequenceMethods)),
    ('tp_as_mapping', ctypes.POINTER(PyMappingMethods)),
    ('tp_hash', ctypes.CFUNCTYPE(ctypes.c_int64, ctypes.py_object), '__hash__'),
    ('tp_call', ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object, ctypes.py_object), '__call__'),
    ('tp_str', ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object), '__str__'),
    ('tp_getattro', ctypes.CFUNCTYPE(ctypes.py_object, ctypes.py_object, ctypes.py_object), '__getattr__', '__getattribute__'),
    ('tp_setattro', ctypes.CFUNCTYPE(ctypes.c_int, ctypes.py_object, ctypes.py_object, ctypes.py_object), '__setattr__'),
    ('tp_as_buffer', ctypes.POINTER(PyBufferProcs)),
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
PyMappingMethods._fields_ = [field[:2] for field in PyMappingMethods_fields]
