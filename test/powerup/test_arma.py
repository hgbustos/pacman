from powerup import GunPowerUp, Bullet
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

from pacman import Pacman
from unittest.mock import MagicMock, patch
os.environ
import pygame
pygame.mixer.init()
class DummyPacman:
    def __init__(self):
        self.has_gun = False
        self.bullets = []

def test_gun_powerup_activate_and_deactivate():
    pacman = DummyPacman()
    powerup = GunPowerUp(0, 0, duration=1)

    # Activa el power up y verifica que Pacman tiene arma y la lista de balas está vacía
    powerup.activate(pacman)
    assert pacman.has_gun is True, "Pacman debería tener arma al activar el power up"
    assert pacman.bullets == [], "La lista de balas debe estar vacía al activar el power up"

    # Desactiva el power up y verifica que Pacman ya no tiene arma y la lista de balas está vacía
    powerup.deactivate(pacman)
    assert pacman.has_gun is False, "Pacman no debería tener arma al desactivar el power up"
    assert pacman.bullets == [], "La lista de balas debe estar vacía al desactivar el power up"

def test_bullet_update_and_render():
    # Crea una bala y verifica que se mueve correctamente
    bullet = Bullet(0, 0, (1, 0), speed=100)
    pos_inicial = bullet.position.x
    bullet.update(0.5)  # medio segundo
    assert bullet.position.x > pos_inicial, "La bala debe avanzar en x después de actualizar"

   