from flask import Flask, redirect, render_template_string, request


app = Flask(__name__)
alertas = []

pagina = """
<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8">
    <title>Alertas</title>
  </head>
  <body>
    <h1>Alertas</h1>

    <form method="post">
      <input name="descricao" required>
      <button>Cadastrar</button>
    </form>

    <ul>
      {% for alerta in alertas %}
        <li>{{ alerta }}</li>
      {% endfor %}
    </ul>
  </body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def inicio():
    if request.method == "POST":
        alertas.append(request.form["descricao"])
        return redirect("/")

    return render_template_string(pagina, alertas=alertas)


if __name__ == "__main__":
    app.run(debug=False)
