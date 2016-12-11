# -*- coding: utf-8 -*-
import json
import urllib
import re
import scrapy
import time
from crawler_zhihu.damatuWeb import DamatuApi, dmt

from crawler_zhihu.items import ZhihuItem
import crawler_zhihu.settings as setting


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    start_urls = [
        'https://www.zhihu.com'
    ]

    def parse(self, response):
        list = json.loads(response.body)['msg']
        for item in list:
            zhihuitem = ZhihuItem()
            selector = scrapy.Selector(text=item)
            zhihuitem['answer'] = re.subn("<[^>]*>","",selector.css('textarea.content::text').extract_first())[0]
            zhihuitem['question'] = selector.css("h2.feed-title>a::text").extract_first()
            zhihuitem['url'] = "https://www.zhihu.com" + selector.css("h2.feed-title>a::attr(href)").extract_first()
            yield zhihuitem;

    def start_requests(self):
        yield scrapy.Request("https://www.zhihu.com", dont_filter=True, callback=self.request_captcha)

    def request_captcha(self, response):
        # 获取_xsrf值
        self.xsrf = response.css('input[name="_xsrf"]::attr(value)').extract()[0]
        captcha_url = "http://www.zhihu.com/captcha.gif?r=%s&type=login" % (int(round(time.time() * 1000)))
        # 获取请求
        yield scrapy.Request(
                url=captcha_url,
                callback=self.post_login,
        )

    def post_login(self, response):
        # image = Image.open(StringIO.StringIO(response.body))
        # image.show()
        # #下载验证码
        # with open("F:\captcha.png", "wb") as fp:
        #     fp.write(response.body)

        result = dmt.decode(response.body,42)

        # 登陆成功后, 会调用after_login回调函数
        return [scrapy.Request(
                url='https://www.zhihu.com/login/phone_num',
                method='POST',
                body=urllib.urlencode({
                    '_xsrf': self.xsrf,
                    'password': setting.ZHIHU_PASSWORD,
                    'captcha':result,
                    'remember_me': 'true',
                    'phone_num': setting.ZHIHU_USERNAME
                }),
                callback=self.after_login,
                dont_filter=True,
                headers={
                    "Referer": "https://www.zhihu.com/",
                }
        )]

    def after_login(self, response):
        list = range(1000)[::10]
        for i in list:
            yield scrapy.Request(
                    url='https://www.zhihu.com/node/TopStory2FeedList',
                    method='POST',
                    body=urllib.urlencode({
                        'params': '{"start":"%s"}' % (i),
                        'method': 'next',
                    }),
                    headers={
                        "Referer": "https://www.zhihu.com/",
                        "X-Requested-With": "XMLHttpRequest",
                        "X-Xsrftoken": self.xsrf,
                        "Origin": "https://www.zhihu.com"
                    },
                    dont_filter=True,
            )
