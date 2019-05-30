"""
Author: Aber Sheeran
Time: 2017-12-20
"""
import re
from Base import Base


class Lesson_Coding_Error(Exception):
    pass


class ChoseLesson(Base):
    def __init__(self, user_dictionary):
        self.coding_format = re.compile(r"\(\d{4}-\d{4}-\d{1}\)-\d+-[0-9 a-z]+-\d{1}")
        super().__init__(user_dictionary)

    def check_lesson_coding(self, coding):
        """检查选课代码是否合法"""
        result = self.coding_format.match(coding)
        if result:
            return True
        else:
            return False

    def get_lesson(self, lesson_coding):
        """发送选课信息"""
        if not self.check_lesson_coding(lesson_coding):
            raise Lesson_Coding_Error
        post_data = {
            'xkkh': lesson_coding,
        }
        return self.cache.post(
            "http://jwgl.ahnu.edu.cn/xk/xxk/savexxk?action=ok",
            data=post_data,
        )

    def del_lesson(self, lesson_coding):
        """发送退课信息"""
        if not self.check_lesson_coding(lesson_coding):
            raise Lesson_Coding_Error
        post_data = {
            'xkkh': lesson_coding,
        }
        return self.cache.post(
            "http://jwgl.ahnu.edu.cn/xk/xxk/delxxk?action=ok",
            data=post_data,
        )


if __name__ == "__main__":
    user = {
        "username": "",
        "password": ""
    }
    main = ChoseLesson(user)
    main.get_lesson("(2017-2018-1)-07492110-0101224-1")
