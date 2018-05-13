"""
自己查成绩实在是麻烦，一次次的查，一个爬虫解决
Author: Aber Sheeran
Time: 2017-12-24
"""
from Base import Base


class GetTheFuckTranscripts(Base):
    """获取期末成绩"""
    def get_transcripts(self, year, semester):
        """获取特定学年特定学期的成绩"""
        html = self.get_page("http://jwgl.ahnu.edu.cn/query/cjquery/index?action=ok&xkxn=%s&xkxq=%s" % (year, semester))
        # 一波切割字符串骚操作,不用re也不用xpath或者bs
        table = html.split("table")[2]
        return "{0}{1}{2}{3}{4}".format(
            '<html>\n<head>\n<link rel="stylesheet" href="https://agent.cathaysian.cn/cloudflare?url=ajax/libs/pure/1.0.0/pure-min.css">\n</head>\n',
            '<body>\n<table class="pure-table pure-table-bordered "',
            table.replace('class="thtd"', 'align="center"'),
            "table>\n</body>",
            '\n</html>',
        )

    def check_transcripts_integrity(self, html):
        """检查成绩的完整性"""
        from bs4 import BeautifulSoup
        page = BeautifulSoup(html, "lxml")
        for each in page.find_all("tr")[1:-1]:
            if each.find_all("td")[7].text == "":
                return False
        return True


if __name__ == "__main__":
    main = GetTheFuckTranscripts({
        "username":"",
        "password":""
    })
    data = main.get_transcripts("2017-2018", "2")
    print(data)
