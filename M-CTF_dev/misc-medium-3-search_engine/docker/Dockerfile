FROM ubuntu:20.04
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y \
	nginx=1.18.* \
	python3-pip=20.0.* \
	python3-wheel=0.34.* \
	python3-setuptools=45.2.* \
	supervisor=4.1.* \
	netcat-openbsd=1.* \
	gettext=0.19.* \
	curl \
	&& rm -rf /var/lib/apt/lists/*

COPY ./docker/nginx-global.conf /etc/nginx/nginx.conf
COPY ./docker/nginx-site.conf /etc/nginx/sites-available/default
COPY ./docker/supervisord.conf /etc/supervisord.conf
COPY ./docker/entrypoint.sh ./

COPY ./requirements.txt ./
RUN pip3 --disable-pip-version-check --no-cache-dir \
	install -r ./requirements.txt

COPY ./app/ ./app/

ENTRYPOINT ["/app/entrypoint.sh"]
