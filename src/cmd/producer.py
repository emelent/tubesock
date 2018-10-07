import sys
sys.path.insert(0, './src')

from rq import Queue
from job.downloader import conn
from cmd.utils import count_words_at_url, fetch_video


def do_word_count(name, url):
	q = Queue(name=name, connection=conn, timeout='1h', result_ttl=3000)
	return q.enqueue(count_words_at_url, url)

def do_video_fetch(url, opts={}):
	q = Queue(name=name, connection=conn, timeout='1h', result_ttl=3000)
	return q.enqueue(count_words_at_url, url)

if __name__ == '__main__':
	num_args = len(sys.argv)
	if num_args < 2:
		print("Please provide url.")
		sys.exit(1)

	name = 'default' if num_args < 3 else sys.argv[2]
	job = do_word_count(name, sys.argv[1])
	while not job.result: pass
	
	print(job.result)
