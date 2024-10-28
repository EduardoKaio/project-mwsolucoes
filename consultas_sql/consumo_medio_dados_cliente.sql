SELECT 
    nomeCliente,
    AVG(consumoDownload) AS media_consumo_download,
    AVG(consumoUpload) AS media_consumo_upload
FROM 
    clientes
GROUP BY 
    nomeCliente
ORDER BY 
    media_consumo_download DESC;