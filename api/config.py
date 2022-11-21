import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.venv'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1e5194932d3906e5a38ab32d02f81a51'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'api.db')
