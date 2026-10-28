import hashlib
from pathlib import Path

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier


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


def calcular_hash(caminho):
    conteudo = caminho.read_bytes()
    return hashlib.sha256(conteudo).hexdigest()


modelo = RandomForestClassifier(random_state=42)
modelo.fit(X, y)

arquivo_modelo = Path(__file__).with_name("modelo_seguranca.pkl")
joblib.dump(modelo, arquivo_modelo)

hash_original = calcular_hash(arquivo_modelo)

print(f"Modelo salvo: {arquivo_modelo.name}")
print(f"Hash SHA-256: {hash_original}")

modelo_carregado = joblib.load(arquivo_modelo)
hash_atual = calcular_hash(arquivo_modelo)

if hash_original != hash_atual:
    print("ALERTA: o arquivo do modelo foi modificado!")
else:
    previsao = modelo_carregado.predict([[60000, 4444, 18]])
    print(f"Hash confere. Previsão de teste: {previsao}")
