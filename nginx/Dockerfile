FROM ubuntu:20.04
RUN apt-get update && apt-get install -y \
    nginx-full \
    && rm -rf /var/lib/apt/lists/*

RUN rm /etc/nginx/sites-available/*
RUN rm /etc/nginx/sites-enabled/*

COPY nginx_vhost /etc/nginx/sites-available/default
RUN ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

VOLUME /var/www/memeusbot

EXPOSE 80

STOPSIGNAL SIGQUIT

CMD ["nginx", "-g", "daemon off;"]