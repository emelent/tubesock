import sys

from rq import Queue
from src.job.downloader import conn
from .utils import fetch_video, fetch_url


# def do_word_count(name, url):
# 	q = Queue(name=name, connection=conn, timeout='1h', result_ttl=3000)
# 	return q.enqueue(count_words_at_url, url)

def do_video_fetch(name, url, opts={}):
	q = Queue(name=name, connection=conn, timeout='1h', result_ttl=3000)
	return q.enqueue(fetch_video, url)