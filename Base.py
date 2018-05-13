from requests import Session


class Base:
    """访问教务系统的基类"""

    def __init__(self, user_dictionary):
        self.cache = Session()
        # 登陆教务系统
        self.cache.post(
            "http://jwgl.ahnu.edu.cn/login/check.shtml",
            data={
                "user": user_dictionary["username"],
                "pass": user_dictionary["password"],
                "usertype": "stu",
            },
        )
        self.cache.headers.update({
            "Host": "jwgl.ahnu.edu.cn",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Referer": "http://jwgl.ahnu.edu.cn/",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0",
        })

    def get_page(self, target_url):
        """获取页面"""
        return self.cache.get(target_url).content.decode("utf-8")
