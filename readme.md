# Multilingual Spam Detection API

An API built with FastAPI that utilizes a machine learning model to predict whether a given message is spam or not. The model supports various languages, including Tamil, English, Malayalam, Kannada, and Telugu.

## Features

- Predicts spam messages in multiple languages.
- Uses a machine learning model trained to identify spam patterns.
- FastAPI-based web API for easy integration.

## Usage

To use the API, send a POST request with a message to the `/predict` endpoint. The response will indicate whether the message is classified as "Ham" (not spam) or "Spam."

## Languages Supported

- Tamil
- English
- Malayalam
- Kannada
- Telugu

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/your_username/your_repository.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
uvicorn main:app --reload
```

## License

This project is licensed under the MIT License.
