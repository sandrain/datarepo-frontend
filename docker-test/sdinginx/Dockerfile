#FROM nginx:latest
# avoid permission problem in openshift
FROM nginxinc/nginx-unprivileged

EXPOSE 8000

COPY docker-test/sdinginx/app.conf /etc/nginx/conf.d/default.conf

#RUN chgrp -R root /var/cache/nginx /var/run /var/log/nginx && \
#    chmod -R 770 /var/cache/nginx /var/run /var/log/nginx

CMD ["nginx", "-g", "daemon off;"]
