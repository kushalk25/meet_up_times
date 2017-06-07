
import datetime
from dateutil import relativedelta

filename = "calendar.csv"
f = open(filename, 'r')

now = datetime.datetime.now().replace(microsecond=0, hour=0, minute=0, second=0)
next_week = now + relativedelta.relativedelta(weeks = 1)

schedule = []

# put all intervals into schedule array
date = f.readline()
while date:
    date = [s.strip() for s in date.split(",")]
    start = datetime.datetime.strptime(date[1], "%Y-%m-%d %H:%M:%S")
    end = datetime.datetime.strptime(date[2], "%Y-%m-%d %H:%M:%S")

    if not (start > next_week or end < now):
        if start < now and end > next_week:
            schedule.append((now, next_week,))
        elif start < now:
            schedule.append((now, end,))
        elif end > next_week:
            schedule.append((start, next_week,))
        else:
            schedule.append((start, end,))

    date = f.readline()

iterator = now

# input times that are unavailable 8am-10pm
while iterator < next_week:
    schedule.append((iterator, iterator+relativedelta.relativedelta(hours=8)))
    schedule.append((iterator+relativedelta.relativedelta(hours=22), iterator+relativedelta.relativedelta(days=1)))
    iterator += relativedelta.relativedelta(days = 1)

schedule = sorted(schedule, key=lambda time: time[0])

free = []
last = schedule[0][1]

# add available time intervals
for time in schedule[1:]:
    if time[1] < last:
        continue

    if time[0] > last:
        free.append((last, time[0],))

    last = time[1]

max_delta = datetime.timedelta(0)
largest_block = None

# find biggest time interval
for time in free:
    delta = time[1] - time[0]
    if delta > max_delta:
        largest_block = time
        max_delta = delta

if not largest_block:
    print("No free times this week")
else:
    print("Longest free block: {} to {}".format(
            largest_block[0].strftime("%Y-%m-%d %H:%M:%S"),
            largest_block[1].strftime("%Y-%m-%d %H:%M:%S")
        )
    )
