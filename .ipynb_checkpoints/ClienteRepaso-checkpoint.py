import threading #Libreria threading, para poner matipular los hilos
import sys #Libreria de sistema, para la interaccion con el interprete (poder hablar con el sistema)
import socket #Libreria socket, para poder enlazarnos cliente-servidoer
import pickle #Libreria pickle para la encriptacion del codigo
import os #Libreria del sistema operativo, para el uso de funciones dependiente del sistema operativo.

class Cliente():
    #Constructor principal
	def __init__(self, host=input("Introduzca la IP del servidor? "), port=int(input("Introduzca el puerto del servidor? ")),user=""): #Los parametros del constructor princial Host(ip), port(puerto) y user(usuario).
		self.s = socket.socket() #inicializar la variable para poder utilizar las funciones de la libreria socket
		while(user==""): #Bucle while para pedir el usuario hasta que le pases uno no vacio.
			user=input("Nombre del usuario: ") #pide por teclado que le pases un usuario
		self.username = ("@" + user) #inicializa y guarda el usuario que le has pasado
		self.s.connect((host, int(port))) #Le pasas la ip y el puerto en la que esta instanciado el servidor
		print('\n\tProceso con PID = ',os.getpid(), '\n\tHilo PRINCIPAL con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tTotal Hilos activos en este punto del programa =', threading.active_count()) #Te pasa proceso actual, como el hilo encargado de tu chat y lo hace demonio, los hilos activos para todo esto.
		threading.Thread(target=self.recibir, daemon=True).start() #Instancia el hilo del chat

		while True: #Bucle para salir del programa
			msg = input('\nEscriba texto ?   ** Enviar = ENTER   ** Salir Chat = 0 \n') #muestra por pantalla la forma de salir de el, para que sepas que caracter clave es.
			if msg != '0' : self.enviar(msg) #Si no es el caracter clave para salir lo manda a la funcion enviar para mandarlo al servidor y lo transmita a los demas chat.
			else: #si es =0
				print(" **** Me piro vampiro; cierro socket y mato al CLIENTE con PID = ", os.getpid()) #te dice que termina el proceso y cierra el programa
				self.s.close() #Cierra el socket
				sys.exit() #Sale del programa y cierra interracion del programa por terminal.

	def recibir(self): #Metodo que recibe los mensajes que manda el servidor
		print('\nHilo RECIBIR con ID =',threading.currentThread().getName(), '\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count()) #imprime que hilos estas utilizando y que id y proceso de cual esta encargado. 
		while True: #Bucle que esta siempre activo para recibir mensajes
			try: #Try except, para que no se pare el programa si llega haber un error o error fatal.
				data = self.s.recv(1024) #Guardamos en una variable el mensaje cifrado y se desifra, mediante la otra variable que esta ligada con la libreria socket (self.s.recv(1024)), ademas de la cantidad de bits que puede tener el mensaje 
				if data: print(pickle.loads(data)) #Condicional para data que imprima el mensaje por pantalla
			except: pass

	def enviar(self, msg): #Metodo enviar, para mandar los mensaje al servidor los pase a los demas usuarios.
		self.s.send(pickle.dumps(msg)) #Serializar, mediante la libreria pickle y mandarlo mediante el enlaze del socket (self.s.send)

arrancar = Cliente() #Ejecuta el programa.