# CWE Classifier

A semantic search tool for Common Weakness Enumeration (CWE) database using ChromaDB vector embeddings. This tool allows you to efficiently search and classify software vulnerabilities based on CWE descriptions.

## Overview

The CWE Classifier provides a command-line interface to:
- Build a searchable vector index from CWE CSV data
- Perform semantic similarity searches across CWE entries
- Find the most relevant CWE classifications for vulnerability descriptions

## Features

- **Vector-based Search**: Uses ChromaDB with default embedding functions for semantic similarity
- **Persistent Storage**: Maintains the search index between sessions
- **Flexible Input**: Works with CWE CSV data from the official MITRE database
- **Configurable Results**: Adjustable number of search results (top-k)
- **Command Line Interface**: Easy-to-use CLI for both indexing and searching

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd cwe-classifier
```

2. Install uv (if you haven't already):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. Install dependencies:
```bash
uv sync
```

## Data Format

The tool expects CWE data in CSV format with the following columns:
- `CWE-ID`: The CWE identifier
- `Name`: The name of the weakness
- `Description`: Short description of the weakness
- `Extended Description`: Detailed description of the weakness

You can download the official CWE database in CSV format from [MITRE's CWE downloads page](https://cwe.mitre.org/data/downloads.html).

## Usage

### Generate Index

First, build the search index from your CWE CSV data:

```bash
python search_cwes.py generate-index path/to/your/cwe-data.csv
```

Example:
```bash
python search_cwes.py generate-index data/all.csv
```

### Search CWEs

Search for relevant CWE entries using natural language queries:

```bash
python search_cwes.py search "your search query"
```

#### Search Options

- `--top-k`: Number of results to return (default: 5)

#### Examples

```bash
# Basic search
python search_cwes.py search "buffer overflow"

# Search with more results
python search_cwes.py search "sql injection" --top-k 10

# Multi-word queries
python search_cwes.py search "cross site scripting vulnerabilities"
```

### Sample Output

```
Searching for: 'buffer overflow'

Found 5 results:

1. CWE-120: Buffer Copy without Checking Size of Input ('Classic Buffer Overflow')
   Description: The program copies an input buffer to an output buffer without verifying that the size of the input buffer is less than the size of the output buffer, leading to a buffer overflow...

2. CWE-121: Stack-based Buffer Overflow
   Description: A stack-based buffer overflow condition is a condition where the buffer being overwritten is allocated on the stack (i.e., is a local variable or, rarely, a parameter to a function)...

...
```

## Use Cases

- **Security Research**: Quickly find relevant CWE classifications for newly discovered vulnerabilities
- **Code Review**: Identify potential weakness categories during security assessments
- **Compliance**: Map identified issues to standard CWE classifications for reporting
- **Education**: Explore relationships between different types of software weaknesses

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Troubleshooting

### Common Issues

1. **"No results found" or collection errors**: Make sure you've generated the index first using the `generate-index` command.

2. **File not found errors**: Verify the path to your CSV file is correct and the file follows the expected format.

3. **ChromaDB errors**: Delete the `chroma/` directory and regenerate the index if you encounter database corruption issues.

### Getting Help

If you encounter issues:
1. Check that your CSV file has the required columns
2. Ensure ChromaDB is properly installed with `uv sync` or `uv pip install chromadb`
3. Verify Python version compatibility (3.8+)

## Acknowledgments

- [MITRE Corporation](https://cwe.mitre.org/) for maintaining the CWE database
- [ChromaDB](https://www.trychroma.com/) for the vector database implementation