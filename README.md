# Final Project for EE250 Distributed Systems and IoT
By Lorand Cheng

Video demo: https://drive.google.com/file/d/1NTLxlnVb0Zasdc5ZsUtEleQWp1mURQqH/view?usp=sharing
## Summary
This project is a morse code translator and messenger system between a raspberry pi and a web interface. There are four basic nodes: raspberry pi, web client, cloud server, and cloud database. There can theoretically be multiple raspberry pis and web clients connected, although it is not necessary to send messages.

## Node Roles
- Raspberry pi: The raspberry pi detects button presses in various combinations of lengths, and decides to take actions based on the result of the combination. The raspberry pi reads in short and long button presses as elements of a morse code letter, then uses a binary tree to determine which letter the code corresponds to. When a message is complete, the user can send the message with a longer button press. The raspberry pi also has a notifier that checks for new messages every second and alerts if there are any.
- Web client: When a client connects on port 4200 of the web server, they are served a simple interface that allows users to send messages as well as view the message history
- Cloud server: The cloud server is in charge of handling requests and returning requested data, as well as updating and querying the database for the necessary resources.
- Cloud database: A simple relational database with only one table containing the entire message history. Only connects to the cloud server directly

## Operation Instructions
The cloud server and db need to be the first to run. The cloud server runs the 'messageServer.py' file locally, while the db just needs to be available for queries. Note: the database.ini file is not included in this repo to hide credentials
- Dependencies/Libraries used: Flask, Flask_socketio, psycopg2, postgresql-client  
Next, web clients can connect through http://{vm host IP}:4200/ and send and receive messages  
Finally, the rpi can connect by running 'rpi.py'  
- Dependencies/Libraries used: GrovePi, Flask, requests, pytz