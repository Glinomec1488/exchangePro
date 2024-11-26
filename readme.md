server libs:
flask_cors
requests
flask

tgbot libs:
aiogram==3.0.0b1

.py req for deploying
aiogram==3.0.0b1
regex
pillow
flask_cors
requests
flask
waitress



ProxyPass /api/ http://localhost:5000/
ProxyPassReverse /api/ http://localhost:5000/
ProxyPass /socket.io/ http://localhost:5000/socket.io/
ProxyPassReverse /socket.io/ http://localhost:5000/socket.io/

