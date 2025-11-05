# GEMINI.MD: AI Collaboration Guide

This document provides essential context for AI models interacting with this project. Adhering to these guidelines will ensure consistency and maintain code quality.

## 1. Project Overview & Purpose

*   **Primary Goal:** This is a containerized Django web application designed for book analysis and recommendation. It leverages a PostgreSQL-compatible database (AlloyDB) with vector support to perform semantic searches on book content. The application exposes a REST API for analysis and data insertion and includes services for interacting with Large Language Models (LLMs) via Vertex AI.
*   **Business Domain:** AI-driven Content Analysis and Recommendation.

## 2. Core Technologies & Stack

*   **Languages:** Python 3.12.4, SQL (for AlloyDB), HCL (for Terraform).
*   **Frameworks & Runtimes:** Django 5.0.6 running on a Python Alpine Linux environment via Gunicorn 22.0.0.
*   **Databases:** Google Cloud AlloyDB (a PostgreSQL-compatible database) with vector support for embeddings. Redis is also included as a dependency, likely for caching or Celery task queuing.
*   **Key Libraries/Dependencies:** `django`, `gunicorn`, `google-cloud-aiplatform` (for Vertex AI), `psycopg2-binary` (PostgreSQL driver), `openai`, `pytest` (for testing), `black`, `flake8`, `isort` (for code quality).
*   **Package Manager(s):** `pip`. Dependencies are managed in `requirements.txt`.

## 3. Architectural Patterns

*   **Overall Architecture:** The project follows a monolithic application architecture using Django's Model-View-Template (MVT) pattern. It is designed for containerization with Docker and deployment to Google Cloud Run. The architecture clearly separates concerns into a web-facing frontend, a RESTful API, and a service layer for business logic.
*   **Directory Structure Philosophy:**
    *   `/src`: Contains all primary Django source code.
        *   `/src/api`: Defines the REST API endpoints, views, and serializers.
        *   `/src/config`: Holds central Django project configuration (`settings.py`, `urls.py`) and deployment configurations (`gunicorn.py`).
        *   `/src/pages`: Manages user-facing web pages and templates.
        *   `/src/services`: Contains decoupled business logic, such as `llm_service.py` for AI model interactions and `dao_service.py` for data access.
    *   `/terraform`: Contains all Infrastructure as Code (IaC) using Terraform to provision Google Cloud resources like Cloud Run, AlloyDB, and networking.
    *   `/sql`: Stores Data Definition Language (DDL) scripts for setting up the database schema.
    *   `/tests`: Contains all unit and integration tests.
    *   `/books`: Contains sample book text files for data ingestion.
    *   `/diagrams`: Stores architecture and workflow diagrams.

## 4. Coding Conventions & Style Guide

*   **Formatting:** The project uses `black`, `isort`, and `flake8`, indicating a strict adherence to the PEP 8 style guide with automated formatting. Indentation is 4 spaces.
*   **Naming Conventions:**
    *   `variables`, `functions`, `modules`: `snake_case` (e.g., `book_title`, `get_llm_service`, `dao_service.py`).
    *   `classes`: `PascalCase` (e.g., `LLMService`, `DAOService`).
*   **API Design:** The API follows RESTful principles. Endpoints exposed under `/api/` are resource-oriented nouns (e.g., `/api/books`, `/api/analysis`). It uses standard HTTP verbs (GET, POST) and communicates via JSON payloads. CSRF protection is disabled on a per-view basis for the API.
*   **Error Handling:** Error handling is done within view functions using `try...except` blocks. The API returns descriptive JSON error messages and appropriate HTTP status codes (e.g., 400 for bad requests, 405 for method not allowed).

## 5. Key Files & Entrypoints

*   **Main Entrypoint(s):**
    *   Development: `src/manage.py` is used to run the development server.
    *   Production: `gunicorn -c python:config.gunicorn config.wsgi` is the command specified in the `Dockerfile`.
*   **Configuration:**
    *   Application: `src/config/settings.py` is the primary Django configuration file.
    *   Environment: Environment variables are loaded via `os.getenv`, implying the use of a `.env` file (as seen in `README.md`).
    *   Infrastructure: `terraform/main.tf` and `terraform/terraform.tfvars` define the cloud infrastructure.
*   **CI/CD Pipeline:** `cloudbuild.yaml` defines the CI/CD pipeline, which builds the application's Docker image and pushes it to Google Artifact Registry.

## 6. Development & Testing Workflow

*   **Local Development Environment:** The `README.md` details two primary methods for local setup: 1) using a local Python virtual environment (`.venv`) and `pip`, and 2) using Docker for a containerized environment. Developers need to connect to a Google Cloud AlloyDB instance for the database backend.
*   **Testing:** Tests are located in the `/tests` directory and are run using `pytest`. The `README.md` provides instructions for running tests and setting the required environment variables.
*   **CI/CD Process:** When code is pushed, Google Cloud Build is triggered (as configured by `cloudbuild.yaml`). It builds the Docker image from the `Dockerfile` and pushes the tagged image to a dedicated Artifact Registry repository. This image is then used for deployment to Cloud Run.

## 7. Specific Instructions for AI Collaboration

*   **Contribution Guidelines:** No `CONTRIBUTING.md` file was found. Assume standard practices like creating feature branches and submitting pull requests.
*   **Infrastructure (IaC):** **CRITICAL:** The `/terraform` directory contains code that defines and manages live cloud infrastructure. Any changes to files in this directory can have significant, real-world consequences on the provisioned cloud resources. All modifications here must be reviewed with extreme care by a human developer.
*   **Security:** Be mindful of security best practices. Do not hardcode secrets, API keys, or passwords in the source code. Use environment variables for all sensitive data, as is the current practice.
*   **Dependencies:** To add a new dependency, add it to the `requirements.txt` file. Ensure the version is pinned to maintain deterministic builds. After updating, the `Dockerfile` will handle installation during the next build.
*   **Commit Messages:** Based on the git history, commit messages are short, imperative, and written in lowercase (e.g., `fix: update dao_service with query for book name`). While not strictly following a formal convention like Conventional Commits, messages should clearly and concisely describe the change.
