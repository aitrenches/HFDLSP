FROM nginx:1.23.3-alpine
RUN apk --no-cache add certbot-nginx=1.32.0-r0 bash=5.2.15-r0

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY services /etc/nginx/conf.d
COPY entrypoint /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint

ENTRYPOINT ["entrypoint"]