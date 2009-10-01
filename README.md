pjkit
=====

pjkit is a simple experiment in rapid GUI development. The aim is to have a
two-way bridge between python and javascript.

The only technology pair currently supported is webkit inside gtk, but other
types of web views (like mozembed) could be paired with other GUI toolkits (qt,
cocoa) if there's enough interest.

The idea is that python is great for developing your application functionality.
But try as I might, I often struggle to make a half-decent GUI in GTK+ alone.
Using webkit allows me to develop nice-looking applications fairly quickly. By
allowing (somewhat) seamless communication between python and javascript, my
programming language of choice can easily be used to power a
html/javascript-based rich UI.

It's kinda like server-client, except:

 - no latency
 - no http server code - you just expose python functions and objects
 - python can initiate javascript functions (like when a system event occurs - a
   file gets updated, or a long-running task completes)

I haven't made anything real with it yet, but I have plans to...

