import random
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    num = data.get('number')
    if num is None:
        return jsonify({'error': 'No number provided'}), 400
    random_number = random.randint(1, 5000)
    return jsonify({
        'input': num,
        'random': random_number,
        'result': num + random_number
    })

if __name__ == '__main__':
    app.run(port=5000)
