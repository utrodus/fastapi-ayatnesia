FROM python:3.11.3

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Add the NLTK download command
RUN python -c "import nltk; nltk.download('popular')"

COPY . .

EXPOSE 3000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000", "--timeout-keep-alive", "300"]
