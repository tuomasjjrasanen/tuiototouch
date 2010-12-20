===========
tuiototouch
===========

A bridge between TUIO protocol and the kernel.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This application is able to treat data received on the standard kernel slot dedicated to the TUIO ptotocol,
create an emulation of a multitouch device, and send trough this device the informations provided by TUIO
in order to treat it like a standard multitouch entry.

Installation
============

In order to use this application, you will need some library used by it.
The two main libraries of this project are pytuio:

	http://pytuio.googlecode.com/files/pytuio-0.1.tar.gz

and uinput:

	http://codegrove.org/projects/python-uinput

When both libraries are installed, you will be able to run the application.

Basic Use
=========

To see the results, you will need to send data on the kernel socket, so the application can treat it.
In order to do that, several ways are possible:
	- There is a simulator to see how TUIO works available on tuio.org
	- There are tracking softwares, using a webcam and tracking fingers, or fiducials
and sending their position by TUIO. So far, three softwares have been tested:

	reacTIVision
	Movid
	CCV

All those softwares are available on tuio.org.
