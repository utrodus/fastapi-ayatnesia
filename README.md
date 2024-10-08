# Quran search - API
>   This final year project focuses on searching Quranic verses using lexical, semantic, and combined approaches.

## Table of Contents:

- [Quran search - API](#quran-search---api)
  - [Table of Contents:](#table-of-contents)
  - [Screenshots \& Demo](#screenshots--demo)
    - [Web App](#web-app)
    - [API Docs](#api-docs)
    - [Demo](#demo)
  - [Description](#description)
    - [Features](#features)
  - [Requirements:](#requirements)
  - [Installation](#installation)
  - [Run it locally](#run-it-locally)
  - [install required data nltk library](#install-required-data-nltk-library)
  - [Basic Usage](#basic-usage)
  - [Deployment 🚀](#deployment-)
    - [Run the FastAPI application using Docker:](#run-the-fastapi-application-using-docker)
    - [Check docker container process](#check-docker-container-process)
    - [View Logs docker container process](#view-logs-docker-container-process)
    - [remove any stopped containers and all unused images](#remove-any-stopped-containers-and-all-unused-images)

## Demo & Screenshots

### Demo
https://github.com/user-attachments/assets/f7317fa5-1f32-4d97-9f8b-c688e8ba5ece

### Web App
![featured image](featured.png)

### API Docs
![API Docs](api_docs.png)

## Description
The Quran Search API allows you to search for text using various measures such as lexical, semantic, and lexical semantic.


It provides an efficient way to access and retrieve information from the Quran.


In this project, we used two exciting methods: one for measuring lexical similarity and another for gauging semantic similarity. In the application, users have the flexibility to opt for either of these methods independently or harness the power of both in combination.

For measuring Lexical Similarity the methods used are TF-IDF and Cosine similarity.

1.  TF-IDF: TF-IDF is used to evaluate the importance of words in the translation of the Qur'an. TF-IDF is a method used to evaluate the importance of a word in a document or text. This is done by calculating how often the word appears in the document (Term Frequency) and the extent to which the word is unique across documents (Inverse Document Frequency).
    
2.  Cosine similarity is a method used to measure the degree to which two vectors (in this case, vector representations of words) are in lexical relationship to each other. In the context of Ayatnesia, cosine similarity is used to compare the TF-IDF vector between the verses of the Qur'an and the keyword. The higher the cosine similarity value between the verse and the keyword, the more lexically similar the two things are.

While to measure Semantic Similarity in Ayatnesia when searching for verses in the Qur'an, the method used is Word Embedding with FastText. This method involves representing words as high-dimensional vectors in a semantic space using FastText, a powerful word embedding tool. 

These vector representations capture the semantic meanings of words, allowing Ayatnesia to compare and measure the similarity between verses in the Qur'an based on their semantic content. By utilizing Word Embedding with FastText, Ayatnesia enables users to find verses with similar semantic meanings, enhancing the effectiveness of verse searches and facilitating a deeper understanding of the Qur'an.


*The API empowers you with these features to enhance your search capabilities and facilitate a comprehensive analysis of the Quran. 🚀*

### Features
💎 Key Features:
- Get all Qur'an Surahs 
- Get detailed information about a specific Quran Surah 
- Search using lexical measures 
- Search using semantic measures 
- Search using lexical semantic measures 

## Requirements:

- Python >= 3

## Installation

1. Clone or download de repository:
```
git clone https://github.com/utrodus/fastapi-quran-finder.git
```

1. Open the console inside the project directory and create a virtual environment (You can skip this step if you have docker installed).

```git bash
python -m venv venv
source venv/Scripts/activate
```

3. Install the app

```git bash
(venv) pip install -r requirements.txt
```

## Run it locally

```git bash
uvicorn main:app --reload
```

## install required data nltk library

```git bash
python src/setup_nltk.py
```

## Basic Usage

first off all, run preprocessing quran data for preprocessing ayahs for each surahs

```git bash
python src/preprocessing/quran_preprocessing.py
```

## Deployment 🚀
### Run the FastAPI application using Docker:
Start a Docker container using the following command:

```git bash
docker-compose up -d
```

### Check docker container process
```git bash
docker ps -a
```

### View Logs docker container process
```git bash
docker logs "container-id"
```

### remove any stopped containers and all unused images
```git bash
docker stop "container-id"
docker system prune -a
```



Once you are running the server open the [Swagger UI App](http://localhost:8000/docs) to checkout the API documentation.
