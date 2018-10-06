from rq import Queue
from job.downloader import conn
from utils import count_words_at_url
import sys

def run(name, url):
	q = Queue(name=name, connection=conn, timeout='1h', result_ttl=3000)
	return q.enqueue(count_words_at_url, url)

if __name__ == '__main__':
	num_args = len(sys.argv)
	if num_args < 2:
		print("Please provide url.")
		sys.exit(1)

	name = 'default' if num_args < 3 else sys.argv[2]
	job = run(name, sys.argv[1])
	while not job.result: pass
	
	print(job.result)
