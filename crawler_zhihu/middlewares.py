#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import base64
from scrapy import log
from crawler_zhihu.settings import PROXIES
from crawler_zhihu.settings import USER_AGENTS


class UserAgentMiddleWare(object):
    def process_request(self, request, spider):
        ua = random.choice(USER_AGENTS)
        if ua:
            # 记录
            log.msg('Current UserAgent: ' + ua, level=log.INFO)
            request.headers.setdefault('User-Agent', ua)


class ProxyMiddleWare(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        if proxy:
            if proxy['user_pass']:
                request.meta['proxy'] = "http://%s" % proxy['ip_port']
                encoded_user_pass = base64.encodestring(proxy['user_pass'])
                request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
                log.msg("Current Proxy (have pass) : %s" % (proxy['ip_port']), log.INFO)
            else:
                log.msg("Current Proxy (no pass) : %s" % (proxy['ip_port']), log.INFO)
                request.meta['proxy'] = "http://%s" % proxy['ip_port']


class CookiesMiddleWare(object):
    def process_request(self, request, spider):
        request.meta['cookiejar'] = 1


class HeadersMiddlerWare(object):
    def process_request(self, request, spider):
        request.headers['Accept'] = "*/*"
        request.headers['Accept-Encoding'] = "gzip, deflate, sdch, br"
        request.headers['Accept-Language'] = "zh-CN,zh;q=0.8"
        request.headers['Content-Type'] = "keep-alive"
        request.headers['Connection'] = "application/x-www-form-urlencoded; charset=UTF-8"
