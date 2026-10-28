import numpy as np
from sklearn.ensemble import IsolationForest


acessos = np.array(
    [
        [9, 1, 200],
        [10, 1, 500],
        [14, 2, 300],
        [11, 1, 250],
        [16, 1, 400],
        [3, 40, 900000],
        [10, 1, 350],
        [15, 2, 280],
        [2, 55, 800000],
    ]
)

modelo = IsolationForest(contamination=0.25, random_state=42)
resultados = modelo.fit_predict(acessos)

for indice, resultado in enumerate(resultados):
    situacao = "ANOMALIA" if resultado == -1 else "Normal"
    print(f"Amostra {indice}: {acessos[indice].tolist()} -> {situacao}")
