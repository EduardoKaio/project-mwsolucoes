SELECT 
    planoContrato,
    SUM(valorPlano) AS receita_total
FROM 
    clientes
GROUP BY 
    planoContrato
ORDER BY 
    receita_total DESC;