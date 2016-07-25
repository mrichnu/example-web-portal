# Software Web Portal Example

This repository contains a flask app (built with docker compose) that can
launch Elastic Container Service tasks. It is intended to be used to launch
a [docker image](https://hub.docker.com/r/epflsti/octave-x11-novnc-docker/)
which present a full graphical desktop and VNC server, along
with a web-based VNC client (noVNC) which allows users to view and interact
with the desktop in their browser.

This is a proof of concept showing how Docker and the Elastic Container
Service can be used to present a graphical desktop over the web.  