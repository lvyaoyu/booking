FROM ubuntu:focal AS booking
LABEL maintainer="linzy@uniner.com"
USER root

ENV LC_ALL=C.UTF-8
ENV LANG=zh_CN.UTF-8
ENV NOVNC_HOME=/root/noVNC \
    DISPLAY=:1.0 \
    TZ=Asia/Shanghai
ENV PLAYWRIGHT_SKIP_BROWSER_GC=1


RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list   && \
    apt-get -qq -y update  && \
    DEBIAN_FRONTEND=noninteractive apt-get -qq -y install --no-install-recommends \
    python3 \
    python3-dev \
    python3-venv \
    python3-pip \
    python3-tk \
    gcc \
    unixodbc-dev \
    g++ \
    make \
    bash \
    vim \
    ntp \
    dbus \
    upower \
    libgles2-mesa \
    libgles2-mesa-dev \
    software-properties-common && \
    rm -rf /var/lib/apt/lists/* && \
    pip config set global.index-url https://pypi.douban.com/simple/ && \
    rm -rf /var/cache/* &&\
    ln -s /usr/bin/python3 /usr/bin/python

COPY . /data/booking
WORKDIR /data/booking/app

COPY requirements.txt run_vnc.sh /
COPY ./noVNC-1.2.0.tar.gz /root/noVNC-1.2.0.tar.gz
COPY ./websockify-0.9.0.tar.gz /root/websockify-0.9.0.tar.gz

RUN pip install wheel && \
    pip install -r /requirements.txt --no-cache-dir && \
    chmod +x /data/booking/run_vnc.sh \
    && mkdir -p /data/UserDatas/chromium \
    &&mkdir -p ~/.vnc \
    && mkdir -p /data/UserDatas/firefox \
    && mkdir -p ../UserData_firefox \
    && mkdir -p /data/UserDatas/webkit \
    && mkdir -p ../cach \
    && service ntp restart \
    && service dbus restart \
    && mkdir -p $NOVNC_HOME/utils/websockify \
    && tar zxvf /root/noVNC-1.2.0.tar.gz --strip 1 -C $NOVNC_HOME \
    && tar zxvf /root/websockify-0.9.0.tar.gz --strip 1 -C $NOVNC_HOME/utils/websockify \
    && chmod +x -v $NOVNC_HOME/utils/*.sh \
    && chmod +x /data/booking/run_vnc.sh


# 1. Install Chromium /  Firefox /dependencies
RUN PLAYWRIGHT_BROWSERS_PATH=$HOME/.cache/ms-playwright python3 -m playwright install firefox chromium &&apt-get update && apt-get install -y --no-install-recommends \
    # Install Chromium dependencies
    libnss3 \
    libxss1 \
    libasound2 \
    fonts-noto-color-emoji \
    libxtst6 \
    libgtk-3-0\
    libxcomposite1\
    libxdamage1\
    libatk1.0-0 \
    libgbm1 \
    # Install Firefox dependencies
    libdbus-glib-1-2 \
    libxt6 \
    #  Install ffmpeg to bring in audio and video codecs necessary for playing videos in Firefox.
    ffmpeg \
    xvfb \
    x11vnc \
    fonts-arphic-* &&\
    apt-get clean

CMD ["bash","-c","./run_vnc.sh"]

