# Quran Finder - API
>   This final year project focuses on searching Quranic verses using lexical, semantic, and combined approaches.

## Table of Contents:

- [Quran Finder - API](#quran-finder---api)
  - [Table of Contents:](#table-of-contents)
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


## Description

The Quran Search API allows you to search for text using various measures such as lexical, semantic, and lexical semantic.


It provides an efficient way to access and retrieve information from the Quran.


*The API empowers you with these features to enhance your search capabilities and facilitate a comprehensive analysis of the Quran. 🚀*

### Features
💎 Key Features:
- Get all Qur'an Surahs (✅ done).
- Get detailed information about a specific Quran Surah (✅ done).
- Search using lexical measures (✅ done).
- Search using semantic measures (⏳ _in progress_).
- Search using lexical semantic measures (⏳ _in progress_).

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
docker-compose up -d --build
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