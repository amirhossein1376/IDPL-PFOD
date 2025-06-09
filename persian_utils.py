import random
from datetime import date

PERSIAN_DIGITS = '۰۱۲۳۴۵۶۷۸۹'

def generate_persian_number(length=10):
    """Return a random string of Persian digits with given length."""
    return ''.join(random.choice(PERSIAN_DIGITS) for _ in range(length))

_digit_map = {str(i): PERSIAN_DIGITS[i] for i in range(10)}

def to_persian_digits(number):
    """Convert an int or numeric string to Persian digits."""
    return ''.join(_digit_map.get(ch, ch) for ch in str(number))

# Conversion algorithm adapted from jdatetime to avoid external dependencies
def gregorian_to_jalali(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if gy > 1600:
        jy = 979
        gy -= 1600
    else:
        jy = 0
        gy -= 621
    gy2 = gm > 2 and gy + 1 or gy
    days = 365 * gy + (gy2 + 3) // 4 - (gy2 + 99) // 100 + (gy2 + 399) // 400 - 80 + gd + g_d_m[gm - 1]
    jy += 33 * (days // 12053)
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if days < 186:
        jm = 1 + days // 31
        jd = 1 + days % 31
    else:
        jm = 7 + (days - 186) // 30
        jd = 1 + (days - 186) % 30
    return jy, jm, jd

def get_persian_date(gregorian_date=None):
    """Return a Persian date string (YYYY/MM/DD) for the given Gregorian date."""
    if gregorian_date is None:
        gregorian_date = date.today()
    jy, jm, jd = gregorian_to_jalali(gregorian_date.year, gregorian_date.month, gregorian_date.day)
    formatted = f"{jy:04d}/{jm:02d}/{jd:02d}"

    return to_persian_digits(formatted)
