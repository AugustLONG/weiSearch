# -*- coding: utf-8 -*-


#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'weixin'

SPIDER_MODULES = ['weixin.spiders']
NEWSPIDER_MODULE = 'weixin.spiders'

#piplines
ITEM_PIPELINES = {
    'scrapy.contrib.pipeline.images.ImagesPipeline': 1,
    'weixin.pipelines.MongoDBPipeline':100,
}
#the crawl default setting
PAGE_MAX_DEFAULT = 1
LOCAL_STORE_DEFAULT = 'false'
UPDATE_DEFAULT = 'false'

#save to mongdodb
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'weixinrrr'
MONGODB_COLLECTION = 'weixin_list'

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
