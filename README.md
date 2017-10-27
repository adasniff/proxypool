# proxypool
## 介绍
ip代理池，支持配置不同数据源抓取方案、自动验证、api服务（进行中）。

支持python3（py2若需要可以加上）

## 参考项目
[**IPProxyPool**](https://github.com/qiyeboy/IPProxyPool)

[**proxy_pool**](https://github.com/jhao104/proxy_pool)

## 使用
- 项目clone到本地:

```shell
    git clone https://github.com/adasniff/proxypool.git
```

- 安装依赖：

```shell
    pip install -r requirements.txt
```

- 配置config.py:

```python
    # 验证地址（http|https），可改为自己需要的
    VALIDATOR_URL_HTTPS = "https://www.baidu.com"
    VALIDATOR_URL_HTTP = "http://www.baidu.com"

    # redis数据库，用户爬虫消息队列和保存代理ip
    REDIS = {
        "host": "127.0.0.1",
        "port": 6379,
        "db": 0,
        "password": "",
        "max_conns": 1
    }

    # api服务配置
    API_HOST = "0.0.0.0"  # 服务监听ip，默认 0.0.0.0
    API_PORT = 5001       # 监听端口

    crawl_list中配置各个数据原的抓取模式和解析规则，比较简单，可以按照规则添加新的源
```

- 运行：

```shell
    # 同时启动爬虫任务、代理ip验证任务、api服务
    python main.py spider validator api
```

## API接口说明

| 接口名称 | 请求方法 | 传递参数 | 说明 |
| :--|:--|:--|:--|
|/proxy/get|GET|None|随机获取一个代理ip|
|/proxy/incr|GET|proxy=ip&amount=1|增加这个ip的score amount分|
|/proxy/decr|GET|proxy=ip&amount=1|减少这个ip的score amount分，score<=0默认删除ip|
|/proxy/count|GET|None|获取数据库中代理ip总数|
|/proxy/clean|GET|None|清空ip（慎用）|

- 每个ip默认score，config.py中配置，用于表示该ip的有效性


## TODO

1. 添加docker






