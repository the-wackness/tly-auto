# tly-auto
---
参考链接：[Action weather](https://blog.csdn.net/qq_40748336/article/details/110749375)<br>
参考链接：[Action python](https://blog.csdn.net/weixin_56760882/article/details/125571075)

----
### issue
![image](https://github.com/the-wackness/tly-auto/assets/65586236/9ccb1ee2-748b-4915-a9a5-58f64a5968d5)<br>
[Error: Version 3.9.1 with arch x64 not found](https://blog.csdn.net/Cosfox/article/details/128281864)<br>
[参考文档：Runnerimage](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners/about-github-hosted-runners)<br>
[参考文档：Ubuntu 22.04](https://github.com/actions/runner-images/blob/main/images/linux/Ubuntu2204-Readme.md)
<br>
<br>
<br>
![image](https://github.com/the-wackness/tly-auto/assets/65586236/465d1c74-e6a8-4e2b-b61f-37152b27cbbc)<br>
[解决问题的例子](https://github.com/77mark/glados-checkin/tree/master)<br>
[发现网上一堆 GLaDOS 网页签到](https://gitee.com/luck-ying/glados_checkin)<br>
发现更好用机场[glados](https://www.right.com.cn/FORUM/thread-8299215-1-1.html)
（貌似） 还没尝试，如果有更好的，那我建立这个repo的目的就可以换方向了<br>
<br>
<br>
j 验证码的接口不开放了，签到失败验证码错误。。。
<br>
<br>
遇到问题：mktime的结果和timt.time()的结果总是有一个奇怪的差值，用当前时间减去过去的时间得到的却是负值。下面帖子的问题提出时间差为28800s刚好8个小时，如果按照北京时间和UTC的区别来看刚刚好。。。难道是时区问题？
![image](https://github.com/the-wackness/tly-auto/assets/65586236/f4ce62b4-a857-400d-bddb-4e75965a22e8)<br>
[相同问题](https://bbs.csdn.net/topics/90093650)
