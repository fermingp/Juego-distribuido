
from multiprocessing.connection import Client

import traceback

import pygame

import sys, os

import time



TMAX = 35

BLACK = (0, 0, 0)

WHITE = (255, 255, 255)



colores=[["amarillo",'pez_amarillo.jpg','alga_amarilla.jpg'],["rosa",'pez_rosa.jpg','alga_rosa.jpg'],["verde claro",'pez_verde_claro.jpg','alga_verde_claro.jpg'],["verde azulado",'pez_verde_azulado.jpg','alga_verde_azulado.jpg'],["naranja",'pez_naranja.jpg','alga_naranja.jpg'],["rojo",'pez_rojo.jpg','alga_roja.jpg']]



X = 0

Y = 1

SIZE = (750, 600) 



FPS = 60





class Pez():

    '''

    Clase Pez: representa cada pez del juego

    

    - index: 0<= index <= npeces - 1 : ID de cada pez

    - pos: posición del pez i

    '''

    def __init__(self, index):        

        self.index = index

        self.pos = [None, None]



    def get_pos(self):

        return self.pos



    def set_pos(self, pos):

        self.pos = pos

        

    def get_index(self):

        return self.index



    def __str__(self):

        return f"P<{self.index, self.pos}>"

    

class Alga():

    '''

    Clase Pez: representa cada alga del juego

    

    - index: 0<= index <= 5*npeces - 1 : ID de cada alga

    - pos: posición de la alga i

    '''

    def __init__(self,index):        

        self.pos= [None, None]

        self.index = index



    def get_pos(self):

        return self.pos



    def set_pos(self, pos):

        self.pos = pos

        

    def get_index(self):

        return self.index



    def __str__(self):

        return f"A<{self.pos}>"

    

class Game():

    '''

    Clase Game

    '''

    def __init__(self,n_peces,gameinfo):

        '''

        Inicializa el juego para un jugador 

        

            -self.peces: lista con los peces del juego

            -self.alga: lista con las algas del juego

            -self.score: lista con los puntos de cada pez del juego

            -self.time: momento en el que se inicia el juego

            -self.running: indica si el juego está en ejecución

        '''

        self.peces = [Pez(i) for i in range(n_peces)]

        self.alga =  [Alga(i) for i in range(5*n_peces)] 

        self.score = [0]*n_peces

        self.time = gameinfo['time']

        self.running = True

    

    '''

    Definimos funciones para poder acceder a los parámetros desde fuera de la clase o 

    resetearlos a un valor específico

    '''

    def get_pez(self, index):

        

        return self.peces[index]



    def set_pos_pez(self, index, pos):

        self.peces[index].set_pos(pos)



    def get_alga(self, i): 

        return self.alga[i]

  

    def set_pos_alga(self,i,pos):

        self.alga[i].set_pos(pos)

  

    def get_score(self):

        return self.score

    def get_time(self):

        return self.time

    def set_time(self,time):

        self.time=time

    def set_score(self, score):

        self.score = score

    #actualizamos el juego;la cantidad de algas obtenidas, asi como la posicion de cada Pez y alga

    def update(self, gameinfo):

        '''

        Función que actualiza la información del juego utilizando las funciones anteriores

        '''

        n_peces = len(self.peces)

        for i  in range (n_peces):

            self.set_pos_pez(i, gameinfo['pos_peces'][i]) 

        for i in range(5*n_peces):

            alga_i = gameinfo['pos_algas'][i]

            self.set_pos_alga(i,alga_i)

        self.set_score(gameinfo['score'])

        

        self.running = gameinfo['is_running']



    def is_running(self):

        return self.running



    def end(self):

        self.running = False



    def __str__(self,n_peces):

      for j in range(n_peces):

        	for i in range(j,5*n_peces,n_peces):

            		return f"G<{self.peces[j]}:{self.alga[i]}>"

                

class pez_Sprite(pygame.sprite.Sprite):

    '''

    Clase pez_Sprite:

        

        Sirve para la representación gráficas de los peces

    '''

    

    def __init__(self,pez):

        super().__init__()

        self.pez = pez

        self.image = pygame.image.load(colores[self.pez.get_index()][1]) #para cargar la imagen

        self.image = pygame.transform.scale(self.image,(90,90)) #para ajustar la imagen a la pantalla

        self.image.set_colorkey(WHITE) #hace transparente el color que le pases de la imagen

        self.rect = self.image.get_rect() 

        self.update()

        

    def update(self):        

        pos = self.pez.get_pos()

        self.rect.centerx, self.rect.centery = pos  

        

   

    def __str__(self):

        return f"P<{self.index}>"



class alga_Sprite(pygame.sprite.Sprite):

    '''

    Clase alga_Sprite:

        

        Sirve para la representación gráficas de las lagas

    '''

    

    def __init__(self, alga,n_peces):

        super().__init__()

        self.alga = alga

        self.image = pygame.image.load(colores[self.alga.get_index()%n_peces][2]) #para cargar la imagen

        self.image = pygame.transform.scale(self.image,(20,60)) #para ajustar la imagen a la pantalla

        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect() 

        self.update()



    def update(self):

        pos = self.alga.get_pos()

        self.rect.centerx, self.rect.centery = pos

        

       

    def __str__(self):

        return f"A<{self.alga.pos}>"

   

