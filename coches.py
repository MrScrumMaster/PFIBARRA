import pandas as pd
from mysql.connector import connect, Error

def conecta():
    try:
        dbconexion = connect(host="127.0.0.1", user="root", password="popote12", database= "ventas_coches")
        if dbconexion.is_connected():
            print("Conexion a la base de datos realizada")
        return dbconexion
    except Error as e:
        print(e)

def guardar_csv_sql(data:pd.DataFrame):
    dbconexion = conecta()
    cursor = dbconexion.cursor()
    for i, row in data.iterrows():
        row = row.where(pd.notnull(row), None)
        consulta = "INSERT INTO VENTAS(Marca, Modelo, Tipo,Potencia,Precio) " \
          "VALUES (%s, %s, %s, %s, %s)"
        valores = tuple(row)
        cursor.execute(consulta,valores)
    dbconexion.commit()
    cursor.close()
    dbconexion.close()

def autos_vendidos(marca = None):
    dbconexion = conecta()
    cursor = dbconexion.cursor(dictionary=True)
    consulta = "SELECT Marca, Modelo, Tipo, Potencia, Precio FROM VENTAS"
    cursor.execute(consulta)
    resultados = cursor.fetchall()
    dbconexion.close()
    df = pd.DataFrame(resultados)
    df['Precio'] = df['Precio'].astype(float)
    if marca:
        df = df[df['Marca'] == marca]
    resultado = df.groupby('Marca').agg({'Precio': 'sum', 'Modelo': 'count'}).rename(
        columns={'Modelo': 'Cantidad_Vendida'})
    print(resultado)

def carros_mayor_precio(cantidad):
    dbconexion = conecta()
    cursor = dbconexion.cursor(dictionary=True)
    consulta ="SELECT Marca, Modelo, Tipo, Potencia, Precio FROM VENTAS"
    cursor.execute(consulta)
    resultados = cursor.fetchall()
    dbconexion.close()
    df = pd.DataFrame(resultados)
    df['Precio'] = df['Precio'].astype(float)
    df = df.sort_values(by='Precio', ascending=False)
    df_mayor = df.head(cantidad)
    print(df_mayor)





if __name__ == "__main__":
    pass

