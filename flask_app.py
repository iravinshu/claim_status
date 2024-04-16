import string

from flask import Flask, request
from flask_cors import CORS
import random
from datetime import datetime, timedelta

app = Flask(__name__)
cors = CORS(app)

tokens = []


@app.route('/raf/login', methods=['POST'])
def login():
    payload = request.json
    if payload.get('user_name') and payload.get('password'):
        now = datetime.now()
        token_expiry = now + timedelta(minutes=10)
        token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        tokens.append(token)
        return {"token": token,
                "expiry_time": token_expiry}
    return {
        'errCode': 500,
        'message': 'Internal Server Error'
    }, 500


@app.route('/api/Claim/GetClaim', methods=['GET'])
def get_claim_status():
    payload = request.args
    payload = {key: value.strip() for key, value in payload.items()}
    print(payload)
    headers = request.headers
    if headers.get('Authorization') not in tokens:
        return {
            "errCode": "RAFER001",
            "msg": "Can not authorize"
        }, 401
    errCodes = ['RAFOK001', 'RAFOK002', 'RAFOK001', 'RAFOK001']
    claim_status = ['Our records indicate that the claim may be too old or there is more than one claim registered '
                    'for this accident on our systems. Please contact our RAF Contact Centre on 087 820 1 111 for '
                    'further reasons of the rejection.',
                    'Kindly note the claim is still open and undergoing further processing and assessment. '
                    'Please contact our RAF Contact Centre on 087 820 1 111 for further assistance.']
    payment_status = ['BATCHED', None, None, 'PAID', '']
    first_names = ["John", "Jane", "Mary", "Bob", "Alice"]
    last_names = ["Smith", "Jones", "Williams", "Brown", "Davis"]

    errCode = random.choice(errCodes)
    if 'OK' in errCode:
        # Select random claim status and payment status
        claim = random.choice(claim_status)
        payment = random.choice(payment_status)
        link_number = payload['linkno']
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        id_no = payload['IDNoORPassportNo']
        dob = generate_random_dob()
        accident_date = payload['accidentDate']
    else:
        claim = ''
        payment = ''
        link_number = ''
        first_name = ''
        last_name = ''
        dob = ''
        id_no = ''
        accident_date = ''
    return {'errCode': errCode, 'linkno': link_number, 'NameAndSurname': first_name + ' ' + last_name,
            'IDNoORPassportNo': id_no, 'DateofBirth': dob, 'accidentDate': accident_date, 'ClaimStatus': claim,
            'PaymentStatus': payment}


def generate_random_dob(start_year=1900, end_year=2024):
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    if month == 2:
        day = random.randint(1, 28)
    else:
        day = random.randint(1, 30 if month in [4, 6, 9, 11] else 31)
    dob = datetime(year, month, day)
    return dob.strftime("%Y-%m-%d")


if __name__ == '__main__':
    app.run(port=7999, debug=True, host="0.0.0.0")
