import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from pacman import Pacman
from unittest.mock import MagicMock, patch

def get_surface_mock():
    surface = MagicMock()
    surface.convert.return_value = surface
    surface.get_at.return_value = (0, 0, 0, 0)
    surface.set_colorkey.return_value = None
    surface.get_width.return_value = 32
    surface.get_height.return_value = 32
    return surface

class TestcollideGhost:
    @patch("pygame.transform.scale", return_value=get_surface_mock())
    @patch("pygame.image.load", return_value=get_surface_mock())
    def test_collide_ghost_true(self, mock_load, mock_scale):
        mock_node = MagicMock()
        pacman = Pacman(mock_node)
        ghost = MagicMock()
        pacman.position = MagicMock()
        ghost.position = pacman.position
        pacman.collideRadius = 5
        ghost.collideRadius = 5

        with patch.object(Pacman, 'collideCheck', return_value=True) as mock_collide:
            result = pacman.collideGhost(ghost)
            mock_collide.assert_called_once_with(ghost)
            assert result is True

    @patch("pygame.transform.scale", return_value=get_surface_mock())
    @patch("pygame.image.load", return_value=get_surface_mock())
    def test_collide_ghost_false(self, mock_load, mock_scale):
        mock_node = MagicMock()
        pacman = Pacman(mock_node)
        ghost = MagicMock()
        pacman.position = MagicMock()
        ghost.position = MagicMock()
        pacman.collideRadius = 5
        ghost.collideRadius = 5

        with patch.object(Pacman, 'collideCheck', return_value=False) as mock_collide:
            result = pacman.collideGhost(ghost)
            mock_collide.assert_called_once_with(ghost)
            assert result is False