SELECT 
    bairroCliente, 
    COUNT(*) AS total_clientes 
FROM 
    clientes 
GROUP BY 
    bairroCliente 
ORDER BY 
    total_clientes DESC;