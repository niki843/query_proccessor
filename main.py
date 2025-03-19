import logging
import os

import requests
from dotenv import load_dotenv

from langchain_community.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

CSV_URL = "https://github.com/JeffSackmann/tennis_atp/raw/refs/heads/master/atp_matches_1968.csv"
MATCHES_PATH = "./atp_matches_1968.csv"

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
llm = GoogleGenerativeAI(model="gemini-2.0-flash")

def load_data():
    """Download CSV file if not already present."""
    if os.path.isfile(MATCHES_PATH):
        return

    logger.info("Downloading dataset...")
    try:
        response = requests.get(CSV_URL)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to download dataset: {e}")

    with open(MATCHES_PATH, "w") as matches_file:
        matches_file.write(response.content.decode('utf-8'))

def index_document():
    """Index data, create FAISS vector."""
    loader = CSVLoader(file_path=MATCHES_PATH)
    documents = loader.load()

    db = FAISS.from_documents(documents, embeddings)

    return db

def query_documents(db, queries):
    """Query vector for matches, based Gemini enhanced queries get best unique matches"""

    all_docs = []
    for query in queries:
        logger.info(f"Searching for query: {query}")
        docs_with_scores = db.similarity_search_with_score(query)
        all_docs.extend(docs_with_scores)

    # Sort documents by similarity score (lower is better)
    all_docs.sort(key=lambda x: x[1])
    unique_docs = list({doc.page_content: doc for doc, _ in all_docs}.values())
    return unique_docs

def enhance_query(user_query):
    """Use an LLM to rewrite the query for better retrieval. Get a list of possible best match queries"""
    template = """
        Rewrite this search query to be more precise for document retrieval using FAISS vector: {user_query}. 
        Return all possible optimized queries split with a comma.
        No additional text.
    """
    prompt = PromptTemplate(template=template, input_variables=["user_query"])
    llm_chain = prompt | llm | StrOutputParser()

    try:
        improved_query = llm_chain.invoke(user_query)
    except Exception as e:
        logger.warning(f"Query enhancement failed: {e}. Using original query!")
        return [user_query]

    logger.info(f"Enhanced possible queries: {improved_query}")
    return improved_query.split(",")

def main(user_query):
    """Load data, Create vector with FAISS, Enhance user query with Gemini, Search Vector"""
    logger.info("Loading Data...")
    load_data()

    logger.info("Indexing vector...")
    db = index_document()

    logger.info("Querying data...")
    enhanced_queries = enhance_query(user_query)

    related_documents = query_documents(db, enhanced_queries)

    if related_documents:
        logger.info(f"Related documents count: {len(related_documents)}")
        logger.info(f"Best match document:\n{related_documents[0].page_content}")
    else:
        logger.info("No relevant documents found!")

if __name__ == "__main__":
    user_input = "Who won the Buenos Aires game between Thomaz Koch and Fred Stolle?"
    main(user_input)
