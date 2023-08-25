from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
app = Flask(__name__)
app.secret_key = '1085897781'


# Configuración de la conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="bd_crodecol",
    user="postgres",
    password="221036066"
)

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/buscarpedido')
def iniciarbusqueda():
    return render_template('BuscarPedido.html')

@app.route('/registrarcl', methods=['GET', 'POST'])
def regitrarcl():
    msg = ''
    if request.method == 'POST':
        if 'registrar' in request.form:
            cedula = request.form['cedula']
            nombres = request.form['nombres']
            genero = request.form['genero']
            correo = request.form['correo']
            telefono = request.form['telefono']
            contraseña = request.form['contraseña']

            # Verificar si la cédula ya existe en la base de datos
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes WHERE cedula = %s", (cedula,))
            existente = cursor.fetchone()

            if existente:
                msg = 'La cédula ya está registrada'
            
            elif existente is None:
                # Guardar los datos en la base de datos
                cursor = conn.cursor()
                cursor.execute("INSERT INTO clientes (cedula, nombres, genero, correo, telefono, contrasena) VALUES (%s, %s, %s, %s, %s, %s)",
                        (cedula, nombres, genero, correo, telefono, contraseña))
                conn.commit()
                cursor.close()
                msg = 'Cliente registrado satisfactoriamente'

        elif 'cancelar' in request.form:
            cedula = ''
            nombres = ''
            genero = ''
            correo = ''
            telefono = ''
            contraseña = ''
    #return render_template('RegistrarUsuario.html', message = msg)
    session['message'] = msg  # Almacena el mensaje en la sesión
    return redirect(url_for('visualizarcl'))

@app.route('/delete/<string:cedula>')
def delete(cedula):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE cedula = %s", (cedula,))
    conn.commit()
    return redirect(url_for('visualizarcl'))

@app.route('/edit/<string:cedula>', methods = ['POST'])
def edit(cedula):
    cedula = request.form['cedula']
    nombres = request.form['nombres']
    genero = request.form['genero']
    correo = request.form['correo']
    telefono = request.form['telefono']
    contraseña = request.form['contraseña']

    cursor = conn.cursor()
    cursor.execute('UPDATE clientes SET nombres = %s, genero = %s, correo = %s, telefono = %s, contrasena = %s WHERE cedula = %s',
                    (nombres, genero, correo, telefono, contraseña, cedula))
    conn.commit()
    return redirect(url_for('visualizarcl'))


@app.route('/registrarped', methods=['GET', 'POST'])
def regitrarped():
    msg = ''
    if request.method == 'POST':
        if 'registrar' in request.form:
            cedula = request.form['cedula']
            nombrepieza = request.form['nombrepieza']
            tipopieza = request.form['tipopieza']
            cantidad = request.form['cantidad']

            # Verificar si la cédula ya existe en la base de datos
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes WHERE cedula = %s", (cedula,))
            existente = cursor.fetchone()

            if existente:
                # Guardar los datos en la base de datos
                cursor = conn.cursor()
                # Obtener el siguiente valor de la secuencia para codigopedido
                cursor.execute("SELECT nextval('pedidos_codpedido_seq')")
                codigopedido = cursor.fetchone()[0]
                cursor.execute("INSERT INTO pedidos (codpedido, cedula, nombrepieza, tipopieza, cantidad) VALUES (%s, %s, %s, %s, %s)",
                                (codigopedido, cedula, nombrepieza, tipopieza, cantidad))
                conn.commit()
                cursor.close()
                msg = f'Pedido {codigopedido} registrado satisfactoriamente'
            
            elif existente is None:
                msg = 'El cliente no esta registrado'
            
        elif 'cancelar' in request.form:
            cedula = ''
            nombrepieza = ''
            tipopieza = ''
            cantidad = ''
        
    #return render_template('RegistrarPedido.html', message = msg)
    session['message'] = msg  # Almacena el mensaje en la sesión
    return redirect(url_for('visualizarped'))

@app.route('/registrarsol', methods=['GET', 'POST'])
def regitrarsol():
    msg = ''
    if request.method == 'POST':
        if 'registrar' in request.form:
            cedula = request.form['cedula']
            titulo = request.form['titulo']
            tiposolicitud = request.form['tiposolicitud']
            fecha = request.form['fecha']
            descripcion = request.form['descripcion']

            # Verificar si la cédula ya existe en la base de datos
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes WHERE cedula = %s", (cedula,))
            existente = cursor.fetchone()

            if existente:
                # Guardar los datos en la base de datos
                cursor = conn.cursor()
                cursor.execute("SELECT nextval('solicitudes_codsolicitud_seq')")
                codsol = cursor.fetchone()[0]
                cursor.execute("INSERT INTO solicitudes (codsolicitud, cedula, titulo, tiposolicitud, fecha, descripcion) VALUES (%s, %s, %s, %s, %s, %s)",
                        (codsol, cedula, titulo, tiposolicitud, fecha, descripcion))
                conn.commit()
                cursor.close()
                msg = f'Solicitud {codsol} registrada satisfactoriamente'
            
            elif existente is None:
                msg = 'El cliente no esta registrado'

        elif 'cancelar' in request.form:
            cedula = ''
            titulo = ''
            tiposolicitud = '' 
            fecha = ''
            descripcion = ''
        
    return render_template('RegistrarSolicitud.html', message = msg)

