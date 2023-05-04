# Juego-distribuido
Juego distribuido diseñado para 2-6 jugadores en el que cada jugador es un pez de un color determinado y compite por comer el mayor número de algas de su color sin comer las algas de otros colores. 

Dependiendo del orden de conexión los colores a asignar son:

Amarillo
Rosa
Verde claro
Verde azulado
Naranja 
Rojo


La duración de una partida es de 35 segundos aunque también está la opción de cerrar la partida pulsando la tecla “espacio”.

En este repositorio contamos con 2 archivos:
 
sala_peces.py: fichero en el que se coordinan a los jugadores y envía la información actual de la partida a cada player_peces.py
player_peces.py: fichero en el que se recibe la información y almacena las posibles movimientos del jugador. Además, contiene las clases Sprite que sirven para representar los objetos del juego 

Para poner en marcha el juego:
1. Ejecutamos el fichero sala_peces.py junto con el IP del ordenador e indicamos el número total de jugadores que se van a unir a la partida
2. Cada jugador que se quiera unir debe ejecutar el player_peces.py junto con la ip del ordenador que ejecuta el fichero sala_peces.py, y a continuación indicar el numero total de jugadores que se van a unir a la partida
