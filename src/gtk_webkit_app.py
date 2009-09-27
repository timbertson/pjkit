import Queue

import gtk
import gobject
import webkit
import logging
import signal
import threading

def gtk_do(action):
	logging.debug('> getting gtk lock')
	gtk.gdk.threads_enter()
	logging.debug('> got gtk lock')
	action()
	logging.debug('> released gtk lock')
	gtk.gdk.threads_leave()

class GtkWebkitApp(object):
	quit = False
	def __init__(self):
		self._worker_threads = []
		
	@classmethod
	def set_quit(cls, *a, **kw):
		gtk_do(gtk.main_quit)
		cls.quit = True
	
	def gtk_action(self, callable, sync=False):
		"""perform an action (optionally synchronously) in the main (GTK+) thread"""
		if sync:
			done = []
			cond = threading.Condition()

		def perform():
			callable()
			if sync:
				cond.acquire()
				done.append(True)
				cond.notify()
				cond.release()

		gobject.idle_add(perform)
		if not sync:
			return
		while len(done) == 0:
			cond.acquire()
			cond.wait()
			cond.release()


	def webkit_window(self, uri):
		window = gtk.Window()
		box = gtk.VBox(homogeneous=False, spacing=0)
		webview = webkit.WebView()

		window.set_default_size(800, 600)
		# Optional
		window.connect('destroy', self.set_quit)

		window.add(box)
		box.pack_start(webview, expand=True, fill=True, padding=0)

		window.show_all()

		webview.open(uri)
		return (window, webview)
	
	def add_thread(self, thread):
		self._worker_threads.append(thread)
	
	def run(self):
		from threading import Thread
		#gtk.gdk.threads_init() # logic says I should call this. repeated failures say maybe it's not ideal

		# queue up secondary threads to run once gtk is settled
		for thread in self._worker_threads:
			gobject.idle_add(lambda: thread.start())

		# and a signal handler
		gobject.idle_add(lambda: signal.signal(signal.SIGINT, self.set_quit))

		logging.debug('starting gtk')
		gtk.main()
		logging.debug('gtk.main() ended')


