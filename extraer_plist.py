import mysql.connector 
from mysql.connector import Error
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

def vaciar_tabla():
    try:

        db = mysql.connector.connect(
            host="labsac.com",
            user="labsacco_banano",
            passwd="ciba15153232",
            database="labsacco_banano_iot"
            )
        mycursor = db.cursor()

        sql = "TRUNCATE TABLE referencia;"
        mycursor.execute(sql)
    except Error as e:
        return("Error en la conexion con la base de datos", e)
    finally:
        if db.is_connected():
            mycursor.close()
            db.close()
            print("MySQL conxion terminada se ha vaciado los datos de la tabla 'referencia'")

def lista_excel(Plistt): #id del packinglist, se ejecuta primero
    try:
        db=mysql.connector.connect(host="labsac.com",user="labsacco_banano", password="ciba15153232", database="labsacco_banano_iot")
        if db.is_connected():
            mycursor = db.cursor()
            query = "SELECT Principal.ID_PRODUCTOR, Principal.FECHA_CORTE, Tcaja.DESCRIPCION FROM packing_list_detalle AS Principal, tipo_caja AS Tcaja WHERE Principal.ID_PACKING_LIST = {} AND Principal.ID_TIPO_CAJA = Tcaja.ID GROUP BY Principal.ID_PRODUCTOR, Principal.ID_TIPO_CAJA, Principal.FECHA_CORTE ORDER BY Principal.ID, Principal.NRO_PALLET ASC".format(Plistt)
            #mycursor.execute(query)
            result_dataFrame = pd.read_sql(query,db)
            #myresult = mycursor.fetchall()
            #return(myresult)
            return(result_dataFrame)
            ##CONVERTIMOS A UNIX EL FORMATO DE LA FECHA

            #print("Unix_Time_stamp: ",temp_BD_LAST_UNIX)
    except Error as e:
        return("Error en la conexion con la base de datos", e)
    finally:
        if db.is_connected():
            mycursor.close()
            db.close()
            #print("MySQL conxion terminada extraccion de dato")

def lista_total(Plistt): #id del packing list se ejecuta lista total
    try:
        db=mysql.connector.connect(host="labsac.com",user="labsacco_banano", password="ciba15153232", database="labsacco_banano_iot")
        if db.is_connected():
            mycursor = db.cursor()
            query = "SELECT Principal.ID, Principal.ID_PACKING_LIST,Principal.FECHA_CORTE,Principal.ID_PRODUCTOR,Principal.NRO_PALLET,Principal.NRO_CAJAS,Tcaja.DESCRIPCION FROM packing_list_detalle AS Principal, tipo_caja AS Tcaja WHERE Principal.ID_PACKING_LIST ={} AND Principal.ID_TIPO_CAJA=Tcaja.ID".format(Plistt)
            result_dataFrame = pd.read_sql(query,db)
            #myresult = mycursor.fetchall()
            #return(myresult)
            return(result_dataFrame)
            ##CONVERTIMOS A UNIX EL FORMATO DE LA FECHA

            #print("Unix_Time_stamp: ",temp_BD_LAST_UNIX)
    except Error as e:
        return("Error en la conexion con la base de datos", e)
    finally:
        if db.is_connected():
            mycursor.close()
            db.close()
            #print("MySQL conxion terminada extraccion de dato")


