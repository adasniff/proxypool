# -*- coding: utf-8 -*-
__author__ = 'ada'
import logging
# Created by ada on 27/04/2017
import sys
from logging.config import fileConfig
from multiprocessing import Process
import cloghandler

from spider.SpiderSchedule import spider_run
from validator.Validator import validator_run


def run(argv):
    #默认为启动所有
    if len(argv) == 0:
        raise Exception("没有参数！")

    proc_list = []
    if "spider" in argv:
        proc_list.append(Process(target=spider_run))
    if "validator" in argv:
        proc_list.append(Process(target=validator_run))

    for proc in proc_list:
        proc.start()
    for proc in proc_list:
        proc.join()

if __name__ == '__main__':
    logging.config.fileConfig('./log.ini')
    run(sys.argv[1:])
