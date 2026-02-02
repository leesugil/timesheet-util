import datetime, zoneinfo

def measureOverlapTimedelta(
        datetime_in_1: datetime.datetime,
        datetime_out_1: datetime.datetime,
        datetime_in_2: datetime.datetime,
        datetime_out_2: datetime.datetime
        ) -> datetime.timedelta:
    """
    datetime_in_1 < datetime_out_1
    datetime_in_2 < datetime_out_2

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

def measurePortion(
        datetime_start: datetime.datetime,
        datetime_end: datetime.datetime,
        timedelta: datetime.timedelta) -> float:

    assert datetime_start <= datetime_end
    assert timedelta >= datetime.timedelta(0)

    timelapse = datetime_end - datetime_start
    output = timedelta / timelapse

    return output

def measureOverlap(
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
    overlap_timedelta = measureOverlapTimedelta(datetime_in_1, datetime_out_1, datetime_in_2, datetime_out_2)
    output = measurePortion(datetime_in_1, datetime_out_1, overlap_timedelta)

    return output

def isInCheckInWindow(
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

def isInCheckOutWindow(
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
