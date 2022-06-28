from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import functions
from werkzeug.exceptions import HTTPException
from forms import FormPackingList
from forms import FormPackingListDetalle
import datetime
import extraer_plist
import time

""" loginv  """
from flask import Flask, render_template, request, redirect, url_for, flash
#from config import config
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect

#from flask_login import LoginManager
from flask_login import LoginManager, login_user,logout_user, login_required

from models.ModelUser import ModelUser

from models.entities.User import User
###

app = Flask(__name__)

login_manager_app=LoginManager(app)
#MYSQL CONECTION
# app.config['MYSQL_HOST'] = '127.0.0.1'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'banano_iot'
# mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'labsac.com'
app.config['MYSQL_USER'] = 'labsacco_banano'
app.config['MYSQL_PASSWORD'] = 'ciba15153232'
app.config['MYSQL_DB'] = 'labsacco_banano_iot'
db = MySQL(app)
 #db=db.connector.connect( host="labsac.com",user="labsacco_dia", password="ciba15153232", database="labsacco_banano")
       
#SETTINGS
app.secret_key = 'mysecretkey'

###login
@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        print("dentro de post")
        print(request.form['username'])
        print(request.form['password'])
        ###COMPARAR
        print("antes de user")
        user = User(0, request.form['username'], request.form['password'])
        print("despues deuser:", user)
        logged_user = ModelUser.login(db, user)
        print("antes de los if")
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                print("usuario validado ")
                return redirect(url_for('home'))

            else:
                flash("invalid password")
                return render_template('auth/login.html')

        else:
            flash("User not found")

            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')
        print("out")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('index.html')

##

""" @app.route('/')
def Index():
   #return render_template ('index.html')
    
     cur = db.connection.cursor()
     cur.execute("SELECT pl.ID, pl.HORA_LLEGADA, pl.INICIO_LLENADO, pl.HORA_SALIDA, pl.NRO_CONTENEDOR, pl.NAVE, mar.DESCRIPCION, emp.DESCRIPCION, pl.FECHA_REGISTRO, pl.NRO_SEMANA. pl.P_LINEA, pl.P_ADUANA FROM packing_list pl, marca mar, empacadora emp WHERE pl.ID_MARCA = mar.ID AND pl.ID_EMPACADORA = emp.ID ORDER BY pl.ID desc ")

     data = cur.fetchall()

     formPackingList = FormPackingList()
     return render_template('viewFormPackingList.html', dataPackingList = data, form = formPackingList) """

@app.route('/viewFormPackingList')
@login_required
def viewFormPackingList():
    #valor = 0
    
     cur = db.connection.cursor()
     cur.execute("SELECT pl.ID, pl.HORA_LLEGADA, pl.INICIO_LLENADO, pl.HORA_SALIDA, pl.NRO_CONTENEDOR, pl.NAVE, mar.DESCRIPCION, emp.DESCRIPCION, pl.FECHA_REGISTRO, pl.NRO_SEMANA, pl.P_LINEA, pl.P_ADUANA FROM packing_list pl, marca mar, empacadora emp WHERE pl.ID_MARCA = mar.ID AND pl.ID_EMPACADORA = emp.ID ORDER BY pl.ID desc")

     data = cur.fetchall()


     #print('data[0] es ', data[0][0])
     #print('data[todo] es ', data)
     
    #  cur.execute('select * from MARCA order by descripcionn ASC')

    #  dataMarca = cur.fetchall()

    #  cur.execute('select * from EMPACADORA order by descripcion ASC')

    #  dataEmpacadora = cur.fetchall()
     formPackingList = FormPackingList()
     return render_template('viewFormPackingList.html', dataPackingList = data, form = formPackingList)



