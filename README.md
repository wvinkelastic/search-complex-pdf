# search-complex-pdf

This project allows you to extract JPEG files from PDF documents, index them in Elasticsearch, and perform searches on the indexed data.

## Installation

To get started, install the necessary dependencies:

```bash
pip install git+https://github.com/illuin-tech/colpali.git elasticsearch
```

```Edit the elastic.env file
vi elastic.env
```

## Step-by-Step Guide

### Step 1: Extract JPEG Files from PDF

1. Set the path to your PDF document in `extractpdf.py`:

    ```python
    pdf_path = "<PDF path and filename>"
    ```

2. Execute the script to extract JPEG files:

    ```bash
    python extractpdf.py
    ```

### Step 2: Index JPEG Files in Elasticsearch

1. Configure your Elasticsearch settings in `indexjpegwithcolpali.py`:

    ```python
    INDEX_NAME = "<index>"
    es_url = "<url>"
    es_api = "<api>"
    ```

2. Execute the script to index the JPEG files:

    ```bash
    python indexjpegwithcolpali.py
    ```

### Step 3: Search the Document

1. Configure your search settings in `searchapp.py`:

    ```python
    INDEX_NAME = "<index>"
    es_url = "<url>"
    es_api = "<api>"
    ```

2. Execute the script to start the search application:

    ```bash
    python searchapp.py
    ```

3. Access the search application at:

    ```
    http://127.0.0.1:5000
    ```

## Notes

- Ensure your Elasticsearch serverless deployment is properly configured and accessible.
- Replace placeholders (`<PDF path and filename>`, `<index>`, `<url>`, `<api>`) with actual values specific to your setup.