def logica(Plistt):
    List_orden = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    #Plistt = 5
    #formato dataframe
    df_excel= lista_excel(Plistt)
    ##Tabla de referencia sin tratar
    #print(df_excel)

    Id_productor = df_excel["ID_PRODUCTOR"]
    Fecha_corte = df_excel["FECHA_CORTE"]
    tipo_caja = df_excel["DESCRIPCION"]

    #print("ID PRODUCTOR:",Id_productor, type(Id_productor), np.shape(Id_productor))
    #convertimos a lista
    #Id_productor = list(Id_productor)
    #print("-Lista final BD:", Id_productor)
    ##eliminamos la columna para agregar la actualizada
    #df_excel.drop(["ID_PRODUCTOR"], axis=1)
    #print("Columna eliminada")

    #COMBINAMOS LAS TABLAS DE INTERES
    j=0
    lista = []
    for i in tipo_caja:
        #print("_________________________________")
        #print(i)
        datos_Plist_new ="{} {}".format(List_orden[j],i)
        #print(datos_Plist_new)
        lista.append(datos_Plist_new)
        j=j+1
    #print("--lista modificada:", lista, type(lista), np.shape(lista))
    #print("datos de PLIST (interes):",datos_Plist, np.shape(datos_Plist))
    #print("--Linea 1:",datos_Plist[0])

    ##nuevo dataframe tabla de referencia modificada
    df = pd.DataFrame()

    df["ID_PRODUCTOR"] = Id_productor
    df["FECHA_CORTE"] = Fecha_corte
    df["DESCRIPCION"] = lista
    #print(df)
    #convertimos el dataframe a lista
    vector_modificada = df.to_numpy().tolist()
    #print("vector modificada:", vector_modificada, type(vector_modificada), np.shape(vector_modificada))



    ###segunda tabla por filas VECTOR DE REFERENCIA

    datos_pallets = lista_total(Plistt)
    filas = len(datos_pallets) #cantidad total de datos a analizar
    #print("cantidad de filas:",filas, type(filas))

    ####  tratamos la tabla de referencia sin cambiar
    vector_referencia = df_excel.to_numpy().tolist()
    #print("vector de referencia:", vector_referencia, type(vector_referencia), np.shape(vector_referencia))

    #datos nuevos
    df2 = pd.DataFrame()

    ID_f = []
    ID_plist_f = []
    Fecha_Corte_f = []
    Id_productor_f = []
    Nro_pallet_f = []
    Nro_cajas_f = []
    tipo_caja_f = []

    for k in range(filas):
        #print("____________________________________________FILA ",k, )
        C_filas = datos_pallets.iloc[k,:]
        ##extraemos los ID de los agricultores
        Id_ = C_filas[0]
        Id_list_ = C_filas[1]
        Fecha_Corte = C_filas[2]
        ID_agricultores = C_filas[3]
        Nro_pallet_ = C_filas[4]
        Nro_cajas_ = C_filas[5]
        T_caja = C_filas[6]

        #print( "Fecha de corte:", Fecha_Corte)
        #print( "ID PRODUCTORES:",ID_agricultores)
        #print( "TIPO DE CAJA:",T_caja)
        #print(C_filas, type (C_filas), np.shape(C_filas))
        trama = [ID_agricultores, Fecha_Corte, T_caja]
        #print("trama es:", trama)
        n=0 ##representa la posicion en el vector de referencia
        #comparamos para cada fila de la referencia
        for V_ref in vector_referencia:
            #print("Trama es:", trama)
            if V_ref == trama:
                #print("____________Posicion en vector modificado", n)
                trama = vector_modificada[n]
                #print("trama actualizada:", trama)
            else:
                trama=trama
            n = n+1

        ID_f.append(Id_)
        ID_plist_f.append(Id_list_)
        Nro_pallet_f.append(Nro_pallet_)
        Nro_cajas_f.append(Nro_cajas_)

        Fecha_Corte_f.append(trama[1])
        Id_productor_f.append(trama[0])
        tipo_caja_f.append(trama[2])


    df2["ID_PRINCIPAL"] = ID_f
    df2["ID_PACKING_LIST"] = ID_plist_f
    df2["FECHA_CORTE"] = Fecha_Corte_f
    df2["ID_PRODUCTOR"] = Id_productor_f
    df2["NRO_PALLET"] = Nro_pallet_f
    df2["NRO_CAJAS"] = Nro_cajas_f
    df2["TIPO_CAJA"] = tipo_caja_f

    #print(df2)


    ##INSERTAMOS EL DATAFRAME
    engine = create_engine("mysql+pymysql://{user}:{pw}@labsac.com/{db}"
                        .format(user="labsacco_banano",
                                pw="ciba15153232",
                                db="labsacco_banano_iot"))
    #db=mysql.connector.connect(host="labsac.com",user="labsacco_banano", password="ciba15153232", database="labsacco_banano_iot")
    df2.to_sql('referencia', con = engine, if_exists = 'append', chunksize = 1000, index=False)
    #print("datos insertados")