import ipaddress

from flask import Flask, jsonify


app = Flask(__name__)

blacklist = {
    "185.220.101.1",
    "45.33.32.156",
    "91.240.118.172",
}


@app.get("/api/checar-ip/<ip>")
def checar_ip(ip):
    try:
        endereco = ipaddress.ip_address(ip)
    except ValueError:
        return jsonify(erro="IP inválido."), 400

    tipo = "privado" if endereco.is_private else "publico"

    return jsonify(
        ip=ip,
        na_blacklist=ip in blacklist,
        tipo=tipo,
    )


if __name__ == "__main__":
    app.run(debug=False)
