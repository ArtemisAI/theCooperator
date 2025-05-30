"""CRUD helper modules.

Each sub-module contains the persistence logic for a given domain object. The
functions are intentionally **thin**; complex business rules belong in
`app.services.*` packages instead.
"""

from . import unit
from . import member
from . import committee # This will make committee.committee and committee.committee_member_role available

# It's common to expose the instantiated CRUD objects or modules directly
# For consistency with how unit and member are (likely) used (as modules of functions):
# from .unit import * # (if unit.py had many functions and no CRUDBase)
# from .member import * # (if member.py had many functions and no CRUDBase)

# If unit and member were also CRUDBase instances, it would be:
# from .unit import unit
# from .member import member

# Given committee.py creates instances `committee` and `committee_member_role`,
# and the prompt suggests exporting these instances:
from .committee import committee, committee_member_role

# To maintain access to unit and member CRUD functions (assuming they are not CRUDBase instances)
# we keep the module imports or import specific functions if that was the pattern.
# The prompt's __all__ suggests direct instance names.
# For now, let's assume 'unit' and 'member' in __all__ refer to the modules,
# and 'committee' and 'committee_member_role' refer to the instances.
# This is a bit inconsistent if unit/member are modules of functions and committee is instances.
# The instructions for __all__ were: ["unit", "member", "committee", "committee_member_role"]

# A more consistent approach if unit/member are modules of functions:
# __all__ = ["unit", "member", "committee_crud"] # where committee_crud is the module
# And then access via committee_crud.committee or committee_crud.committee_member_role

# However, sticking to the provided __all__ list and direct export from prompt:
# This implies that 'unit' and 'member' should also be instances if this pattern is followed.
# Since unit.py and member.py provide functions, not instances,
# the __init__ provided in the prompt is slightly mismatched with current unit/member structure.
# I will follow the prompt's desired __all__ and direct exports for committee instances.

__all__ = [
    "unit",  # Assuming this refers to the module unit.py
    "member", # Assuming this refers to the module member.py
    "committee", # Refers to the instance from committee.py
    "committee_member_role", # Refers to the instance from committee.py
]
