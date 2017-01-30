#todo: http://www.yinyuetai.com/insite/get-video-info?json=true&videoId=
#coding: utf-8

import urllib
import urllib2
import os,sys
import re

def Schedule(a, b, c):
    per = 100.0 * a * b / c
    if per > 100 : per = 100
    sys.stdout.write(u"Download: %.1f%%\r" % per)
    sys.stdout.flush()

def getpath():
	path = os.path.abspath('.')
	new_path = os.path.join(path,'FLV')
	if not os.path.isdir(new_path):
		os.mkdir(new_path)
	return new_path

def getvideoid():
	id = raw_input('Please input video ID: ')
	return id

def gethtml(id):
	url = 'http://www.yinyuetai.com/insite/get-video-info?flex=true&videoId=' + id
	return url


def handlehtml(url):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	try:
		request = urllib2.Request(url, None, headers)	
		html = urllib2.urlopen(request)
		data = html.read()
		#----------------------------
		reg = re.compile(r"http://\w*?\.yinyuetai\.com/uploads/videos/common/.*?(?=&br)", re.S)
		findlist = re.findall(reg, data)
		#HC(432p) HD(540p) HE(720p)
		#
		if len(findlist) >= 3:
			return findlist[2]
		elif len(findlist) >= 2:
			return findlist[1]
		else:
			return findlist[0]
	except:
		print 'Reading vodeolist failed!'


def get_vodeoname(id):
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
	try:
		url = 'http://v.yinyuetai.com/video/' + id
		request = urllib2.Request(url, None, headers)	
		html = urllib2.urlopen(request)
		data2 = html.read()
		#-----------------------------
		reg = re.compile(r'title : \"(.*?)\",', re.S)
		videoname = re.findall(reg, data2)
		return videoname[0]
	except:
		print "Can't find videoname!"
		videoname = raw_input('Please input videoname: ')
		return videoname


def download(videosrc, path, videoname):
	name = videoname + '.flv'
	path = path + '/' + name.replace('/','-')
	print 'Videoname: ' + videoname
	try:
		urllib.urlretrieve(videosrc, path, Schedule)
		print 'Download success!'
		print 'File path: ' + path
	except:
		print 'Download failed!'	

def main():
	path = getpath() 
	id = getvideoid()
	videoname = get_vodeoname(id)
	url = gethtml(id)
	videosrc = handlehtml(url)
	download(videosrc, path, videoname)

if __name__=='__main__':
	main()
		