@app.route('/add_packingList', methods=['POST'])
@login_required
def add_packingList():
    #return 'Add contact'
    if request.method =='POST':
        fechaRegistro = request.form['fechaRegistro']
        horaLlegada = request.form['horaLlegada']
        inicioLlenado = request.form['inicioLlenado']
        horaSalida = request.form['horaSalida']
        nroSemana = request.form['nroSemana']
        nroContenedor = request.form['nroContenedor']
        nave = request.form['nave']
        pLinea = request.form['pLinea']
        pAduana = request.form['pAduana']

        marca = request.form['cmbMarca']
        empacadora = request.form['cmbEmpacadora']
        
        #print("hora llegada", horaLlegada)
        #print("hora Salida", horaSalida)

        cur = db.connection.cursor()

        if(horaLlegada==""): horaLlegada="00:00:00"
        if(inicioLlenado==""): inicioLlenado="00:00:00"
        if(horaSalida==""): horaSalida="00:00:00"

        #cur.execute('INSERT INTO packing_list values (%s,%s,%s, %s, )', (fullaname, phone, email))
        
        #consulta = 'INSERT INTO NROHOJAS (fecha, valor) values (now(),'+nroHojas+')'
        consulta = 'INSERT INTO packing_list (FECHA_REGISTRO, HORA_LLEGADA, INICIO_LLENADO, HORA_SALIDA, NRO_SEMANA, NRO_CONTENEDOR, NAVE, ID_MARCA, ID_EMPACADORA, P_LINEA, P_ADUANA) VALUES ("'+fechaRegistro+'","'+horaLlegada+'", "'+inicioLlenado+'", "'+horaSalida+'","'+nroSemana+'", "'+nroContenedor+'", "'+nave+'", '+marca+', '+empacadora+', "'+pLinea+'", "'+pAduana+'" )'
        print ("insert consulta",  consulta)
        cur.execute(consulta)
        #print("ultimo id insertado ",db.connection.insert_id())
        session['packingListId'] = db.connection.insert_id()
        db.connection.commit()
        
        flash('Packing List creado exitosamente, agregar el detalle') #mensaje a la vista

        #return 'recibido'
        return redirect(url_for('viewFormPackingListDetalle')) #función de la ruta original

#para recibir parametros
@app.route('/deletePackingList/<string:id>')
@login_required
def deletePackingList(id):
    #return 'Delete contact'
    #print(id)
    #return id
    cur = db.connection.cursor()
    cur.execute('DELETE FROM packing_list_detalle WHERE ID_PACKING_LIST = {0}'.format(id) )
    db.connection.commit()

    cur = db.connection.cursor()
    cur.execute('DELETE FROM packing_list WHERE ID = {0}'.format(id) )
    db.connection.commit()


    return redirect(url_for('viewFormPackingList'))


@app.route('/editPackingList/<id>')
@login_required
def editPackingList(id):
    #return 'Edit contact'
    cur = db.connection.cursor()
    cur.execute('SELECT pl.ID, pl.HORA_LLEGADA, pl.INICIO_LLENADO, pl.HORA_SALIDA, pl.NRO_CONTENEDOR, pl.NAVE, mar.DESCRIPCION, emp.DESCRIPCION, emp.ID, mar.ID, pl.FECHA_REGISTRO, pl.NRO_SEMANA, pl.P_LINEA, pl.P_ADUANA  FROM packing_list pl, marca mar, empacadora emp WHERE pl.ID_MARCA = mar.ID AND pl.ID_EMPACADORA = emp.ID and pl.ID = %s', [id])
    data = cur.fetchall()

    formPackingList = FormPackingList()
    print("10 es " , str(data[0][10]))

    if (data[0][10]!=None):
     print("10 dentro del if es " , data[0][10])
     fechaRegistroString = str(data[0][10])
     fechaRegistroTime = datetime.datetime.strptime(fechaRegistroString, '%Y-%m-%d')
     formPackingList.fechaRegistro.data = fechaRegistroTime.date()
    

    horaLlegadaString = str(data[0][1])
    horaLlegadaTime = datetime.datetime.strptime(horaLlegadaString, '%H:%M:%S')

    formPackingList.horaLlegada.data = horaLlegadaTime.time()

    inicioLlenadoString = str(data[0][2])
    print("inicio llenado es",inicioLlenadoString )
    inicioLlenadoTime = datetime.datetime.strptime(inicioLlenadoString, '%H:%M:%S')
    formPackingList.inicioLlenado.data = inicioLlenadoTime.time()
    
    horaSalidaString = str(data[0][3])
    horaSalidaTime = datetime.datetime.strptime(horaSalidaString, '%H:%M:%S')
    formPackingList.horaSalida.data = horaSalidaTime.time()


    formPackingList.nroContenedor.data =data[0][4]
    formPackingList.nroSemana.data =data[0][11]
    formPackingList.nave.data = data[0][5]
    formPackingList.pLinea.data =data[0][12]
    formPackingList.pAduana.data =data[0][13]
    #print ("1 ",  formPackingList.horaLlegada.data )
    #print ("2 ",   formPackingList.inicioLlenado.data )
    return render_template('editPackingList.html', dataPackingList = data[0], form = formPackingList)

