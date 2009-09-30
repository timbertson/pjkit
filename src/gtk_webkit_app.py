import gtk
import gobject
import webkit
import logging
import signal
import threading
from threading import Thread
import gtk_helpers

class GtkWebkitApp(object):
	quit = False
	def __init__(self):
		gtk.gdk.threads_init()
		self._worker_threads = []
		
	@classmethod
	def set_quit(cls, *a, **kw):
		gtk_helpers.asynchronous_gtk_message(gtk.main_quit)
		cls.quit = True

	def webkit_window(self, uri):
		window = gtk.Window()
		box = gtk.VBox(homogeneous=False, spacing=0)
		webview = webkit.WebView()

		window.set_default_size(400, 200)
		# Optional
		window.connect('destroy', self.set_quit)

		window.add(box)
		box.pack_start(webview, expand=True, fill=True, padding=0)

		window.show_all()

		webview.open(uri)
		return (window, webview)
	
	def add_thread(self, thread_or_func):
		thread = thread_or_func
		if callable(thread_or_func):
			# wrap functions (callables) in their own thread
			thread = Thread(target=thread_or_func)
		self._worker_threads.append(thread)
	
	def run(self):
		gtk.gdk.threads_enter()
		# queue up secondary threads to run once gtk is settled
		for thread in self._worker_threads:
			gobject.idle_add(lambda: thread.start())

		# and a signal handler
		gobject.idle_add(lambda: signal.signal(signal.SIGINT, self.set_quit))

		logging.debug('starting gtk')
		gtk.main()
		gtk.gdk.threads_leave()
		logging.debug('gtk.main() ended')


