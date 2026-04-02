import math
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def norm_cdf(x):
    return (1 + math.erf(x / math.sqrt(2))) / 2

def norm_pdf(x):
    return math.exp(-0.5 * x ** 2) / math.sqrt(2 * math.pi)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    try:
        S     = float(data['S'])
        K     = float(data['K'])
        r     = float(data['r'])
        T     = float(data['T'])
        sigma = float(data['sigma'])
        if any(v <= 0 for v in [S, K, T, sigma]):
            raise ValueError("S, K, T and sigma must be positive")
    except (KeyError, TypeError, ValueError) as e:
        return jsonify({'error': str(e)}), 400

    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    discounted_K = K * math.exp(-r * T)
    sqrt_T = math.sqrt(T)
    pdf_d1 = norm_pdf(d1)

    call = S * norm_cdf(d1) - discounted_K * norm_cdf(d2)
    put  = discounted_K * norm_cdf(-d2) - S * norm_cdf(-d1)

    return jsonify({
        'd1': round(d1, 4),
        'd2': round(d2, 4),
        'call': round(call, 4),
        'put':  round(put, 4),
        'greeks': {
            'Delta': [round(norm_cdf(d1), 4),                                  round(norm_cdf(d1) - 1, 4)],
            'Gamma': [round(pdf_d1 / (S * sigma * sqrt_T), 4),                 round(pdf_d1 / (S * sigma * sqrt_T), 4)],
            'Vega':  [round(S * pdf_d1 * sqrt_T / 100, 4),                     round(S * pdf_d1 * sqrt_T / 100, 4)],
            'Theta': [round((-(S*pdf_d1*sigma)/(2*sqrt_T) - r*discounted_K*norm_cdf(d2))  / 365, 4),
                      round((-(S*pdf_d1*sigma)/(2*sqrt_T) + r*discounted_K*norm_cdf(-d2)) / 365, 4)],
            'Rho':   [round( discounted_K * T * norm_cdf(d2)  / 100, 4),
                      round(-discounted_K * T * norm_cdf(-d2) / 100, 4)],
        }
    })

if __name__ == '__main__':
    app.run(port=5001)
