# -*- coding: utf-8 -*-
__author__ = 'ada'
# Created by ada on 09/05/2017
import random, math

def proxy2str(proxy, ftype=1):
    """
    把dict的proxy，转为str格式
    ftype: 1-ip:port格式， 2-type:protocol格式
    :param proxy: 
    :return: 
    """
    try:
        if ftype == 1:
            return "{}:{}".format(proxy["ip"], proxy["port"])
        elif ftype == 2:
            return "{}:{}".format(proxy["type"], proxy["protocol"])
        else:
            return None
    except Exception:
        return None

def get_random(start, end):
    return math.floor(random.random() * (end - start) + start)

# def get_redis():
#     if sys.platform.find('win') >= 0:
#         host, port = REDIS['host_local'], REDIS['port_local']
#     else:
#         host, port = REDIS['host'], REDIS['port']
#     return RedisClient(host=host, port=port, db=REDIS['db'], password=REDIS['password'], max_conns=REDIS['max_conns'])
