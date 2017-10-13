# -*- coding: utf-8 -*-
__author__ = 'ada'
# Created by ada on 28/04/2017
from lxml import etree
import logging

logger = logging.getLogger('proxy.parser')

class HtmlParser(object):
    """
    html解析器
    """

    @classmethod
    def parse(cls, url, response, crawl_conf):
        """
        :param response: 
        :param crawl_conf: 
        :return: 
        """
        if crawl_conf["type"] == "xpath":
            return cls.xpath_parser(url, response, crawl_conf)
        elif crawl_conf["type"] == "func":
            return getattr(cls, crawl_conf["func"], None)(url, response, crawl_conf)
        else:
            return None

    @staticmethod
    def xpath_parser(url, response, crawl_conf):
        proxy_list = []
        root = etree.HTML(response)
        sels = root.xpath(crawl_conf["pattern"])
        for sel in sels:
            try:
                ip = sel.xpath(crawl_conf["pos"]["ip"])[0].text
                port = sel.xpath(crawl_conf["pos"]["port"])[0].text
                type = 0
                protocol = 0
                if crawl_conf["pos"]["type"] != "":
                    type = HtmlParser.type_str2int(sel.xpath(crawl_conf["pos"]["type"])[0].text)
                if crawl_conf["pos"]["protocol"] != "":
                    protocol = HtmlParser.protocol_str2int(sel.xpath(crawl_conf["pos"]["protocol"])[0].text)
                proxy = {"ip": ip, "port": int(port), "type": int(type), "protocol": int(protocol)}
                proxy_list.append(proxy)
            except Exception as e:
                logger.error("xpath parser error, url: {}, crawl name: {}, exception: {}".format(url, crawl_conf["name"], e))
                continue
        if len(proxy_list) == 0:
            logger.error("xpath parser抽取proxy为空，crawl name: {}".format(crawl_conf["name"]))
        return proxy_list

    @staticmethod
    def type_str2int(type_str=""):
        """
        0：高匿； 1：普通； 2：透明
        :param type_str: 
        :return: 
        """
        if not type_str or type_str.find(u"高"):
            return 0
        elif type_str.find(u"普"):
            return 1
        else:
            return 2

    @staticmethod
    def protocol_str2int(protocol_str=""):
        """
        0：http； 1: https http
        :param protocol_str: 
        :return: 
        """
        return 1 if protocol_str and protocol_str.lower().find("https") >= 0 else 0
