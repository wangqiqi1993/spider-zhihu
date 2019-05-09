# -*- coding: utf-8 -*-
import pymysql
import re
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MysqlPipeline(object):
    def process_item(self, item, spider):
        item=dict(item)
        print(item['answer_count'])
        def table_exists(conn, table_name):
            sql = "show tables;"
            conn.execute(sql)
            tables = [conn.fetchall()]
            table_list = re.findall('(\'.*?\')', str(tables))
            table_list = [re.sub("'", '', each) for each in table_list]
            if table_name in table_list:
                return 1
            else:
                return 0
        self.conn= pymysql.connect(host='localhost',user='root',password='8911980',port=3306,db='test')
        self.cursor = self.conn.cursor()
        table_name = 'zhihu'
        if (table_exists(self.cursor, table_name) != 1):
            self.cursor.execute('create table zhihu(answer_count int,articles_count int,follower_count int,gender tinyint,headline varchar(100),name varchar(100),type varchar(32),url_token varchar(100),user_type varchar(32)) ENGINE=InnoDB DEFAULT character set utf8mb4 collate utf8mb4_general_ci;')
        try:
            self.cursor.execute("insert into zhihu (answer_count,articles_count,follower_count,gender,headline,name,type,url_token,user_type) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(item['answer_count'],item['articles_count'],item['follower_count'],item['gender'],item['headline'],item['name'],item['type'],item['url_token'],item['user_type']))
        except:
            pass
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
