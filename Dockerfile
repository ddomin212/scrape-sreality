FROM python:3.10.7
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV PORT 5000
EXPOSE $PORT
#CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app --timeout 120
CMD python app.py