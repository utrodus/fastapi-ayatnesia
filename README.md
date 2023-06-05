
  

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

  

$ git clone https://github.com/utrodus/fastapi-quran-finder.git

  

```

  

  

2. Open the console inside the project directory and create a virtual environment (You can skip this step if you have docker installed).

  

```git bash

  

$ python -m venv env

  

$ source env/Scripts/activate

  

```

  

  

3. Install the app

  

```git bash

  

(venv) $ pip install -r requirements.txt

  

```

  

  

## Run it locally

  

```git bash

  

$ uvicorn main:app --reload

  

```

  

  

## install required data nltk library

  

```git bash

  

$ python src/setup_nltk.py

  

```

  

  

## Basic Usage

  

first off all, run preprocessing quran data for preprocessing ayahs for each surahs

  

```git bash

  

$ python src/preprocessing/quran_preprocessing.py

  

```

  

Once you are running the server open the [Swagger UI App](http://localhost:8000/docs) to checkout the API documentation.