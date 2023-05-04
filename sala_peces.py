from multiprocessing.connection import Listener

from multiprocessing import Process, Manager, Value, Lock

import traceback

import sys

import random

import time


TMAX = 35

SIZE = (725, 600)



X=0

Y=1



STEP = 20



class Pez():

    

    """

    Clase Pez:

        - index: 0<= index <= n_peces - 1 : ID de cada pez

        - pos: posición del pez i, inicializado en posición aleatoria sobre el eje X

    """

    

    def __init__(self, index):

        self.pos =[random.randint(0,SIZE[X]),SIZE[Y] - 40] 

        self.index = index 

        

    def get_pos(self):

        return self.pos

    

    def get_index(self):

        return self.index

    

    """

    Definimos los movimientos para que los peces no se salgan de la pantalla.

    Los movimientos posibles son izquierda, derecha, arriba y abajo

    """

    def moveLeft_M(self):

        self.pos[X] -= STEP

        if self.pos[X] < 0:

            self.pos[X] = 0 

     

    def moveRight_M(self):

        self.pos[X] += STEP

        if self.pos[X] > SIZE[X]:

                self.pos[X] = SIZE[X] 

                

    def moveDown(self):

        self.pos[Y] += STEP

        if self.pos[Y] > SIZE[Y]:

            self.pos[Y] = SIZE[Y]



    def moveUp(self):

        self.pos[Y] -= STEP

        if self.pos[Y] < 0:

            self.pos[Y] = 0

         

    def __str__(self):

        return str(self.pos)

    



class Alga():

    """

    Clase Alga

    

    - index: 0<= index <= 5*n_peces - 1 : ID de cada alga

    - pos: posición de la alga i, inicializada aleatoriamente en la parte superior de la pantalla

    - velocity: velocidad de la alga. La velocidad sobre el eje X es 0 y sobre el Y se inicializa

                con un número aleatoria entre 1 y 3. La razón de esto es porque las algas van

                cayendo verticalmente.

    """

    

    def __init__(self,index):

                    

        self.x = random.randint(1,749)

        self.y = 0

            

        self.pos = [self.x , self.y]

        self.vel_y = random.randint(1,3)  

        self.velocity = [0, self.vel_y] 

    

    def get_pos(self):

        return self.pos         

    

    """

    Con la función update se actualiza la posición de las algas. Si un alga llega al suelo vuelve a

    aparecer en la parte superior de la pantalla y ahora caerá con más velocidad. Esto último se 

    debe a la condición   self.vel_y += random.randint(0,1)   de la función restart

    """

    def update(self):            

        self.pos[X] = self.pos[X] 

        self.pos[Y] += self.velocity[Y] 

        if self.pos[Y]>SIZE[Y]:

           self.restart() 

           

    def restart(self):

        self.pos=[random. randint(0, SIZE[X]),0 ]

        self.vel_y += random.randint(0,1)

        self.velocity = [0, self.vel_y]

        

    """

    En el archivo player_peces.py hemos ajustado las imágenes de los peces con tamaño (90,90). Por

    tanto consideramos que un pez come un alga si la distancia de las coordenadas X de pez y alga 

    distan menos de 45 (90/2) y lo mismo con la coordenada Y.

    """

    def come_alga(self,pez):

        dist_x= abs(self.pos[0]-pez.get_pos()[0])

        dist_y=abs(self.pos[1]-pez.get_pos()[1])

        radio_pez=90/2

        if(dist_x < radio_pez and dist_y < radio_pez):

            return True 



    def __str__(self):

        return f"A<{self.pos}>"





