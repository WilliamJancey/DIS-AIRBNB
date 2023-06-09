from flask import Flask
import psycopg2
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fc089b9218301ad987914c53481bff04'

# set your own database
db = "dbname='airbnb' user='postgres' host='127.0.0.1' password = 'Filippa' port=5431"
conn = psycopg2.connect(db)

bcrypt = Bcrypt(app)


login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


roles = ["ingen","host","user"]
print(roles)
mysession = {"state" : "initializing","role" : "Not assingned", "id": 0 ,"age" : 202212}
print(mysession)

from bank.Login.routes import Login
from bank.routesU import User

app.register_blueprint(Login)
app.register_blueprint(User)
