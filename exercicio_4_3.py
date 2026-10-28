from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)


y_verdadeiro = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]
y_previsto = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

print("Matriz de confusão:")
print(confusion_matrix(y_verdadeiro, y_previsto))
print(f"Acurácia: {accuracy_score(y_verdadeiro, y_previsto):.2f}")
print(f"Precisão: {precision_score(y_verdadeiro, y_previsto):.2f}")
print(f"Recall: {recall_score(y_verdadeiro, y_previsto):.2f}")
print(f"F1: {f1_score(y_verdadeiro, y_previsto):.2f}")

print("\nA acurácia de 90% esconde que metade dos ataques não foi detectada.")
print("O recall mostra quantos ataques reais o modelo encontrou.")
print("Em um SOC, deixar um ataque passar pode causar um incidente grave.")
