import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite3'

class DevelopmentConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@db/fall_risk_db'
