# search-complex-pdf

This project allows you to extract JPEG files from PDF documents, index them in Elasticsearch, and perform searches on the indexed data.

## Installation

To get started, install the necessary dependencies:

```bash
pip install git+https://github.com/illuin-tech/colpali.git elasticsearch
```

Edit the elastic.env file, ElasticSearch serverless URL, api-kep, pdf filename and index to be created.
```Edit the elastic.env file
vi elastic.env
```

## Step-by-Step Guide

### Step 1: Extract JPEG Files from PDF

Execute the script to extract JPEG files:

    ```bash
    python extractpdf.py
    ```

### Step 2: Index JPEG Files in Elasticsearch

Execute the script to index the JPEG files:

    ```bash
    python indexjpegwithcolpali.py
    ```

### Step 3: Search the Document

Execute the script to start the search application:

    ```bash
    python searchapp.py
    ```

Access the search application at:

    ```
    http://127.0.0.1:5000
    ```

## Notes

- Ensure your Elasticsearch serverless deployment is properly configured and accessible.
- Replace placeholders (`<PDF path and filename>`, `<index>`, `<url>`, `<api>`) with actual values specific to your setup.
