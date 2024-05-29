FROM python:3.11.9

WORKDIR /app

# dependencies don't change so it's better to do this for production
COPY . /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# just copy and run app... easy
# COPY . /app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]