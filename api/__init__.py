# -*- coding: utf-8 -*-
__author__ = 'ada'
# Created by ada on 13/10/2017
from flask import Flask
from config import REDIS
from db.RedisClient import RedisClient

app = Flask(__name__)

client = RedisClient(host=REDIS['host'], port=REDIS['port'], db=REDIS['db'], password=REDIS['password'], max_conns=REDIS['max_conns'])

from .ProxyApi import *

