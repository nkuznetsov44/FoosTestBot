FROM python:3.9.7-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
WORKDIR .
COPY ./common ./common
COPY ./foos_test_bot .

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python3", "foos_test_bot.py"]