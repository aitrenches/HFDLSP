FROM nginx:1.23.3-alpine
ENTRYPOINT ["entrypoint"]
RUN rm -r /etc/nginx/conf.d
RUN apk --no-cache add certbot-nginx=1.32.0-r0 bash=5.2.15-r0
COPY entrypoint /usr/local/bin/
COPY nginx.conf /etc/nginx/nginx.conf
COPY services /etc/nginx/conf.d
