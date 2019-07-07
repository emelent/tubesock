
from .downloader import conn, listen
from rq import Worker, Queue, Connection

with Connection(conn):
    worker = Worker(map(Queue, listen))
    worker.work()