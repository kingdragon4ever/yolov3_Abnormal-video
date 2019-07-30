import sys
from video3_count import unnormal_video
from toH264 import H264
from person_flow import YOLO
from person_flow import detect_video
import datetime

from celery_app.client_testN import pass_start
# if len(sys.argv) < 2:
#     print("Usage: $ python {0} [video_path] [output_path(optional)]", sys.argv[0])
#     exit()
def detect(station,video_path):
 start = datetime.datetime.now()
    # video_path = sys.argv[1]
    # if len(sys.argv) > 2:
        # output_path = sys.argv[2]
        # detect_video(YOLO(), video_path, output_path)
    # else:
 image_dir,x = detect_video(YOLO(),station,video_path)
 print(image_dir)
 video_dir = unnormal_video(station,image_dir,x,8)
 H264(video_dir)
#print (video_dir)
 end = datetime.datetime.now() 
 print (end-start)
 pass_start.delay(station,'video')

if __name__ == '__main__':
	video_path = sys.argv[1]
	detect('station4',video_path)