@app.route('/verDetallePackingList/<id>')
@login_required
def verDetallePackingList(id):
    #return 'Edit contact'

    session['packingListId'] = id
    valorId=id
    cur = db.connection.cursor()
    
    consulta = 'SELECT pld.ID, pld.FECHA_CORTE, CONCAT(prod.NOMBRES," ", prod.APELLIDOS), pld.NRO_PALLET, pld.NRO_CAJAS, tc.DESCRIPCION FROM packing_list_detalle pld, productores prod, tipo_caja tc WHERE pld.ID_PRODUCTOR = prod.ID AND pld.ID_TIPO_CAJA = tc.ID and pld.ID_PACKING_LIST = "'+str(id)+'" ORDER BY pld.ID desc'

    #print ("select consulta detalle ",  consulta)
    cur.execute(consulta)
     
    dataPackingListDetalle = cur.fetchall()
    formPackingListDetalle = FormPackingListDetalle()

    return render_template('viewFormPackingListDetalle.html',dataPackingListDetalle = dataPackingListDetalle, form = formPackingListDetalle, valorId=valorId)

    # cur = mysql.connection.cursor()
    # cur.execute('SELECT pl.ID, pl.HORA_LLEGADA, pl.INICIO_LLENADO, pl.HORA_LLEGADA, pl.NRO_CONTENEDOR, pl.NAVE, mar.DESCRIPCIONN, emp.DESCRIPCION FROM packing_list pl, marca mar, empacadora emp WHERE pl.ID_MARCA = mar.ID AND pl.ID_EMPACADORA = emp.ID and pl.ID = %s', [id])
    # data = cur.fetchall()
    # # print('data[0] es ', data[0][0])
    # # print('data[todo] es ', data)
    # return render_template('editPackingList.html', dataPackingList = data[0])

@app.route('/updatePackingList/<id>', methods = ['POST'])
@login_required
def updatePackingList(id):
    if request.method == 'POST':
        fechaRegistro = request.form['fechaRegistro']
        horaLlegada = request.form['horaLlegada']
        inicioLlenado = request.form['inicioLlenado']
        horaSalida = request.form['horaSalida']
        nroSemana = request.form['nroSemana']
        nroContenedor = request.form['nroContenedor']
        nave = request.form['nave']
        pLinea = request.form['pLinea']
        pAduana = request.form['pAduana']
        marca = request.form['cmbMarca']
        empacadora = request.form['cmbEmpacadora']

        if(horaLlegada==""): horaLlegada="00:00:00"
        if(inicioLlenado==""): inicioLlenado="00:00:00"
        if(horaSalida==""): horaSalida="00:00:00"


        cur = db.connection.cursor()
        cur.execute("""
        UPDATE packing_list 
        SET FECHA_REGISTRO = %s, HORA_LLEGADA = %s,
            INICIO_LLENADO = %s,
            HORA_SALIDA = %s,
            NRO_SEMANA = %s,
            NRO_CONTENEDOR = %s,
            NAVE = %s,
            P_LINEA = %s,
            P_ADUANA = %s,
            ID_MARCA = %s,
            ID_EMPACADORA = %s
        where id = %s
        """, (fechaRegistro, horaLlegada, inicioLlenado, horaSalida, nroSemana, nroContenedor,nave, pLinea, pAduana,marca,empacadora, id ))
        db.connection.commit()
        flash('Registro de packing list actualizado correctamente')
        return redirect(url_for('viewFormPackingList'))


@app.route('/verReportePackingList/<id>')
@login_required
def verReportePackingList(id):
    #return 'Edit contact'

    extraer_plist.vaciar_tabla()
    extraer_plist.logica(id)

    #extraer_plist.lista_total(id)

    #time.sleep(2)
    #return render_template('http://labsac.com/webgestion/admin/catalogo/evaluacionplagas/formExportarPackingList.htm?id='+id+'')
    return redirect('https://labsac.com/webgestion/admin/catalogo/evaluacionplagas/formExportarPackingList.htm?id='+id+'')

    #return render_template('http://labsac.com/webgestion/admin/catalogo/evaluacionplagas/formExportarPackingList.htm?id=5')

    
    # cur = mysql.connection.cursor()
    # cur.execute('SELECT pl.ID, pl.HORA_LLEGADA, pl.INICIO_LLENADO, pl.HORA_LLEGADA, pl.NRO_CONTENEDOR, pl.NAVE, mar.DESCRIPCIONN, emp.DESCRIPCION FROM packing_list pl, marca mar, empacadora emp WHERE pl.ID_MARCA = mar.ID AND pl.ID_EMPACADORA = emp.ID and pl.ID = %s', [id])
    # data = cur.fetchall()
    # # print('data[0] es ', data[0][0])
    # # print('data[todo] es ', data)
    # return render_template('editPackingList.html', dataPackingList = data[0])



















