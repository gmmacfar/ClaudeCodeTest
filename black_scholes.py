import math

def norm_cdf(x):
    return (1 + math.erf(x / math.sqrt(2))) / 2

def norm_pdf(x):
    return math.exp(-0.5 * x ** 2) / math.sqrt(2 * math.pi)

def black_scholes(S, K, r, T, sigma):
    d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    discounted_K = K * math.exp(-r * T)

    call = S * norm_cdf(d1) - discounted_K * norm_cdf(d2)
    put  = discounted_K * norm_cdf(-d2) - S * norm_cdf(-d1)

    sqrt_T   = math.sqrt(T)
    pdf_d1   = norm_pdf(d1)

    greeks = {
        "Delta": (norm_cdf(d1), norm_cdf(d1) - 1),
        "Gamma": (pdf_d1 / (S * sigma * sqrt_T),) * 2,
        "Vega":  (S * pdf_d1 * sqrt_T / 100,) * 2,          # per 1% vol move
        "Theta": (
            (-(S * pdf_d1 * sigma) / (2 * sqrt_T) - r * discounted_K * norm_cdf(d2))  / 365,
            (-(S * pdf_d1 * sigma) / (2 * sqrt_T) + r * discounted_K * norm_cdf(-d2)) / 365,
        ),
        "Rho": (
             discounted_K * T * norm_cdf(d2)  / 100,
            -discounted_K * T * norm_cdf(-d2) / 100,
        ),
    }

    return call, put, d1, d2, greeks

def get_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  Please enter a valid number.")

print("\n=== Black-Scholes Option Calculator ===\n")
S     = get_input("Stock price (S):              ")
K     = get_input("Strike price (K):             ")
r     = get_input("Risk-free rate (r, e.g 0.05): ")
T     = get_input("Time to expiry in years (T):  ")
sigma = get_input("Volatility (sigma, e.g 0.20): ")

call, put, d1, d2, greeks = black_scholes(S, K, r, T, sigma)

print(f"\n--- Results ---")
print(f"  d1:         {d1:.4f}")
print(f"  d2:         {d2:.4f}")
print(f"  Call price: ${call:.4f}")
print(f"  Put price:  ${put:.4f}")

print(f"\n--- Greeks ---")
print(f"  {'Greek':<8}  {'Call':>10}  {'Put':>10}")
print(f"  {'-'*32}")
for name, (c, p) in greeks.items():
    print(f"  {name:<8}  {c:>10.4f}  {p:>10.4f}")
print()
