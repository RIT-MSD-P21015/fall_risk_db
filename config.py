class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../db.sqlite3'
    ADMIN_ACCT = {
        'username' : 'admin',
        'password' : 'secret',
        'email' : 'admin@rit.edu'
    }
