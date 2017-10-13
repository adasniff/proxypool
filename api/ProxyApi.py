# -*- coding: utf-8 -*-
__author__ = 'ada'
# Created by ada on 13/10/2017

from flask import request

from config import POOL_NAME, POOL_SCORE_NAME, QUEUE_NAME
from config import API_HOST, API_PORT
from . import app, client


@app.route('/proxy/get/', methods=['GET'])
def get_proxy():
    return client.srandmember(POOL_NAME) or 'none'

@app.route('/proxy/incr/', methods=['GET'])
def incr_proxy():
    name = request.args.get('proxy')
    amount = request.args.get('amount', 1)
    if name is None:
        return '-1'
    return str(client.hincrby(POOL_SCORE_NAME, name, amount=amount)) or '-1'

@app.route('/proxy/decr/', methods=['GET'])
def decr_proxy():
    name = request.args.get('proxy')
    amount = request.args.get('amount', 1)
    if name is None:
        return '-1'
    score = client.hincrby(POOL_SCORE_NAME, name, -amount)
    if score <= 0:
        # 删除相关数据
        print("删除proxy：" + name)
        _delete_proxy(name)
    return str(score) or '-1'

@app.route('/proxy/count/', methods=['GET'])
def count_proxy_pool():
    return str(client.scard(POOL_NAME)) or '0'

@app.route('/proxy/queuelen/', methods=['GET'])
def count_proxy_queue():
    return str(client.llen(QUEUE_NAME))

@app.route('/proxy/delete/', methods=['GET'])
def delete_proxy():
    return "delete cmd"

@app.route('/proxy/clean/', methods=['GET'])
def clean_proxy():
    count = 0
    while True:
        name = client.srandmember(POOL_NAME)
        if name is None:
            break
        _delete_proxy(name)
        count += 1
    return str(count)

def _delete_proxy(proxy):
    """
    删除proxy
    :param proxy:
    :return:
    """
    client.srem(POOL_NAME, proxy)
    client.hdel(POOL_SCORE_NAME, proxy)
    client.delete(proxy)

def api_run():
    app.run(host=API_HOST, port=API_PORT)
