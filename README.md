# search-complex-pdf

This project allows you to extract JPEG files from PDF documents, index them in Elasticsearch, and perform searches on the indexed data.

## Installation

To get started, install the necessary dependencies:

```
pip install git+https://github.com/illuin-tech/colpali.git elasticsearch PyMuPDF Pillow Flask colpali-engine dotenv
```

Edit the elastic.env file, required are the Elasticsearch serverless URL, api-kep, pdf directory + filename and the Elastic index to be created.
- elastic_url = "url"
- elastic_api = "api-key>"
- pdf-path = "full directory plus file name .pdf"
- index-name = "Elastic index"

```
vi elastic.env
```

## Step-by-Step Guide

### Step 1: Extract JPEG Files from PDF

Execute the script to extract JPEG files:

```
python extractpdf.py
```

### Step 2: Index JPEG Files in Elasticsearch

Execute the script to index the JPEG files:

```
python indexjpegwithcolpali.py
```

### Step 3: Search the Document

Execute the script to start the search application:

```
python searchapp.py
```

Access the search application at:

```
http://127.0.0.1:5000
```

## Notes

- Ensure your Elasticsearch serverless deployment is properly configured and accessible.
- Replace placeholders (`<PDF path and filename>`, `<index>`, `<url>`, `<api>`) with actual values specific to your setup.