@app.route('/viewFormPackingListDetalle')
def viewFormPackingListDetalle():
    #valor = 0
    
    #  cur = mysql.connection.cursor()
    #  cur.execute("SELECT pl.ID, pl.HORA_LLEGADA, pl.INICIO_LLENADO, pl.HORA_LLEGADA, pl.NRO_CONTENEDOR, pl.NAVE, mar.DESCRIPCIONN, emp.DESCRIPCION FROM packing_list pl, marca mar, empacadora emp WHERE pl.ID_MARCA = mar.ID AND pl.ID_EMPACADORA = emp.ID ORDER BY pl.ID desc ")
     
    #  data = cur.fetchall()
    packingListId = session['packingListId']

    cur = db.connection.cursor()
    
    consulta = 'SELECT pld.ID, pld.FECHA_CORTE, CONCAT(prod.NOMBRES," ", prod.APELLIDOS), pld.NRO_PALLET, pld.NRO_CAJAS, tc.DESCRIPCION FROM packing_list_detalle pld, productores prod, tipo_caja tc WHERE pld.ID_PRODUCTOR = prod.ID AND pld.ID_TIPO_CAJA = tc.ID and pld.ID_PACKING_LIST = "'+str(packingListId)+'" ORDER BY pld.ID desc'

    print ("select consulta detalle ",  consulta)
    
    cur.execute(consulta)
     
    dataPackingListDetalle = cur.fetchall()
    formPackingListDetalle = FormPackingListDetalle()
    print("antes de primer html")
    return render_template('viewFormPackingListDetalle.html',dataPackingListDetalle = dataPackingListDetalle, form= formPackingListDetalle )


@app.route('/add_packingListDetalle', methods=['POST'])
def add_packingListDetalle():
    if request.method =='POST':
        idPackingList =  session['packingListId']
        print("Id_packing_list:", idPackingList)
        pallet = request.form['cmbPallet']
        fechaCorte = request.form['fechaCorte']
        productor = request.form['cmbProductor']
        print("Id productor:", productor)
        nroCajas = request.form['nroCajas']
        tipoCaja = request.form['cmbTipoCaja']
        
        cur = db.connection.cursor()

        consulta = 'INSERT INTO packing_list_detalle (ID_PACKING_LIST, FECHA_CORTE, ID_PRODUCTOR, NRO_PALLET, NRO_CAJAS, ID_TIPO_CAJA) VALUES ('+str(idPackingList)+', "'+fechaCorte+'", '+productor+', '+pallet+', '+nroCajas+', '+tipoCaja+')'
        #print ("insert consulta",  consulta)
        cur.execute(consulta)
        print("ultimo id insertado packinglist detalle ",db.connection.insert_id())
        session['packingListDetalleId'] = db.connection.insert_id()
    
        db.connection.commit()
        
        flash('Detalle agregado exitosamente') #mensaje a la vista

        #return 'recibido'
        return redirect(url_for('viewFormPackingListDetalleSet', id= session['packingListDetalleId']  )) #función de la ruta original



@app.route('/deletePackingListDetalle/<string:id>')
def deletePackingListDetalle(id):
    #return 'Delete contact'
    #print(id)
    #return id
    cur = db.connection.cursor()
    cur.execute('DELETE FROM packing_list_detalle WHERE ID = {0}'.format(id) )
    db.connection.commit()

    return redirect(url_for('verDetallePackingList',id=session['packingListId']))


