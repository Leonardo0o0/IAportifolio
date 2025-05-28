import math

# Função de classificação y^
def sigmoid(z):
    return 1 / (1 + math.exp(-z))

# Derivada da Função objetivo
def compute_gradient(x, y, theta):
    prediction = sigmoid(theta * x)
    return (prediction - y) * x

# Função objetivo
def compute_loss(data, theta):
    total_loss = 0
    for x, y in data:
        h = sigmoid(theta * x)
        loss = -y * math.log(h + 1e-10) - (1 - y) * math.log(1 - h + 1e-10)
        total_loss += loss
    return total_loss / len(data)

# Otimização com gradient descent
def gradient_descent(data, learning_rate=0.1, iterations=1000):
    theta = 0.1  # Peso inicial
    for i in range(iterations):
        gradient_sum = sum(compute_gradient(x, y, theta) for x, y in data)
        theta -= learning_rate * gradient_sum / len(data)

        if i % 100 == 0:
            loss = compute_loss(data, theta)
            print(f"Iteração {i}: theta = {theta:.4f}, perda = {loss:.4f}")

    return theta

# Representação de características da entrada (dados ficticios)
# 1 = teve pedra, 0 = não teve
data = [
    # < 1.2L - 50% chance
    (0.8, 1), (0.9, 0), (1.0, 1), (1.1, 0),
    
    # 1.5L - 33% chance
    (1.5, 1), (1.5, 0), (1.5, 0),
    
    # 1.8L - 20% chance
    (1.8, 1), (1.8, 0), (1.8, 0), (1.8, 0), (1.8, 0),
    
    # 2.0L - 10% chance
    (2.0, 1), (2.0, 0), (2.0, 0), (2.0, 0), (2.0, 0), (2.0, 0), (2.0, 0), (2.0, 0), (2.0, 0), (2.0, 0),
    
    # 2.2L - 10% chance
    (2.2, 1), (2.2, 0), (2.2, 0), (2.2, 0), (2.2, 0), (2.2, 0), (2.2, 0), (2.2, 0), (2.2, 0), (2.2, 0),
    
    # 2.5L, 3.0L, 3.5L - 5% chance
    (2.5, 1), (2.5, 0), (2.5, 0), (2.5, 0), (2.5, 0), (2.5, 0), (2.5, 0), (2.5, 0), (2.5, 0), (2.5, 0),
    (3.0, 1), (3.0, 0), (3.0, 0), (3.0, 0), (3.0, 0), (3.0, 0), (3.0, 0), (3.0, 0), (3.0, 0), (3.0, 0),
    (3.5, 1), (3.5, 0), (3.5, 0), (3.5, 0), (3.5, 0), (3.5, 0), (3.5, 0), (3.5, 0), (3.5, 0), (3.5, 0),
]

# Treinando o modelo
theta_final = gradient_descent(data)

# Previsão
def prever(litros):
    prob = sigmoid(theta_final * litros)
    print(f"Consumo: {litros}L → Risco de pedra nos rins: {prob*100:.2f}%")
    return prob

# Testando
prever(1.5)
prever(2.3)
prever(3.3)