release: chmod u+x release.sh && ./release.sh
web: gunicorn -w 4 "lynx:create_app()" --log-file -