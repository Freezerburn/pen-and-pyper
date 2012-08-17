pen-and-pyper
=============

A 2D graphics/game library built in Python, on top of pyglet. It attempts to get around the Python GIL by running two separate processes: one which does all of the actual drawing, which I call the 'Paper', and one which does the heavy number crunching, which I call the 'Pen'. The Paper will do nothing except draw all the created entities, and listen to the simple commands sent by the Pen. For example: moving an entity, creating an entity, caching an image, etc. The Pen will calculate velocities, accelerations, collision, AI, etc. and send all needed commands to the Paper. This is likely to largely include movement commands as you control a player, AI moves enemies/NPCs around, effects of gravity, etc.
As of August 17, 2012 this library is in heavy development. That was the first commit, and it still has issues and plenty of room to improve.

IMPORTANT NOTES
===============

There are some pngs in the res directory which are specific to a separate project that I am working on. These will be removed eventually. The library is currently in very early development, and as such it has everything in it that I am using for testing various things. Also of note there is a png that I do not own, with 'claudius' in the name. I pulled it randomly off of Google, and I do not know who it belongs to. I am purely using it temporarily to test animation, and it will be removed as soon as is possible so as to not infringe upon another person's property.
