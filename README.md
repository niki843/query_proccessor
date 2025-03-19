# Document Retrieval System with FAISS and Google Gemini AI

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![LangChainCommunity](https://img.shields.io/badge/LangChainCommunity-0.3.19-green)
![FAISS](https://img.shields.io/badge/FAISS-1.10.0-orange)
![LangChain Google Gemini AI](https://img.shields.io/badge/LangChain%20Google%20Gemini%20AI-2.1.0-yellow)

A simple yet powerful document retrieval system that uses **FAISS** for fast similarity search and **Google Gemini AI** for query enhancement and semantic understanding. This system is designed to retrieve the most relevant documents from a small dataset based on user queries.

---

## Features

- **Document Indexing**: Indexes documents using FAISS for fast and efficient similarity search.
- **Query Enhancement**: Uses Google Gemini AI to generate multiple query variations for improved retrieval.
- **Semantic Search**: Retrieves documents based on semantic similarity to the user's query.
- **Scalable Design**: Built with scalability in mind, allowing for easy adaptation to larger datasets.

---

## How It Works

1. **Document Dataset**:
   - The system uses a small dataset of documents (e.g., CSV files) relevant to a specific domain (e.g., tennis match results).
   - The dataset is loaded and preprocessed for indexing.

2. **Document Indexing**:
   - Each document is converted into a vector embedding using **Google Gemini AI**.
   - The embeddings are indexed using **FAISS** for fast similarity search.

3. **Query Processing**:
   - When a user submits a query, the system uses **Google Gemini AI** to generate multiple variations of the query.
   - These enhanced queries are used to retrieve the most relevant documents from the FAISS index.

4. **Document Retrieval**:
   - The system retrieves documents that are semantically similar to the query variations.
   - Duplicate results are removed, and the most relevant documents are returned to the user.

---

## Assumptions

- **Small Dataset**: The system is designed for small datasets. For larger datasets, consider using distributed FAISS or approximate nearest neighbor (ANN) algorithms.
- **In-Memory Processing**: The FAISS index is stored in memory, which is suitable for small to medium-sized datasets.
- **Google Gemini API**: The system requires access to Google Gemini API for generating embeddings and enhancing queries. And presumes that the output will be in the same formate every time. 
- **CSV Format**: The dataset is created to work with CSV format, but the system can be adapted for other formats (e.g., JSON, plain text).

---

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- Create a .env file, see .env_example
- Google Gemini API key (Gemini API KEY page https://aistudio.google.com/apikey)

### Installation

   ```bash
   git clone https://github.com/niki843/query_proccessor.git
   cd query_proccessing_system