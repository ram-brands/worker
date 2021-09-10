## Análisis de factura Ecomsur, despachos por BlueExpress

Este programa calcula el volumen y peso de cada referencia de pedido, y luego lo compara con
lo que fue cobrado por Ecomsur para el mismo pedido. 

Luego del análisis, se crea un archivo 'diferencias.csv', el cual contiene todas las diferencias encontradas.
En este archivo, cada línea corresponde a una referencia, y compara los cálculos del análisis con el cobrado.


# Como utilizar el programa:

1. Cargar documentos en la carpeta 'data'. Asegurarse de que los nombres de los archivos sean los mismos del archivo 'paths.py'.

2. Abrir y ejecutar el archivo 'main.py'.

3. Revisar resultados en la carpeta 'results'.


# En caso de error:

Enviar mensaje con el error que se ve en pantalla a Alex Apt:
- +56777909037
- aapt@uc.cl


# Librerías usadas:

- unidecode
- xlrd

