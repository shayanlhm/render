from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

TARGET_URL = "https://api.divar.ir"

@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    url = f"{TARGET_URL}/{path}"

    # ساخت هدرهای جدید و فیلتر کردن هدرهای ناخواسته
    excluded_headers = ['host', 'content-length', 'connection', 'accept-encoding', 'content-encoding', 'transfer-encoding']
    headers = {}
    for name, value in request.headers.items():
        if name.lower() not in excluded_headers:
            headers[name] = value

    # اضافه کردن هدرهای ضروری (می‌تونی تغییرشون بدی)
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    headers['Accept'] = 'application/json, text/plain, */*'
    headers['Origin'] = 'https://divar.ir'
    headers['Referer'] = 'https://divar.ir'

    if request.method == 'GET':
        resp = requests.get(url, headers=headers, params=request.args)
    else:
        # اگر payload JSON هست، استفاده از json=request.get_json(force=True)
        # در غیر اینصورت data=request.get_data()
        try:
            json_data = request.get_json(force=True)
            resp = requests.post(url, headers=headers, json=json_data, params=request.args)
        except:
            resp = requests.post(url, headers=headers, data=request.get_data(), params=request.args)

    excluded_resp_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    response_headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_resp_headers]

    response = Response(resp.content, resp.status_code, response_headers)
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
