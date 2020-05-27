FROM python:latest
#FROM centos

#RUN pip install --upgrade pip
RUN echo $(uname -a)

# Create user for uwsgi
RUN useradd --shell /bin/false uwsgi

# Set an environment variable with the directory
# where we'll be running the app
ENV APP /app

# Create the directory and instruct Docker to operate
# from there from now on
RUN mkdir $APP
WORKDIR $APP

# Expose the port uWSGI will listen on
EXPOSE 5000
# Copy the requirements file in order to install
# Python dependencies
COPY requirements-deployment.txt requirements.txt
# Install Python dependencies
RUN pip install --no-cache -r requirements.txt
# We copy the rest of the codebase into the image
COPY app.ini .
COPY docker-test/container-scripts/connect.py .
COPY docker-test/container-scripts/wait-for-db.sh .
COPY manage.py .

RUN chown -R uwsgi $APP
RUN ls -la

# Finally, we run uWSGI with the ini file we
# created earlier
CMD which env; ./wait-for-db.sh \
    && bash -c "python manage.py collectstatic --no-input" \
    && bash -c "python manage.py migrate --settings=sdifrontend.settings.production" \
    && uwsgi --ini app.ini
