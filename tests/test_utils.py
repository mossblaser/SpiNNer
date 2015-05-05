import pytest

from mock import Mock

from spinner import utils
from spinner import topology


@pytest.fixture
def mock_rhombus_to_rect(monkeypatch):
	from spinner import transforms
	
	m = Mock()
	m.side_effect = transforms.rhombus_to_rect
	
	monkeypatch.setattr(transforms, "rhombus_to_rect", m)
	return m


@pytest.mark.parametrize("w,h", [(1, 1), (4, 4), (5, 5),
                                 (4, 2), (2, 4),
                                 (6, 3), (3, 6)])
def test_torus_without_long_wires(w, h, mock_rhombus_to_rect):
	hex_boards, folded_boards = utils.torus_without_long_wires(w, h)
	
	# Right number of boards produced
	assert len(hex_boards) == len(folded_boards) == 3 * w * h
	
	# Same board should be present in hexagonal layout as in folded layout
	assert set(b for (b, c) in hex_boards) == set(b for (b, c) in folded_boards)
	
	# Positions allocated should be unique
	assert len(set(c for (b, c) in hex_boards)) == len(hex_boards)
	assert len(set(c for (b, c) in folded_boards)) == len(folded_boards)
	
	# Should only use rhombus-to-rect when a twice-as-tall-as-wide system is
	# presented. (Tests that the right heuristic is used)
	if h == 2*w:
		assert mock_rhombus_to_rect.called
	else:
		assert not mock_rhombus_to_rect.called
	
	min_x = min(c[0] for (b, c) in folded_boards)
	min_y = min(c[1] for (b, c) in folded_boards)
	
	# Should be based from 0,0
	assert min_x == 0
	assert min_y == 0
	
	max_x = max(c[0] for (b, c) in folded_boards)
	max_y = max(c[1] for (b, c) in folded_boards)
	
	# Folded boards should fit within expected bounds (note that the 'or's here
	# are to allow for folding odd numbers of boards in each dimension).
	if h == 2 * w:
		assert max_x == 2*w or max_x + 1 == 2*w
		assert max_y == int(1.5*h) or max_y + 1 == int(1.5 * h)
	else:
		assert max_x == 3*w or max_x + 1 == 3*w
		assert max_y == h or max_y + 1 == h