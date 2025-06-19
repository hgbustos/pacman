import pytest
from powerup import LaserPowerUp
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from pacman import Pacman
from unittest.mock import MagicMock, patch
os.environ
import pygame
pygame.mixer.init()


class DummyPacman:
    def __init__(self):
        self.has_laser = False

def test_laser_powerup_activate_and_deactivate():
    pacman = DummyPacman()
    powerup = LaserPowerUp(0, 0, duration=1)

    # Activa el power up y verifica que Pacman tiene láser
    powerup.activate(pacman)
    assert pacman.has_laser is True, "Pacman debería tener láser al activar el power up"

    # Desactiva el power up y verifica que Pacman ya no tiene láser
    powerup.deactivate(pacman)
    assert pacman.has_laser is False, "Pacman no debería tener láser al desactivar el power up"


def test_laser_powerup_auto_deactivate():
    pacman = DummyPacman()
    powerup = LaserPowerUp(0, 0, duration=0.5)
    powerup.activate(pacman)
    powerup.update(pacman, dt=1.0)  # Simula el paso del tiempo
    assert powerup.active is False, "El power up debe estar inactivo tras finalizar la duración"
    assert pacman.has_laser is False, "Pacman no debe tener láser tras finalizar la duración"


#para probar que no se puede activar dos veces el powerup
# y que se desactiva correctamente
def test_laser_powerup_multiple_activate():
    pacman = DummyPacman()
    powerup = LaserPowerUp(0, 0, duration=1)
    powerup.activate(pacman)
    powerup.activate(pacman)  # Llamada doble
    assert pacman.has_laser is True
    powerup.deactivate(pacman)
    assert pacman.has_laser is False