import gtk
import gobject
import logging

def gtk_do(action):
	logging.debug('> getting gtk lock')
	gtk.gdk.threads_enter()
	logging.debug('> got gtk lock')
	action()
	logging.debug('> released gtk lock')
	gtk.gdk.threads_leave()

def asynchronous_gtk_message(action):
	gobject.idle_add(lambda: gtk_do(action))

def gtk_action(self, callable, sync=False):
	"""perform an action (optionally synchronously) in the main (GTK+) thread"""
	if not sync:
		asynchronous_gtk_message(callable)
		return

	done = []
	cond = threading.Condition()

	def perform():
		callable()
		cond.acquire()
		done.append(True)
		cond.notify()
		cond.release()

	asynchronous_gtk_message(perform)
	while len(done) == 0:
		cond.acquire()
		cond.wait()
		cond.release()

