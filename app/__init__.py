from flask import Flask


def crate_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
