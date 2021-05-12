FROM elasticsearch:7.12.1

VOLUME /usr/share/elasticsearch/data
EXPOSE 9200

RUN mkdir -p /opt/memeusbot_elastic
COPY . /opt/memeusbot_elastic/
RUN chown -R elasticsearch:root /opt/memeusbot_elastic/
RUN chmod +x /opt/memeusbot_elastic/start.sh

WORKDIR /opt/memeusbot_elastic
USER elasticsearch:root
ENTRYPOINT ["./start.sh"]
