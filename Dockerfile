FROM python:3.11.3

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Add the NLTK download command
RUN python -c "import nltk; nltk.download('popular')"

COPY . .

EXPOSE 3100

CMD ["gunicorn", "main:app"]
