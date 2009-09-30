#!/opt/local/bin/python2.5
import sys, os
import urllib
base = os.path.dirname(__file__)
sys.path.append(os.path.join(base, '..'))

import logging, logging.config
logging.config.fileConfig(os.path.join(base, 'logging.conf'))

# pjkit for gtk:
from pjkit.gtk_webkit_app import GtkWebkitApp as App
from pjkit.gtk_webkit_bridge import GtkWebkitBridge


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
		bridge = GtkWebkitBridge(webview)
		bridge.context = {'get_uname': get_uname}
		# once we set up the bridge, we can treat the proxy
		# object as if it were the javascript runtime
		self.js = bridge.proxy
	
	def run(self):
		# add_thread takes either a thread or a callable
		self.app.add_thread(self.app_main)
		self.app.run()

	def app_main(self):
		logging.info("first JS call...")
		print "your name is: %r" % (self.js.getUserInput('name'),)


if __name__ == '__main__':
	sys.exit(Main().run())


