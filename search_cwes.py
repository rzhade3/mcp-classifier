import chromadb
from chromadb.utils import embedding_functions
import argparse
import sys

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

def main():
    """
    Main CLI function that handles command line arguments.
    """
    parser = argparse.ArgumentParser(description='CWE Classifier - Generate index and search CWE database')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate index command
    generate_parser = subparsers.add_parser('generate-index', help='Generate CWE index from CSV file')
    generate_parser.add_argument('filepath', help='Path to the CSV file containing CWE data')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search the CWE index')
    search_parser.add_argument('query', nargs='+', help='Search query text')
    search_parser.add_argument('--top-k', type=int, default=5, help='Number of top results to return (default: 5)')
    
    args = parser.parse_args()
    
    if args.command == 'generate-index':
        try:
            print(f"Loading CWE data from {args.filepath}...")
            cwe_data = load_cwe_data(args.filepath)
            print(f"Loaded {len(cwe_data)} CWE entries.")
            generate_index(cwe_data)
        except FileNotFoundError:
            print(f"Error: File '{args.filepath}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error generating index: {e}")
            sys.exit(1)
    
    elif args.command == 'search':
        try:
            query = ' '.join(args.query)
            print(f"Searching for: '{query}'")
            results = search_cwe(query, top_k=args.top_k)
            
            if results['documents']:
                print(f"\nFound {len(results['documents'][0])} results:\n")
                for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0]), 1):
                    print(f"{i}. CWE-{metadata['CWE-ID']}: {metadata['Name']}")
                    print(f"   Description: {doc[:200]}{'...' if len(doc) > 200 else ''}")
                    print()
            else:
                print("No results found.")
        except Exception as e:
            print(f"Error searching: {e}")
            print("Make sure you have generated the index first using 'generate-index' command.")
            sys.exit(1)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

