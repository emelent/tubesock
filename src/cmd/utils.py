from __future__ import unicode_literals
import os
import requests
import subprocess
import youtube_dl

ydl_opts = {
	'nocheckcertificate': True,
	'outtmpl': os.path.join('./src/web/static/video/', '%(id)s.%(ext)s'),
}

def count_words_at_url(url):
	resp = requests.get(url)
	return len(resp.text.split())

def fetch_url(url, opts=''):
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    data = ydl.extract_info(url, download=False)
    cmd = ['youtube-dl', '-g', '-q', '--no-check-certificate', url]
    cmd.extend(opts.split())
    result = subprocess.check_output(cmd)
    return {
        'url': result.decode('utf-8'),
        'title': data['title'],
        'ext': data['ext'],
    }

def fetch_video(url, opts=ydl_opts):
	# merge the opts
	opts.update(ydl_opts)

	# download the video
	with youtube_dl.YoutubeDL(opts) as ydl:
		data = ydl.extract_info(url, download=False)
		ydl.download([url])
		fname = '{}.{}'.format(data['id'], data['ext'])
		return {
			'url': '/static/video/{}'.format(fname),
			'ext': data['ext'],
			'title': data['title']
		}
	return 'FAIL'
