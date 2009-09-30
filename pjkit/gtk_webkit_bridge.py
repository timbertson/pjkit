import gtk
import gobject
import threading
import logging
from json_bridge import JsonBridge
from gtk_helpers import asynchronous_gtk_message

class GtkWebkitBridge(JsonBridge):
	def __init__(self, *a):
		super(type(self), self).__init__(*a)
		self.__ready = False
		self.__readycond = threading.Condition()
		self.web.connect('title-changed', self.__on_title_changed)
		self.web.connect('load-finished', self.__on_ready)
	
	def __on_ready(self, widget, frame):
		logging.debug("webkit view is ready!")
		self.__readycond.acquire()
		self.__ready = True
		self.__readycond.notifyAll()
		self.__readycond.release()

	def __on_title_changed(self, widget, frame, title):
		self.recv(title)
	
	def perform(self, callable):
		# this should be called from a webkit-title-change, which
		# is alway in the main thread. so we can just run it immediately
		callable()

	def do_send(self, msg):
		self.__readycond.acquire()
		if self.__ready is False:
			logging.debug("waiting for webkit readyness")
			self.__readycond.wait()
		self.__readycond.release()
		logging.debug("sending webkit message: %s" % (msg,))
		def doit():
			self.web.execute_script(msg)
			logging.debug("message SENT! (%s)" % (msg,))
		#asynchronous_gtk_message(lambda: self.web.execute_script(msg))
		asynchronous_gtk_message(doit)
