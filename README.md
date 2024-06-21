# django豆瓣图书可视化管理系统
> 基于django豆瓣图书可视化管理系统，具有搜索，查看，分类，评论，评分后台图书管理，可视化等功能,

## 部分项目简单展示

### 前台
![img.png](./images/img.png)
![img_1.png](./images/img_1.png)
![img_2.png](./images/img_2.png)
![img_3.png](./images/img_3.png)
![img_4.png](./images/img_4.png)
![img_5.png](./images/img_5.png)
![img_6.png](./images/img_6.png)
![img_7.png](./images/img_7.png)

###
![img_8.png](./images/img_8.png)
![img_11.png](./images/img_11.png)
![img_9.png](./images/img_9.png)
![img_10.png](./images/img_10.png)
## 运行
1.下载项目
```shell
git clone https://github.com/duanguolei/doubanbook.git
```

2.下载依赖
```shell
cd doubanbook
```
```shell
pip install -r requirements.txt
```

3.配置环境

> 并配置mysql,redis

4.迁移数据库
```shell
python manage.py makemigrations

python manage.py migrate
```

5.运行
```shell
python manage.py runserver
```
- 前台访问:http://127.0.0.1:8000
- 后台访问:
```shell
python book/scripts/init_manage_user.py
```
http://127.0.0.1:8000/manage
账户密码: admin 123456



- __代码中存在一定逻辑漏洞，不完善之处，欢迎点评指正__
- __如果代码对你有帮助，麻烦给个免费的star__
