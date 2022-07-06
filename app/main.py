from flask import Flask
from endpoints.user_endpoint import user_blueprint
from endpoints.restaurant_endpoint import restaurant_blueprint
from app.config import config
from app.service.db import db


app = Flask(__name__)
app.register_blueprint(user_blueprint)
app.register_blueprint(restaurant_blueprint)

app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{config.mysql_username}:" \
                                        f"{config.mysql_pass}@" \
                                        f"{config.mysql_host}:" \
                                        f"{config.mysql_port}/" \
                                        f"{config.mysql_database}"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

if __name__ == "__main__":

    app.run(debug=True, port=8282, host="0.0.0.0")
