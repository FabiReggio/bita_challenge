'''

Solución 2 - Solución sin utilizar pandas, aplicando filtro y sobreescribiendo csv

Librerias utilizadas:

csv:      Se utiliza para acceder y leer los datos del archivo .csv
psycopg2: Se utiliza para establecer la conexion con la BD en Postgres, crear la tabla e insertar registros en la misma.
time:     Se utiliza para medir el tiempo de ejecución. No es obligatorio utilizar esta libreria para objetivos del ejercicio.
argparse: Se utiliza para generar una interfaz del programa con el usuario, pasando todos los argumentos de entrada que utilizara el programa.

Se leen los datos del archivo original Stock.csv y se aplica filtro en el .csv para obtener los registros 
donde el primer campo del .csv PointOfSale contenga el carácter "_" y luego se sobreescribe el csv en donde finalmente se tendran 4.554.888 de registros

Para objetivos de pruebas también se utilizó la función time para medir el tiempo de ejecución del código en segundos 

El código lee el archivo CSV en lotes de tamaño configurable (en este caso se utilizó el tamano de lote 10000).
Después, realiza inserciones en la base de datos utilizando el método `executemany()` de `psycopg2`, el cual permite insertar múltiples filas 
en una sola consulta. Esto es más eficiente que realizar una inserción por cada fila.

'''

import csv
import psycopg2
import time
import argparse

# Inicio del tiempo de ejecución
inicio = time.time()

# Parsear los argumentos de línea de comandos
parser = argparse.ArgumentParser()
parser.add_argument("--database", help="Nombre de la base de datos")
parser.add_argument("--user", help="Nombre de usuario")
parser.add_argument("--password", help="Contraseña")
parser.add_argument("--host", help="Dirección del host")
parser.add_argument("--port", help="Número de puerto")
parser.add_argument("--archivo_csv", help="Ruta del archivo CSV")
parser.add_argument("--tabla_bd", help="Nombre de la tabla en la base de datos")
args = parser.parse_args()

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(database=args.database, user=args.user, password=args.password, host=args.host, port=args.port)

# Crear un cursor para ejecutar consultas
cursor = conn.cursor()

# Crear tabla en la base de datos si no existe
crear_tabla_query = f"""
CREATE TABLE IF NOT EXISTS {args.tabla_bd} (
    PointOfSale character varying(200), 
    Product character varying(200), 
    Date date, 
    Stock numeric
);
"""

cursor.execute(crear_tabla_query)
conn.commit()

#Procesamiento y sobreescritura del archivo csv original para filtrar los registros deseados

# Crear una lista para almacenar los registros filtrados
registros_filtrados = []

# Abrir el archivo en modo lectura
with open(args.archivo_csv, "r") as file:
    # Leer el archivo csv
    reader = csv.reader(file)
    # Obtener el encabezado del archivo
    header = next(reader)
    # Agregar el encabezado a la lista de registros filtrados
    registros_filtrados.append(header)
    # Recorrer cada registro del archivo
    for registro in reader:
        # Verificar si el primer campo del registro contiene el carácter "_"
        if "_" in registro[0]:
            # Agregar el registro a la lista de registros filtrados
            registros_filtrados.append(registro)

# Abrir el archivo en modo escritura
with open(args.archivo_csv, "w", newline="") as file:
    # Escribir los registros filtrados en el archivo
    writer = csv.writer(file)
    writer.writerows(registros_filtrados)


# Abrir el archivo CSV ajustado con los filtros aplicados previamente y leer los datos

# Leer datos del archivo CSV y realizar inserciones en lotes
with open(args.archivo_csv, 'r') as f:
    reader = csv.reader(f, delimiter=';')
    next(reader) # Saltar la primera fila si contiene encabezados

    lote = []
    num_filas = 0
    tamano_lote = 10000 # Número de filas por lote (esta valor se puede ajustar)

    for fila in reader:
        if "_" in fila[0]:  # Filtrar las filas cuyo primer campo contiene el carácter "_"
            lote.append(fila)
            num_filas += 1

            # Insertar lote de filas en la base de datos cuando alcanza el tamaño del lote
            if num_filas % tamano_lote == 0:
                cursor.executemany(f"INSERT INTO {args.tabla_bd} (PointOfSale, Product, Date, Stock) VALUES (%s, %s, %s, %s)", lote)
                conn.commit()
                lote = []

    # Insertar las filas restantes en un último lote (si no se dividieron exactamente en el tamaño del lote)
    if lote:
        cursor.executemany(f"INSERT INTO {args.tabla_bd} (PointOfSale, Product, Date, Stock) VALUES (%s, %s, %s, %s)", lote)
        conn.commit()

# Cerrar la conexión a la base de datos
cursor.close()
conn.close()

# Fin del tiempo de ejecución
fin = time.time()

# Tiempo total de ejecución
tiempo_total = fin - inicio

# Imprimiendo el tiempo de ejecución en segundos
print("Tiempo de ejecución:", tiempo_total, "segundos")
