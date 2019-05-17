"""
查询电费, 突然断电的心情很糟糕
Author: Aber Sheeran
Time: 2019-05-17
"""
import json
import hashlib
import smtplib
from email.mime.text import MIMEText
from email.header import Header

import requests

"""
在Linux服务器上使用 sudo crontab -e
写入一下内容 0 11 * * * python3 /path/to/electfee.py > /path/to/log.electfee
"""

mail_user = "你自己的QQ邮箱"
mail_pass = "QQ邮箱的授权码"
学号 = "16111******"
密码 = "111111"


def sendmail(name: str, fee_1: float, fee_2: float):
    """发送邮件通知电费"""
    mail_host = "smtp.qq.com"  # 设置服务器

    sender = mail_user
    receivers = [mail_user]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    message = MIMEText(f'你的空调电费为{fee_1}, 照明电费为{fee_2}', 'plain', 'utf-8')
    message['From'] = Header("电费监控", 'utf-8')
    message['To'] = Header(name, 'utf-8')

    subject = '电费监控通知'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


def get_fee(userid: str, token: str, acccode: int) -> float:
    """
    acccode: 1是空调费, 2是电费
    """
    return requests.post(
        "http://hqapi.ahnu.edu.cn/CardApi/Card/GetElectricity",
        data=f"jsonSessionDTO=%7B+%22UserID%22%3A+%22{userid}%22%2C+%22Token%22%3A+%22{token}%22%7D&Acccode={acccode}",
        headers={
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "http://hqfw.ahnu.edu.cn",
            "Referer": "http://hqfw.ahnu.edu.cn//KDZR.ElectricityCharges/indexDFCX.html?TenantID=8"
        }
    ).json()


def login(username: str, password: str) -> dict:
    return requests.post(
        "http://hqfw.ahnu.edu.cn/BaseModule/m-Mobile/Login/BindUser",
        data={
            "username": username,
            "password": hashlib.md5(password.encode("UTF-8")).hexdigest(),
            "serviceProvider": "",
            "openId": "",
            "headimgurl": "",
            "appidtype": "",
            "unionid": "",
            "tenantID": "8"
        },
    ).json()


if __name__ == "__main__":
    userinfo = json.loads(login(学号, 密码)['userinfo'])
    name = userinfo['RealName']
    userid = userinfo['UserIDOrginal']
    token = userinfo['OAuthToken']
    fee_1 = get_fee(userid, token, 1)['ViewList']['RemainEy']
    fee_2 = get_fee(userid, token, 2)['ViewList']['RemainEy']
    if float(fee_1) < 5.0 or float(fee_2) < 5.0:
        sendmail(name, fee_1, fee_2)
