SELECT 
    planoContrato,
    COUNT(*) AS total_clientes
FROM 
    clientes
GROUP BY 
    planoContrato
ORDER BY 
    total_clientes DESC;