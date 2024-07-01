FROM python:3.8-slim-buster


# We copy just the requirements.txt first to leverage Docker cache


WORKDIR /app


COPY ./requirements.txt /app/requirements.txt


RUN pip3 install -r requirements.txt


COPY . /app


ENTRYPOINT [ "python" ]


EXPOSE 5000


CMD [ "app.py" ]