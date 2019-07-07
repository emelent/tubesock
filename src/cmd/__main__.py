import sys
from .producer import do_video_fetch


num_args = len(sys.argv)
if num_args < 2:
    print("Please provide video url.")
    sys.exit(1)

name = 'default' if num_args < 3 else sys.argv[2]
job = do_video_fetch(name, sys.argv[1])
print("Waiting for download to complete...")
while not job.result: pass
print(job.result)
