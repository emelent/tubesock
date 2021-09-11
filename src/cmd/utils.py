from __future__ import unicode_literals
import os
import subprocess
import youtube_dl
import logging

LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger()

video_dir = os.path.join("./", "src/web/static/video/")
ydl_opts = {
    "nocheckcertificate": True,
    "outtmpl": os.path.join(video_dir, "%(id)s.%(ext)s"),
}


def get_file_name(name):
    files = os.listdir(video_dir)
    for f in files:
        if f.split(".")[0] == name:
            return f
    return ""


def fetch_url(url, opts=""):
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    data = ydl.extract_info(url, download=False)
    cmd = ["youtube-dl", "-g", "-q", "--no-check-certificate", url]
    cmd.extend(opts.split())
    result = subprocess.check_output(cmd)
    return {
        "url": result.decode("utf-8"),
        "title": data["title"],
        "ext": data["ext"],
    }


def fetch_video(url, opts=ydl_opts, hd=False, start=None, duration=None):
    # merge the opts
    opts.update(ydl_opts)

    # use SD if hd not set
    if not hd:
        opts["format"] = "18"

    # download the video
    with youtube_dl.YoutubeDL(opts) as ydl:
        logger.info("extracting url info")
        data = ydl.extract_info(url, download=False)
        logger.info("downloading url")
        ydl.download([url])
        fname = os.path.join(video_dir, get_file_name(data["id"]))

        # trim the video
        if start is not None and duration is not None:
            logger.info("trimming url")
            trim_bideo(start, duration, fname, fname)

        # upload to firebase
        logger.info("uploading to firebase")
        url = upload_to_firebase(fname)

        return {"url": url, "ext": data["ext"], "title": data["title"]}
    return "FAIL"


def trim_video(start, duration, src_filename, dst_filename):
    """
    Trim video using input video
    """
    cmd = [
        "ffmpeg",
        "-i",
        src_filename,
        "-ss",
        start,
        "-t",
        duration,
        "-async",
        "1",
        dst_filename,
    ]
    subprocess.check_output(cmd)


def upload_to_firebase(filename):
    import os
    import uuid
    from datetime import timedelta
    import firebase_admin
    from firebase_admin import credentials, storage

    # get credentials
    google_cred_json = os.getenv("GOOGLE_SERVICES_JSON")
    if google_cred_json == None:
        cred = credentials.Certificate("./google-services.json")
    else:
        import json

        cred = json.loads(google_cred_json)

    # initialize firebase
    bucket_name = "nimbus9-5.appspot.com"
    firebase_admin.initialize_app(cred, {"storageBucket": bucket_name})

    # get bucket
    bucket = storage.bucket(bucket_name)

    # upload file
    blob = bucket.blob(uuid.uuid4().hex)
    blob.upload_from_filename(filename)
    download_url = blob.generate_signed_url(expiration=timedelta(3))
    print(download_url)

    return download_url
