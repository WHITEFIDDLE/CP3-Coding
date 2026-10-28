CREATE DATABASE IF NOT EXISTS vulnerabilidades_db;

USE vulnerabilidades_db;

CREATE TABLE ativos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    ip VARCHAR(45) NOT NULL UNIQUE,
    tipo VARCHAR(50) NOT NULL,
    criticidade ENUM('baixa', 'media', 'alta', 'critica') NOT NULL
);

CREATE TABLE vulnerabilidades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cve_id VARCHAR(20) NOT NULL UNIQUE,
    descricao TEXT NOT NULL,
    severidade ENUM('baixa', 'media', 'alta', 'critica') NOT NULL,
    cvss DECIMAL(3, 1) NOT NULL CHECK (cvss BETWEEN 0 AND 10)
);

CREATE TABLE ativo_vulnerabilidade (
    ativo_id INT NOT NULL,
    vulnerabilidade_id INT NOT NULL,
    status VARCHAR(30) DEFAULT 'aberta',
    detectada_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (ativo_id, vulnerabilidade_id),
    FOREIGN KEY (ativo_id) REFERENCES ativos(id),
    FOREIGN KEY (vulnerabilidade_id) REFERENCES vulnerabilidades(id)
);

INSERT INTO ativos (nome, ip, tipo, criticidade)
VALUES ('SRV-WEB01', '192.168.1.10', 'servidor', 'alta');

INSERT INTO vulnerabilidades (cve_id, descricao, severidade, cvss)
VALUES ('CVE-2024-001', 'Vulnerabilidade usada no exercício', 'alta', 8.5);

INSERT INTO ativo_vulnerabilidade (ativo_id, vulnerabilidade_id)
SELECT ativos.id, vulnerabilidades.id
FROM ativos
CROSS JOIN vulnerabilidades
WHERE ativos.nome = 'SRV-WEB01'
  AND vulnerabilidades.cve_id = 'CVE-2024-001';