class Display():

    '''

    Clase Display

    '''

    

    def __init__(self,game, n_peces):  

        '''

        self.game = objeto de la clase Game que contiene el juego

        self.npeces = número de jugadores que juegan la partida

        self.score = puntuación de cada jugador

        self.time = momento exacto de cuando se ha iniciado el juego

        self.peces_Sp = lista de objetos (un total de npeces) de la clase Pez que representan

                        cada pez de la partida

        self.algas_Sp = lista de objetos (un total de 5*npeces) de la clase Pez que representan

                        cada pez de la partida

        

        Además, variables sprite para poder actualizarlas durante la partida

        

        Por último, representamos gráficamente el fondo del juego

        '''

        self.game = game

        self.n_peces=n_peces

        self.score = game.get_score()

        self.time=game.get_time()

        self.peces_Sp = [pez_Sprite(self.game.get_pez(i)) for i in range(n_peces)]

        self.algas_Sp = [alga_Sprite(self.game.get_alga(i),n_peces) for i in range(5*n_peces)]

        self.all_sprites = pygame.sprite.Group() #para administrar los multiples objetos sprite

        self.pez_group = pygame.sprite.Group()

        self.alga_group = pygame.sprite.Group()

        for pez in self.peces_Sp:

            self.all_sprites.add(pez)

            self.pez_group.add(pez)

        for alga in self.algas_Sp:

            self.all_sprites.add(alga)

            self.alga_group.add(alga)

        self.screen = pygame.display.set_mode(SIZE)

        self.clock =  pygame.time.Clock()  #FPS

        self.time_group=pygame.sprite.Group()

        self.background = pygame.image.load('fondo_marino.jpg')

        self.background = pygame.transform.scale(self.background,(750,625))

        pygame.init()









    def analyze_events(self):

        '''

        Función que anota en una lista el movimiento del jugador según la tecla que presione

        (left, right, up, down) // (quit - en caso de querer abandonar la partida)

        '''

        events = []        

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE: 

                    events.append("quit")

                elif event.key == pygame.K_LEFT:

                    events.append("left")

                elif event.key == pygame.K_RIGHT:

                    events.append("right")

                elif event.key == pygame.K_UP:

                    events.append("up")

                elif event.key == pygame.K_DOWN:

                    events.append("down")

            elif event.type == pygame.QUIT:

                events.append("quit")       

        return events



    def refresh(self):

        '''

        Función que sirve para actualizar los objetos sprite del juego 

        '''

        self.all_sprites.update() 

        self.screen.blit(self.background, (0, 0)) 

        score = self.game.get_score()

        font_title=pygame.font.Font(None,45) 

        font_score=pygame.font.Font(None,30)

        text1 = font_title.render('JUEGO PECES', 1, BLACK, (20,95,38,250))

        self.background.blit(text1, (SIZE[X]-475, 8))

        

        for i in range(self.n_peces):

        	text2 = font_score.render(f"Jugador {colores[i][0]}: {score[i]}", 1, WHITE,(116,87,83,255))

        	self.screen.blit(text2, (SIZE[X]-240, i*30+10))

        self.all_sprites.draw(self.screen)

        pygame.display.flip()

   

    def tick(self):  

        '''

        Función que añade el contador de tiempo a la pantalla de cada jugador

        

        ¿Cómo calculamos el tiempo restante?

            

            Restamos el TMAX, que denota la duración que va durar la partida, 

            menos los segundos transcurridos desde que empieza la partida. 

            

            Este último período de tiempo se puede ver como la diferencia entre 

            el momento actual (time.time()) y el momento de inicio de la partida (self.time)

        '''

        font2 = pygame.font.Font(None,30)

        self.clock.tick(FPS)

        tiempo = int(TMAX - (time.time() - self.time))

        contador = font2.render("TIEMPO: " + str(tiempo),1,WHITE, (116,87,83,255))

        self.screen.blit(contador,(SIZE[X]-710, 10))

        pygame.display.update()



    @staticmethod

    def quit():

        pygame.quit()



def main(ip_address):

    print ('¿Cuántos peces desean comer algas?')

   

    n_peces=int(input())

    port = 6000

    try:

        with Client((ip_address, port), authkey=b'secret password') as conn:

            i,gameinfo = conn.recv()

            game = Game(n_peces,gameinfo)

            print(f"Eres el pez de color {colores[i][0]}")

            game.update(gameinfo)

            display = Display(game, n_peces)

            while game.is_running():

                events = display.analyze_events()

                for ev in events:

                    conn.send(ev)

                    if ev == 'quit':

                        game.end()

                conn.send("next")

                gameinfo = conn.recv()

                game.update(gameinfo)

                display.refresh()

                display.tick()

            gameScore = list(game.get_score())

            for i in range (n_peces):

                if (gameScore[i] == max(gameScore) ):

                        print (f"El GANADOR es el pez de color {colores[i][0]} con {gameScore[i]} puntos" )

                elif (gameScore[i] == min(gameScore) ):

                        print (f"El PERDEDOR es el pez de color {colores[i][0]} con {gameScore[i]} puntos" )

    except:

        traceback.print_exc()

    finally:

        pygame.quit()



if __name__=="__main__":

    ip_address = "127.0.0.1"

    if len(sys.argv)>1:

        ip_address = sys.argv[1]

    main(ip_address)   

