#!/opt/local/bin/python2.5
import sys
import os
base = os.path.dirname(__file__)
sys.path.append(os.path.join(base, '..','src'))

import logging
import logging.config
logging.config.fileConfig(os.path.join(base, 'logging.conf'))

import threading
import urllib

import json_bridge
from gtk_webkit_app import GtkWebkitApp as App


def get_uname():
	# an example function to call from javascript
	uname = '\n'.join(os.uname())
	return uname

class Main(object):
	def __init__(self):
		self.app = App()
		path = os.path.abspath(os.path.join(base, 'hello.html'))

		# setup the webkit / js bridge
		window, webview = self.app.webkit_window('file://' + urllib.quote(path))
		bridge = json_bridge.GtkWebkitBridge(webview)
		bridge.context = {'get_uname': get_uname}
		self.js = bridge.proxy
	
	def run(self):
		self.app.add_thread(threading.Thread(target=self.app_main))
		self.app.run()

	def app_main(self):
		logging.info("first JS call...")
		print "your name is: %r" % (self.js.getUserInput('name'),)


if __name__ == '__main__':
	sys.exit(Main().run())


