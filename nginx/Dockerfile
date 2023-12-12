FROM nginx:1.25

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
COPY services /etc/nginx/conf.d
COPY entrypoint /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint

ENTRYPOINT ["entrypoint"]