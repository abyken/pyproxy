# pyproxy
python proxy server, which based on https://github.com/abhinavsingh/proxy.py

setup
virtualenv --no-site-packages pyproxy
cd pyproxy
. bin/activate
git clone https://github.com/abyken/pyproxy.git
cd pyproxy
pip install -r requirements.txt
python runproxy.py --hostname 127.0.0.1 --port 8000 --log-level INFO

then setup your browser proxy to: 127.0.0.1:8000
following by post on habrahabr
