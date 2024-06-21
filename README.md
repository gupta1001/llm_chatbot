# Q&A Chatbot with Vector Store

## Project Overview
This project involves creating a Q&A chatbot using a vector store and the Retrieval-Augmented Generation (RAG) model. The chatbot can answer user questions based on embedded knowledge from markdown files. It supports conversation persistence and offers users options to start new conversations, continue from where they left off, or stop.

## Setup Steps

1. **Install Dependencies**
   - Clone the repository:
     ```bash
     git clone <repository_url>
     cd <repository_directory>
     ```
   - Install required packages using `pip`:
     ```bash
     pip install -r requirements.txt
     ```

2. **Setup Environment Variables**
   - Create a `.env` file based on `.env-example` and fill in the required keys:
     ```
     MONGO_URI=your_mongodb_uri
     MONGO_DB=your_database_name
     VECTOR_DB_NAME=your_vector_db_name
     ```

3. **Create Vector Store**
   - Ensure the vector store checkpoint (`vectorstore_checkpoint.json`) is correctly configured:
     ```json
     {"vector_db_created": false}
     ```
   - Run `app.py` to create and populate the vector store in MongoDB:
     ```bash
     python app.py
     ```
   - Alternatively you can Run `create_vector_db.py` to create and populate the vector store in MongoDB independently:
     ```bash
     python ./data/vectors/create_vector_db.py
     ```

4. **Setup Atlas Vector Search Index**
   - Configure an index in Atlas Vector Search with the following settings:
     ```json
     {
       "mappings": {
         "dynamic": true,
         "fields": {
           "embedding": {
             "dimensions": 1536,
             "similarity": "cosine",
             "type": "knnVector"
           }
         }
       }
     }
     ```

5. **Prepare Markdown Knowledge Base**
   - Create a folder containing markdown files with information for the chatbot's knowledge base.

## Running the App

- After completing the setup steps, execute the main application:
  ```bash
  python app.py
