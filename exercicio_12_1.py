import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


X = np.array(
    [
        [500, 80, 0.1],
        [1200, 80, 0.5],
        [64, 22, 0.02],
        [64000, 4444, 10.0],
        [45000, 8080, 15.0],
        [60000, 31337, 20.0],
        [800, 443, 0.3],
        [300, 53, 0.05],
        [55000, 9999, 18.0],
        [200, 25, 0.2],
        [700, 443, 0.2],
        [52000, 6666, 17.0],
        [150, 53, 0.03],
        [58000, 4444, 19.0],
        [900, 80, 0.4],
    ]
)

y = np.array([0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0])

pipeline = Pipeline(
    [
        ("normalizacao", StandardScaler()),
        ("classificador", RandomForestClassifier(random_state=42)),
    ]
)

resultados = cross_val_score(
    pipeline,
    X,
    y,
    cv=5,
)

print(f"Acurácia média: {resultados.mean():.2f}")
print(f"Desvio padrão: {resultados.std():.2f}")
