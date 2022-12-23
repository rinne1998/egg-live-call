# 中国绊爱直播间打CALL工具

## 运行环境
 Python 3.5+

## 使用方法
在`cookie.txt`文件中加入B站账号的Cookie（提取方法：[https://www.cnblogs.com/wdysblog/p/16615453.html](https://www.cnblogs.com/wdysblog/p/16615453.html)，最后一步时请勿复制最前面的`cookie:`部分），若有多个账号请每行一个，程序会依次使用对应的账号发送弹幕。

## 自定义语句
在`main.py`中的以下部分加入你想要的句子即可。
```python
sentences = [
    "\爱哥/\爱哥/\爱哥/",
    "这是爱哥，ta是最棒的！",
    "\中国绊爱，无所替代/"
]
```
