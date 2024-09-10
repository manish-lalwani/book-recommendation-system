
# Book Recommendation System

## Overview
The **Book Recommendation System** is a modular microservice-based system that provides functionality for book and review CRUD operations, book recommendations using Machine Learning, and book summaries using LLM (Large Language Model).
The system comprises several REST APIs and services that communicate to deliver these features.

## Architecture

The system is designed to work as a set of REST microservices, each responsible for its own task, including book and review management, generating recommendations, and producing content summaries. All components interact via REST API calls, and the book data is persisted in a PostgreSQL database.

### Components:

- **Book CRUD Service**: 
  - Handles book and review-related CRUD operations.
  - **Tech Stack**: FastAPI, SQLAlchemy, PostgreSQL, Pytest
  
- **Book Recommendation Service**:- (Integration and Optimization Pending) (Have kept the Jupyter-notebook test files for verification)
  - Provides book recommendations using a Machine Learning model that analyzes the textual content of book descriptions.
  - **Tech Stack**: 
    - `scikit-learn`: For TF-IDF vectorization and Nearest Neighbors algorithm.
    - **Machine Learning Approach**: 
      - **TF-IDF (Term Frequency-Inverse Document Frequency)**: Converts book descriptions into numerical vectors for similarity comparison.
      - **Nearest Neighbors Algorithm**: Recommends similar books by measuring cosine similarity between book descriptions.
    - **Other**: Flask

- **Summary Generation Service**: (Integration and testing Pending) 
  - Uses a large language model (Llama3) to generate summaries for book content and reviews.
  - **Technologies**: 
    - **LLM**: A large language model for generating summaries (codellama-13b quantized).
    - **LangChain**: For integration with Llama3.
    - **Machine Learning Approach**: 
      - **Chunk-based Summarization**: Summarizes chunks of the book for improved context comprehension.
      - **Second-level Summarization**: Combines the summaries of individual chunks into a coherent final summary.
    - **Others**: FastAPI

- **PostgreSQL Database**:
  - A PostgreSQL database is used for persistent storage of book records and metadata for recommendations and summaries.

- **Common Technologies**: Poetry, Docker, Kubernetes, Helm

---

## Features

- **Book and Review CRUD Operations**: 
  - Manage book and review records with APIs to create, retrieve, update, and delete book and review information.
  
- **Book Recommendations**:
  - Provides machine-learning-driven recommendations based on book content descriptions using TF-IDF vectorization and Nearest Neighbors for similarity analysis.
  
- **Book Summary Generation**:
  - Generates a summary of the book's content using LLM, splitting long content into chunks to ensure accurate summarization of large texts.

- **Review Summary Generation**:
  - Aggregates and summarizes book reviews using the LLM to provide a concise summary of user opinions.

---

## Getting Started

### Prerequisites
- **Helm**: Required for deploying the services to Kubernetes via Helm charts.
- **Kubernetes**: A running Kubernetes cluster to deploy the services 

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/book-recommendation-system.git
   ```

2. **Deploy Book CRUD Service Using Helm**:
   The Book CRUD Service is deployed using Helm. Ensure that the Helm package `book-crud-service-0.1.0.tgz` is available.

   To install the Book CRUD service, run the following command:
   ```bash
   helm install book-crud-release ./book-crud-service-0.1.0.tgz --namespace book-recommendation-system --create-namespace
   ```

3. **Summary-Generation and Book-Recommendation Service Deployment with Helm** (Pending):

    Currently, the Docker and Kubernetes files for the **Book Recommendation Service** and **Summary Generation Service** are still pending.


5. **Verify the Deployment**:
   Once all Pods are up and running
   You will be able to access Swagger API for Book-CRUD-Service on
   ```bash
    http://minikube-ip:30001/docs and http://minikube-ip:30001/redoc
   ```
---

## API Endpoints

### Book CRUD Service

| Endpoint                  | Method | Description               |
|---------------------------|--------|---------------------------|
| `/books`                  | GET    | Retrieve all books         |
| `/books/{id}`             | GET    | Retrieve a book by ID      |
| `/books`                  | POST   | Create a new book          |
| `/books/{id}`             | PUT    | Update a book by ID        |
| `/books/{id}`             | DELETE | Delete a book by ID        |

### Review API

| Endpoint                  | Method | Description               |
|---------------------------|--------|---------------------------|
| `/books/{book_id}/reviews`| POST   | Create a new review        |
| `/books/{book_id}/reviews`| GET    | Get all reviews for a book |
| `/reviews/{review_id}`    | PUT    | Update a review by ID      |
| `/reviews/{review_id}`    | DELETE | Delete a review by ID      |

### Book Recommendation Service

| Endpoint                       | Method | Description                        |
|---------------------------------|--------|------------------------------------|
| `/recommend_books`              | POST   | Get book recommendations by title  |

**Request** (example):
```json
{
  "title": "The Great Gatsby",
  "n_neighbors": 5
}
```

**Response** (example):
```json
{
  "recommended_books": [
    "This Side of Paradise",
    "Tender is the Night",
    "The Beautiful and Damned",
    "Brave New World",
    "1984"
  ]
}
```

### Summary Generation Service

| Endpoint                     | Method | Description                     |
|-------------------------------|--------|---------------------------------|
| `/generate-summary`           | POST   | Upload a PDF and generate a summary  |
| `/generate-review-summary`     | POST   | Generate a summary for book reviews  |

**Request** (example for reviews):
```json
{
  "reviews": [
    "The book was a thrilling read from start to finish!",
    "I loved the character development but the pacing was slow.",
    "An enjoyable and immersive experience, but not as good as the first book."
  ]
}
```

**Response** (example):
```json
{
  "summary": "The reviews highlight positive character development and an immersive experience but point out issues with pacing. Overall, readers found the book enjoyable but not on par with the first in the series."
}
```

---

## Technologies Used

- **FastAPI**: Backend for the Book CRUD Service and Summary Generation Service.
- **Flask**: Backend for the Book Recommendation Service.
- **PostgreSQL**: Database for storing book data.
- **scikit-learn**: For implementing the TF-IDF vectorizer and Nearest Neighbors model for book recommendations.
- **LangChain**: For integrating with Llama3 model and handling summarization tasks.
- **Llama3 (Large Language Model)**: Used for generating summaries of books and reviews.
- **Kubernetes**: Orchestrating the microservices (optional if you're deploying using Kubernetes).
- **Docker**: Containerization of services for easier deployment and scaling.
- **Helm**: Package manager for Kubernetes to deploy services.

---


## License

This project is licensed under the MIT License.

---

## Contact

For any questions or issues, please reach out to the repository owner.
