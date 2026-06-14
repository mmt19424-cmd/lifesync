from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
import os
import requests

app = Flask(__name__)
CORS(app)

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY", "sk_7h2cz50l_hN9g4rn1Dw0nMlbnj26TBYDTpy")

def load_donors():
    with open('donors.json') as f:
        return json.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def match():
    data = request.json
    blood_type = data.get('blood_type')
    donors = load_donors()
    matched = [d for d in donors 
               if d['blood_type'] == blood_type 
               and d['available']]
    return jsonify({"matched": matched[:3], "count": len(matched)})

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    donors = load_donors()
    new_donor = {
        "id": len(donors)+1,
        "name": data['name'],
        "blood_type": data['blood_type'],
        "area": data['area'],
        "phone": data['phone'],
        "language": data.get('language','Telugu'),
        "available": True
    }
    donors.append(new_donor)
    with open('donors.json','w') as f:
        json.dump(donors, f)
    return jsonify({"message":"Donor registered!", "donor": new_donor})

@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    donor_name = data.get('donor_name')
    blood_type = data.get('blood_type')
    hospital = data.get('hospital')
    language = data.get('language', 'Telugu')

    message = f"Emergency! {blood_type} blood needed at {hospital}. Please respond immediately."

    lang_code = {
        'Telugu': 'te-IN',
        'Hindi': 'hi-IN', 
        'Urdu': 'ur-IN'
    }.get(language, 'te-IN')

    try:
        response = requests.post(
            'https://api.sarvam.ai/text-to-speech',
            headers={
                'api-subscription-key': SARVAM_API_KEY,
                'Content-Type': 'application/json'
            },
            json={
                'inputs': [message],
                'target_language_code': lang_code,
                'speaker': 'meera',
                'model': 'bulbul:v1'
            }
        )
        return jsonify({
            "success": True,
            "audio": response.json().get('audios', [''])[0],
            "language": language,
            "message": message
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)