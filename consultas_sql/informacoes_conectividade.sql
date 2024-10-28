SELECT 
    nomeConcentrador,
    AVG(tempoConectado) AS tempo_medio_conectado,
    COUNT(*) AS total_clientes
FROM 
    clientes
GROUP BY 
    nomeConcentrador
ORDER BY 
    tempo_medio_conectado DESC;