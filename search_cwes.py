import chromadb
from chromadb.utils import embedding_functions

def load_cwe_data(file_path):
    """
    Loads CWE data from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file containing CWE data. The format of this file should include columns like 'CWE-ID', 'Name', 'Description', and 'Extended Description'. It uses the format dictated in https://cwe.mitre.org/data/downloads.html
        
    Returns:
        list: A list of dictionaries containing CWE data.
    """
    import csv
    cwe_data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cwe_data.append(row)
        return cwe_data

def generate_index(cwe_data):
    """
    Generates a ChromaDB index from the provided CWE data.
    
    Args:
        cwe_data (list): A list of dicts containing CWE data with 'CWE-ID', 'Name', 'Description', 'Extended Description' columns.
        
    """
    client = chromadb.PersistentClient()
    
    documents = []
    metadatas = []
    for entry in cwe_data:
        description = entry.get('Description')
        extended_description = entry.get('Extended Description')
        doc_text = f"{description}\n{extended_description}"
        documents.append(doc_text)
        metadatas.append({"CWE-ID": entry.get('CWE-ID'), "Name": entry.get('Name')})

    openai_ef = embedding_functions.DefaultEmbeddingFunction()
    embeddings = openai_ef(documents)
    collection = client.get_or_create_collection(name="cwe_index")
    collection.add(
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
        ids=[meta["CWE-ID"] for meta in metadatas]
    )
    print("CWE index generated successfully.")

def search_cwe(query, top_k=5):
    """
    Searches the CWE index for the most relevant entries based on the query.
    
    Args:
        query (str): The search query.
        top_k (int): The number of top results to return.
        
    Returns:
        list: A list of dictionaries containing the search results.
    """
    client = chromadb.PersistentClient()
    collection = client.get_collection(name="cwe_index")
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    return results

