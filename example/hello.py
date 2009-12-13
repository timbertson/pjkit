#!/usr/bin/env python
import sys, os
import urllib
base = os.path.dirname(__file__)
sys.path.append(os.path.join(base, '..'))

import logging, logging.config
logging.config.fileConfig(os.path.join(base, 'logging.conf'))

# pjkit for gtk:
from pjkit.gtk_webkit_app import GtkWebkitApp
from pjkit.gtk_webkit_bridge import GtkWebkitBridge

class Context(object):
	def get_uname(self):
		# an example function to call from javascript
		return '\n'.join(os.uname())

class Main(object):
	def __init__(self):
		self.app = GtkWebkitApp()

		uri = 'file://' + urllib.quote(
			os.path.abspath(os.path.join(base, 'hello.html')))

		# setup the webkit / js bridge
		window, webview = self.app.webkit_window(uri)
		self.js = GtkWebkitBridge(webview, Context()).proxy
	
	def run(self):
		# register app_main to run once GTK has started
		self.app.add_thread(self.app_main)
		self.app.run()

	def app_main(self):
		logging.info("first JS call...")
		print "your name is: %r" % (self.js.getUserInput('name'),)


if __name__ == '__main__':
	sys.exit(Main().run())


