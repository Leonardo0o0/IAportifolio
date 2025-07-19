import numpy as np

# calcula provável comportamento do usuário
# Estados Ocultos (Intenção)
states = ['Explorando', 'Pesquisando', 'Finalizando Compra']

# Observações (Ações)
observations = ['Ver Página Principal', 'Usar Barra de Pesquisa', 'Ver Página de Produto', 'Adicionar ao Carrinho']

# Matriz de Transição T: P(Intenção_t | Intenção_{t-1})
transition_matrix = np.array([[0.6, 0.3, 0.1],
                              [0.1, 0.6, 0.3],
                              [0.1, 0.2, 0.7]])

# Matriz de Emissão (Observação) E: P(Ação_t | Intenção_t)
emission_matrix = np.array([[0.5, 0.1, 0.05],
                            [0.2, 0.6, 0.05],
                            [0.3, 0.3, 0.4],
                            [0.2, 0.1, 0.5]])

def infer_user_intent(observed_actions):
    # Realiza a filtragem (algoritmo forward) para estimar a intenção do usuário.
    num_states = transition_matrix.shape[0]
    
    # Crença inicial
    initial_belief = np.full(num_states, 1.0 / num_states)
    
    # f_{1:t} que é P(X_t | e_{1:t})
    forward_message = initial_belief
    
    print(f"Crença Inicial P(Intenção_0): { {s: round(p, 2) for s, p in zip(states, forward_message)} }")
    print("-" * 30)

    for i, action_index in enumerate(observed_actions):
        # 1. Passo de Predição
        predicted_state = transition_matrix.T @ forward_message
        
        # 2. Passo de Atualização
        likelihood_of_action = emission_matrix[action_index, :]
        updated_state = likelihood_of_action * predicted_state
        
        # 3. Normalização
        updated_state /= updated_state.sum()
        
        forward_message = updated_state
        
        print(f"Ação {i+1}: '{observations[action_index]}'")
        print(f"Crença Atualizada P(Intenção_{i+1}|Ações_{1:{i+1}}):")
        for s, p in zip(states, forward_message):
            print(f"  - {s}: {p:.3f}")
        print("-" * 30)

    return forward_message

# Sequência de ações observadas do usuário:
# Ex: 0: Ver Página Principal -> 1: Usar Barra de Pesquisa -> 2: Ver Página de Produto -> 3: Adicionar ao Carrinho
user_session_actions = [0, 1, 2, 3]

print("--- Iniciando Inferência de Intenção do Usuário ---")
final_intent_belief = infer_user_intent(user_session_actions)

print("\nCrença final sobre a intenção do usuário:")
for s, p in zip(states, final_intent_belief):
    print(f"  - {s}: {p:.3f}")

most_likely_intent_index = np.argmax(final_intent_belief)
print(f"\nIntenção mais provável ao final da sessão: '{states[most_likely_intent_index]}'")