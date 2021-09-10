from datetime import datetime, timedelta


def read_log(month=None, year=2020):
    with open("log.txt", 'r') as f:
        times = []
        for line in f:
            line = line.strip().split(" ")[:2]
            date = datetime.strptime(line[0], "%Y-%m-%d")
            time = line[1].split(',')[0].split(":")
            time = [int(x) for x in time]
            date = date.replace(minute=time[1], hour=time[0], second=time[2])
            if month:
                if date.month == month and date.year == year:
                    times.append(date)
            else:
                times.append(date)
    return times


def calculate_time(t, times):
    data = []
    start = None
    mid = None
    for time in times:
        if not start:
            start = time
            mid = None
        elif not mid:
            if time > start + timedelta(minutes=t):
                data.append([start, start + timedelta(minutes=t)])
                mid = None
                start = time
            else:
                mid = time
        else:
            if time > mid + timedelta(minutes=t):
                data.append([start, mid + timedelta(minutes=t)])
                mid = None
                start = time
            else:
                mid = time
    if not mid:
        mid = start
    data.append([start, mid + timedelta(minutes=t)])
    total_s = 0
    for d in data:
        start = d[0]
        end = d[1]
        time_s = (end - start).total_seconds()
        total_s += time_s
    total_time = timedelta(seconds=total_s)
    # print(total_s)
    # print(f"El tiempo trabajado fue de {total_time} para el {month}/{year}")
    return total_time


if __name__ == "__main__":
    t = 10
    month = 5
    year = 2020
    times = read_log(month, year)
    total_time = calculate_time(t, times)
    print(f"El tiempo trabajado fue de {total_time} para el {month}/{year}")

