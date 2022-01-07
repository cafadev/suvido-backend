FROM python:3.8.11

RUN curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && apt-get install -y nodejs && npm install -g nodemon

ARG user=backend
ARG uid=1000
ARG gid=1000

RUN addgroup --gid $gid ${user}
RUN adduser --disabled-password --gecos '' --uid $uid --gid $gid ${user}

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN mkdir -p /usr/share/${user}
RUN chown -R ${user}:${user} /usr/share/${user}
RUN chown -R ${user}:${user} /opt/venv

USER ${user}

WORKDIR /usr/share/${user}

RUN mkdir -p static
RUN mkdir -p media

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

COPY requirements .

RUN $VIRTUAL_ENV/bin/python3 -m pip install --upgrade pip
RUN $VIRTUAL_ENV/bin/python3 -m pip install -r requirements

COPY . .

USER root

RUN chown -R ${user}:${user} /usr/share/${user}/static
RUN chown -R ${user}:${user} /usr/share/${user}/media

USER ${user}
RUN sed -i 's/\r$//g' ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
