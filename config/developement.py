from config.default import *

SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(BASE_DIR, "pybo.db"))
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "dev"
FLASK_DEBUG = True
