FROM python:latest
RUN mkdir -p /usr/src/bot
WORKDIR /user/src/bot
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
RUN chmod 755 .
COPY . .
CMD ["python","./bot.py"]