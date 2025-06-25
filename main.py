import argparse
import sys
from search_cwes import load_cwe_data, generate_index, search_cwe

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
