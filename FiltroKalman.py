import numpy as np

# --- Configuração do Cenário ---
dt = 0.1  # Intervalo de tempo (segundos)
total_time = 50 # Tempo total reduzido
t = np.arange(0, total_time, dt)
n_steps = len(t)

# --- Modelo Real do Drone ---
true_altitude = np.zeros(n_steps)
true_velocity = np.zeros(n_steps)
acceleration_commands = np.zeros(n_steps)
acceleration_commands[int(1/dt):int(4/dt)] = 2.0   # Subir

# Ruído do processo 
process_noise_std = 0.5
# Ruído do sensor
measurement_noise_std = 2.0

# Simulação do movimento real
# Usando semente para resultados reproduzíveis
np.random.seed(42)
for k in range(1, n_steps):
    true_velocity[k] = true_velocity[k-1] + acceleration_commands[k-1] * dt
    true_altitude[k] = true_altitude[k-1] + true_velocity[k-1] * dt + 0.5 * acceleration_commands[k-1] * dt**2
    true_velocity[k] += np.random.randn() * process_noise_std # Adicionando ruído do processo à velocidade real

# Gerar medições ruidosas do altímetro
measurements = true_altitude + np.random.randn(n_steps) * measurement_noise_std

# Filtro de Kalman
# Vetor de estado
x_hat = np.zeros((2, n_steps))
P = np.eye(2) * 500  # Incerteza inicial

# Matrizes do Filtro de Kalman
F = np.array([[1, dt], [0, 1]])
B = np.array([[0.5 * dt**2], [dt]])
H = np.array([[1, 0]])
Q = B @ B.T * process_noise_std**2
R = np.array([[measurement_noise_std**2]])

# Loop do Filtro de Kalman com saída no terminal
print(f"{'Tempo (s)':<10} | {'Altitude Real':<15} | {'Medição (Sensor)':<18} | {'Altitude Estimada':<20} | {'Velocidade Estimada':<20}")
print("-" * 90)

for k in range(1, n_steps):
    # Passo de Predição
    u = np.array([[acceleration_commands[k-1]]])
    x_hat_pred = F @ x_hat[:, k-1].reshape(-1, 1) + B @ u
    P_pred = F @ P @ F.T + Q

    # Passo de Atualização
    z = measurements[k]
    y_tilde = z - H @ x_hat_pred
    S = H @ P_pred @ H.T + R
    K = P_pred @ H.T @ np.linalg.inv(S)

    x_hat[:, k] = (x_hat_pred + K @ y_tilde).flatten()
    P = (np.eye(2) - K @ H) @ P_pred
    
    # Imprime os resultados para o passo atual
    print(f"{t[k]:<10.1f} | {true_altitude[k]:<15.3f} | {measurements[k]:<18.3f} | {x_hat[0, k]:<20.3f} | {x_hat[1, k]:<20.3f}")