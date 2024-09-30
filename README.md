# ragex

![](src/images/rag-stack.png)

Leveraging LlamaIndex, ChromaDB, this RAG system is designed to process data from files of varying formats. This system can ingest data from files, store them in a ChromaDB vector database, and be used to query them with precision thanks to LlamaIndex’s retrieval tools.

The backend is a FastAPI server handling file upload and chat connection requests made from a Streamlit client app. 


### Architecture:
Programming Language             - Python <b>
Model Provider                   - Groq, Google Vertex <b>
LLM Orchestrators and Frameworks - LlamaIndex, FastAPI, Streamlit <b>
Operational and Vector Database  - ChromaDB, SQLite <b>
Monitoring and Observability     - Python Logger <b>
Deployment                       - Streamlit, GCP <b>

