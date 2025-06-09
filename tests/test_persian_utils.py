import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import re
from datetime import date
from persian_utils import generate_persian_number, get_persian_date

PERSIAN_DIGITS = '۰۱۲۳۴۵۶۷۸۹'

def test_generate_persian_number_length_and_digits():
    num = generate_persian_number()
    assert len(num) == 10
    assert all(ch in PERSIAN_DIGITS for ch in num)

def test_get_persian_date_known_value():
    # Gregorian 2021-03-21 corresponds to Persian 1400/01/01
    d = date(2021, 3, 21)
    persian = get_persian_date(d)
    assert re.match(r'۱۴۰۰/۰۱/۰۱', persian)

