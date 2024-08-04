from typing import Any

from aiowialon.generics.core import *
from strong_typing import serialization



def myfunc(*args: Any, **kwargs: TSearchAction):
    print(kwargs)


# myfunc(spec={'propName': 'value', 'propValueMask': ''})

ex_data = {
    "spec": {
        "itemsType": "",
        "propName": "",
        "propValueMask": "",
        "sortType": "",
        # "propType": "",
        # "or_logic": False
    },
    "force": True,
    "flags": 0,
    "from": 0,
    "to": 0
}

o = serialization.json_to_object(
    TSearchAction, ex_data
)

print(o)


print(serialization.object_to_json(ex_data))
print(serialization.object_to_json(o))

myfunc()
