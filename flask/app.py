#!/usr/bin/env python
#-*- coding: utf-8 -*-
import math
import re
import pymongo
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
# setting:
MONGODB_SERVER = 'localhost'
MONGODB_PORT = 27017
MONGODB_DB = 'weixinrrr'
MONGODB_COLLECTION_BUGS = 'weixin_list'

ROWS_PER_PAGE = 20
# flask app:
app = Flask(__name__)
app.config.from_object(__name__)
# monogodb connection string
connection_string = "mongodb://%s:%d" % (
    app.config['MONGODB_SERVER'], app.config['MONGODB_PORT'])
content = {'by_bugs':
           {'mongodb_collection': app.config[
               'MONGODB_COLLECTION_BUGS'], 'template_html': 'search_bugs.html'},
           }


def get_search_regex(keywords):
    keywords_regex = {}
    kws = [ks for ks in keywords.strip().split(' ') if ks != '']
    field_name = 'gongzhonghao_type'
    if len(kws) > 0:
        reg_pattern = re.compile('|'.join(kws), re.IGNORECASE)
        # keywords_regex[field_name]={'$regex':'|'.join(kws)}
        keywords_regex[field_name] = reg_pattern

    return keywords_regex


def search_mongodb(keywords, page, content_search_by):
    client = pymongo.MongoClient(connection_string)
    db = client[app.config['MONGODB_DB']]
    keywords_regex = get_search_regex(keywords)
    collection = db[content[content_search_by]['mongodb_collection']]
    # get the total count and page:
    total_rows = collection.find(keywords_regex).count()
    total_page = int(
        math.ceil(total_rows / (app.config['ROWS_PER_PAGE'] * 1.0)))
    page_info = {'current': page, 'total': total_page,
                 'total_rows': total_rows, 'rows': []}
    # get the page rows
    if total_page > 0 and page <= total_page:
        row_start = (page - 1) * app.config['ROWS_PER_PAGE']
        cursors = collection.find(keywords_regex)\
            .sort('author', pymongo.DESCENDING).skip(row_start).limit(app.config['ROWS_PER_PAGE'])
        for c in cursors:

            page_info['rows'].append(c)
    client.close()
    return page_info


def get_weixin_total_count():
    client = pymongo.MongoClient(connection_string)
    db = client[app.config['MONGODB_DB']]
    collection_bugs = db[app.config['MONGODB_COLLECTION_BUGS']]
    total_count_bugs = collection_bugs.find().count()
    client.close()

    return (total_count_bugs)


@app.route('/')
def index():
    total_count_bugs = get_weixin_total_count()
    return render_template('index.html', total_count_bugs=total_count_bugs, title=u'微信公众号搜索')


@app.route('/search', methods=['get'])
def search():
    keywords = request.args.get('keywords')
    page = int(request.args.get('page', 1))
    content_search_by = request.args.get('content_search_by', 'by_bugs')
    if page < 1:
        page = 1

    page_info = search_mongodb(
        keywords, page, content_search_by)

    return render_template(content[content_search_by]['template_html'], keywords=keywords, page_info=page_info, title=u'搜索结果-微信公众号搜索')


def main():
    app.run(host='0.0.0.0', debug=True)

if __name__ == '__main__':
    main()
