
INSERT INTO alertas (tipo, ip_origem, severidade)
VALUES
    ('BRUTE_FORCE', '185.220.101.1', 'critica'),
    ('BRUTE_FORCE', '185.220.101.1', 'alta'),
    ('BRUTE_FORCE', '185.220.101.1', 'alta'),
    ('BRUTE_FORCE', '185.220.101.1', 'critica'),
    ('PORT_SCAN', '45.33.32.156', 'alta'),
    ('PORT_SCAN', '45.33.32.156', 'media'),
    ('PORT_SCAN', '45.33.32.156', 'critica'),
    ('XSS', '91.240.118.172', 'alta'),
    ('XSS', '8.8.8.8', 'media'),
    ('SQLI', '1.1.1.1', 'baixa');

SELECT severidade, COUNT(*) AS total
FROM alertas
GROUP BY severidade
ORDER BY total DESC;

SELECT tipo, COUNT(*) AS total
FROM alertas
GROUP BY tipo
ORDER BY total DESC;

SELECT ip_origem, COUNT(*) AS total
FROM alertas
GROUP BY ip_origem
ORDER BY total DESC
LIMIT 5;
