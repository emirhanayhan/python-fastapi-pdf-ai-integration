FROM python:3.11-bullseye
WORKDIR /app
ADD . /app
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
ENV PORT 8000
EXPOSE $PORT
ENV CONFIG prod
CMD python /app/main.py --config=$CONFIG --migrate=true