@app.route('/buscar_cliente', methods=['POST'])
def buscar_cliente():
    cedula_buscar = request.form['cedula']
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clientes WHERE cedula = %s', (cedula_buscar,))
    cliente = cursor.fetchone()
    cursor.close()
    if cliente:
        return render_template('ActualizarUsu.html', cliente=cliente)
    else:
        return render_template('inicio.html', mensaje='Cliente no encontrado')


@app.route('/actualizarcl',  methods=['POST'])
def actualizarcl():
    if request.method == 'POST':
        if 'actualizar' in request.form:
            cedula = request.form['cedula']
            nombres = request.form['nombres']
            genero = request.form['genero']
            correo = request.form['correo']
            telefono = request.form['telefono']
            contrasena = request.form['contrasena']

            cursor = conn.cursor()
            cursor.execute('UPDATE clientes SET nombres = %s, genero = %s, correo = %s, telefono = %s, contrasena = %s WHERE cedula = %s',
                        (nombres, genero, correo, telefono, contrasena, cedula))
            conn.commit()
            cursor.close()

            mensaje = 'Cliente actualizado con éxito'
        elif 'cancelar' in request.form:
            return render_template('inicio.html')
    return render_template('ActualizarUsu.html', cliente=(cedula, nombres, genero, correo, telefono, contrasena), mensaje = mensaje)


@app.route('/buscar_pedido', methods=['POST'])
def buscar_pedido():
    codped_buscar = request.form['codpedido']
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pedidos WHERE codpedido = %s', (codped_buscar,))
    pedido = cursor.fetchone()
    cursor.close()
    if pedido:
        return render_template('ActualizarPedido.html', pedido=pedido)
    else:
        return render_template('BuscarPedido.html', mensaje='Pedido no encontrado')

@app.route('/actualizarped', methods=['POST'])
def actualizarped():
    if request.method == 'POST':
        if 'actualizar' in request.form:
            codpedido = request.form['codpedido']
            cedula = request.form['cedula']
            nombrepieza = request.form['nombrepieza']
            tipopieza = request.form['tipopieza']
            cantidad = request.form['cantidad']

            cursor = conn.cursor()
            cursor.execute('UPDATE pedidos SET cedula = %s, nombrepieza = %s, tipopieza = %s, cantidad = %s WHERE codpedido = %s',
                        (cedula, nombrepieza, tipopieza, cantidad, codpedido))
            conn.commit()
            cursor.close()

            mensaje = 'Pedido actualizado con éxito'
        elif 'cancelar' in request.form:
            return render_template('BuscarPedido.html')
    return render_template('ActualizarPedido.html', pedido=(codpedido, cedula, nombrepieza, tipopieza, cantidad), mensaje = mensaje)


@app.route('/resolversol')
def resolversol():
    cursor = conn.cursor()
    cursor.execute(" select codsolicitud, solicitudes.cedula, nombres, titulo, tiposolicitud, fecha, descripcion from solicitudes inner join clientes on solicitudes.cedula = clientes.cedula;")
    myresult = cursor.fetchall()
    #convertir los datos a diccionario
    insertObject = []
    ColumnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(ColumnNames, record)))
    cursor.close()
    return render_template('ResolverSolicitud.html', data = insertObject)

@app.route('/buscar_solicitud', methods=['POST'])
def buscar_solicitud():
    sol_buscar = request.form['codsolicitud']
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM solicitudes WHERE codsolicitud = %s', (sol_buscar,))
    solicitud = cursor.fetchone()
    cursor.close()
    if solicitud:
        return render_template('Respondersol.html', solicitud=solicitud)
    else:
        return render_template('ResolverSolicitud.html', mensaje='Solicitud no encontrada')

@app.route('/visualizarcl')
def visualizarcl():
    message = session.pop('message', None)  # Recupera y elimina el mensaje de la sesión
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    myresult = cursor.fetchall()
    #convertir los datos a diccionario
    insertObject = []
    ColumnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(ColumnNames, record)))
    cursor.close()
    return render_template('RegistrarUsuario.html', data = insertObject, message=message)

@app.route('/visualizarped')
def visualizarped():
    message = session.pop('message', None)  # Recupera y elimina el mensaje de la sesión
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedidos")
    myresult = cursor.fetchall()
    #convertir los datos a diccionario
    insertObject = []
    ColumnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(ColumnNames, record)))
    cursor.close()
    return render_template('RegistrarPedido.html', data = insertObject, message=message)

if __name__=='__main__':
    app.run(debug=True)