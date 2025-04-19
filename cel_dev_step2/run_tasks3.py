from tasks import add2
res = add2.delay(4, 4)
print(res.get())