from flask import Flask
from app.config import config
from app.service.db import db
from endpoints.login_endpoint import login_blueprint
from endpoints.restaurant_endpoint import restaurant_blueprint
from endpoints.user_endpoint import user_blueprint
from endpoints.review_endpoint import review_blueprint
from endpoints.like_endpoint import like_blueprint
from flask_cors import CORS
from waitress import serve

app = Flask(__name__)
app.register_blueprint(user_blueprint)
app.register_blueprint(restaurant_blueprint)
app.register_blueprint(login_blueprint)
app.register_blueprint(review_blueprint)
app.register_blueprint(like_blueprint)

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{config.mysql_username}:" \
                                        f"{config.mysql_pass}@" \
                                        f"{config.mysql_host}:" \
                                        f"{config.mysql_port}/" \
                                        f"{config.mysql_database}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)

db.init_app(app)
db.create_all(app=app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8282)
    #serve(app, host="0.0.0.0", port=8282)
