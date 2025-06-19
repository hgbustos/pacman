import pytest
from powerup import SpeedBoostPowerUp
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from pacman import Pacman
from unittest.mock import MagicMock, patch
velocidadprueba = 5.0
os.environ
import pygame
pygame.mixer.init()
class DummyPacman:
    
    def __init__(self):
        self.speed = velocidadprueba

def test_speed_boost_activate_and_deactivate():
    pacman = DummyPacman()
    powerup = SpeedBoostPowerUp(0, 0, duration=1)

    # Activa el power up y verifica que la velocidad aumente
    powerup.activate(pacman)
    assert pacman.speed > velocidadprueba, "La velocidad de Pacman debería aumentar al activar el power up"

    # Desactiva el power up y verifica que la velocidad vuelva a la normalidad
    powerup.deactivate(pacman)
    assert pacman.speed == velocidadprueba, "La velocidad de Pacman debería volver a la normalidad al desactivar el power up"

def test_speed_boost_auto_deactivate():
    class DummyPacman:
        def __init__(self):
            self.speed = 1.0

    pacman = DummyPacman()
    powerup = SpeedBoostPowerUp(0, 0, duration=0.5)
    powerup.activate(pacman)
    powerup.update(pacman, dt=1.0)  # Simula el paso del tiempo
    assert powerup.active is False, "El power up debe estar inactivo tras finalizar la duración"
    assert pacman.speed == 1.0, "La velocidad debe volver a la normalidad tras finalizar la duración"
# #para probar que el powerup sigue activo si no se ha cumplido la duracion
def test_speed_boost_update_still_active():
    class DummyPacman:
        def __init__(self):
            self.speed = 1.0

    pacman = DummyPacman()
    powerup = SpeedBoostPowerUp(0, 0, duration=2.0)
    powerup.activate(pacman)
    powerup.update(pacman, dt=1.0)
    assert powerup.active is True, "El power up debe seguir activo si no terminó la duración"
    assert pacman.speed > 1.0, "La velocidad debe seguir aumentada mientras el power up está activo"
#activacion de powerup dos veces
def test_speed_boost_multiple_activate():
    class DummyPacman:
        def __init__(self):
            self.speed = 1.0

    pacman = DummyPacman()
    powerup = SpeedBoostPowerUp(0, 0, duration=1)
    powerup.activate(pacman)
    powerup.activate(pacman)  # Llamada doble
    # Ahora la velocidad será 4.0 (1.0 * 2 * 2)
    assert pacman.speed == 4.0
    powerup.deactivate(pacman)
    # Ahora la velocidad será 2.0 (4.0 / 2)
    assert pacman.speed == 2.0