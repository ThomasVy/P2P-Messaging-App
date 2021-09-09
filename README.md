# P2P Messaging App

Messaging app that uses P2P to send messages along. In the beginning, users connect to the registry using UDP to get the lists of users. Then the users sends/receives peer messages and text snippets from peers by TCP. New users will recieve catch up messages to allow them to see previous messages sent before they joined. The registry will send a done message to let all the users quit.

https://thomasvy.github.io/Website/static/media/P2PMessagingApp.9511de03.mp4
