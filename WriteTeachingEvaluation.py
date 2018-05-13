"""
写教学评价简直是在浪费我的时间
Author: Aber Sheeran
Time: 2017-12-16
"""
from bs4 import BeautifulSoup
from Base import Base


class FuckTheTeachingEvaluation(Base):
    """教学评价"""
    def get_links(self):
        """获取教学评价页面每一个link"""
        result_list = []
        page = BeautifulSoup(self.get_page("http://jwgl.ahnu.edu.cn/jxpj/xsjxpj"), "html.parser")
        for each_tag in page.find_all("a"):
            result_list.append("http://jwgl.ahnu.edu.cn" + each_tag['href'])
        return result_list

    def deal_teaching_evaluation_page(self, page_url):
        """处理单个教学评价页面"""
        post_data = {}  # 将发送的信息
        page = BeautifulSoup(self.get_page(page_url), "html.parser")
        # 这里不能改，教务系统写死的
        for each_input in page.find_all("input", type="hidden"):
            post_data[each_input["name"]] = each_input["value"]
        # 打分部分，可以自行下调
        for each_input in page.find_all("input", class_="number"):
            post_data[each_input["name"]] = each_input["max"]
        # 评语部分，随便改
        post_data["PJXX"] = "上课生动有趣，深入浅出，我很喜欢！"
        self.cache.post(
            "http://jwgl.ahnu.edu.cn/jxpj/xsjxpj/saveinfo?action=ok",
            data=post_data,
        )


if __name__ == "__main__":
    user = {
        "username": "",  # 学号
        "password": "",  # 教务系统密码
    }
    main = FuckTheTeachingEvaluation(user)
    for each in main.get_links():
        main.deal_teaching_evaluation_page(each)
