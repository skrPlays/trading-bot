"""
For type-hinting, use stub files i.e. .pyi files

Use a static type checker that analyzes the code and tries to detect if we are violating the Type-Hints or not.
The best known type checker is “mypy“. We can install it as below:-

>> pip install mypy

To run the code now, we have to simply call the Python interpreter and we have to specify “-m” to indicate that
we want to load a module and then specify the script which we want to check. For example:

mypy program.py

https://docs.python.org/3/library/typing.html

https://stackoverflow.com/questions/35602541/create-pyi-files-automatically
"""

from typing import Any, Collection

def read_file(file_name: str) -> Any: ...
def write_file(data: Collection, file_name: str, append: str) -> None: ...
def get_directory(name: str) -> str: ...
