# Use for production
FROM python:3.8
LABEL maintainer "Daniel Stratti <daniels@vamp.me>"

ENV APP_HOME /app
ENV PYTHONUNBUFFERED True
WORKDIR $APP_HOME

COPY requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt && pip install --no-cache-dir gunicorn
RUN groupadd -r app && useradd -r -g app app
USER app

COPY --chown=app:app . ./

#COPY ./vamp-cast-staging-e5ffa19bffe8.json ./ # Update this to copy your JSON service account creds into the docker image

EXPOSE 8080

CMD exec gunicorn --bind :$PORT --log-level info --workers 1 --threads 8 --timeout 0 app:server
#CMD ["python", "./app.py"]

# docker build . -t cast-exp
# docker run -it -v $PWD:/app -p 8080:8080 --env-file=.env cast-exp
