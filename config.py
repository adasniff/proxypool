# -*- coding: utf-8 -*-
__author__ = 'ada'
# Created by ada on 27/04/2017


'''
代理网站爬虫配置
'''

"""
ip： IP地址
port：端口号
type：0-高匿；1-普通；2-透明
protocol：0-http；1-https、http
"""
crawl_list = [
    {
        'name': '66ip1',
        'enable': True,
        'urls': ['http://www.66ip.cn/%s.html' % n for n in ['index'] + list(range(2, 4))],
        # 每6个小时跑一次
        'interval': {"hours": 6},
        'type': 'xpath',
        "pattern": ".//*[@id='main']/div/div[1]/table/tr[position()>1]",
        "pos": {"ip": "./td[1]", "port": "./td[2]", "type": "./td[4]", "protocol": ""}
    },
    {
        'name': '66ip2',
        'enable': True,
        'urls': ['http://www.66ip.cn/areaindex_%s/%s.html' % (m, n) for m in range(1, 35) for n in range(1, 3)],
        # 每3个小时跑一次
        'interval': {"hours": 3},
        'type': 'xpath',
        "pattern": ".//*[@id='footer']/div/table/tr[position()>1]",
        "pos": {"ip": "./td[1]", "port": "./td[2]", "type": "./td[4]", "protocol": ""}
    },
    {
        'name': 'ip181-1',
        'enable': True,
        'urls': ['http://www.ip181.com'],
        # 每6分钟更新
        'interval': {"minutes": 6},
        'type': 'xpath',
        'pattern': ".//div[@class='row']/div[2]/table/tbody/tr[position()>1]",
        'pos': {'ip': './td[1]', 'port': './td[2]', 'type': './td[3]', 'protocol': './td[4]'}
    },
    {
        'name': 'ip181-2',
        'enable': True,
        'urls': ['http://www.ip181.com/daili/%s.html' % n for n in range(1, 3)],
        # 每天7,10,15,21点更新
        'cron': {"hour": "7,10,15,21"},
        'type': 'xpath',
        'pattern': ".//div[@class='row']/div[3]/table/tbody/tr[position()>1]",
        'pos': {'ip': './td[1]', 'port': './td[2]', 'type': './td[3]', 'protocol': './td[4]'}
    },
    {
        'name': 'kuaidaili1',
        'enable': True,
        'urls': ['http://www.kuaidaili.com/proxylist/%s/' % n for n in range(1, 2)],
        # 每5分钟更新
        'interval': {"minutes": 5},
        'type': 'xpath',
        'pattern': ".//*[@id='index_free_list']/table/tbody/tr[position()>0]",
        'pos': {'ip': './td[1]', 'port': './td[2]', 'type': './td[3]', 'protocol': './td[4]'}
    },
    {
        'name': 'kuaidaili2',
        'enable': True,
        'urls': ['http://www.kuaidaili.com/free/%s/%s/' % (m, n) for m in ['inha', 'intr', 'outha', 'outtr'] for n in range(1, 3)],
        # 每小时更新
        'interval': {"hours": 1},
        'type': 'xpath',
        'pattern': ".//*[@id='list']/table/tbody/tr[position()>0]",
        'pos': {'ip': './td[1]', 'port': './td[2]', 'type': './td[3]', 'protocol': './td[4]'}
    },
    {
        'name': 'xici',
        'enable': True,
        'urls': ['http://www.xicidaili.com/%s/%s' % (m, n) for m in ['nn', 'nt', 'wn', 'wt'] for n in range(1, 3)],
        # 每15分钟更新
        'interval': {"minutes": 15},
        'type': 'xpath',
        'pattern': ".//*[@id='ip_list']/tr[position()>1]",
        'pos': {'ip': './td[2]', 'port': './td[3]', 'type': './td[5]', 'protocol': './td[6]'}
    }
]

def get_crawl_by_name(name):
    for crawl in crawl_list:
        if crawl.get("name") == name:
            return crawl
    return None

# 验证池最大并行个数
VALIDATOR_WORKERS = 5
VALIDATOR_URL_HTTPS = "https://www.baidu.com"
VALIDATOR_URL_HTTP = "http://www.baidu.com"

'''
数据库配置
'''

REDIS = {
    "host": "127.0.0.1",
    "port": 6379,
    "db": 0,
    "password": "",
    "max_conns": 1
}

QUEUE_NAME = "pq"                   # 代理队列名称

# 验证池信息，已验证过的代理
# 保存的存活时间
BUCKET_TTL = 60 * 60 * 8

POOL_NAME = "ppool"                 # 代理缓存池名称
POOL_SCORE_NAME = "pscore"          # 记录代理分值的hash表name
PROXY_SCORE = 5                     # 代理的分值，为零则删除

"""
http配置
"""

DOWNLOAD_TIMEOUT = 10               # 下载超时时间
DOWNLOAD_RETRIES = 2                # 下载重连次数
DOWNLOAD_DELAY = 1                  # 下载延时

"""
api server
"""

API_HOST = "0.0.0.0"                # host
API_PORT = 5001                     # port
