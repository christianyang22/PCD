import threading #Libreria threading, para poner matipular los hilos
import sys #Libreria de sistema, para la interaccion con el interprete (poder hablar con el sistema)
import socket #Libreria socket, para poder enlazarnos cliente-servidoer
import pickle #Libreria pickle para la encriptacion del codigo
import os #Libreria del sistema operativo, para el uso de funciones dependiente del sistema operativo.

class Servidor():
    # Constructor principal.
	def __init__(self, host=socket.gethostname(), port=int(input("Que puerto quiere usar ? "))): #Parametros del constructor host(ip), port(puerto).
		self.clientes = [] #Array para guardar el puerto por el que ha ingresado.
		print('\nSu IP actual es : ',socket.gethostbyname(host)) #Imprime por pantalla para que semas cual es tu ip.
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(), '\n\tTotal Hilos activos en este punto del programa =', threading.active_count()) #Te pasa proceso actual, como el hilo encargado de tu chat y lo hace demonio, los hilos activos para todo esto.
		self.s = socket.socket() #inicializar la variable para poder utilizar las funciones de la libreria socket
		self.s.bind((str(host), int(port))) #Enlaza el socket al address, tiene que estar libre el socket, si no no podra enlazarse y encender el servidor.
		self.s.listen(30) #Decirle al socket cuantos usuarios podran solicitarse conectar al servidor.
		self.s.setblocking(False) #Para que que el socket sea no bloqueante, para que no se bloque durante la ejecucion del programa.

		threading.Thread(target=self.aceptarC, daemon=True).start() #Hace que este hilo sea un hilo demonio mientras se ejecute el programa.
		threading.Thread(target=self.procesarC, daemon=True).start() #Hace que este hilo sea un hilo demonio mientras se ejecute el programa.

		while True: #Bucle para salir del programa
			msg = input('\n << SALIR = 0 >> \n') #Te dice por pantalla como cerrar el servidor.
			if msg == '0': #El mensaje recibido es igual a "0", entra.
				print(" **** Me piro vampiro; cierro socket y mato SERVER con PID = ", os.getpid()) #Imprime que se cerrara el server y el proceso que se termina
				with open("u22133089AI1UserList.txt", "w") as f: #Resetea la lista de usuario activos en blanco.
					f.write(" ") #Guarda un archivo en blanco.
				self.s.close() #Cierra el socket.
				sys.exit() #Cierra el interprete
			else: pass #Si no es un 0 pasa del tema y sigue el programa activo.

	def aceptarC(self): #Metodo que acepta el enlace entre cliente-servidor.
		print('\nHilo ACEPTAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count()) #imprime que hilos estas utilizando y que id y proceso de cual esta encargado. 
		while True: #Bucle que se mantiene siempre activo
			try: #Try except, para posibles errores y no se detenga el programa.
				conn, addr = self.s.accept() #Acepta el enlace entre cliente-servidor.
				print(f"\nConexion aceptada via {addr}\n") #Imprime el puerto por el que se ha conectado.
				conn.setblocking(False) #Desactivamos el bloqueo, para que no se bloquee mientras este en ejecucion..
				self.clientes.append(conn) #Guardamos el puerto en la pila, para saber cual es el de cada cliente, al momento de mandar los mensajes a cada uno.
				self.imprimirUsuarios()  #Leemos los usuarios que van entrando para enseñarlos por pantalla
			except: pass #Si llega suceder o saltar algun error, ignorarlo sin terminar el problema

	def imprimirUsuarios(self): #Metodo que imprime por pantalla todos los usuarios activos.
		with open("u22133089AI1UserList.txt", "r") as f: #Una lista de los usuarios en txt, que mantiene los usuarios activos que hay en el chatroom
			print("Clientes conectados ahora [\n" + f.read() + "]") #Imprime por pantalla todos los usuarios.

	def procesarC(self): #Metodo que procesa el mensaje mandado, para deserealizar/descencriptarlo, prepararlo mandar a todos los usuarios menos al que envio el mensaje.
		print('\nHilo PROCESAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count()) #imprime que hilos estas utilizando y que id y proceso de cual esta encargado. 
		while True: #Bucle que se mantiene siempre activo
			if len(self.clientes) > 0: #Tiene que haber al menos 2 usuarios para poder recibir informacion.
				for c in self.clientes: #Pasamo la lista de usuarios como el for va valer siempre al menos 1, aunque se repetira el total de usuarios esten conectados.
					try: #Try except, para posibles errores y no se detenga el programa.
						data = c.recv(1024) #Deserealizar/descencriptar el mensaje, para llamar al metodo broadcaste()
						if data: self.broadcast(data,c) #Llamo al broadcast tantas veces como usuarios haya menos 1, para mandarle la informacion a todos ellos.
					except: pass #Si llega suceder o saltar algun error, ignorarlo sin terminar el problema

	def broadcast(self, msg, cliente): #Metodo que se encarga de mandar el mensaje a cada usuario.
		aux=0 #Variable que utilizaremos para que no imprima tantas veces como usuarios -1 haya.
		for c in self.clientes: #Un bucle que le pasa los puertos y se repite tantos usuarios haya.
			try: #Try except, para posibles errores y no se detenga el programa.
				if c != cliente: #Condicional solo deja pasar, si c es diferente al usuario(cliente) que mando el mensaje.
					if aux==0: #Condicional, para que no imprima cuantos conectados hay y imprimir el mismo mensaje del servidor como tantos usuarios-1 haya.
						print("\nClientes conectados Right now = ", len(self.clientes)) #Te dice el numero de usuarios conectados.
						self.imprimirUsuarios() #Te dice el nombre de los usarios conectados.
						print(pickle.loads(msg)) #Serializa/encripta el mensaje.
						aux=1 #Al valer 1 el auxiliar, hace que no entre al condicional solo 1 vez.
					c.send(msg) #Manda el mensaje a todos los usuarios que no sea el que lo haya enviado.
			except: self.clientes.remove(c) #Si el usuario no esta lo desapila de la lista, para mantener solo los activos.

arrancar = Servidor() #Variable que se encarga de correr la clase servidor.