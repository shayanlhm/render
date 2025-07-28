from flask import Flask, request, Response
import requests

app = Flask(__name__)

TARGET_URL = "https://api.divar.ir"

@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    url = f"{TARGET_URL}/{path}"
    if request.method == 'GET':
        resp = requests.get(url, headers=request.headers, params=request.args)
    else:
        resp = requests.post(url, headers=request.headers, params=request.args, data=request.get_data())
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
    response = Response(resp.content, resp.status_code, headers)
    return response

if __name__ == '__main__':
    app.run()
