import pygame, sys
from pygame.locals import *
from random import randint

#variables globales
ancho = 900
alto = 480
puntaje = 0
listaEnemigos = []

class NaveSpacial(pygame.sprite.Sprite):
	""""Clase para las Naves"""

	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.ImagenNave = pygame.image.load("imagenes/nave.jpg")
		self.imagenExplocion = pygame.image.load("imagenes/explosion.jpg")

		self.rect = self.ImagenNave.get_rect()
		self.rect.centerx = ancho/2
		self.rect.centery = alto-30

		self.listaDisparo = []
		self.vida = True

		self.velocidad = 5

	def movimiento(self):
		if self.vida == True:
			if self.rect.left <=0:
				self.rect.left = 0

			elif self.rect.right > 900:
				self.rect.right = 900


	def disparar(self, x, y):
		miProyectil = Proyectil(x, y, "imagenes/disparoa.jpg", True)
		self.listaDisparo.append(miProyectil)

	def destruccion(self):
		self.vida = False
		self.velocidad = 0
		self.ImagenNave = self.imagenExplocion


	def dibujar(self, superficie):
		superficie.blit(self.ImagenNave, self.rect)


class Proyectil(pygame.sprite.Sprite):
	def __init__(self, posx, posy, ruta, personaje):
		pygame.sprite.Sprite.__init__(self)

		self.iamgenProyectil = pygame.image.load(ruta)

		self.rect = self.iamgenProyectil.get_rect()

		self.velocidadDisparo = 3

		self.rect.top = posy
		self.rect.left = posx

		self.disparoPersonaje = personaje

	def trayactoria(self):
		if self.disparoPersonaje == True:
			self.rect.top = self.rect.top - self.velocidadDisparo
		else:
			self.rect.top = self.rect.top + self.velocidadDisparo

	def dibujar(self, superficie):
		superficie.blit(self.iamgenProyectil, self.rect)


class Invasor(pygame.sprite.Sprite):
	def __init__(self, posx, posy, distancia, imagenUno, imagenDos):
		pygame.sprite.Sprite.__init__(self)

		self.imagenA = pygame.image.load(imagenUno)
		self.imagenB = pygame.image.load(imagenDos)

		self.listaImagenes = [self.imagenA, self.imagenB]
		self.posImagen = 0

		self.imagenInvasor = self.listaImagenes[self.posImagen]
		self.rect = self.imagenInvasor.get_rect()

		self.listaDisparo = []
		self.velocidadDisparo = 1
		self.velocidad = 3
		self.rect.top = posy
		self.rect.left = posx

		self.rangoDisparo = 1
		self.tiempoCambio = 1

		self.conquista = False

		self.derecha = True
		self.contador = 0
		self.maxdescenso = self.rect.top + 40

		self.limiteDerecha = posx + distancia
		self.limiteIzquierda = posx - distancia

	def dibujar(self, superficie):
		self.imagenInvasor = self.listaImagenes[self.posImagen]
		superficie.blit(self.imagenInvasor, self.rect)

	def comportamiento(self, tiempo):
		if self.conquista == False:
			self.__ataque()
			self.movimientos()
			if self.tiempoCambio == tiempo:
				self.posImagen += 1
				self.tiempoCambio += 1

				if self.posImagen > len(self.listaImagenes)-1:
					self.posImagen = 0
		else:
			listaEnemigos = []

	def movimientos(self):
		if self.contador <3:
			self.__movimientoLateral()
		else:
			self.__descenso()

	def __descenso(self):
		if self.maxdescenso == self.rect.top:
			self.contador = 0
			self.maxdescenso = self.rect.top + 40
		else:
			self.rect.top += 1

	def __movimientoLateral(self):
		if self.derecha == True:
			self.rect.left += self.velocidad
			if self.rect.left > self.limiteDerecha:
				self.derecha = False

				self.contador += 1
		else:
			self.rect.left -= self.velocidad
			if self.rect.left < self.limiteIzquierda:
				self.derecha = True

	def __ataque(self):
		if (randint(0, 100) < self.rangoDisparo):
			self.__disparo()

	def __disparo(self):
		x, y = self.rect.center
		miProyectil = Proyectil(x-7, y+10, "imagenes/disparob.jpg", False)
		self.listaDisparo.append(miProyectil)


def detenerTodo():
	for enemigo in listaEnemigos:
		for disparo in enemigo.listaDisparo:
			enemigo.listaDisparo.remove(disparo)
		listaEnemigos.remove(enemigo)
	#enemigo.conquista = True

