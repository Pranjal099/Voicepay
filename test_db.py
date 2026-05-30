from db import get_balance, update_balance

print("Before =", get_balance())

update_balance(500)

print("After =", get_balance())