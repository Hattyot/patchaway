# PatchAway

Patch away all your internal python problems with PatchAway! (does not work on numbers cause of segementation faults)

Based on forbiddenfruit

## Usage
```py
from patchaway import dunder_patch

dunder_patch(list, '__str__', "rekt")

print(str([1, 2, 3]))  # => rekt
```