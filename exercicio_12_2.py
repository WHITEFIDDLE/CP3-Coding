import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


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

modelos = {
    "Random Forest": RandomForestClassifier(random_state=42),
    "SVM": Pipeline(
        [
            ("normalizacao", StandardScaler()),
            ("modelo", SVC()),
        ]
    ),
    "KNN": Pipeline(
        [
            ("normalizacao", StandardScaler()),
            ("modelo", KNeighborsClassifier()),
        ]
    ),
}

validacao = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42,
)

pontuacoes = {}

for nome, modelo in modelos.items():
    resultados = cross_val_score(
        modelo,
        X,
        y,
        cv=validacao,
    )
    pontuacoes[nome] = resultados.mean()
    print(f"{nome}: {resultados.mean():.2f}")

vencedor = max(pontuacoes, key=pontuacoes.get)
print(f"Vencedor: {vencedor}")

grades = {
    "Random Forest": {
        "n_estimators": [50, 100, 200],
        "max_depth": [None, 3, 5],
    },
    "SVM": {
        "modelo__C": [0.1, 1, 10],
        "modelo__kernel": ["linear", "rbf"],
    },
    "KNN": {
        "modelo__n_neighbors": [1, 3, 5],
    },
}

busca = GridSearchCV(
    modelos[vencedor],
    grades[vencedor],
    cv=validacao,
)
busca.fit(X, y)

print(f"Melhores parâmetros: {busca.best_params_}")
