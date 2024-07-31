from dataclasses import dataclass, asdict

@dataclass
class MyDataClass(dict):
    field1: int
    field2: str

    def __post_init__(self):
        # Initialize the dict with dataclass fields
        super().__init__(asdict(self))

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        self[key] = value

    def __delattr__(self, key):
        super().__delattr__(key)
        del self[key]

# Example usage
my_instance = MyDataClass(field1=123, field2='abc')
print(my_instance)  # Output: {'field1': 123, 'field2': 'abc'}

def my_method(**kwargs):
    print(kwargs)

my_method(**my_instance)  # Output: {'field1': 123, 'field2': 'abc'}
