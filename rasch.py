import math

def rasch_probability(theta, b):
    return 1 / (1 + math.exp(-(theta - b)))

def estimate_theta(responses, difficulties, max_iter=20):
    theta = 0.0
    
    for _ in range(max_iter):
        num = 0
        den = 0
        
        for x, b in zip(responses, difficulties):
            p = rasch_probability(theta, b)
            num += x - p
            den += p * (1 - p)
        
        if den == 0:
            break
        
        theta += num / den
    
    return round(theta, 4)

def scale_score(theta, scale=100):
    return round((theta + 3) / 6 * scale, 2)
