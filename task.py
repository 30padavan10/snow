


# def decorator_arg(a, b):
#     def decorator(func):
#         def wrapper(*args):
#             return f'{a} {b}' + func(*args)
#         return wrapper
#     return decorator
#
# @decorator_arg(2,3)
# def func(c):
#     return f'a + b + {c}'
#
#
#
# print(func(5))
ddf = []
df = (1, 3)
ddf.append(df)
for i in ddf:
    cont, res = i
    print(cont)
    print(res)



