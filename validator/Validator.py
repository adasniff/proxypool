# -*- coding: utf-8 -*-
__author__ = 'ada'
# Created by ada on 27/04/2017
import time, json, logging
from threading import Thread, RLock
from util.Downloader import Downloader
from util.CustomUtils import proxy2str
from config import VALIDATOR_WORKERS, QUEUE_NAME, BUCKET_TTL, POOL_NAME, POOL_SCORE_NAME
from config import PROXY_SCORE, REDIS
from db.RedisClient import RedisClient

mylock = RLock()

def validator_run():
    workers  = []
    # 启动验证线程
    for i in range(VALIDATOR_WORKERS):
        workers.append(Validator(i + 1))
    for i in range(VALIDATOR_WORKERS):
        workers[i].start()
    for i in range(VALIDATOR_WORKERS):
        workers[i].join()

class Validator(Thread):
    """
    验证器
    """
    def __init__(self, thread_id):
        super(Validator, self).__init__()
        # id从1开始
        self.thread_id = thread_id
        self.log = logging.getLogger('proxy.validator_{}'.format(thread_id))
        self.client = RedisClient(host=REDIS['host'], port=REDIS['port'], db=REDIS['db'], password=REDIS['password'], max_conns=REDIS['max_conns'])

    def _check_exists(self, proxy):
        return self.client.exist(proxy2str(proxy))

    def _save_to_pool(self, proxy):
        mylock.acquire()
        #保存到缓存池
        if self.client.sadd(POOL_NAME, proxy2str(proxy)) > 0:
            #保存代理信息
            self.client.hset(POOL_SCORE_NAME, proxy2str(proxy), PROXY_SCORE)
        mylock.release()

    def _save_to_bucket(self, proxy, ttl=BUCKET_TTL):
        return self.client.set(proxy2str(proxy), proxy2str(proxy, 2), ex=ttl)

    def _brpop_queue(self):
        datas = self.client.brpop(QUEUE_NAME)
        try:
            return json.loads(str(datas[1], encoding='utf-8'))
        except Exception:
            return None

    def _valid_proxy(self, proxy):
        ret = Downloader.valid_proxy(proxy)
        if ret == False and proxy.get("protocol", 0) == 1:
            # https的代理，再用http请求一遍
            proxy["protocol"] = 0
            ret = Downloader.valid_proxy(proxy)
        return ret

    def run(self):
        while True:
            proxy = self._brpop_queue()
            if proxy is None:
                # 队列中没有需要验证的代理，则睡眠10s
                time.sleep(10)
                continue
            #验证是否存在
            if self._check_exists(proxy):
                continue
            #测试代理
            if self._valid_proxy(proxy):
                self.log.info("[passed]proxy：{}".format(proxy2str(proxy)))
                #保存到代理池中
                self._save_to_pool(proxy)
                self._save_to_bucket(proxy, ttl=None)
            else:
                #保存到已验证的桶中，通过验证则一直保留，否则添加ttl
                self._save_to_bucket(proxy)

if __name__ == '__main__':
    validator_run()
