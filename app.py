from flask import Flask, render_template, redirect, request, session, url_for
from flask_pymongo import PyMongo
import os


########## CONFIGURACION FLASK ###########
app = Flask(__name__)
app.secret_key = str(os.system('openssl rand -base64 24'))

#########################################

########### CONFIGURACION MONGO ##########

app.config['MONGO_DBNAME'] = 'myDatabase'
mongo_ip = '192.168.43.44'
port = '27017'
app.config['MONGO_URI'] = 'mongodb://'+mongo_ip+':'+port+'/'+app.config['MONGO_DBNAME']
mongo = PyMongo(app)

##########################################

########### FUNCIONES #############

def validacion(usuario,psw):
	try:
		valor=mongo.db.authenticate(usuario,psw)
	except:
		valor=False			
	return valor

###################################



@app.route("/" ,methods=["GET"])
def index():
	usuario = request.form.get("usuario")
	psw = request.form.get("psw")
	return render_template("index.html",usuario=usuario,psw=psw)
	
@app.route("/" ,methods=["GET"])
def loginerror():
	usuario = request.form.get("usuario")
	psw = request.form.get("psw")
	return render_template("loginerror.html",usuario=usuario,psw=psw)

@app.route("/login" ,methods=["POST"])
def login():
	usuario = request.form.get("usuario")
	psw = request.form.get("psw")
	valor = validacion(usuario,psw)
	if valor:
		session["usuario"]= usuario
		session["psw"]=psw
		return redirect("/bd")
	else:
		return render_template("loginerror.html")

@app.route("/bd")
def bd():
	usuario=(session["usuario"])
	colecciones= mongo.db.collection_names()
	return render_template("login.html",colecciones=colecciones)

@app.route("/bd/<col>")
def colecciones(col):

	listacol=list(mongo.db[col].find())
	return render_template("colecciones.html",listacol=listacol)




if __name__ == '__main__':
    app.run(host='0.0.0.0')
