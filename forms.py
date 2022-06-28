from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField, StringField
from wtforms.validators import Required, DataRequired, Email, Length, NumberRange
from wtforms.fields.html5 import DateField, TimeField


class FormPackingList(FlaskForm):

    fechaRegistro = DateField('Fecha de registro', format='%Y-%m-%d', validators=(DataRequired(),))
    horaLlegada = TimeField('Hora de llegada')
    #inicioLlenado = DateField('Inicio de Llenado', format='%Y-%m-%d', validators=(DataRequired(),))
    inicioLlenado = TimeField('Inicio de llenado')
    
    horaSalida = TimeField('Hora de Salida')
    nroSemana = StringField("Número de semana", validators=[DataRequired(message="el campo es obligatorio")])
    nroContenedor = StringField("Número de contenedor")
    pLinea = StringField("P. Línea")
    pAduana = StringField("P. Aduana")
    nave = StringField("Nave")


    # fecha = DateField('Fecha', format='%Y-%m-%d', validators=(DataRequired(),))

    # nombre = StringField("Nombre", validators=[
    #     DataRequired(message="el campo es obligatorio"),
    #     Length(max=10, min=3,message="El texto debe estar entre 10 y 3")       
    #     ])
    
    # correo = StringField("E-mail", validators=[
    #     DataRequired(),
    #     Email()
    # ])
    
    # telefono = StringField("Teléfono", validators=[
    #     DataRequired(),
    #     Length(max=10, min=3)       
    #     ])

    submit = SubmitField('Guardar nuevo registro')
    # num1 = IntegerField("Número1", validators=[Required("Tienes que introducir el dato")])
    # num2 = IntegerField("Número2", validators=[Required("Tienes que introducir el dato")])
    # operador = SelectField("Operador", choices=[("+", "Sumar"), ("-", "Resta"),  ("*", "Multiplicar"), ("/", "Dividir")])
    # submit = SubmitField('Submit')


class FormPackingListDetalle(FlaskForm):
    fechaCorte = DateField('Fecha de corte', format='%Y-%m-%d', validators=(DataRequired(),))
    nroCajas = IntegerField("Número de cajas", validators=[DataRequired("Tienes que introducir el dato")])
    submit = SubmitField('Guardar este detalle')