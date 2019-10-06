from flask import Flask
from routes.swipes import swipe_route
from routes.user import user_route
from routes.users import users_route
from flask_pymongo import PyMongo #connect to mongo DB

app = Flask(__name__)

#register routes
app.register_blueprint(swipe_route, url_prefix='/swipe')
app.register_blueprint(user_route, url_prefix='/user')
app.register_blueprint(users_route, url_prefix='/users')

@app.route('/')
def hello_world():
    return 'Welcome at the swiping api. Made by the enjuneers!'

if __name__ == "__main__":
    app.run(use_reloader=True)
    # app.run(host='0.0.0.0', debug=True, use_reloader=True)