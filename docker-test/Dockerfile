FROM centos/python-36-centos7
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY docker-test /code/