class Game():

    

    def __init__(self, manager,n_peces):

        """

        Inicializa el juego  

        

            -self.peces: lista con los peces del juego

            -self.algas: lista con las algas del juego

            -self.score: lista con los puntos de cada pez del juego

            -self.time: momento en el que se inicia el juego

            -self.running: indica si el juego está en ejecución

            

        Empleamos listas de tipo manager y value pues trabajamos con objetos compartidos.

        Hacemos uso de dos semáforos de tipo Lock para garantizar la exclusión mutua.

        """

        self.peces= manager.list( [Pez(i) for i in range(n_peces)]  )

        self.algas = manager.list( [Alga(i) for i in range(5*n_peces)] )

        self.score = manager.list([0]*n_peces)

        self.time = time.time()

        self.running = Value('i', 1) # 1 running

        self.lock = Lock()

        self.mutex = Lock()



    def get_Pez(self, index):

        return self.peces[index]



    def get_alga(self,index):

        return self.algas[index]

    

    def get_score(self):

        return list(self.score)



    def is_running(self):

        return self.running.value == 1



    def stop(self):

        if time.time() - self.time > TMAX:

            self.running.value = 0

 

    def end(self):

        self.running.value = 0

        

    def moveLeft(self, index):

        self.mutex.acquire()

        p = self.peces[index]        

        p.moveLeft_M()

        self.peces[index] = p

        self.mutex.release()

        

    def moveRight(self, index):

        self.mutex.acquire()

        p = self.peces[index]        

        p.moveRight_M()

        self.peces[index] = p

        self.mutex.release()

        

    def moveUp(self, index):

        self.mutex.acquire()

        p = self.peces[index]

        p.moveUp()

        self.peces[index] = p

        self.mutex.release()



    def moveDown(self, index):

        self.mutex.acquire()

        p = self.peces[index]

        p.moveDown()

        self.peces[index] = p

        self.mutex.release()

        

    """

    La función get_info devuelve un diccionario con los valores:

        - Lista con las posiciones de cada pez

        - Lista con las posiciones de las algas

        - Lista con la puntuación de cada pez

        - Booleano que indica si el juego está en ejecución
        
        - Tiempo de comienzo del juego

    """

    def get_info(self):

        pos_alga= []

        n_peces=len(self.peces)

        for i in range(5*n_peces):

             pos_alga.append(self.algas[i].get_pos())

        info = {

            'pos_peces': [Pez.get_pos() for Pez in self.peces],

            'pos_algas': pos_alga,

            'score': list(self.score),

            'is_running': self.running.value == 1,

            'time' : self.time

        }

        return info

   

    """

    La siguiente función actualiza cada alga en la lista de algas tras el movimiento de estas.

    Además actualiza la lista de puntuaciones. Si un pez come un alga de su color se le suma un 

    punto pero si come un alga de otro color se le resta un punto. Para ello vemos si los índices

    de pez y el índice del alga módulo n_peces coinciden.

    """

    def move_alga(self):

        self.lock.acquire()

        n_peces=len(self.peces)

        for i in range(5*n_peces):

            alga = self.algas[i]

            for j in range(n_peces):

            	if(alga.come_alga(self.peces[j]) and (i%n_peces)==j): #funcion que contabiliza la puntuacion de cada Pez

            		alga.restart()

            		self.score[j]+=1

            		break

            	elif(alga.come_alga(self.peces[j]) and (i%n_peces)!=j): #funcion que contabiliza la puntuacion de cada Pez

            		alga.restart()

            		self.score[j]-=1

            		break

            alga.update()

            self.algas[i]=alga

        self.lock.release()

        

    def __str__(self):

        return f"{self.get_info()}"







def player(index, conn, game):

    try:

        print(f"{game.get_info()}")

        conn.send( (index, game.get_info()) )

        while game.is_running():

            command = ""

            while command != "next":

                command = conn.recv()                

                if command == "left":

                    game.moveLeft(index)

                elif command == "right":

                    game.moveRight(index) 

                elif command == "up":

                    game.moveUp(index)

                elif command == "down":

                    game.moveDown(index)



                elif command == "quit":

                    game.end()

                               

            if index == 0:

                game.move_alga()

                if game.stop():

                    return f"GAME OVER"

            conn.send(game.get_info())

    except:

        traceback.print_exc()

        conn.close()

    finally:

        print(f"Game ended {game}")



def main(ip_address):

    manager = Manager()

    print ('¿Cuántos peces desean comer algas?')

    n_peces = int(input()) #en primer lugar hay que seleccionar el número de peces que van a jugar

    port = 6000

    try:

        with Listener((ip_address, port),

                      authkey=b'secret password') as listener:

            n_player = 0

            players = [None]*n_peces

            game = Game(manager,n_peces)

            while True:

                print(f"accepting connection {n_player}")

                conn = listener.accept()

                players[n_player] = Process(target=player,

                                            args=(n_player, conn, game))

                n_player += 1

                #cuando se han conectado el número de jugadores indicado se incializan los procesos

                if n_player == n_peces: 

                    for i in range(n_peces):

                        players[i].start()

                    game = Game(manager,n_peces)

    except Exception as e:

        traceback.print_exc()



if __name__=='__main__':

    ip_address = "127.0.0.1"

    if len(sys.argv)>1:

        ip_address = sys.argv[1]

    main(ip_address)

