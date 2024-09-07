
# import datetime

# def time(func):
#     def wrapper(a, b):
#         res = func(a, b)
#         now = datetime.datetime.now()
#         print(now)
#         return res
#     return wrapper

# @time
# def add(a, b):
#     print(f"a + b = {a + b}")

# add(1, 3)

import datetime
def Time(add):
    def wrapper(a, b):
        now = datetime.datetime.now()
        print(now)
        return add(a, b)
    return wrapper
@Time
def add(a, b):
    print(f"a + b = {a + b}")

# add = Time(add)
add(1, 2)
