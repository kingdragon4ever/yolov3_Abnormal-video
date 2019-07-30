# -*- coding:utf8 -*-
import os
import cv2
import numpy as np
import pprint
import datetime
import time
from celery_app.redisOperation import redisOperation


def unnormal_video(station_name,img_dir,x,quezhi):
  # station_name="station1"
  
  sourceDir="/mnt/video-detect"
  date=datetime.datetime.now().strftime("%Y-%m-%d")
  print (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
  video_dir=os.path.join(sourceDir,date+'/'+station_name+'/')

  if not os.path.isdir(video_dir):
      os.makedirs(video_dir)
  else: 
      pass


  # x = [11, 12, 12, 12, 12, 11, 12, 12, 11, 11, 11, 10, 10, 10, 10, 11, 10, 10, 11, 12, 11, 12, 12, 13, 14, 14, 14, 14, 14, 13, 15, 14, 14, 13, 14, 13, 14, 13, 14, 14, 12, 13, 15, 15, 16, 15, 15, 15, 15, 16, 17, 17, 15, 14, 15, 15, 15, 15, 16, 14, 15, 14, 13, 11, 12, 11, 11, 11, 12, 13, 12, 11, 12, 14, 15, 14, 15, 15, 16, 16, 14, 13, 14, 13, 13, 13, 14, 11, 12, 12, 12, 12, 13, 13, 13, 12, 13, 14, 13, 14, 14, 14, 11, 12, 14, 12, 12, 12, 13, 14, 12, 13, 13, 12, 12, 11, 11, 11, 10, 11, 11, 13, 12, 13, 13, 15, 16, 14, 12, 10, 10, 10, 10, 11, 11, 12, 11, 12, 12, 12, 14, 14, 14, 14, 13, 14, 14, 15, 14, 14, 14, 13, 14, 13, 12, 13, 12, 12, 13, 13, 14, 13, 13, 13, 13, 13, 12, 11, 12, 13, 12, 11, 10, 10, 11, 12, 11, 12, 12, 13, 12, 16, 13, 13, 13, 14, 12, 13, 11, 13, 12, 11, 11, 13, 13, 13, 12, 12, 12, 13, 14, 15, 13, 13, 13, 12, 14, 14, 15, 14, 13, 15, 14, 15, 16, 16, 16, 16, 14, 15, 15, 15, 13, 13, 12, 12, 15, 14, 13, 12, 10, 12, 10, 12, 9, 11, 12, 11, 10, 10, 9, 11, 10, 9, 10, 13, 12, 14, 14, 14, 15, 15, 13, 12, 11, 13, 13, 12, 11, 11, 10, 11, 12, 13, 13, 11, 10, 11, 13, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 15, 14, 14, 14, 15, 13, 13, 14, 14, 14, 14, 13, 13, 14, 12, 13, 12, 12, 12, 15, 14, 14, 15, 14, 14, 14, 13, 13, 13, 13, 15, 14, 14, 14, 14, 14, 14, 12, 12, 11, 11, 12, 13, 13, 13, 13, 13, 13, 12, 13, 14, 13, 12, 12, 12, 11, 13, 13, 12, 15, 14, 16, 15, 14, 14, 14, 14, 14, 13, 15, 14, 14, 13, 12, 12, 13, 13, 14, 13, 14, 14, 14, 12, 13, 12, 13, 11, 13, 12, 12, 13, 12, 12, 11, 12, 12, 11, 13, 10, 11, 12, 14, 13, 11, 12, 12, 13, 12, 13, 14, 13, 12, 12, 13, 13, 14, 13, 14, 13, 13, 15, 14, 13, 14, 13, 13, 14, 13, 14, 14, 15, 15, 15, 15, 15, 15, 16, 15, 14, 15, 16, 16, 16, 17, 17, 16, 16, 16, 15, 15, 15, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 13, 14, 14, 14, 15, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 15, 14, 14, 13, 13, 13, 13, 13, 14, 14, 15, 15, 16, 14, 13, 13, 12, 10, 11, 12, 14, 13, 13, 11, 13, 14, 12, 10, 10, 11, 12, 13, 13, 13, 13, 13, 14, 13, 13, 13, 13, 14, 12, 12, 11, 12, 11, 11, 11, 11, 11, 11, 12, 11, 11, 12, 13, 13, 12, 12, 12, 12, 12, 12, 12, 12, 13, 12, 13, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 13, 12, 13, 13, 13, 13, 13, 13, 12, 13, 14, 14, 13, 13, 13, 13, 12, 12, 13, 13, 13, 13, 13, 13, 12, 12, 10, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 13, 13, 11, 11, 11, 11, 12, 11, 11, 11, 12, 12, 14, 12, 11, 12, 14, 12, 12, 12, 12, 12, 12, 12, 12, 10, 10, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 10, 11, 11, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 11, 12, 11, 11, 12, 11, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 12, 12, 11, 11, 11, 13, 12, 13, 13, 15, 15, 15, 13, 13, 13, 13, 13, 14, 13, 13, 13, 13, 13, 13, 13, 12, 12, 13, 13, 14, 11, 10, 10, 10, 10, 11, 9, 9, 9, 9, 10, 9, 12, 11, 12, 11, 12, 12, 12, 12, 11, 11, 13, 13, 13, 12, 14, 12, 11, 12, 13, 13, 12, 12, 11, 12, 13, 11, 11, 11, 11, 12, 11, 10, 13, 13, 12, 15, 13, 13, 14, 11, 12, 11, 10, 12, 12, 12, 12, 14, 13, 12, 13, 13, 12, 12, 12, 11, 11, 11, 11, 11, 12, 13, 14, 13, 12, 13, 12, 13, 13, 12, 12, 12, 12, 11, 11, 11, 11, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 12, 13, 13, 14, 14, 14, 14, 13, 13, 13, 13, 13, 14, 14, 12, 13, 13, 13, 12, 14, 14, 13, 13, 13, 13, 13, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 12, 12, 12, 13, 11, 11, 11, 12, 11, 12, 12, 12, 12, 13, 12, 12, 12, 12, 12, 13, 13, 14, 12, 12, 12, 13, 13, 14, 14, 14, 13, 13, 13, 14, 13, 14, 14, 13, 14, 14, 14, 14, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 13, 13, 13, 14, 14, 14, 15, 14, 14, 14, 14, 14, 14, 14, 14, 13, 13, 14, 13, 14, 13, 12, 12, 13, 13, 12, 11, 11, 12]
  x_length = len(x)
  print (x_length)
  y=[]
  finallist=[]
  avglist=[]

  for index1,i in enumerate(x):
      #print(index1,i)
      if i>quezhi: 
         y.append(index1)
        # file = open('station3.txt', 'w')
        # #file.write(str(y));
         #file.close()
         #print(y)
        
  result=[]
  avgresult=[]
  for index,x1 in enumerate(y):
      last_index = index-1
      if last_index > 0:
        if (y[index]-y[last_index] <= 15):
           for i in range(y[last_index]+1,y[index]+1):
               result.append(str(i)+'.jpg')
               avgresult.append(i)
        else:
            if len(result) >= 30:
               # print ("add successful!")
               finallist.append(result)
               avglist.append(avgresult)
            result = []
            avgresult = []
      else:
        result.append(str(x1)+'.jpg')
        avgresult.append(x1)
  # add last result to finallist :(when result not is null!)
  if len(result) >= 30:
      finallist.append(result)
      avglist.append(avgresult)
  '''for index,x1 in enumerate(y):
      print(index,x1)'''




  path = './guanfang3/'
  filelist = os.listdir(path)

  print (len(finallist))


  m = []
  avg = []

  unnormal_index = []


  for index2,item2 in enumerate(avglist):
      print(index2, item2)
      print(item2[0])
      print(item2[-1])
      unnormal_index.append((item2[0],item2[-1]))
      avg.append(round(np.mean([x[i] for i in item2])))


  print (unnormal_index,avg)



  for index,item in enumerate(finallist):
      print(index,item)
      r = redisOperation()
      r.getKeys() 
      x = r.getData(date+"_"+station_name)


      timestamp=x['start_time']
      # video=cv2.VideoWriter(video_dir+"{}_".format(index)+"_"+str(item2[0])+"-"+str(item2[-1])+"--"+str(round(avg[index]))+".mp4", cv2.VideoWriter_fourcc('m','p','4','v'), 30, (1920,1080))
      #video = cv2.VideoWriter(video_dir+str(unnormal_index[index][0])+"_"+str(unnormal_index[index][1])+"_"+str(int(avg[index]))+"_bak"+".mp4",cv2.VideoWriter_fourcc('m','p','4','v'), 10, (1920,1080))
      video = cv2.VideoWriter(video_dir+str(int(round(timestamp+unnormal_index[index][0]/30)))+"-"+str(int(round(timestamp+unnormal_index[index][1]/30)))+"-"+str(int(avg[index]))+"_bak"+".mp4",cv2.VideoWriter_fourcc('m','p','4','v'), 30, (1920,1080))
      print (video_dir+str(unnormal_index[index][0])+"_"+str(unnormal_index[index][1])+"_"+str(int(avg[index]))+".mp4")
      for value in item:
        if value.endswith('.jpg'):
          # file_path='/mnt/image-detect/2019-07-14/station1/'+value   
          file_path=img_dir+value
          img1 = cv2.imread(file_path)
          video.write(img1)
      video.release()

  return video_dir






