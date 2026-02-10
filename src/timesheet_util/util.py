import datetime, zoneinfo

def measure_overlap_timedelta(
        datetime_in_1: datetime.datetime,
        datetime_out_1: datetime.datetime,
        datetime_in_2: datetime.datetime,
        datetime_out_2: datetime.datetime
        ) -> datetime.timedelta:
    """
    datetime_in_1 < datetime_out_1
    datetime_in_2 < datetime_out_2

    input:
    [datetime_in_1,     datetime_out_1]
           [datetime_in_2,              datetime_out_2]
    
    output:
           |---timedelta--------------|

    output: the timedelta value of the overlapping region (if any)
    """
    assert datetime_in_1 < datetime_out_1
    assert datetime_in_2 < datetime_out_2

    range_1, range_2 = sorted(
            [(datetime_in_1, datetime_out_1), (datetime_in_2, datetime_out_2)],
            key=lambda x: x[0])

    output = datetime.timedelta(0)
    if range_2[0] < range_1[1]:
        start = range_2[0]
        end = min(range_1[1], range_2[1])
        print(end)
        output = end - start

    return output

def measure_portion(
        datetime_start: datetime.datetime,
        datetime_end: datetime.datetime,
        timedelta: datetime.timedelta) -> float:
    """
    input:
    [datetime_start,         datetime_end]
    |---timedelta-----|

    output:
    |--- %? ----------|
    |--- 100% ---------------------------|
    """

    assert datetime_start <= datetime_end
    assert timedelta >= datetime.timedelta(0)

    timelapse = datetime_end - datetime_start
    output = timedelta / timelapse

    return output

def measure_overlap(
        datetime_in_1: datetime.datetime,
        datetime_out_1: datetime.datetime,
        datetime_in_2: datetime.datetime,
        datetime_out_2: datetime.datetime
        ) -> float:
    """
    datetime_in_1 < datetime_out_1
    datetime_in_2 < datetime_out_2

    output: float 0.0 - 1.0 of the overlapping portion compare to (datetime_in_1, datetime_out_1)
    """
    overlap_timedelta = measure_overlap_timedelta(datetime_in_1, datetime_out_1, datetime_in_2, datetime_out_2)
    output = measure_portion(datetime_in_1, datetime_out_1, overlap_timedelta)

    return output

def is_in_check_in_window(
        timestamp: datetime.datetime,
        shift_start: datetime.datetime,
        window_length: datetime.timedelta
        ) -> bool:
    """
    Checks whether a given timestamp is recorded between `shift_start - check_in_window` and `shift_start`.
    """
    
    assert window_length >= datetime.timedelta(0)

    window_start = shift_start - window_length
    window_end = shift_start
    output = (window_start <= timestamp) and (timestamp <= window_end)

    return output

def is_in_check_out_window(
        timestamp: datetime.datetime,
        shift_end: datetime.datetime,
        window_length: datetime.timedelta
        ) -> bool:
    """
    Checks whether a given timestamp is recorded between `shift_end` and `shift_end + window_length`.
    """
    
    assert window_length >= datetime.timedelta(0)

    window_start = shift_end
    window_end = shift_end + window_length
    output = (window_start <= timestamp) and (timestamp <= window_end)

    return output

def check_in_time(
        timestamp: datetime.datetime,
        shift_start: datetime.datetime,
        window_length: datetime.timedelta
        ) -> datetime.datetime:
    """
    Returns shift_start as check-in time if timestamp is in check-in window.
    """
    
    output = timestamp
    if is_in_check_in_window(timestamp, shift_start, window_length):
        output = shift_start

    return output

def check_out_time(
        timestamp: datetime.datetime,
        shift_end: datetime.datetime,
        window_length: datetime.timedelta
        ) -> datetime.datetime:
    """
    Returns shift_end as check-out time if timestamp is in check-out window.
    """
    
    output = timestamp
    if is_in_check_out_window(timestamp, shift_end, window_length):
        output = shift_end

    return output

def round_time_by_minute(
        timestamp: datetime.datetime,
        n: int,
        method: str='round'
        ) -> datetime.datetime:
    """
    Returns the rounded time up to the nearst n minutes, n dividing 60.
    Possible rounding `method` paramters: 'round', 'up', 'down'
    This function does NOT support units smaller than second.
    """
    assert (0 < n) and (n < 60)
    assert (n // 60) == 0
    assert method in {'round', 'up', 'down'}

    output = timestamp
    t = timestamp.minute * 60 + timestamp.second
    m = n * 60
    r = t % m
    dt = (m - r) % m

    if method == 'round':
        method = 'up' if r >= (n * 30) else 'down'

    if method == 'up':
        output += datetime.timedelta(seconds=dt)
    else: # round == 'down'
        output -= datetime.timedelta(seconds=r)

    return output
