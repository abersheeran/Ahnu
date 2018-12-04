import time


def year() -> int: return int(time.strftime("%Y", time.localtime()))


def month() -> int: return int(time.strftime("%m", time.localtime()))


def _schoolyear(): return f"{year()}-{year()+1}" if month() > 9 else f"{year()-1}-{year()}"


def _semester(): return "2" if 2 < month() < 9 else "1"
