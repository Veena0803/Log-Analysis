#!/usr/bin/env python2.7

"""Database to connect to newsdata.sql"""

import psycopg2

DBNAME = "news"


'''Fetch the most popular articles of all time.'''
art_title = "\nWhat are the most popular articles of all time?\n"
q = """SELECT articles.title, count(*) AS num_of_views
FROM articles JOIN log
ON '/article/' || articles.slug = log.path
GROUP BY articles.title
ORDER BY num_of_views DESC
LIMIT 3;"""

'''Fetch the most popular article authors of all time.'''
aut_title = "\nWhat are the most popular article authors of all time?\n"
r = """SELECT authors.name, count(articles.title) AS views
FROM authors JOIN articles
ON authors.id = articles.author JOIN log
ON '/article/' || articles.slug = log.path
WHERE log.status = '200 OK'
GROUP BY authors.name
ORDER BY views DESC;"""

'''Fetch days that had more than 1% failed requests.'''
fr_title = "\nOn which days did more than 1% of requests lead to errors?\n"
final_query = """SELECT *
FROM final_log_view
WHERE error_percentage >= 1;"""


def connect():
    """Connect to the news database"""
    conn = psycopg2.connect(database=DBNAME)
    cursor = conn.cursor()
    return conn, cursor


def get_results(query):
    "Returns results for all the queries"
    conn, cursor = connect()
    cursor.execute(query)
    return cursor.fetchall()
    conn.close()


def print_results(query_results):
    print(query_results[1])
    for title, views in query_results[0]:
        print('"{}" - {} views'.format(title, views))


def print_errors(query_results):
    print(query_results[1])
    for time, error_percentage in query_results[0]:
        print('{} - {} % errors'.format(time, error_percentage))


if __name__ == '__main__':
    results_popular_articles = get_results(q), art_title
    results_popular_authors = get_results(r), aut_title
    results_failed_requests = get_results(final_query), fr_title

    print_results(results_popular_articles)
    print_results(results_popular_authors)
    print_errors(results_failed_requests)
