import os

# 프로젝트의 root 디렉터리인 BASE_DIR 은 기존 config.py 파일에 있던 환경변수다. 여기서 os.path.dirname 을 겹쳐 사용한 점이 눈에 띌 것이다. 기존 config.py 파일의 위치는 /dev/myproject 였다.
# 그런데 이제 default.py 파일의 위치가 /dev/myproject/config 로 디렉터리의 깊이가 1 만큼 더 늘어났으므로 os.path.dirname 을 한 번 더 사용하여 BASE_DIR 을 설정한 것이다.
K
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
