#!/opt/local/bin/python2.5

import sys
import os
import urllib

import gtk
import gtk.keysyms
import gobject
import webkit

import cgi

import logging
logging.basicConfig(level=logging.DEBUG)

def main():
	gtk.gdk.threads_init()
	thread.start_new_thread(gtk.main, ())
	

if __name__ == '__main__':
	sys.exit(main())
