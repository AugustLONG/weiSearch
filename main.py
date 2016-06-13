#-*-coding:utf-8-*-
'''
    @usage: 定时服务
'''
import os
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime,timedelta
import random

###################  自定义logging格式  #######################################
logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='%s/main.log' % '../log',
                filemode='a')




######################### 爬虫 ################################################

#------运行单条爬虫------------------
def _crawl(spider_name=None,project=None):
    if spider_name and project:
        #改变当前工作目录到项目下
        os.chdir('../%s' % project)
        isExists=os.path.exists('../log/%s'%project)
        if not isExists:
            os.makedirs('../log/%s'%project)

        logging.info('running spider: %s/%s' % (project,spider_name))
        starttime = datetime.now()

        # os.system('scrapy crawl %s -a page_max=10 2>&1 |tee -a '\
        #           '../logrrr/%s/%s.log ../logrrr/%s/%s_stderr.log'\
        #           % ('weixin','weixin','weixin','weixin','weixin'))
        os.system('scrapy crawl %s -a page_max=10 2>&1 |tee -a '\
                  '../log/%s/%s.log'\
                  % (spider_name,project,spider_name))

        #os.system('scrapy crawl weixin -a page_max=10')
    endtime = datetime.now()
    runtime = (endtime-starttime).seconds
    logging.info('end spider: %s/%s, runtime: %s s' % (project,spider_name,runtime))

    return None


#------定时任务----------------------
def main():
    sched = BlockingScheduler()
    try:

        #微信公众号及其功能的爬虫任务
        @sched.scheduled_job('cron', day_of_week='mon-sun', hour=_hour,minute=_minute)
        def timed_job_news():
            logging.info('running cron job for --微信公众号功能搜索--  spider')
            try:
                _crawl(spider_name='weixin',project='weixin')
            except Exception as e:
                logging.error(e)

        sched.start()

    except Exception as e:
        logging.error(e)


if __name__ == "__main__":

    #设置爬虫运行时间
    _hour = '5-23'
    _minute = '*/30'
    _second = random.randint(2, 50)
    _deltatime = 10
    main()


