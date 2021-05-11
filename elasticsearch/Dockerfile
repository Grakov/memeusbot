FROM elasticsearch:7.12.1

VOLUME /usr/share/elasticsearch/data
EXPOSE 9200

RUN mkdir -p /etc/elasticsearch/hunspell/ru_RU
COPY ru_RU.* /etc/elasticsearch/hunspell/ru_RU/

USER elasticsearch:root

ENTRYPOINT ["elasticsearch"]
