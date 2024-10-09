# ragex

![](src/images/rag-stack.png)

Leveraging LlamaIndex, ChromaDB, this RAG system is designed to process data from files of varying formats. This system can ingest data from files, store them in a ChromaDB vector database, and be used to query them with precision thanks to LlamaIndex’s retrieval tools.

The backend is a FastAPI server handling file upload and chat connection requests made from a Streamlit client app. 

![](src/images/convo-screenshot.png)

#### System Architecture:
Programming Language             - Python <br>
Model Provider                   - Groq, Google Vertex <br>
LLM Orchestrators and Frameworks - LlamaIndex, FastAPI, Streamlit <br>
Operational and Vector Database  - ChromaDB, SQLite <br>
Monitoring and Observability     - Python Logger <br>
Deployment                       - Streamlit, GCP <br>

