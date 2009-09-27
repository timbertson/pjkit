import Queue

import gtk
import gobject
import webkit
import logging

def gtk_do(action):
	logging.debug('> getting gtk lock')
	gtk.gdk.threads_enter()
	logging.debug('> got gtk lock')
	action()
	logging.debug('> released gtk lock')
	gtk.gdk.threads_leave()

class Global(object):
	quit = False
	@classmethod
	def set_quit(cls, *args, **kwargs):
		gtk_do(gtk.main_quit)
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

		def init_gtk():
			gtk.gdk.threads_enter()
			print 'starting gtk'
			gtk.main()
			print 'gtk.main() ended'
			gtk.gdk.threads_leave()

		Thread(target=init_gtk).start()
		print "sontinuing in the main thread"
		import signal
		signal.signal(signal.SIGINT, Global.set_quit)

