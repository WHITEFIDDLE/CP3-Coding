
INSERT INTO alertas (tipo, ip_origem, severidade)
VALUES
    ('BRUTE_FORCE', '185.220.101.1', 'alta'),
    ('PORT_SCAN', '45.33.32.156', 'alta'),
    ('SQL_INJECTION', '91.240.118.172', 'critica');

SELECT *
FROM alertas
WHERE severidade = 'alta';

UPDATE alertas
SET status = 'resolvido'
WHERE id = 1;

SELECT severidade, COUNT(*) AS total
FROM alertas
GROUP BY severidade
ORDER BY total DESC;

DELETE FROM alertas
WHERE criado_em < NOW() - INTERVAL 90 DAY;
