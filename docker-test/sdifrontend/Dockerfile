FROM python:latest

# Create user for uwsgi
RUN useradd --shell /bin/false uwsgi

# Set an environment variable with the directory
# where we'll be running the app
ENV APP /app

# Create the directory and instruct Docker to operate
# from there from now on
RUN mkdir $APP

COPY ./requirements-deployment.txt requirements-deployment.txt
# Install Python dependencies
RUN pip install --no-cache -r requirements-deployment.txt

# copy everything
COPY docker-test/sdifrontend/app.ini $APP

RUN mkdir -p $APP/static

WORKDIR $APP

# Expose the port uWSGI will listen on
EXPOSE 5000

COPY docker-test/container-scripts/connect.py .
COPY docker-test/container-scripts/wait-for-db.sh .
COPY ./manage.py .

# Copy APP
COPY ./sdifrontend $APP
RUN chown -R uwsgi:uwsgi ${APP}

USER uwsgi:uwsgi

# Finally, we run uWSGI with the ini file we created earlier
CMD ./wait-for-db.sh && \
    export DJANGO_SETTINGS_MODULE=sdifrontend.settings.production && \
    bash -c "python manage.py collectstatic --no-input" && \
    bash -c "python manage.py compress" && \
    bash -c "python manage.py migrate" && \
    uwsgi --ini app.ini
