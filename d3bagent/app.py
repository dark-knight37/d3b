import requests
from flask import Flask, request


def download_url(url, query, save_path, chunk_size=128):
    r = requests.post(url, json=query, stream=True)
    if r.status_code == 200:
        with open(save_path, "wb") as fs:
            for chunk in r.iter_content(chunk_size=chunk_size):
                fs.write(chunk)
        return True
    return False


app = Flask(__name__)

fed_urls = {}


# MONGO_ULR = os.environ.get("MONGO_ULR")

@app.route("/")
def hello_world():
    return "<p>D3B Agent</p>"


@app.route("/registry", methods=['POST', 'GET'])
def registry():
    s = 'Error'
    c = 500
    if request.method == 'POST':
        # D3B Fed si registra
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            data = request.json
            if 'd3bfed_url' not in data or 'd3bfed_name' not in data:
                s = 'Invalid request'
                c = 400
                return s, c
            fed_urls[data['d3bfed_name']] = data['d3bfed_url']
            return 'Ok', 200
    return fed_urls
    # D3B fed chiede informazioni


@app.route('/distributed_search', methods=['POST'])
def distributed_search():
    s = 'Error'
    c = 500
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.json
        print(data, type(data))
        if 'query' not in data or 'type' not in data:
            s = 'Invalid request'
            c = 400
            return s, c
        try:
            if fed_urls:
                for fed in fed_urls:
                    res = download_url(f'{fed_urls[fed]}/get_patient_data', data, f'{fed}_out.zip')
            return 'Ok', 200
        except Exception as e:
            print(str(e))
            s = 'Erorr'
            c = 500
    return s, c
