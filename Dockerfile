FROM joyzoursky/python-chromedriver:3.9
ARG BOT_TOKEN=production
ENV BOT_TOKEN=$BOT_TOKEN
WORKDIR /usr/src/app/
COPY . /usr/src/app/
RUN pip install -r requirements.txt
CMD ["python", "bot.py"]