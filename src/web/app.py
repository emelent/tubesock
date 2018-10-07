import sys
sys.path.insert(0, './src')

import os
from flask import Flask, render_template, jsonify, request
from rq import Queue
from job.downloader import conn
from cmd.utils import count_words_at_url, fetch_video

q = Queue(connection =conn, timeout='1h', result_ttl='3h')

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key'
    )

    return app

app = create_app()


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/download", methods=['POST'])
def downlad():
	job = q.enqueue(count_words_at_url, request.form['url'])
	return jsonify({
		'id': job.id 
	})

@app.route("/fetch", methods=['POST'])
def fetch():
	job = q.enqueue(fetch_video, request.form['url'])
	return jsonify({
		'id': job.id 
	})

@app.route('/poll/<id>')
def poll(id):
	job = q.fetch_job(id)
	if job is None:
		return jsonify({'error': "Invalid id", 'result': None})

	return jsonify({'result': job.result})


@app.route("/result/<id>")
def result(id):
	job = q.fetch_job(id)
	if job is None:
		return jsonify({'error': "Invalid id"})
	return jsonify({'result': job.result})

if __name__ == "__main__":
	app.run(debug=True)