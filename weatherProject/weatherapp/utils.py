import pytz
from datetime import datetime


def timezone_conv(last_upd_loc, loc_tz_str):
    date_format = '%Y-%m-%d %H:%M'
    last_upd_dt = datetime.strptime(last_upd_loc, date_format)

    loc_tz = pytz.timezone(loc_tz_str)
    last_upd_dt_loc = loc_tz.localize(last_upd_dt)

    new_tz = pytz.timezone('Europe/Moscow')
    last_update = last_upd_dt_loc.astimezone(new_tz)
    last_update_conv_str = last_update.strftime(date_format)

    return last_update_conv_str