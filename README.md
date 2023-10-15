# Bita Challenge 

# 1. Objetivo del ejercicio

- Escribir un programa en python que lea datos de un archivo .csv e insertar estos datos en una tabla en PostgreSQL localmente
- No usar la funcion COPY, ni ningun mecanismo de importacion masiva de PostgreSQL
- Antes de insertar en la base de datos, eliminar contenido de una posible importacion anterior
- Tomar en cuenta rendimiento y recursos
- Aplicar buenas prácticas de desarrollo y codigo bien escrito
- Documentación del ejercicio en un README.md

# 2. Estructura de las archivos

- **README.md**: Documentación general
- **csv_to_sql_1.py**: Solución 1
- **csv_to_sql_2.py**: Solución 2
- **csv_to_sql_3.py**: Solución 3
- **csv_to_sql_4.py**: Solución 4

# 3. Explicación de la Resolución

1. En el archivo .csv se identificaron los registros que se van a considerar para insertar en la base de datos. El archivo originalmente tiene 17.175.295 registros, se aplicó un filtro sobre el campo PointOfSale del archivo .csv considerando que los registros correctos son aquellos los cuales contienen el caracter "_" ya que aportan más valor a los datos. Es decir, los diferentes valores para la primera columna, serían los siguientes:


     CDSB2C_P_SALE 
     CDSB2C_S_FULLPRICE 
     CDSB2C_S_SALE
     CSP064_S_FULLPRICE
     CSP064_S_SALE
     OBR041_P_SALE
     OBR041_S_SALE
     OCA077_P_SALE
     OCA077_S_SALE
     OIT033_P_SALE
     OIT033_S_SALE
     ONH074_P_SALE
     ONH074_S_SALE
     OSA080_P_SALE
     OSA080_S_SALE
     OSC079_P_SALE
     OSC079_S_SALE
     PDP050_S_FULLPRICE
     PDP050_S_SALE
     PMA066_S_FULLPRICE
     PMA066_S_SALE

2. Con el filtro aplicado previamente, el número de registros totales a insertar en la tabla serían: 4.554.888 

3. Para la solución se hicieron diferentes pruebas utilizando diversas librerías de python para procesamiento de datos e inserción de los datos postgres como: `csv`, `psycopg2` y `pandas`. Adicionalmente para medir el tiempo de ejecución de los scripts se utilizó la libreria: `time` y para crear una interfaz para el usuario que va a ejecutar el programa pasando todos los argumentos de entrada se utilizó la libreria `argparse`

4. Se implementaron 4 soluciones, en donde a continuación se explicarán con mayor detalle.

# 4. Soluciones 

 - **csv_to_sql_1.py**: En este script se implementó una solución utilizando las librerías (`csv`,`psycopg2`). 
    - `csv:`      Se utiliza para acceder y leer los datos del archivo .csv
    - `psycopg2:` Se utiliza para establecer la conexión con la BD en Postgres, crear la tabla e insertar registros en la misma.
    - **Explicación del código:** Se leen los datos del archivo original Stock.csv que tiene 17.175.295 registros y se aplica el filtro en el .csv antes de insertar los datos en una tabla para obtener los registros donde el primer campo del .csv PointOfSale contenga el carácter "_", insertando asi 4.554.888 de registros. El código lee el archivo CSV en lotes de tamaño configurable (en este caso se utilizó el tamano de lote 10000). Después, realiza inserciones en la base de datos utilizando el método `executemany()` de `psycopg2`, el cual permite insertar múltiples filas en una sola consulta. Esto es más eficiente que realizar una inserción por cada fila.
 
 - **csv_to_sql_2.py**: En este script se implementó una solución utilizando las librerías (`csv`,`psycopg2`).
    - `csv:`      Se utiliza para acceder y leer los datos del archivo .csv
    - `psycopg2:` Se utiliza para establecer la conexión con la BD en Postgres, crear la tabla e insertar registros en la misma.
    - **Explicación del código:**: La única diferencia de esta solución con la anterior es que en vez de filtrar en el .csv antes de insertar, se aplica el filtro en el archivo .csv y se sobreescribe ese archivo .csv teniendo 4.554.888 de registros y partir de ese archivo, se inserta en la base de datos de la misma forma que se explicó en la solución anterior.

 - **csv_to_sql_3.py**: En este script se implementó una solución utilizando las librerías (`pandas`,`psycopg2`).
    - `pandas`:   Se utiliza para acceder al archivo .csv y leer ese archivo por lotes (chunks).
    - `psycopg2`: Se utiliza para establecer la conexión con la BD en Postgres, crear la tabla e insertar registros en la misma.
    - **Explicación del código**: Se leen los datos del archivo original Stock.csv utilizando la librería de pandas y a la vez se lee el archivo por lotes (chunks), se aplica el filtro en el .csv para obtener los registros donde el primer campo del .csv PointOfSale contenga el carácter "_" y luego se va insertando en la tabla en lotes pequeños (batch_size = 1000). Finalmente, la tabla tendrá los 4.554.888 de registros.
 
 - **csv_to_sql_4.py**: En este script se implementó una solución utilizando las librerías (`pandas`,`psycopg2`).
    - `pandas`: Se utiliza para acceder al archivo .csv y leer ese archivo por lotes (chunks).
    - `psycopg2`: Se utiliza para establecer la conexion con la BD en Postgres, crear la tabla e insertar registros en la misma (utilizando executemany).
    - **Explicación del código**: El objetivo de esta solución es poder mezclar dos de las soluciones previas, usando la librería de pandas para leer el archivo por lotes (chunks) y a la vez insertar en la base de datos utilizando el método `executemany()` de `psycopg2` , el cual permite insertar múltiples filas en una sola consulta. Igualmente a medida de que se itera sobre cada lote (chunk), se aplica el filtro en el .csv para obtener los registros donde el primer campo del .csv PointOfSale contenga el carácter "_" y luego se va insertando en la tabla.

