from cel_dev_step2.tasks import add2
for i in range(100):
    res = add2.delay(i, 4)
    # print(res.get(propagate=False))


# res = add2.apply_async((10, 2), queue='lopri2', countdown=10)
# print(res.get())
