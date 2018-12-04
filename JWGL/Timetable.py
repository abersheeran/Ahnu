"""
清洗学校课程数据出来。
Author: AberSheeran
Time: 2018-12-04
"""
import re

from ._time import _schoolyear, _semester


def get_course_schedule(session, year: str = _schoolyear(), semester: str = _semester()):
    """获取特定学年特定学期的课程表, 默认为当前学期"""
    html = session.get_page(f"kcb/main/index?action=ok&xkxn={year}&xkxq={semester}")
    table = re.search(r"<tbody[\s\S]*?</tbody>", html).group(0)
    result = {}
    course_time = ["am0", "am1", "placeholder_1", "pm0", "pm1", "placeholder_2", "ng"]
    for i, tr in enumerate(re.findall(r"<tr[\s\S]*?</tr>", table.replace("<td>晚上</td>", ""))):
        if course_time[i].startswith("pl"):
            continue
        result[course_time[i]] = []
        for index, td in enumerate(re.findall(r"<td>[\s\S]*?</td>", tr)):
            if index != 0:
                result[course_time[i]].append(get_single_course_data(td.replace("<td>", "").replace("</td>", "").strip()))
    return result


def get_single_course_data(data: str) -> dict:
    result = []
    if len(data) == 0:
        return result
    data = data.replace("<br/>", "<br>").split("<br>")
    data = data[:-1]
    try:  # 移除所有横杠
        while True:
            data.remove('----------------------------')
    except ValueError:
        pass
    for index in range(0, len(data), 4):
        name = data[index]
        _temporary = re.search(r"第(?P<num>.*?)节", data[index+1])
        section = _temporary.group("num").split(',')
        _temporary = re.search(r"第(?P<start>\d+)-(?P<end>\d+)周", data[index+1])
        weeks = [i for i in range(int(_temporary.group("start")), int(_temporary.group("end"))+1)]
        teacher = data[index+2]
        place = data[index+3]
        for course in result:  # 合并被实训周分割的课程
            if course["name"] == name:
                course["weeks"] += weeks
                break
        else:
            result.append({
                "name": name,
                "section": section,
                "weeks": weeks,
                "teacher": teacher,
                "place": place
            })
    return result