@app.route('/editPackingListDetalle/<id>')
def editPackingListDetalle(id):
    #return 'Edit contact'
    cur = db.connection.cursor()
    #cur.execute('SELECT pld.ID, pld.FECHA_CORTE, CONCAT(prod.NOMBRES," ", prod.APELLIDOS), pld.NRO_PALLET, pld.NRO_CAJAS, tc.DESCRIPCION, prod.ID, tc.ID FROM packing_list_detalle pld, productores prod, tipo_caja tc WHERE pld.ID_PRODUCTOR = prod.ID AND pld.ID_TIPO_CAJA = tc.ID and pld.ID = "'+str(id)+'" ORDER BY pld.ID desc')
    cur.execute('SELECT pld.ID, pld.FECHA_CORTE, CONCAT(prod.NOMBRES," ", prod.APELLIDOS), pld.NRO_PALLET, pld.NRO_CAJAS, tc.DESCRIPCION, prod.ID, tc.ID, pld.ID_PACKING_LIST FROM packing_list_detalle pld, productores prod, tipo_caja tc WHERE pld.ID_PRODUCTOR = prod.ID AND pld.ID_TIPO_CAJA = tc.ID and pld.ID = "'+str(id)+'" ORDER BY pld.ID desc')
    data = cur.fetchall()
    # print('data[0] es ', data[0][0])
    # print('data[todo] es ', data)

    formPackingListDetalle = FormPackingListDetalle()

  

    fechaCorteString = str(data[0][1])
    fechaCorteTime = datetime.datetime.strptime(fechaCorteString, '%Y-%m-%d')
    formPackingListDetalle.fechaCorte.data = fechaCorteTime.date()
    
    formPackingListDetalle.nroCajas.data =data[0][4]

    valorId = data[0][8]

    return render_template('editPackingListDetalle.html', dataPackingListDetalle = data[0], form = formPackingListDetalle, valorId=valorId)


@app.route('/updatePackingListDetalle/<id>', methods = ['POST'])
def updatePackingListDetalle(id):
    if request.method == 'POST':

        pallet = request.form['cmbPallet']
        fechaCorte = request.form['fechaCorte']
        productor = request.form['cmbProductor']
        nroCajas = request.form['nroCajas']
        tipoCaja = request.form['cmbTipoCaja']
        print("id:", id)

        cur = db.connection.cursor()
        cur.execute("""
        UPDATE packing_list_detalle 
        SET FECHA_CORTE = %s,
            ID_PRODUCTOR = %s,
            NRO_PALLET = %s,
            NRO_CAJAS = %s,
            ID_TIPO_CAJA = %s
        where id = %s
        """, (fechaCorte, productor, pallet,nroCajas,tipoCaja, id ))
        db.connection.commit()
        flash('Detalle de packing list actualizado correctamente')
        return redirect(url_for('viewFormPackingListDetalleSet', id=id))


@app.route('/viewFormPackingListDetalleSet/<id>')
def viewFormPackingListDetalleSet(id):

    packingListId = session['packingListId']

    cur = db.connection.cursor()
    
    consulta = 'SELECT pld.ID, pld.FECHA_CORTE, CONCAT(prod.NOMBRES," ", prod.APELLIDOS), pld.NRO_PALLET, pld.NRO_CAJAS, tc.DESCRIPCION FROM packing_list_detalle pld, productores prod, tipo_caja tc WHERE pld.ID_PRODUCTOR = prod.ID AND pld.ID_TIPO_CAJA = tc.ID and pld.ID_PACKING_LIST = "'+str(packingListId)+'" ORDER BY pld.ID desc'

    print ("select consulta detalle ",  consulta)
    
    cur.execute(consulta)
     
    dataPackingListDetalle = cur.fetchall()



    cur = db.connection.cursor()
    cur.execute('SELECT pld.ID, pld.FECHA_CORTE, CONCAT(prod.NOMBRES," ", prod.APELLIDOS), pld.NRO_PALLET, pld.NRO_CAJAS, tc.DESCRIPCION, prod.ID, tc.ID FROM packing_list_detalle pld, productores prod, tipo_caja tc WHERE pld.ID_PRODUCTOR = prod.ID AND pld.ID_TIPO_CAJA = tc.ID and pld.ID = "'+str(id)+'" ORDER BY pld.ID desc')
    data = cur.fetchall()
    # print('data[0] es ', data[0][0])
    # print('data[todo] es ', data)

    formPackingListDetalle = FormPackingListDetalle()

  

    fechaCorteString = str(data[0][1])
    fechaCorteTime = datetime.datetime.strptime(fechaCorteString, '%Y-%m-%d')
    formPackingListDetalle.fechaCorte.data = fechaCorteTime.date()
    
    #formPackingListDetalle.nroCajas.data =data[0][4]




    #formPackingListDetalle = FormPackingListDetalle()
    return render_template('viewFormPackingListDetalleSet.html',dataPackingListDetalle = dataPackingListDetalle, dataPackingListDetalle2=data[0], form= formPackingListDetalle )


def status_401(error):
    return redirect(url_for('login'))

def status_404(error):
    return "<h1> Página no encontrada </h1>", 404

if __name__ == '__main__':

    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(port=3000, debug=True)