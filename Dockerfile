# https://hub.docker.com/_/python/
FROM python:3.6.9
MAINTAINER andreu vallbona
WORKDIR /app

COPY docker/locale.gen /etc/locale.gen
COPY docker/entrypoint.sh /entrypoint.sh
RUN ln -s /usr/local/bin/python /bin/python

# pipenv
COPY Pipfile* /srv/
RUN pip install -U pip && pip install pipenv
WORKDIR /srv
RUN pipenv install --system --ignore-pipfile
# end pipenv

WORKDIR /app
COPY src/ .
ENTRYPOINT ["/entrypoint.sh"]
CMD ["run-devel"]
