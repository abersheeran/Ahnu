import logging
import socket

from requests import Session
import socks


log = logging.getLogger("Ahnu")


class Base:
    """访问教务系统的基类"""

    def __init__(self, user_dictionary, debug=False, proxy=False):
        if debug:
            self._open_debug()
        if proxy:
            self._set_proxy()

        self.cache = Session()
        # 登陆教务系统
        message = self.cache.post(
            # "http://mjwgl.ahnu.edu.cn/login/check.shtml", # 旧接口
            "http://mjwgl.ahnu.edu.cn/login/remotelogin",
            data={
                "username": user_dictionary["username"],
                "password": user_dictionary["password"],
                "usertype": "stu",
                "device": "aphone",
            },
            headers={
                "Host": "mjwgl.ahnu.edu.cn",
            }
        )
        self.sessionid = message.cookies["PHPSESSID"]
        assert message.json()["success"] == "success", message.json()["message"]

    def _open_debug(self):
        logging.basicConfig(
            level=logging.DEBUG,
            format='[%(levelname)s]-[%(asctime)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )

    def _set_proxy(self):
        socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, "210.45.192.197", 419)
        socket.socket = socks.socksocket

    def get_page(self, target_url):
        """GET 获取页面内容"""
        if target_url.startswith("http://"):
            return self.cache.get(target_url).content.decode("utf-8")
        return self.cache.get("http://mjwgl.ahnu.edu.cn/"+target_url).content.decode("utf-8")

    def get_url(self, op: str) -> str:
        """
        根据操作的拼音缩写获取对应的URL

        如: 课表查询: kbcx
        """
        rep = self.cache.post("http://mjwgl.ahnu.edu.cn/appdata.shtml", {"requesttype": op, "sessionid": self.sessionid})
        self.sessionid = rep.cookies["PHPSESSID"]
        return rep.headers["Location"]
