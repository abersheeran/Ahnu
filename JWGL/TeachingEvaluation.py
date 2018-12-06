"""
写教学评价简直是在浪费我的时间
Author: Aber Sheeran
Time: 2017-12-16
"""
import re
import json

from .Base import log


def fuck_the_teaching_evaluation(session):
    """教学评价"""
    for each in re.findall(r"<a[\s\S]*?href='([\s\S]+?)'", (session.get_page("jxpj/xsjxpj.shtml"))):
        log.debug(f"处理{each}中...")
        _deal_teaching_evaluation_page(session, each)


def _deal_teaching_evaluation_page(session, page_url):
    """处理单个教学评价页面"""
    post_data = {}  # 将发送的信息
    page = session.get_page(page_url)
    # 这里不能改，教务系统写死的
    for hidden_input in re.findall(r'input.+?type="hidden".*?>', page):
        temproray = re.search(r'name="(?P<key>.*?)".*?value="(?P<value>.*?)"', hidden_input)
        post_data[temproray.group("key")] = temproray.group("value")
    # 打分部分，可以自行下调
    for key, max_num in re.findall(r'input name="(?P<name>.+?)".+?max="(?P<max>\d+)".+?class="number', page):
        post_data[key] = max_num
    # 评语部分，随便改
    post_data["PJXX"] = "上课生动有趣，深入浅出！"
    log.debug(post_data)
    message = session.post_data(
        "/jxpj/xsjxpj/saveinfo?action=ok",
        data=post_data,
    )
    try:
        assert message["success"] == "success", message["msg"]
    except AssertionError as e:
        log.error(e)
