# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import time
from crawler_zhihu.settings import TO_ADDR
import random
import crawler_zhihu.settings as setting



def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


from_addr = setting.YOUR_EMAIL_ADDR
password = setting.YOUR_EMAIL_PWD
smtp_server = setting.YOUR_EMAIL_SMTP_SERVER


def sendEmail(text):
    #to_addr = '642811191@qq.com'
    to_addr = random.choice(TO_ADDR)
    msg = MIMEText(text, 'plain', 'utf-8')
    msg['From'] = _format_addr(u'知乎爬虫机器人 <%s>' % from_addr)
    msg['To'] = _format_addr(u'DaDa <%s>' % to_addr)
    msg['Subject'] = Header(u'知乎问题精选', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


class EmailPipeline(object):
    def process_item(self, item, spider):
        sendEmail('你好，我是知乎爬虫机器人\r\n问题：\r\n%s\r\n回答：\r\n%s\r\n地址：\r\n%s\r\n'%(item['question'].strip(),item['answer'].strip(),item['url'].strip()))
        time.sleep(30)
        return item
