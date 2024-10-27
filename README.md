# rag-refapp

## About 
This is an API that allows you to interact with a Retrieval Augmented Generation (RAG) system. I made this project primarily
for learning purposes.

## Local Development

### OpenSearch
Make sure the OpenSearch nodes and dashboard are up and running before using this command. Take a look at [instructions](app/opensearch/README.md) for
setting up OpenSearch locally.

### Running Application with Docker
Run `docker compose up` at the root level. 

### Running Application
Use `poetry run python -m app.main` to run using Poetry.

### Postman
In *~/postman~, there is a Postman collection containing all the working endpoints of this application that you can use
once this app is running. If you take a look at *~/docs~, there are some sample documents you can use to get started.

### Testing
Use `pytest` at the root directory to run all tests

### Code Formatting
Use `black .` at the root directory to auto format. This project
has a pre-commit hook setup that runs black and checks formatting using
flake8. 