#-*-coding:utf-8-*-

from celery_app import task1
from celery_app import task2

task1.add.delay(2,8)

task2.multiply.delay(3,7)

print ('hello,world!')