Adicionalmente en las 4 soluciones explicadas previamente se utilizaron las siguientes librerías de Python: 

- `time:` Se utiliza para medir el tiempo de ejecución. Se utilizó para comparar los tiempos de ejecución en cada solución.  
- `argparse:` Se utiliza para generar una interfaz del programa con el usuario final, pasando todos los argumentos de entrada que utilizará el programa. En la última sección se explica cómo ejecutar cada script. Los argumentos de entrada que debe proveer el usuario que va a ejecutar el código son:

    - **database**: Nombre de la base de datos
    - **user**: Nombre de usuario
    - **password**: Contraseña para acceder a la base de datos
    - **host**: Dirección del host
    - **port**: Número de puerto
    - **archivo_csv**: Ruta del archivo CSV
    - **tabla_bd**: Nombre de la tabla en la base de datos

# 5. Resultados de los tiempos de ejecución 

 - **csv_to_sql_1.py**: 
    - Tiempo de ejecución: 688.130 seg = 11.46 min  
    - Tiempo de ejecución: 715.97 seg = 11.93 min
 - **csv_to_sql_2.py**:
    - Tiempo de ejecución: 678.368 seg = 11.30 min
    - Tiempo de ejecución: 692.99 seg = 11.54 min 
 - **csv_to_sql_3.py**:
   -  Tiempo de ejecución: 2651.24 segundos = 44.187 min 
 - **csv_to_sql_4.py**
     - Tiempo de ejecución: 1050.20 seg = 17.5min

Es importante destacar que antes de llegar a estos scripts como soluciones finales, se implementaron varias soluciones previas y ejecutaron corridas de prueba obteniendo el mismo resultado en promedio que el mostrado previamente. También se evaluó el rendimiento con diferentes tamanos de batches en cada script, concluyendo que el mejor rendimiento se obtuvo en el tamano de batch definido en cada script.

# 6. Conclusiones

En base a las soluciones presentadas previamente, los mejores tiempos de ejecución fueron para los scripts: **csv_to_sql_1.py**, **csv_to_sql_2.py** y **csv_to_sql_4.py**

**csv_to_sql_1.py** me parece la mejor solución en comparación a **csv_to_sql_2.py** porque en el primer caso se aplican los filtros directamente en el archivo .csv sin necesidad de sobreescribirlo, conservando así el archivo original. Además en esta solución se utiliza el método `executemany()` de `psycopg2`, el cual permite insertar múltiples filas en una sola consulta.

**csv_to_sql_2.py** puede ser un poco más eficiente en los tiempos de ejecución, ya que no requiere leer y filtrar el archivo .csv en una operación separada. Sin embargo, existe un riesgo de perder los datos originales al sobreescribir el archivo .csv, si no se realiza una copia de seguridad adecuada. 

En cuanto al script **csv_to_sql_4.py**. Aunque el tiempo de ejecución es mayor que en los scripts anteriores. Esta solución puede ser muy eficiente en términos de lectura del archivo .csv y escritura en la tabla ya que lee por lotes y se insertan múltiples filas en una sola consulta.

Es importante considerar que el rendimiento puede depender de varios factores, como el tamaño del archivo, la capacidad de la máquina, la configuración de la base de datos, si existen operaciones de escritura y lectura al mismo tiempo sobre la base de datos, entre otros. Por eso siempre es importante realizar las pruebas pertinentes y ajustes particulares dependiendo del caso.

# 7. Cómo ejecutar los scripts en terminal cada caso

**Script 1**

**Comando en consola**

*python csv_to_sql_1.py --database --user --password --host --port --archivo_csv --tabla_bd*

**Ejemplo de como ejecutarlo**

*python csv_to_sql_1.py --database bita_db --user postgres --password "" --host localhost --port 5433 --archivo_csv "C:/Users/fabia/Desktop/Challenge BITA/archivos_escritorio/solucion_final/Stock.csv" --tabla_bd stock_big*

**Script 2**

**Comando en consola**

*python csv_to_sql_2.py --database --user --password --host --port --archivo_csv --tabla_bd*

**Ejemplo de como ejecutarlo**

*python csv_to_sql_2.py --database bita_db --user postgres --password "" --host localhost --port 5433 --archivo_csv "C:/Users/fabia/Desktop/Challenge BITA/archivos_escritorio/solucion_final/Stock.csv" --tabla_bd stock_big*

**Script 3**

**Comando en consola**

*python csv_to_sql_3.py --database --user --password --host --port --archivo_csv --tabla_bd*

**Ejemplo de como ejecutarlo**

*python csv_to_sql_3.py --database bita_db --user postgres --password "" --host localhost --port 5433 --archivo_csv "C:/Users/fabia/Desktop/Challenge BITA/archivos_escritorio/solucion_final/Stock.csv" --tabla_bd stock_big*

**Script 4**

**Comando en consola**

*python csv_to_sql_4.py --database --user --password --host --port --archivo_csv --tabla_bd*

**Ejemplo de como ejecutarlo**

*python csv_to_sql_4.py --database bita_db --user postgres --password "" --host localhost --port 5433 --archivo_csv "C:/Users/fabia/Desktop/Challenge BITA/archivos_escritorio/solucion_final/Stock.csv" --tabla_bd stock_big*





