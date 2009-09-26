import Queue

import gtk
import gobject
import webkit

class Global(object):
	quit = False
	@classmethod
	def set_quit(cls, *args, **kwargs):
		def asynchronous_gtk_message(fun):
			def worker((function, args, kwargs)):
				apply(function, args, kwargs)

			def fun2(*args, **kwargs):
				gobject.idle_add(worker, (fun, args, kwargs))
			return fun2
		asynchronous_gtk_message(gtk.main_quit)()
		cls.quit = True


class GtkWebkitApp(object):
	def __init__(self):
		pass
		
	def open_window(self, uri):
		window = gtk.Window()
		box = gtk.VBox(homogeneous=False, spacing=0)
		browser = webkit.WebView()

		window.set_default_size(800, 600)
		# Optional
		window.connect('destroy', Global.set_quit)

		window.add(box)
		box.pack_start(browser, expand=True, fill=True, padding=0)

		window.show_all()

		print uri
		browser.open(uri)
		return browser
	
	def spawn(self):
		# Start GTK in its own thread:
		from threading import Thread
		gtk.gdk.threads_init()
		Thread(target=gtk.main).start()
		import signal
		signal.signal(signal.SIGINT, Global.set_quit)

def my_quit_wrapper(fun):
	import signal
	signal.signal(signal.SIGINT, Global.set_quit)
	def fun2(*args, **kwargs):
		try:
			x = fun(*args, **kwargs) # equivalent to "apply"
		finally:
			kill_gtk_thread()
			Global.set_quit()
		return x
	return fun2



