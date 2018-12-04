"""
获取考试安排.
Author: AberSheeran
Time: 2018-12-04
"""
import re


def get_examination_time(session, year: str = None, semester: str = None):
    # session.post_data("/appdata.shtml", data={"requesttype": "kxcx"})
    if year is None:
        html = session.get_page(f"/query/ksquery/index?action=ok&xkxn={year}&xkxq={semester}")
    else:
        html = session.get_page("/query/ksquery.shtml")
    result = []
    for tr in re.findall(r"<tr>[\s\S]*?</tr>", re.search(r"<tbody[\s\S]*?</tbody>", html).group(0)):
        result.append(dict(zip(["课程", "时间", "地点", "座位号"], [td for td in re.findall(r"<td>(.*?)</td>", tr)[1:]])))
    return result
