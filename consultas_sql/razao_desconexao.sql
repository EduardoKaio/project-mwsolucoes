SELECT 
    motivoDesconexao, 
    COUNT(*) AS total_desconexoes 
FROM 
    clientes 
WHERE 
    motivoDesconexao IS NOT NULL 
GROUP BY 
    motivoDesconexao 
ORDER BY 
    total_desconexoes DESC;