FROM nikolaik/python-nodejs:python3.10-nodejs20

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl xz-utils ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
    -o /tmp/ffmpeg.tar.xz && \
    tar -xJf /tmp/ffmpeg.tar.xz -C /tmp && \
    mv /tmp/ffmpeg-*-static/ffmpeg /usr/local/bin/ffmpeg && \
    mv /tmp/ffmpeg-*-static/ffprobe /usr/local/bin/ffprobe && \
    chmod +x /usr/local/bin/ffmpeg /usr/local/bin/ffprobe && \
    rm -rf /tmp/ffmpeg*

RUN ffmpeg -version && ffprobe -version

COPY . /app/
WORKDIR /app/

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["bash", "start"]

