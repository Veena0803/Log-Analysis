"""Database to connect to newsdata.sql"""

#!/usr/bin/env python2

import psycopg2
import re

DBNAME = "news"


def popular_articles():
    '''Fetch the most popular articles of all time.'''
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    q = """select articles.title, count(*) as num_of_views from articles \
        join log on articles.slug = \
        (regexp_split_to_array(path,E'/article/'))[2] where path != '/' \
        group by (regexp_split_to_array(path, E'/article/'))[2], \
        articles.title order by num_of_views desc limit 3;"""
    c.execute(q)
    posts = c.fetchall()
    print "\nWhat are the most popular articles of all time?\n"
    for p in posts:
        print ' -- '.join(str(item) for item in p) + " views"

    '''Fetch the most popular article authors of all time.'''
    r = """select authors.name, count(articles.title)\
            as views from authors join articles on authors.id = \
            articles.author join log on articles.slug = \
            (regexp_split_to_array(path,E'/article/'))[2]\
            where log.status = '200 OK' group by \
            authors.name order by views DESC;"""
    c.execute(r)
    posts1 = c.fetchall()
    print "\nWhat are the most popular article authors of all time?\n"
    for p in posts1:
        print ' -- '.join(str(item) for item in p) + " views"

        '''Fetch days that had more than 1% failed requests.'''

    drop_command1 = """DROP VIEW IF EXISTS log_view CASCADE;"""
    drop_command2 = """DROP VIEW IF EXISTS final_log_view CASCADE;"""
    query1 = """create view log_view as select status,\
                date(time) as day from log;"""
    query2 = """create view final_log_view as select day,\
             100 * (sum(case when status != '200 OK' then 1 else 0 end)\
             ::float / count(day)::float)\
             as test from log_view group by day;"""
    query3 = """select * from final_log_view where test >= 1;"""
    final_query = drop_command1 + drop_command2 + query1 + query2 + query3
    c.execute(final_query)
    posts2 = c.fetchall()
    print "\nOn which days did more than 1% of requests lead to errors?\n"
    for p in posts2:
        print ' -- '.join(str(item) for item in p) + " % error"
    db.close()

popular_articles()
