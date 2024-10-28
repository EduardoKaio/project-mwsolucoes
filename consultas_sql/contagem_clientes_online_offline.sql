SELECT 
    cidadeCliente, 
    SUM(CASE WHEN statusCliente THEN 1 ELSE 0 END) AS clientes_online, 
    SUM(CASE WHEN NOT statusCliente THEN 1 ELSE 0 END) AS clientes_offline 
FROM 
    clientes 
GROUP BY 
    cidadeCliente;