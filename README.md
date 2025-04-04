# search-complex-pdf

pip install git+https://github.com/illuin-tech/colpali.git
pip install elasticsearch

Step 1 - Extract a jpeg file for each page of your pdf document
    In extractpdf.py set pdf_path = "<PDF path and filename>"    
    Execute extractpdf.py

Step 2 - Index the extracted jpeg files to a new index in your Elasticsearch serverless deployment
    In indexjpegwithcolpali.py set   
        INDEX_NAME = "<index>"
        es_url = "<url>"
        es_api = "<api>"
    Execute indexjpegwithcolpali.py

Step 3 - Search the document
    In searchapp.py set   
        INDEX_NAME = "<index>"
        es_url = "<url>"
        es_api = "<api>"
    Execute searchapp.py

    Access search app under : 127.0.0.1:5000
