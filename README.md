# PatchAway

Patch away all your internal python problems with PatchAway! (does not work on numbers cause of segementation faults)

Based on forbiddenfruit

## Usage
Patch the list __str__ method
```py
from patchaway import patch

patch(list, '__str__', "rekt")
print(str([1, 2, 3]))  # => "rekt"


patch(int, 'hello', lambda: *a, **kw: "Hi!")
number = 2
print(number.hello())  # => "Hi!"

unpatch(int, 'hello')
print(number.hello())  # => AttributeError: 'int' object has no attribute 'hello'

```