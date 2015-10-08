from google.appengine.api import urlfetch
import time
import urllib2

def fetchURL(url):
    
	
	for i in range(10):
		rpc = urlfetch.create_rpc()
		urlfetch.make_fetch_call(rpc,url)
	
		try:
			result = rpc.get_result()
			if result.status_code == 200:
				return result.content
	
		except urlfetch.DownloadError:
			pass
		
		time.sleep(0.01)
	
	return 502
	
def synch_fetchURL(url):
	try:
		result = urlfetch.fetch(url)
		if result.status_code == 200:
			return result.content
	except :
		return 502
	return 502	