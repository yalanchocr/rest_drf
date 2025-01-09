from tasks import add
res = add.delay(4, 4)
# print(res.get())