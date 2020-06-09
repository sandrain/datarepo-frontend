FROM python:latest

# Create user for uwsgi
RUN useradd --shell /bin/false uwsgi

# Set an environment variable with the directory
# where we'll be running the app
ENV APP /app

# Create the directory and instruct Docker to operate
# from there from now on
RUN mkdir $APP

# copy everything
COPY . $APP
COPY openshift/sdifrontend/app.ini $APP

RUN mkdir -p $APP/static

WORKDIR $APP

# Expose the port uWSGI will listen on
EXPOSE 5000

# Install Python dependencies
RUN pip install --no-cache -r requirements-deployment.txt

COPY openshift/scripts/connect.py .
COPY openshift/scripts/wait-for-db.sh .

RUN chown -R uwsgi:uwsgi ${APP}

USER uwsgi:uwsgi

# Finally, we run uWSGI with the ini file we created earlier
CMD ./wait-for-db.sh && \
    bash -c "python manage.py collectstatic --no-input" && \
    bash -c "python manage.py migrate --settings=sdifrontend.settings.production" && \
    uwsgi --ini app.ini
