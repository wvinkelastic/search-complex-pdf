from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import torch
from colpali_engine.models import ColPali, ColPaliProcessor
from elasticsearch import Elasticsearch
import os
import sys
from google import genai
from PIL import Image
import time

app = Flask(__name__,static_folder='static')

load_dotenv("elastic.env")
INDEX_NAME = os.getenv("index-name")
es_url = os.getenv("elastic_url")
es_api = os.getenv("elastic_api")
google_api_key = os.getenv("google_api_key")

google_model = "gemini-2.0-flash-lite"

client = genai.Client(api_key=google_api_key)
es = Elasticsearch(es_url, api_key=es_api)

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

# Check if the index exists
if not es.indices.exists(index=INDEX_NAME):
    print(f"Index '{INDEX_NAME}' doesn't exists. Exiting script.")
    sys.exit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('search_string')
        
        # Measure Elasticsearch query time
        start_time = time.time()
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
        #es_time = time.time() - start_time
        es_time = results['took'] / 1000

        file_paths = [os.path.basename(hit['_id']) for hit in results['hits']['hits']]
        image_paths = [hit['_id'] for hit in results['hits']['hits']]

        image_scores = [(hit['_score']) for hit in results['hits']['hits']]
        print(image_scores)

        # Measure Google Gemini query time
        start_time = time.time()
        images = [Image.open(image_path) for image_path in image_paths]
        response = client.models.generate_content(
            model=google_model,
            contents=[images, query + " Answer the question in not more than 10 sentences. Result should be an easy-to-read paragraph. Only use the information on the images to answer the question."]
        )
        google_time = time.time() - start_time
        
        # Return file paths and response times
        return jsonify(file_paths=file_paths, response_text=response.text, es_time=es_time, google_time=google_time)
    
    return render_template('index.html', file_paths=[], response_text="", es_time=0, google_time=0)

if __name__ == '__main__':
    app.run(debug=False)
    
