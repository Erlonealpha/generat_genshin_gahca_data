from datetime import datetime, timedelta
import random
def random_time(start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
    time_between_dates = end - start

    random_second = random.randint(0, time_between_dates.total_seconds())
    random_date = start + timedelta(seconds=random_second)

    random_date_str = random_date.strftime('%Y-%m-%d %H:%M:%S')
    return random_date_str

def convert_time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

def random_time_within_day_bounds(date, min_time, max_time):
    min_seconds = convert_time_to_seconds(min_time)
    max_seconds = convert_time_to_seconds(max_time)
    random_seconds = random.randint(min_seconds, max_seconds)
    return (datetime.combine(date, datetime.min.time()) + timedelta(seconds=random_seconds)).strftime('%Y-%m-%d %H:%M:%S')

def random_time_(start_date, end_date, min_time, max_time):
    start = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').date()
    end = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').date()
    random_date = start + timedelta(days=random.randint(0, (end - start).days))
    return random_time_within_day_bounds(random_date, min_time, max_time)

def generate_random_times(start_date, end_date, count, min_time='08:30:00', max_time='23:00:00'):
    start = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').date()
    end = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S').date()
    random_dates = [start + timedelta(days=random.randint(0, (end - start).days)) for _ in range(count)]
    random_times = [random_time_within_day_bounds(date, min_time, max_time) for date in random_dates]

    return sorted(random_times)
