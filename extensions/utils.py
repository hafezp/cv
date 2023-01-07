from . import jalali
from django.utils import timezone

def persian_num_converter(mystr):
    numbers ={
        '0':'٠',
        '1':'١',
        '2':'٢',
        '3':'٣',
        '4':'٤',
        '5':'٥',
        '6':'٦',
        '7':'٧',
        '8':'٨',
        '9':'٩',
    }
    for e, p in numbers.items():
        mystr = mystr.replace(e, p)
    return mystr

def jalali_converter(time):
    jmonths =['فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند']

    time = timezone.localtime(time)

    time_to_str = '{},{},{}'.format(time.year, time.month, time.day)
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()

    time_to_list = list(time_to_tuple)

    for index, month in enumerate(jmonths):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    output = '{} {} {}  ساعت  {}:{}'.format(
        time_to_list[2],
        time_to_list[1],
        time_to_list[0],
        time.hour,
        time.minute,
    )
    return persian_num_converter(output)