#-*-coding:utf-8-*-
import psutil 
import copy
import datetime,time
import pprint
import os
import numpy as np
from .redisOperation import redisOperation

def detail_information(station_name="station1"):
	# 先预设信息存储的字典格式:
	information = {}

	machine = information.setdefault('machine',{})

	# 主机信息：CPU负载，CPU核数，CPU睿频;内存消耗，内存容量；磁盘使用情况，磁盘总容量；
	
	# 操作系统版本:
	os_information = os.popen('lsb_release -a').read()
	machine['os_name'] = os_information[os_information.find('Description')+13:os_information.find('Release')-2]

	# 最大主频：
	machine['max_frequent'] = os.popen('lscpu|grep Model').read()[-8:-1]

	#CPU负载：
	machine['cpu_load'] = str(psutil.cpu_percent(interval=0.5))+"%"  ## 这个为啥老是0？？？？（必须设置一个时间间隔才行-！！！）

	#CPU核数:
	machine['kernel_num'] = psutil.cpu_count()

	#CPU当前频率:
	machine['cpu_frequent'] = str(round(psutil.cpu_freq().current/1024,2))+'GHz'

	#内存容量：
	machine['memory_total'] = str(round(float(psutil.virtual_memory().total)/(1024*1024*1024),2))+'GB'

	#内存消耗情况:
	machine['memory_percent'] = str(psutil.virtual_memory().percent) + '%'

	#磁盘总容量:
	machine['disk_total'] = str(round(float(psutil.disk_usage('/').total)/(1024*1024*1024),2))+'GB'

	#磁盘使用占比：
	machine['disk_precent'] =  str(psutil.disk_usage('/').percent)+'%'
	
	#发包数量:
	machine['packet_sent'] = psutil.net_io_counters().packets_sent

	#收包数量:
	machine['packet_recv'] = psutil.net_io_counters().packets_recv

	#接收时的错误数:
	machine['err_in'] = psutil.net_io_counters().errin

	#发送时的错误数:
	machine['err_out'] = psutil.net_io_counters().errout

	#丢弃的传入数据包总数:
	machine['drop_in'] = psutil.net_io_counters().dropin

	#丢弃的传出数据包总数:
	machine['drop_out'] = psutil.net_io_counters().dropout

	#----------------------------------------------------------------------------------------
	# 这里监控程序只考虑几个固定的程序：(twiseted,识别程序，消息队列！)

	process = information.setdefault('process',{})

	# 进程总数：
	process['process_toal'] = len(psutil.pids())

	# 进程相关信息:
	process['process_information'] = []

	# 获取相应的进程信息：
	process_information = {}
	# process_name = ['Twiseted','Recongniton','Message_Queue']
	process_name = ['celery','redis-server']
	information_templete = {
		'ID':None, # 进程ID
		'physical_memory':0, # 占用物理内存
		'status':None, # 进程状态
		'run_time':0 # 进程运行时间
	}

	for name in process_name:
		process_information.setdefault(name,copy.deepcopy(information_templete))


	for pid in psutil.pids():
		p = psutil.Process(pid)  # have an error! some process from celery have error!
		if len(p.cmdline()) > 0:
			if ('client_test.py' in p.cmdline()) or (p.name() in process_name):
				information_detail  = process_information.get('client_test.py' if 'client_test.py' in p.cmdline() else p.name())
				information_detail['ID'] = pid
				information_detail['physical_memory'] += p.memory_full_info().uss/(1024*1024) # 单位是MB
				information_detail['status'] = p.status() 
				information_detail['run_time'] += round((datetime.datetime.now() - datetime.datetime.fromtimestamp(p.create_time())).total_seconds()/3600,1) # 单位：小时

	print (process_information)

	for key,values in process_information.items():
		values['process_name'] = key
		values['physical_memory'] = str(values['physical_memory']) + 'MB'
		values['run_time'] = str(values['run_time']) + 'h'
		if key == 'celery':
			values['status'] = 'running'
		process['process_information'].append(values)


	# 人数告警信息:
	information['video'] = {
		# 'person_number':None,
		# 'person_overflow': False,
		'data':None, # []
	}

	if True:
		r = redisOperation(station_name=station_name)
		r_key = datetime.datetime.now().strftime('%Y-%m-%d')+"_"+station_name
		r_data = r.getData(r_key)
		overflow_value = r.getData('overflow_dict').get(station_name)
		index = r.getData(r_key+"_index")
		print (r_key,r_key+"_index",index)
		last_index = index+(15*30)
		data = r_data['data'][index:last_index]
		Length = len(data)
		# index = index+Length
		# 此时，被处理的数据的长度必须要大于一秒的图片数量，否则不进行处理。
		if Length >= 15:
			r.setData(r_key+"_index",index+Length)
			result = getSecondPerson(data,15,overflow_value,station_name,(r_data['start_time']+int(index/15)))
			information['video']['data'] = result
		else:
			information['video']['data'] = []
	else:
		pass


	# 信息时间：(这里要注意一点：时间戳都是以UTC时间来定的，跟时区没关系，只有时间才跟时区有关系！	)
	# information['time'] = r_data['start_time']
	information['time'] = time.mktime(datetime.datetime.now().timetuple())
	# information['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	return information


def getVideoData(data,interval,limit,station_name,utc_seconds):

	date = datetime.datetime.fromtimestamp(utc_seconds).strftime('%Y-%m-%d')

	data_templete = {
		'start_time': False,
		'end_time': False,
		'address': station_name,
		'mean_person': None,
		'video_path': None
	}

	temporary_result = []
	time_key = utc_seconds 
	result = []

	copy_data = copy.deepcopy(data_templete)

	for index,value in enumerate(data):
		time_key = int((index+1)/interval) + utc_seconds
		if value >= limit:
			temporary_result.append(value)
			if not copy_data['start_time']:
				copy_data['start_time'] = time_key
		else:
			if len(temporary_result) >= interval:
				copy_data['end_time'] = int((index)/interval) + utc_seconds
				copy_data['address'] = station_name
				copy_data['mean_person'] = int(round(np.mean(temporary_result)))
				copy_data['video_path'] = os.path.join("/static/recommend/"+date+"/"+station_name,str(copy_data['start_time'])+'-'+str(copy_data['end_time']))
				result.append(copy_data)
				temporary_result = []
			copy_data = copy.deepcopy(data_templete)
			temporary_result = []
	
	return result
			 



def getSecondPerson(data,interval,limit,station_name,utc_seconds):

	data_templete = {
		'time': utc_seconds,
		'address': station_name,
		'person_number': None,
		'person_overflow': None
	}

	temporary_result = []
	result = []

	for index,value in enumerate(data):
		temporary_result.append(value)
		if len(temporary_result) == interval:
			second_data = copy.deepcopy(data_templete)
			second_data['time'] += ((index+1)/interval)
			second_data['person_number'] = int(round(np.mean(temporary_result)))
			second_data['person_overflow'] = True if (int(round(np.mean(temporary_result))) >= limit) else False
			result.append(second_data)
			temporary_result = []

	return result



if __name__=='__main__':
	pprint.pprint (detail_information())





