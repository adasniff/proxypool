# proxypool
## 介绍
ip代理池，支持配置不同数据源抓取方案、自动验证、api服务（进行中）。

支持python3（py2若需要可以加上）

## 参考项目
[**qiyeboy/IPProxyPool**](https://github.com/qiyeboy/IPProxyPool)

[**jhao104/proxy_pool**](https://github.com/jhao104/proxy_pool)

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

```shell
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

        crawl_list中配置各个数据原的抓取模式和解析规则，比较简单，可以按照规则添加新的源
```

- 运行：

```shell
        # 同时启动爬虫任务和代理ip验证任务
        python main.py spider validator
```

## TODO

1. 添加api服务
2. 添加docker






