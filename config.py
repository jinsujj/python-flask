import os

BASE_DIR = os.path.dirname(__file__)
SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(BASE_DIR, "pybo.db"))
SQLALCHEMY_TRACK_MODIFICATIONS = False


# SECRET_KEY
# secret_key 는 CSRF(cross-site request forgery) 라는 웹 사이트 취약점 공격을 방지하는 데 사용된다. CSRF 는 사용자의 요청을 위조하는 웹 사이트 공격 기법인데, SECRET_KEY 를 기반으로 해서 생성되는 CSRF 토큰은 폼으로 전송된 데이터가 실제 웹 페이지에서 작성된 데이터인지를 판단해 주는 가늠자 역할을 한다
SECRET_KEY = "dev"
