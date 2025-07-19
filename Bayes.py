import numpy as np

def medical_diagnosis_network(has_fever, has_cough, test_positive):
    #Calcula a probabilidade de ter uma doença com base em sintomas e resultado de exame.

    # P(Doença)
    p_disease = 0.05

    # P(Febre | Doença)
    p_fever_given_disease = 0.80
    p_fever_given_no_disease = 0.05

    # P(Tosse | Doença)
    p_cough_given_disease = 0.90
    p_no_cough_given_disease = 1 - p_cough_given_disease
    p_cough_given_no_disease = 0.10
    p_no_cough_given_no_disease = 1 - p_cough_given_no_disease

    # P(Exame Positivo | Doença)
    p_test_pos_given_disease = 0.95
    p_test_neg_given_disease = 1 - p_test_pos_given_disease
    p_test_pos_given_no_disease = 0.02
    p_test_neg_given_no_disease = 1 - p_test_pos_given_no_disease

    # Selecionar as probabilidades de evidência com base nas observações
    p_fever = p_fever_given_disease if has_fever else (1 - p_fever_given_disease)
    p_no_fever = p_fever_given_no_disease if has_fever else (1 - p_fever_given_no_disease)

    p_cough = p_cough_given_disease if has_cough else (1 - p_cough_given_disease)
    p_no_cough = p_cough_given_no_disease if has_cough else (1 - p_cough_given_no_disease)

    p_test = p_test_pos_given_disease if test_positive else (1 - p_test_pos_given_disease)
    p_no_test = p_test_pos_given_no_disease if test_positive else (1 - p_test_pos_given_no_disease)

    # Probabilidade conjunta para Doença = True
    p_joint_disease_true = p_fever * p_cough * p_test * p_disease
    
    # Probabilidade conjunta para Doença = False
    p_joint_disease_false = p_no_fever * p_no_cough * p_no_test * (1 - p_disease)

    # Normalizar para obter a distribuição de probabilidade final
    alpha = 1 / (p_joint_disease_true + p_joint_disease_false)

    p_disease_given_evidence = alpha * p_joint_disease_true
    p_no_disease_given_evidence = alpha * p_joint_disease_false

    return {'Prob_Doença': p_disease_given_evidence, 'Prob_Sem_Doença': p_no_disease_given_evidence}


evidence1 = {'has_fever': True, 'has_cough': True, 'test_positive': True}
result1 = medical_diagnosis_network(**evidence1)
print(f"Evidência: {evidence1}")
print(f"Resultado: {result1}\n")

evidence2 = {'has_fever': False, 'has_cough': False, 'test_positive': True}
result2 = medical_diagnosis_network(**evidence2)
print(f"Evidência: {evidence2}")
print(f"Resultado: {result2}\n") 

evidence3 = {'has_fever': True, 'has_cough': True, 'test_positive': False}
result3 = medical_diagnosis_network(**evidence3)
print(f"Evidência: {evidence3}")
print(f"Resultado: {result3}\n")

evidence4 = {'has_fever': True, 'has_cough': False, 'test_positive': False}
result4 = medical_diagnosis_network(**evidence4)
print(f"Evidência: {evidence4}")
print(f"Resultado: {result4}\n") 

evidence5 = {'has_fever': False, 'has_cough': True, 'test_positive': True}
result5 = medical_diagnosis_network(**evidence5)
print(f"Evidência: {evidence5}")
print(f"Resultado: {result5}\n") 