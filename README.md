# minimal-llm-backend

## About 
Project that builds a backend that integrates with an LLM.

## Local Development

### Running Application with Docker
Run `docker compose up` at the root level. Make sure the OpenSearch nodes and dashboard are up
and running before using this command. Take a look at [instructions](rag_refapp/api/opensearch/README.md) for
setting up OpenSearch locally.

### Running Application
Use `poetry run python -m rag_refapp.main` to run using Poetry.

### Testing
Use `pytest` at the root directory to run all tests

### Code Formatting
Use `black .` at the root directory to auto format. This project
has a pre-commit hook setup that runs black and checks formatting using
flake8. 