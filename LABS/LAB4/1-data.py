import datetime 

#1
x = datetime.datetime.now()
print(x.strftime("%d") , x.strftime("%m") , x.strftime("%Y") )
y = x - datetime.timedelta(days=5)
print(y.strftime("%d") , y.strftime("%m") , y.strftime("%Y") )

#2 

today = datetime.date.today()

tomorrow = today + datetime.timedelta(days=1)
yesterday = today - datetime.timedelta(days=1)
print(yesterday)
print(today)
print(tomorrow)

#3 

xtime = datetime.datetime.now()
print("with microseconds" , xtime)

without_microseconds = xtime.replace(microsecond=0)
print("without_microseconds", without_microseconds)

# 4
date1 = datetime.datetime(2025, 2, 15, 10, 0, 0)
date2 = datetime.datetime(2025, 2, 15, 10, 5, 30)


difference = (date2 - date1).total_seconds()

print(difference)
