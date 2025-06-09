import random
from datetime import date, timedelta

try:
    from khayyam import JalaliDate
except ImportError:  # pragma: no cover - fallback for environments without khayyam
    JalaliDate = None

PERSIAN_DIGITS = '۰۱۲۳۴۵۶۷۸۹'

def generate_persian_number(length=10):
    """Return a random string of Persian digits with given length."""
    return ''.join(random.choice(PERSIAN_DIGITS) for _ in range(length))

_digit_map = {str(i): PERSIAN_DIGITS[i] for i in range(10)}

def to_persian_digits(number):
    """Convert an int or numeric string to Persian digits."""
    return ''.join(_digit_map.get(ch, ch) for ch in str(number))


def _random_gregorian_date(start_year=1970, end_year=2100):
    """Return a random ``date`` between the given years."""
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, delta_days))

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
        gregorian_date = _random_gregorian_date()

    if JalaliDate is not None:
        jalali = JalaliDate(gregorian_date)
        formatted = jalali.strftime("%Y/%m/%d")
    else:  # pragma: no cover - fallback when khayyam is unavailable
        jy, jm, jd = gregorian_to_jalali(
            gregorian_date.year, gregorian_date.month, gregorian_date.day
        )
        formatted = f"{jy:04d}/{jm:02d}/{jd:02d}"

    return to_persian_digits(formatted)


def _default_font(size):
    """Return a truetype font with basic Farsi support."""
    from pathlib import Path
    from PIL import ImageFont
    default = Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    return ImageFont.truetype(str(default), size)


def _create_plain_background(width, height):
    from PIL import Image
    return Image.new('RGB', (width, height), 'white')


def _create_noisy_background(width, height):
    from PIL import Image, ImageChops
    bg = _create_plain_background(width, height)
    noise = Image.effect_noise((width, height), 50).convert('RGB')
    return ImageChops.add(bg, noise)


def _render_text_image(text, background='noise', font_path=None, font_size=32,
                       width=700, height=50):
    """Render ``text`` on a plain or noisy background and return a PIL Image."""
    try:  # Delay PIL import so tests without Pillow still run
        from PIL import ImageDraw, ImageFont, Image
    except ImportError:  # pragma: no cover - PIL not available
        raise ImportError('Pillow is required for rendering images')

    if background == 'plain':
        img = _create_plain_background(width, height)
    else:
        img = _create_noisy_background(width, height)

    if font_path is None:
        font = _default_font(font_size)
    else:
        font = ImageFont.truetype(font_path, font_size)

    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(text, font=font)
    x = max((width - w) // 2, 0)
    y = max((height - h) // 2, 0)
    draw.text((x, y), text, font=font, fill='black')
    return img


def generate_persian_number_image(length=10, background='noise', font_path=None,
                                  font_size=32, width=700, height=50):
    """Return an image of a random Persian number using the given style."""
    number = generate_persian_number(length)
    return _render_text_image(number, background, font_path, font_size, width,
                              height)


def get_persian_date_image(gregorian_date=None, background='noise',
                           font_path=None, font_size=32, width=700, height=50):
    """Return an image of the Persian date using the given style."""
    text = get_persian_date(gregorian_date)
    return _render_text_image(text, background, font_path, font_size, width,
                              height)
