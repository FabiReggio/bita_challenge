'''

Solución 3 - Solución utilizando pandas y aplicando filtro sobre el archivo .csv (No se sobreescribe el .csv)

Librerias utilizadas:

pandas:   Se utiliza para acceder al archivo .csv y leer ese archivo por lotes (chunks).
psycopg2: Se utiliza para establecer la conexion con la BD en Postgres, crear la tabla e insertar registros en la misma.
time:     Se utiliza para medir el tiempo de ejecución. No es obligatorio utilizar esta libreria para objetivos del ejercicio.
argparse: Se utiliza para generar una interfaz del programa con el usuario, pasando todos los argumentos de entrada que utilizara el programa.

Se leen los datos del archivo original Stock.csv utilizando la libreria de pandas y a la vez se lee el archivo por lotes (chunks), se aplica el
filtro en el .csv para obtener los registros donde el primer campo del .csv PointOfSale contenga el carácter "_" y luego se va insertando en la tabla 
en lotes pequeños (batch_size = 1000). Finalmente, la tabla tendra los 4.554.888 de registros

Para objetivos de pruebas también se utilizó la función time para medir el tiempo de ejecución del código en segundos 

'''

import pandas as pd
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

# Establecer la conexión con la base de datos PostgreSQL
conn = psycopg2.connect(
    host=args.host,
    port=args.port,
    database=args.database,
    user=args.user,
    password=args.password
)

# Crear un cursor para ejecutar comandos SQL
cursor = conn.cursor()

# Crear una tabla en PostgreSQL
create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {args.tabla_bd} (
        PointOfSale character varying(200),
        Product character varying(200),
        Date date,
        Stock numeric
    );
"""

cursor.execute(create_table_query)
conn.commit()

batch_size = 1000 #Tamano del batch
low_memory=False  #Se utilizó esta condición para mejorar el rendimiento del programa

# Leer el archivo CSV utilizando Pandas en lotes
for chunk in pd.read_csv(args.archivo_csv, delimiter=';', chunksize=batch_size): 

    # Filtrar los datos del chunk donde el campo "PointOfSale" contiene el carácter "_"
    filtered_chunk = chunk[chunk['PointOfSale'].astype(str).str.contains('_')]

    # Insertar los datos filtrados en la tabla en lotes pequeños
    for index, row in filtered_chunk.iterrows():
        insert_query = f"INSERT INTO {args.tabla_bd} (PointOfSale, Product, Date, Stock) VALUES (%s, %s, %s, %s)"

        values = (row['PointOfSale'], row['Product'], row['Date'], row['Stock'])
        cursor.execute(insert_query, values)
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
