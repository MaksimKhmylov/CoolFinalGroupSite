class Config:
    SECRET_KEY = 'bla_super_secret_key' # FOR CSRF TOKEN
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tttsite.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
