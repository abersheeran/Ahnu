# Ahnu

## JWGL

关于教务系统的一套代码, 可用其查成绩, 查GPA, 查课表, 查考试安排, 填教学评价, 抢课等.

### 如何使用

将整个库下载下来，安装`pip install -r requirements.txt`。

根据自己的需求修改`main.py`中的参数和函数. 运行即可.

#### Base参数说明

1. `proxy`: 当处于非校园网时, 可设为True. 即可正常访问教务系统
2. `debug`: 当你需要一些debug说明时, 将它设为True. 当然这一般没什么用

### 参与开发

此项目是基于手机端的. 因为PC端有验证码, 懒得弄.

使用`Base.py`中的`Base`来访问教务系统, 自行编写处理页面的函数, 挂到`__init__.py`里方便调用. 可参考Timetable等文件

## 非校园网环境使用FTP

访问[下载地址](https://github.com/AberSheeran/Ahnu/files/2636776/FileZilla.zip)下载zip文件, 解压之后, 运行FileZilla.exe即可.
