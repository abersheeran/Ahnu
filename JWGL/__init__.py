from .Base import Base
from .Timetable import get_course_schedule
from .Examination import get_examination_time


class FuckJWGL(Base):
    """
    教务系统页面太丑了, 可操作性也差.
    """

    def get_course_schedule(self, year: str = None, semester: str = None) -> dict:
        """
        获取对应学年-学期的课程信息. 默认为当前学期

        year: 学年. 格式 "2018-2019"

        semester: 学期. 格式 "2" 
        """
        if (year is None) ^ (semester is None):
            raise ValueError("学年与学期两个参数必须同时使用/不使用")
        if year is None:
            return get_course_schedule(self)
        return get_course_schedule(self, year=year, semester=semester)

    def get_examination_time(self, year: str = None, semester: str = None) -> dict:
        """
        获取对应学年-学期的考试安排. 默认为当前学期.
        一个奇怪的现象, 如果查询本学期的考试安排会没有考场和座位号.

        year: 学年. 格式 "2018-2019"

        semester: 学期. 格式 "2"
        """
        if (year is None) ^ (semester is None):
            raise ValueError("学年与学期两个参数必须同时使用/不使用")
        if year is None:
            return get_examination_time(self)
        return get_examination_time(self, year=year, semester=semester)
