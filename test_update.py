from db import *

print("Before:", get_balance())

update_balance(500)

print("After:", get_balance())