def cargarEnemigos():

	posy = -60
	posx = 100
	for x in range(0, 4):
		enemigo = Invasor(posx, posy, 70, "imagenes/MarcianoA.jpg", "imagenes/MarcianoB.jpg")
		listaEnemigos.append(enemigo)
		posx += 200

	posy -= 100
	posx = 100
	for x in range(0, 4):
		enemigo = Invasor(posx, posy, 70, "imagenes/Marciano2A.jpg", "imagenes/Marciano2B.jpg")
		listaEnemigos.append(enemigo)
		posx += 200

	posy -= 100
	posx = 100
	for x in range(0, 4):
		enemigo = Invasor(posx, posy, 70, "imagenes/Marciano3A.jpg", "imagenes/Marciano3B.jpg")
		listaEnemigos.append(enemigo)
		posx += 200

def SpaceInvader():
	global puntaje
	pygame.init()
	ventana = pygame.display.set_mode((ancho, alto))
	pygame.display.set_caption("Space Invader!!!")

	ImagenFondo = pygame.image.load('imagenes/Fondo.jpg')

	jugador = NaveSpacial()

	reloj = pygame.time.Clock()

	velocidadEnemigo = 3

	aumentarVelocidad = False
	enJuego = True
	derecha = False
	izquierda = False


	while True:
		reloj.tick(60)
		jugador.movimiento()

		tiempo = pygame.time.get_ticks()/1000


		if len(listaEnemigos) == 0 and enJuego == True:
			cargarEnemigos()
			velocidadEnemigo += 1
			aumentarVelocidad = True

		if aumentarVelocidad == True:
			for enemigo in listaEnemigos:
				enemigo.velocidad = velocidadEnemigo + 1
				print ("velocidad del enemigo", enemigo.velocidad)
			aumentarVelocidad = False


		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			if enJuego == True:
				if event.type == pygame.KEYDOWN:
					if event.key == K_LEFT:
						izquierda = True
					elif event.key == K_RIGHT:
						derecha = True
					elif event.key == K_SPACE:
						x, y = jugador.rect.center
						jugador.disparar(x-6, y-43)

				#Detener el movimiento al soltar el boton
				elif event.type == pygame.KEYUP:
					if event.key == K_LEFT:
						izquierda = False
					elif event.key == K_RIGHT:
						derecha = False
			#si en juego es False abilita el reinicio
			else:
				detenerTodo()
				if event.type == pygame.KEYDOWN:
					if event.key == K_r:
						detenerTodo()
						iniciar()



		#continuidar el movimiento al mantener el boton precionado
		if derecha == True:
			jugador.rect.right += jugador.velocidad
		elif izquierda == True:
			jugador.rect.left -= jugador.velocidad

		ventana.blit(ImagenFondo, (0,0))

		jugador.dibujar(ventana)

		#desaparecer el proyectil al salir de la ventana
		if len(jugador.listaDisparo)>0:
			for x in jugador.listaDisparo:
				x.dibujar(ventana)
				x.trayactoria()

				if x.rect.top < -10:
					jugador.listaDisparo.remove(x)
				else:
					for enemigo in listaEnemigos:
						if x.rect.colliderect(enemigo.rect):
							puntaje = puntaje + 1
							print (puntaje)
							listaEnemigos.remove(enemigo)
							jugador.listaDisparo.remove(x)

		if len(listaEnemigos) > 0:
			for enemigo in listaEnemigos:
				enemigo.comportamiento(tiempo)
				enemigo.dibujar(ventana)

				if enemigo.rect.colliderect(jugador.rect):
					enJuego = False
					detenerTodo()

				if enemigo.rect.top > 400:
					#print 'Los Invasores aterrisaron!!!'
					#listaEnemigos.remove(enemigo)
					enJuego = False
					detenerTodo()

				if len(enemigo.listaDisparo)>0:
					for x in enemigo.listaDisparo:
						x.dibujar(ventana)
						x.trayactoria()

						if x.rect.colliderect(jugador.rect):
							jugador.destruccion()
							enJuego = False
							detenerTodo()

						if x.rect.top > 500:
							enemigo.listaDisparo.remove(x)
						else:
							for disparo in jugador.listaDisparo:
								if x.rect.colliderect(disparo):
									jugador.listaDisparo.remove(disparo)
									enemigo.listaDisparo.remove(x)
		if enJuego == False:
			izquierda = derecha = False
			miFuenteSystema = pygame.font.SysFont('Arial', 40)
			Texto = miFuenteSystema.render("Fin del Juego!!!", 0, (120,100,40))
			TextoPuntos = miFuenteSystema.render("Puntuacion "+str(puntaje), 0, (200,0,0))
			ventana.blit(Texto, (300,300))
			ventana.blit(TextoPuntos, (310,200))

		pygame.display.update()

def iniciar():
	global puntaje
	puntaje = 0
	SpaceInvader()
iniciar()
