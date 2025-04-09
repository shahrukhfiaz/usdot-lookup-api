from flask import Flask, request, jsonify
import requests
import re
import os

app = Flask(__name__)

@app.route("/usdot", methods=["GET"])
def get_usdot():
    mc = request.args.get('mc')
    if not mc:
        return {"error": "Missing MC number"}, 400

    url = f"https://safer.fmcsa.dot.gov/query.asp?searchtype=ANY&query_type=queryCarrierSnapshot&query_param=MC_MX&original_query_param=NAME&query_string={mc}"
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://safer.fmcsa.dot.gov/",
        "Accept": "text/html,application/xhtml+xml"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return {"error": "FMCSA rejected the request", "status": res.status_code}

        match = re.search(r'USDOT Number:.*?(\d{4,8})', res.text)
        usdot = match.group(1) if match else "Not found"

        return {
            "mc": mc,
            "usdot": usdot
        }

    except Exception as e:
        return {"error": "Something went wrong", "details": str(e)}, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
