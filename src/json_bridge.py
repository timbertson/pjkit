from lib.json import json
import re
from time import sleep
import Queue

import logging

SLEEP_TIME = 0.3

def escape(str):
	escaped_slashes = str.replace('\\','\\\\')
	return escaped_slashes.replace("'","\\'")
	
class JsProxy(object):
	def __init__(self, bridge):
		self.__bridge = bridge
	
	def __getattr__(self, name):
		result = []
		def handle_result(val):
			logging.debug("got result for function %s!" % (name,))
			result.append(val)
			
		def perform_action_sync(*args):
			self.__bridge.send(name, args, on_return=handle_result)
			while len(result) == 0:
				sleep(SLEEP_TIME)
			logging.debug("2: got result for function %s!" % (name,))
			return result[0]
		return perform_action_sync


class JsonBridge(object):
	def __init__(self, web, context={}):
		self.web = web
		self.context = context
		self._next_cb = 1
		self._callbacks = {}
		self.proxy = JsProxy(self)
	
	def send(self, function, args=(), on_return=None):
		obj = {
			'method':function,
			'args': args,
		}
		if on_return is not None:
			cb_key = obj['respond_to'] = self._next_cb
			self._next_cb += 1
			self._callbacks[cb_key] = on_return

		self.do_send("PYTHON._recv('%s');" % (escape(json.write(obj)),))
	
	def _respond_to(self, callback_id, value):
		json_val = json.write(value)
		self.do_send("PYTHON._recv_cb(%s, '%s');" % (callback_id, escape(json_val)))

	def recv(self, jsonStr):
		"""receive a json string from javascript.
		fields we expect in the JSON:
		if this is the result of a javascript computation requested by python, these MUST be set:
			- responding_to: the id of the python callback to which this result should be sent
			- value: if responding_to, this is the javascript result

		if responding_to is not present, these MUST be set:
			- method: the python method to call. Note that this can be any eval-able string - e.g foo[-1].bar
					this object is looked up from the `context` dictionary
			- args: arguments to be sent to the python object
		and this MAY be set:
			-respond_to: the id of the javascript callback that will handle the return value

		Note that as a result of a call to recv, the action will be placed in a queue,
		rather than executed immediately
		"""
		obj = json.read(jsonStr)
		logging.debug("recveiving obj: %r" % (obj,))
		if 'responding_to' in obj:
			def do_work():
				callback_id = obj['responding_to']
				callback = self._callbacks[callback_id]
				callback(obj['value'])
				del self._callbacks[callback_id]
		else:
			def do_work():
				logging.debug("callable = x")
				callable = eval(obj['method'], {}, self.context)
				logging.debug("callable = %r" % (callable,))
				result = callable(*obj['args'])
				logging.debug("result of requested computation: %r" % (result,))
				if 'respond_to' in obj:
					self._respond_to(obj['respond_to'], result)
		self.perform(do_work)



import gtk
import gobject
import threading
import logging
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

