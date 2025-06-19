# PACMAN

## KNOWN ISSUES

+ [FIXED] Morir con el poder de velocidad a veces hace respawnear con un pacman lento
+ [OPEN] Los powerups aparecen en los nodos del medio, donde pacman no puede pasar
+ [OPEN] A veces no se puede disparar cuando se está en un nodo (Fixed?)
+ [OPEN] Elegir continue despues de una muerte deja un cartel en el medio de todo

## TODO

+ Pacman no deberia tener hasgun, probablemente. GameController dibuja el "armita" y maneja los tiros LISTO excepto el armita
+ Arma: duración a base de timer o con un cartucho? Disparo continuo o con presionar un botón? LISTO (Timer)
+ Matar con arma no suma puntos LISTO
+ Balas persistentes en las paredes (cuando quedan en un nodo final) LISTO

## REMINDER

Volver a poner todos los powerups como spawneables antes de pedir merge!!!!

## Ideas

+ CheckPowerupEvents(), PowerupGroup? Siguiendo la línea de lo ya escrito
+ dt como atributo del ghostsubject



## ACTUAL

+ GhostSubject solo envia cambios de estado. NO ACTUALIZA LOS FANTASMAS (Por ahora???)
+ Fantasmas rapidazos
+ Modificar sprites
