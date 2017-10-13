# -*- coding: utf-8 -*-
__author__ = 'ada'
# Created by ada on 28/04/2017
import requests
import time
import config
from .HttpUtils import HttpUtils


class Downloader(object):
    """
    下载器
    """
    @staticmethod
    def download(url, proxies=None, timeout=30, retries=2):
        count = 0
        while count <= retries:
            try:
                r = requests.get(url=url, headers=HttpUtils.get_header(), proxies=proxies, timeout=timeout, verify=False)
                if not r.ok:
                    raise ConnectionError
                else:
                    return r.content
            except Exception as e:
                # logger.error("download url: {}, exception: {}".format(url, e))
                time.sleep(3)
                count += 1
        return None

    @staticmethod
    def valid_proxy(proxy, timeout=10, retries=0):
        #url选择http还是https
        url = config.VALIDATOR_URL_HTTPS if proxy.get("protocol", 0) == 1 else config.VALIDATOR_URL_HTTP
        if proxy is None:
            return False
        proxies = {"http": "http://{}:{}".format(proxy["ip"], proxy["port"]),
                   "https": "https://{}:{}".format(proxy["ip"], proxy["port"])}
        content = Downloader.download(url, proxies, timeout, retries)
        return False if content is None or len(content) < 100 else True

