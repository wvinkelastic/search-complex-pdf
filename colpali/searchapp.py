from flask import Flask, render_template, request, jsonify
import torch
from colpali_engine.models import ColPali, ColPaliProcessor
from elasticsearch import Elasticsearch
import os
import sys

app = Flask(__name__,static_folder='static')

# Set following
INDEX_NAME = "<index>"
es_url = "<url>"
es_api = "<api>"
# Set 

model_name = "vidore/colpali-v1.3"
model = ColPali.from_pretrained(
    "vidore/colpali-v1.3",
    torch_dtype=torch.float32,
    device_map="mps",  # "mps" for Apple Silicon, "cuda" if available, "cpu" otherwise
).eval()

col_pali_processor = ColPaliProcessor.from_pretrained(model_name)

def create_col_pali_query_vectors(query: str) -> list:
    queries = col_pali_processor.process_queries([query]).to(model.device)
    with torch.no_grad():
        return model(**queries).tolist()[0]

es = Elasticsearch(es_url, api_key=es_api)

# Check if the index exists
if not es.indices.exists(index=INDEX_NAME):
    print(f"Index '{INDEX_NAME}' doesn't exists. Exiting script.")
    sys.exit()

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        query = request.form.get('search_string')
        
        es_query = {
            "_source": False,
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "maxSimDotProduct(params.query_vector, 'col_pali_vectors')",
                        "params": {"query_vector": create_col_pali_query_vectors(query)},
                    },
                }
            },
            "size": 5,
        }
        
        results = es.search(index=INDEX_NAME, body=es_query)

        file_paths = [os.path.basename(hit['_id']) for hit in results['hits']['hits']]

        for file_path in file_paths:
            print(file_path)

        return jsonify(file_paths=file_paths)
    return render_template('index.html', file_paths=[])

if __name__ == '__main__':
    app.run(debug=True)