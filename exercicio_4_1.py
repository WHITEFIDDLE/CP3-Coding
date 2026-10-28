import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split


X = np.array(
    [
        [1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1],
        [2, 1, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [8, 1, 1, 1, 5],
        [12, 0, 1, 1, 8],
        [6, 1, 1, 1, 3],
        [10, 1, 1, 1, 6],
        [0, 0, 0, 0, 0],
        [15, 1, 1, 1, 9],
    ]
)

y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 0, 1])

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42,
    stratify=y,
)

modelo = RandomForestClassifier(random_state=42)
modelo.fit(X_treino, y_treino)
previsoes = modelo.predict(X_teste)

print(f"Acurácia: {accuracy_score(y_teste, previsoes):.2f}")
print(f"Precisão: {precision_score(y_teste, previsoes):.2f}")
print(f"Recall: {recall_score(y_teste, previsoes):.2f}")
print(f"F1: {f1_score(y_teste, previsoes):.2f}")

novo_email = [[11, 1, 1, 1, 7]]
resultado = modelo.predict(novo_email)[0]
print("Novo e-mail:", "Phishing" if resultado == 1 else "Legítimo")
