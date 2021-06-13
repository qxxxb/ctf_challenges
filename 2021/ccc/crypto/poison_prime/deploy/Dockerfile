FROM python:3

RUN pip3 install --no-cache-dir pycryptodome && \
apt-get update && \
apt-get install -y socat

WORKDIR /opt/app
COPY server.py ./
ENV FLAG=CCC{sm0l_subgr0up_w1th_a_m3rs3nn3_pr1m3}
CMD socat -d -d -s TCP-LISTEN:4000,reuseaddr,fork EXEC:'timeout 30 python -u /opt/app/server.py'
