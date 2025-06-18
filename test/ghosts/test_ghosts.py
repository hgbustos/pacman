import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from ghosts import Ghost, Blinky, Pinky, Inky, Clyde, GhostGroup
from constants import SPAWN, FREIGHT
from unittest.mock import MagicMock, patch
import pytest

class DummyNode:
    def __init__(self):
        self.position = MagicMock()
        self.position.x = 0
        self.position.y = 0
    def denyAccess(self, direction, ghost):
        pass

class DummyPacman:
    def __init__(self):
        self.position = MagicMock()
        self.direction = 0
        self.directions = {0: MagicMock()}

@pytest.fixture
@patch("pygame.transform.scale", return_value=MagicMock())
@patch("pygame.image.load", return_value=MagicMock())
def ghost(mock_load, mock_scale):
    node = DummyNode()
    pacman = DummyPacman()
    g = Ghost(node, pacman)
    g.mode = MagicMock()
    g.setSpeed = MagicMock()
    g.spawnNode = node
    g.directionMethod = MagicMock()
    return g

def test_startSpawn_sets_spawn_mode_and_speed(ghost):
    ghost.mode.current = SPAWN
    ghost.spawn = MagicMock()
    ghost.startSpawn()
    ghost.setSpeed.assert_called_with(150)
    assert ghost.directionMethod == ghost.goalDirection
    ghost.spawn.assert_called_once()

def test_startSpawn_does_nothing_if_not_spawn_mode(ghost):
    ghost.mode.current = None
    ghost.spawn = MagicMock()
    ghost.startSpawn()
    ghost.setSpeed.assert_not_called()
    ghost.spawn.assert_not_called()

def test_startFreight_sets_freight_mode_and_speed(ghost):
    ghost.mode.current = FREIGHT
    ghost.randomDirection = MagicMock()
    ghost.startFreight()
    ghost.setSpeed.assert_called_with(50)
    assert ghost.directionMethod == ghost.randomDirection

def test_startFreight_does_nothing_if_not_freight_mode(ghost):
    ghost.mode.current = None
    ghost.randomDirection = MagicMock()
    ghost.startFreight()
    ghost.setSpeed.assert_not_called()
    assert ghost.directionMethod != ghost.randomDirection

@patch("pygame.transform.scale", return_value=MagicMock())
@patch("pygame.image.load", return_value=MagicMock())
def test_ghostgroup_startSpawn_and_startFreight(mock_load, mock_scale):
    node = DummyNode()
    pacman = DummyPacman()
    group = GhostGroup(node, pacman)
    for ghost in group:
        ghost.startSpawn = MagicMock()
        ghost.startFreight = MagicMock()
    # Test startFreight
    group.startFreight()
    for ghost in group:
        ghost.startFreight.assert_called_once()
        assert ghost.points == 200