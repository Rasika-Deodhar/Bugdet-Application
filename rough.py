import datetime

x = datetime.datetime.now()
print(x.date().day, x.date().month, x.date().year)

x = datetime.datetime(2020, 5, 17)
print(x.date().day, x.date().month, x.date().year)


