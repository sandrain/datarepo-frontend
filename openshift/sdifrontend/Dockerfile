FROM python:latest

# Create user for uwsgi
RUN useradd --shell /bin/false uwsgi

# Expose the port uWSGI will listen on
EXPOSE 5000

# Set an environment variable with the directory
# where we'll be running the app
ENV APP /app

# Create the directory and instruct Docker to operate
# from there from now on
RUN mkdir $APP

# set Working DIR
WORKDIR $APP

# Install Python dependencies
COPY openshift/sdifrontend/app.ini .
COPY openshift/sdifrontend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache -r requirements.txt

RUN mkdir -p $APP/static

# copy scripts
COPY openshift/scripts/connect.py .
COPY openshift/scripts/wait-for-db.sh .
COPY ./manage.py .

# Copy APP
# This should be the last step, Docker will use the caching and speed up the builds
COPY . ${APP}
RUN chown -R uwsgi:uwsgi ${APP}

# set the user
USER uwsgi:uwsgi

# Make sure we use the production environment
ENV DJANGO_SETTINGS_MODULE sdifrontend.settings.production
# Finally, we run uWSGI with the ini file we created earlier
CMD ./wait-for-db.sh && \
    bash -c "python manage.py collectstatic --ignore *.scss --no-input" && \
    bash -c "python manage.py compilescss" && \
    bash -c "python manage.py compress" && \
    bash -c "python manage.py migrate" && \
    uwsgi --ini app.ini
