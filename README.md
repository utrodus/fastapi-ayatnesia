# Quran Finder - API
> This is final year project about searching qur'an ayah using lexical and semantic

## Table of Contents:
- [Quran Finder - API](#quran-finder---api)
  - [Table of Contents:](#table-of-contents)
  - [Description](#description)
    - [Features](#features)
  - [Requirements:](#requirements)
  - [Installation](#installation)
  - [Run it locally](#run-it-locally)
  - [Basic Usage](#basic-usage)


## Description
This is project is a simple REST API made with FastAPI for learning purposes.

### Features
Features included:
- Preprocessing quran json


## Requirements:
- Python >= 3

## Installation
1. Clone or download de repository:
    ```
    $ git clone https://github.com/utrodus/fastapi-quran-finder.git
    ```

2. Open the console inside the project directory and create a virtual environment (You can skip this step if you have docker installed).
    ```git bash
    $ python -m venv venv
    $ source venv/Script/activate
    ```

3. Install the app 
    ```bash
    (venv) $ pip install -r requirements.txt
    ```

## Run it locally
Copy the `env.example` file into the same directory with the name `.env`
```bash
$ uvicorn main:app --reload
```

## Basic Usage
Once you are running the server open the [Swagger UI App](http://localhost:8000/docs) to checkout the API documentation.
