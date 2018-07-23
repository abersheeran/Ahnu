"""
自己查成绩实在是麻烦，一次次的查，一个爬虫解决
Author: Aber Sheeran
Time: 2017-12-24
"""
from Base import Base
from bs4 import BeautifulSoup


class GetTheFuckTranscripts(Base):
    """获取期末成绩"""

    def get_transcripts(self, year=None, semester=None):
        """
        获取特定学年特定学期的成绩
        如果两个参数都为None,那么返回全学年
        """
        if year is None and semester is None:
            html = self.get_page("http://jwgl.ahnu.edu.cn/query/cjquery")
        else:
            html = self.get_page("http://jwgl.ahnu.edu.cn/query/cjquery/index?action=ok&xkxn=%s&xkxq=%s" % (year, semester))
        return html
        # # 一波切割字符串骚操作,不用re也不用xpath或者bs
        # table = html.split("table")[2]
        # return "{0}{1}{2}{3}{4}".format(
        #     '<html>\n<head>\n<link rel="stylesheet" href="https://agent.cathaysian.cn/cloudflare?url=ajax/libs/pure/1.0.0/pure-min.css">\n</head>\n',
        #     '<body>\n<table class="pure-table pure-table-bordered "',
        #     table.replace('class="thtd"', 'align="center"'),
        #     "table>\n</body>",
        #     '\n</html>',
        # )

    def parser(self, html):
        page = BeautifulSoup(html, "html.parser")
        all_lesson = list()
        keys = list()
        for td in page.find_all("tr")[1].find_all("td"):
            keys.append(td.text)
        for tr in page.find_all("tr")[2:-1]:
            lesson = dict()
            for index, td in enumerate(tr.find_all("td")):
                lesson[keys[index]] = td.text
            all_lesson.append(lesson)
        return all_lesson

    def get_average(self, html):
        sum_, sum_grade, count = 0, 0, 0
        for lesson in self.parser(html):
            if lesson["课程性质"] == "必修课":
                try:
                    学分 = int(lesson["学分"])
                    成绩 = int(lesson["成绩"])
                    sum_ += 学分*成绩
                    sum_grade += 学分
                    count += 1
                except:
                    pass
        average = sum_ / sum_grade
        return average

    def check_transcripts_integrity(self, html):
        """检查成绩的完整性"""
        for lesson in self.parser(html):
            if lesson["成绩"] == "":
                return False
        return True


if __name__ == "__main__":
    main = GetTheFuckTranscripts({
        "username": "",
        "password": ""
    })
    for year, month in [("2016-2017", "1"), ("2016-2017", "2"), ("2017-2018", "1"), ("2017-2018", "2")]:
        data = main.get_transcripts(year, month)
        print(year, month, ":", main.get_average(data))
