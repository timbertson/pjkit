#!/opt/local/bin/python2.5
import sys
import os
base = os.path.dirname(__file__)
sys.path.append(os.path.join(base, '..','src'))

import logging
import logging.config
logging.config.fileConfig(os.path.join(base, 'logging.conf'))

import json_bridge
from gtk_webkit_app import GtkWebkitApp as App

def main():
	app = App()
	path = os.path.abspath(os.path.join(base, 'hello.html'))
	import urllib
	webkit = app.open_window('file://' + urllib.quote(path))
	bridge = json_bridge.GtkWebkitBridge(webkit)
	bridge.context = {'get_uname':lambda: os.uname}
	js = bridge.proxy
	app.spawn()
	import time; time.sleep(0.3)
	logging.info("first JS call...")
	print "your name is: %r" % (js.getUserInput('name'),)

if __name__ == '__main__':
	sys.exit(main())


