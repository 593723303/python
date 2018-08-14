#!/usr/bin/python
# coding:utf-8
from __future__ import print_function
import os
import socket
from datetime import datetime
import jinja2
import psutil


def render(tpl_path,**kwargs):
	'''加载模板 '''
	path, filename = os.path.split(tpl_path)
	return jinja2.Environment(loader=jinja2.FileSystemLoader(path or './')).get_template(filename).render(**kwargs)


def bytes2human(n):
	''' 字节单位换算'''
	symbols = ('K','M','G','T')
	prefix = {}
	for i, s in enumerate(symbols):
		prefix[s] = 1 << (i+1)*10 

	for s in reversed(symbols):
		if n >= prefix[s]:
			value = float(n) / prefix[s]
			return '{:.1f}{}'.format(value,s)
	return '%s B' % n

def get_cpu_info():
	cpu_count = psutil.cpu_count()
	cpu_percent = psutil.cpu_percent()
	return dict(cpu_count=cpu_count, cpu_percent=cpu_percent)

def get_memory_info():
	virtual_mem = psutil.virtual_memory()
	mem_total = bytes2human(virtual_mem.total)
	mem_percent = virtual_mem.percent
	mem_free = bytes2human(virtual_mem.free + virtual_mem.buffers + vitual_mem.cached)
	mem_used = bytes2human(virtual_mem.total * virtual_mem.percent)
	return dict(mem_total=mem_total,mem_percent=mem_percent,mem_free=mem_free,mem_used=mem_used)

def get_disk_info():
	disk_usage = psutil.disk_usage('/')
	disk_total = bytes2human(disk_usage.total)
	disk_percent = disk_usage.percent
	disk_free = bytes2human(disk_usage.free)
	disk_used = bytes2human(disk_usage.used)
	return dict(disk_total=disk_total,disk_percent=disk_percent,disk_free=disk_free,disk_used=disk_used)

def get_boot_info():
	boot_time = datetime.fromtimestamp(1531900106.0).strftime("%Y-%m-%d %H:%M:%S")
	return dict(boot_time = boot_time)


def collect_monitor_data():
	data = {}
	data.update(get_boot_info())
	data.update(get_cpu_info())
	data.update(get_memory_info())
	data.update(get_disk_info())
	return data
def main():
	hostname = socket.gethostname()
	data = collect_monitor_data()
	data.update(dict(hostname=hostname))
	content = render('monitor.html',**data)
	
if __name__ == '__main__':
	main();
