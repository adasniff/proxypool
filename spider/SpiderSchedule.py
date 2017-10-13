# -*- coding: utf-8 -*-
__author__ = 'ada'
# Created by ada on 27/04/2017
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from util.Downloader import Downloader
from spider.HtmlParser import HtmlParser
import config, logging
from config import crawl_list, get_crawl_by_name, REDIS, QUEUE_NAME, DOWNLOAD_DELAY
from db.RedisClient import RedisClient


def spider_run():
    ss = SpiderSchedule()
    ss.run()


class SpiderSchedule(object):
    """
    爬虫调度，不同的数据源，采取不同的爬取策略
    """
    def __init__(self):
        self.log = logging.getLogger("proxy.spider")
        self.sched = BlockingScheduler()
        self.client = RedisClient(host=REDIS['host'], port=REDIS['port'], db=REDIS['db'], password=REDIS['password'], max_conns=REDIS['max_conns'])
        self._config_schedule()

    def _config_schedule(self):
        """
        配置任务
        :return: 
        """
        for crawl in crawl_list:
            # 是否可用
            if not crawl["enable"]:
                continue
            self.log.info("添加job：{}".format(crawl["name"]))
            #执行方式，是间隔时间，还是定时任务
            if "interval" in crawl:
                d = crawl["interval"]
                self.sched.add_job(self._spider, "interval", [crawl["name"]], **d)
            elif "cron" in crawl:
                d = crawl["cron"]
                self.sched.add_job(self._spider, "cron", [crawl["name"]], **d)

    def _spider(self, name):
        """
        爬虫实现
        :param name: 
        :return: 
        """
        self.log.info("爬取源：{}".format(name))
        crawl_conf = get_crawl_by_name(name)
        for url in crawl_conf["urls"]:
            # 延时下载
            time.sleep(crawl_conf.get("delay", None) or DOWNLOAD_DELAY)
            content = Downloader.download(url, timeout=config.DOWNLOAD_TIMEOUT, retries=config.DOWNLOAD_RETRIES)
            if content is None:
                self.log.error("download失败，url：" + url)
                continue
            #解析页面
            proxy_list = HtmlParser().parse(url, content, crawl_conf)
            #保存proxy
            self._save(proxy_list, crawl_conf)

    def _save(self, proxy_list, crawl_conf):
        self.client.lpushlist(QUEUE_NAME, proxy_list)

    def run(self):
        try:
            # 判断是否有job
            jobs = self.sched.get_jobs()
            if len(jobs) == 0:
                self.log.error("当前jobs为0")
                return

            self.sched.start()
        except Exception:
            self.log.error("执行调度任务失败")

if __name__ == '__main__':
    spider = SpiderSchedule()
    spider._spider("ip181-1")
