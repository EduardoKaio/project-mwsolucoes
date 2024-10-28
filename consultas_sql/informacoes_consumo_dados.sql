SELECT 
    cidadeCliente,
    SUM(consumoDownload) AS total_consumo_download,
    SUM(consumoUpload) AS total_consumo_upload
FROM 
    clientes
GROUP BY 
    cidadeCliente
ORDER BY
    total_consumo_download DESC;