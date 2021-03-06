import pytest

from six import next

from spinner import topology


def test_next():
	# Clockwise
	assert topology.Direction.east.next_cw ==       topology.Direction.south
	assert topology.Direction.north_east.next_cw == topology.Direction.east
	assert topology.Direction.north.next_cw ==      topology.Direction.north_east
	assert topology.Direction.west.next_cw ==       topology.Direction.north
	assert topology.Direction.south_west.next_cw == topology.Direction.west
	assert topology.Direction.south.next_cw ==      topology.Direction.south_west
	
	# Counter-Clockwise
	assert topology.Direction.east.next_ccw ==       topology.Direction.north_east
	assert topology.Direction.north_east.next_ccw == topology.Direction.north
	assert topology.Direction.north.next_ccw ==      topology.Direction.west
	assert topology.Direction.west.next_ccw ==       topology.Direction.south_west
	assert topology.Direction.south_west.next_ccw == topology.Direction.south
	assert topology.Direction.south.next_ccw ==      topology.Direction.east

def test_opposite():
	assert topology.Direction.east.opposite ==       topology.Direction.west
	assert topology.Direction.north_east.opposite == topology.Direction.south_west
	assert topology.Direction.north.opposite ==      topology.Direction.south
	assert topology.Direction.west.opposite ==       topology.Direction.east
	assert topology.Direction.south_west.opposite == topology.Direction.north_east
	assert topology.Direction.south.opposite ==      topology.Direction.north

def test_direction():
	ad = topology.add_direction
	
	assert ad((11,11,11), topology.Direction.east) ==       (12,11,11)
	assert ad((11,11,11), topology.Direction.north_east) == (11,11,10)
	assert ad((11,11,11), topology.Direction.north) ==      (11,12,11)
	assert ad((11,11,11), topology.Direction.west) ==       (10,11,11)
	assert ad((11,11,11), topology.Direction.south_west) == (11,11,12)
	assert ad((11,11,11), topology.Direction.south) ==      (11,10,11)


def test_manhattan():
	assert topology.manhattan([0]) ==      0
	assert topology.manhattan([1]) ==      1
	assert topology.manhattan([-1]) ==     1
	assert topology.manhattan([-1, 0]) ==  1
	assert topology.manhattan([-1, -1]) == 2
	assert topology.manhattan([-1,  1]) == 2


def test_median_element():
	assert topology.median_element([0]) == 0
	assert topology.median_element([0,1,2]) == 1
	assert topology.median_element([2,1,0]) == 1
	assert topology.median_element([1,2,0]) == 1
	assert topology.median_element([2,0,1]) == 1
	assert topology.median_element([2,2,2]) == 2


def test_to_shortest_path():
	assert topology.to_shortest_path((0,0,0)) == (0,0,0)
	assert topology.to_shortest_path((1,1,1)) == (0,0,0)
	assert topology.to_shortest_path((0,1,2)) == (-1,0,1)
	assert topology.to_shortest_path((-2,0,2)) == (-2,0,2)


def test_to_xy():
	assert topology.to_xy((0,0,0)) == (0,0)
	assert topology.to_xy((1,1,1)) == (0,0)
	assert topology.to_xy((0,1,2)) == (-2,-1)
	assert topology.to_xy((-2,0,2)) == (-4,-2)


def test_hexagon():
	it = topology.hexagon(2)
	
	# Inner layer
	assert next(it) == ( 0, 0)
	assert next(it) == (-1, 0)
	assert next(it) == ( 0, 1)
	
	# Outer layer
	assert next(it) == ( 1, 1)
	assert next(it) == ( 1, 0)
	assert next(it) == ( 0,-1)
	assert next(it) == (-1,-1)
	assert next(it) == (-2,-1)
	assert next(it) == (-2, 0)
	assert next(it) == (-1, 1)
	assert next(it) == ( 0, 2)
	assert next(it) == ( 1, 2)
	
	# Stop now
	with pytest.raises(StopIteration):
		next(it)


def test_hexagon_zero():
	it = topology.hexagon_zero(2)
	
	# Inner layer
	assert next(it) == (2,1)
	assert next(it) == (1,1)
	assert next(it) == (2,2)
	
	# Outer layer
	assert next(it) == (3,2)
	assert next(it) == (3,1)
	assert next(it) == (2,0)
	assert next(it) == (1,0)
	assert next(it) == (0,0)
	assert next(it) == (0,1)
	assert next(it) == (1,2)
	assert next(it) == (2,3)
	assert next(it) == (3,3)
	
	# Stop now
	with pytest.raises(StopIteration):
		next(it)


def test_threeboards():
	# Creating no threeboards makes no boards...
	assert list(topology.threeboards(0)) == []
	
	# Creating 2x2 threeboards (throw away the boards...)
	boards = [topology.to_xy(c) for c in topology.threeboards(2)]
	assert len(boards) == 3*2*2
	# Threeboard (0,0)
	assert (0,0) in boards
	assert (0,1) in boards
	assert (1,1) in boards
	# Threeboard (1,0)
	assert (2,1) in boards
	assert (2,2) in boards
	assert (3,2) in boards
	# Threeboard (0,1)
	assert (-1,1) in boards
	assert (-1,2) in boards
	assert (0,2) in boards
	# Threeboard (1,1)
	assert (1,2) in boards
	assert (1,3) in boards
	assert (2,3) in boards


def test_wrap_around():
	# Exhaustively test single threeboard case
	# Stays in board
	assert topology.wrap_around((0,0,0), (1,1)) == (0,0,0)
	assert topology.wrap_around((0,1,0), (1,1)) == (0,1,0)
	assert topology.wrap_around((1,1,0), (1,1)) == (1,1,0)
	
	# Off the top-left of (0,0)
	assert topology.wrap_around((-1,0,0), (1,1)) == (1,1,0)
	# Off the bottom-left of (0,0)
	assert topology.wrap_around((-1,-1,0), (1,1)) == (0,1,0)
	# Off the bottom-right of (0,0)
	assert topology.wrap_around((1,0,0), (1,1)) == (0,1,0)
	# Off the bottom of (0,0)
	assert topology.wrap_around((0,-1,0), (1,1)) == (1,1,0)
	
	# Off the bottom-left of (0,1)
	assert topology.wrap_around((-1,0,0), (1,1)) == (1,1,0)
	# Off the top-left of (0,1)
	assert topology.wrap_around((-1,1,0), (1,1)) == (0,0,0)
	# Off the top of (0,1)
	assert topology.wrap_around((0,2,0), (1,1)) == (1,1,0)
	# Off the top-right of (0,1)
	assert topology.wrap_around((0,-1,0), (1,1)) == (1,1,0)
	
	# Off the top of (1,1)
	assert topology.wrap_around((1,2,0), (1,1)) == (0,0,0)
	# Off the top-right of (1,1)
	assert topology.wrap_around((2,2,0), (1,1)) == (0,1,0)
	# Off the bottom-right of (1,1)
	assert topology.wrap_around((2,1,0), (1,1)) == (0,0,0)
	# Off the bottom of (1,1)
	assert topology.wrap_around((1,0,0), (1,1)) == (0,1,0)
	
	# Try some random examples for a larger system
	assert topology.wrap_around((-3,5,0), (4,4)) == (1,1,0)
	assert topology.wrap_around((8,4,0), (4,4)) == (0,0,0)
	assert topology.wrap_around((0,-1,0), (4,4)) == (4,7,0)
	assert topology.wrap_around((4,8,0), (4,4)) == (0,0,0)
	
	# And now non-equally sized systems
	assert topology.wrap_around((0,-1,0), (4,3)) == (5,6,0)
	assert topology.wrap_around((5,7,0), (4,3)) == (0,0,0)
	
	# Multi-world-sized steps
	assert topology.wrap_around((4,5,0), (1,1)) == (0,0,0)
	assert topology.wrap_around((-2,2,0), (1,1)) == (0,0,0)


def test_hex_to_cartesian():
	# Test single element cases
	assert topology.hex_to_cartesian((0,0,0)) == (0,0)
	assert topology.hex_to_cartesian((0,1,0)) == (0,2)
	assert topology.hex_to_cartesian((1,1,0)) == (1,1)


def test_board_to_chip():
	assert topology.board_to_chip((0,0,0), (0,0))
	assert topology.board_to_chip((1,0,0), (8,4))
	assert topology.board_to_chip((0,1,0), (4,8))
	assert topology.board_to_chip((1,1,0), (12,12))


def test_hex_to_skew_cartesian():
	# Test single element cases
	assert topology.hex_to_skewed_cartesian((0,0,0)) == (0,0)
	assert topology.hex_to_skewed_cartesian((0,1,0)) == (1,2)
	assert topology.hex_to_skewed_cartesian((1,1,0)) == (2,1)


def test_euclidean():
	assert topology.euclidean((0, 0)) == 0.0
	assert topology.euclidean((1, 0)) == 1.0
	assert topology.euclidean((0, 1)) == 1.0
	assert topology.euclidean((1, 1)) == 2.0**0.5
	assert topology.euclidean((-1, 1)) == 2.0**0.5
	assert topology.euclidean((-1, -1)) == 2.0**0.5
	
	assert topology.euclidean((0, 0, 0)) == 0.0
	assert topology.euclidean((1, 0, 0)) == 1.0
	assert topology.euclidean((0, 1, 0)) == 1.0
	assert topology.euclidean((0, 0, 1)) == 1.0
	assert topology.euclidean((0, 1, 1)) == 2.0**0.5
	assert topology.euclidean((1, 1, 0)) == 2.0**0.5
	assert topology.euclidean((1, 0, 1)) == 2.0**0.5
	assert topology.euclidean((1, 1, 1)) == 3.0**0.5


def test_fold_dimension():
	# No folding
	assert topology.fold_dimension(0, 4, 1) == (0,0)
	assert topology.fold_dimension(1, 4, 1) == (1,0)
	assert topology.fold_dimension(2, 4, 1) == (2,0)
	assert topology.fold_dimension(3, 4, 1) == (3,0)
	
	# Single fold (into two sides)
	# Folds for things on the first side
	assert topology.fold_dimension(0, 4, 2) == (0,0)
	assert topology.fold_dimension(1, 4, 2) == (1,0)
	# Folds on the inside
	assert topology.fold_dimension(2, 4, 2) == (1,1)
	assert topology.fold_dimension(3, 4, 2) == (0,1)
	
	# Odd number of folds (into three pieces)
	assert topology.fold_dimension(0, 9, 3) == (0,0)
	assert topology.fold_dimension(1, 9, 3) == (1,0)
	assert topology.fold_dimension(2, 9, 3) == (2,0)
	
	assert topology.fold_dimension(3, 9, 3) == (2,1)
	assert topology.fold_dimension(4, 9, 3) == (1,1)
	assert topology.fold_dimension(5, 9, 3) == (0,1)
	
	assert topology.fold_dimension(6, 9, 3) == (0,2)
	assert topology.fold_dimension(7, 9, 3) == (1,2)
	assert topology.fold_dimension(8, 9, 3) == (2,2)
	
	
	# Folded twice (into four sides)
	# Front
	assert topology.fold_dimension(0, 12, 4) == (0,0)
	assert topology.fold_dimension(1, 12, 4) == (1,0)
	assert topology.fold_dimension(2, 12, 4) == (2,0)
	# Mid Front
	assert topology.fold_dimension(3, 12, 4) == (2,1)
	assert topology.fold_dimension(4, 12, 4) == (1,1)
	assert topology.fold_dimension(5, 12, 4) == (0,1)
	# Mid Back
	assert topology.fold_dimension(6, 12, 4) == (0,2)
	assert topology.fold_dimension(7, 12, 4) == (1,2)
	assert topology.fold_dimension(8, 12, 4) == (2,2)
	# Back
	assert topology.fold_dimension(9, 12, 4) == (2,3)
	assert topology.fold_dimension(10, 12, 4) == (1,3)
	assert topology.fold_dimension(11, 12, 4) == (0,3)


def test_fold_interleave_dimension():
	# No folds
	assert topology.fold_interleave_dimension(0, 4, 1) == 0
	assert topology.fold_interleave_dimension(1, 4, 1) == 1
	assert topology.fold_interleave_dimension(2, 4, 1) == 2
	assert topology.fold_interleave_dimension(3, 4, 1) == 3
	
	# Two sides (one fold)
	assert topology.fold_interleave_dimension(0, 4, 2) == 0
	assert topology.fold_interleave_dimension(3, 4, 2) == 1
	assert topology.fold_interleave_dimension(1, 4, 2) == 2
	assert topology.fold_interleave_dimension(2, 4, 2) == 3
	
	# Odd number of sides
	assert topology.fold_interleave_dimension(0, 9, 3) == 0
	assert topology.fold_interleave_dimension(5, 9, 3) == 1
	assert topology.fold_interleave_dimension(6, 9, 3) == 2
	assert topology.fold_interleave_dimension(1, 9, 3) == 3
	assert topology.fold_interleave_dimension(4, 9, 3) == 4
	assert topology.fold_interleave_dimension(7, 9, 3) == 5
	assert topology.fold_interleave_dimension(2, 9, 3) == 6
	assert topology.fold_interleave_dimension(3, 9, 3) == 7
	assert topology.fold_interleave_dimension(8, 9, 3) == 8
	
	# Four sides (2 folds)
	assert topology.fold_interleave_dimension(0, 12, 4) == 0
	assert topology.fold_interleave_dimension(5, 12, 4) == 1
	assert topology.fold_interleave_dimension(6, 12, 4) == 2
	assert topology.fold_interleave_dimension(11, 12, 4) == 3
	assert topology.fold_interleave_dimension(1, 12, 4) == 4
	assert topology.fold_interleave_dimension(4, 12, 4) == 5
	assert topology.fold_interleave_dimension(7, 12, 4) == 6
	assert topology.fold_interleave_dimension(10, 12, 4) == 7
	assert topology.fold_interleave_dimension(2, 12, 4) == 8
	assert topology.fold_interleave_dimension(3, 12, 4) == 9
	assert topology.fold_interleave_dimension(8, 12, 4) == 10
	assert topology.fold_interleave_dimension(9, 12, 4) == 11


def test_cabinetise():
	# Test a 4x4 system exhaustively
	#                          +---+---+  +---+---+
	# +---+---+---+---+        |0,3|1,3|  |2,3|3,3|
	# |0,3|1,3|2,3|3,3|        +---+---+  +---+---+        +-------------+ +-------------+
	# +---+---+---+---+        |0,2|1,2|  |2,2|3,2|        |+-----------+| |+-----------+|
	# |0,2|1,2|2,2|3,2|  ---\  +---+---+  +---+---+  ---\  ||02:03:12:13|| ||22:23:32:33||
	# +---+---+---+---+  ---/                        ---/  |+-----------+| |+-----------+|
	# |0,1|1,1|2,1|3,1|        +---+---+  +---+---+        ||00:01:10:11:| ||20:21:30:31||
	# +---+---+---+---+        |0,1|1,1|  |2,1|3,1|        |+-----------+| |+-----------+|
	# |0,0|1,0|2,0|3,0|        +---+---+  +---+---+        +-------------+ +-------------+
	# +---+---+---+---+        |0,0|1,0|  |2,0|3,0|
	#                          +---+---+  +---+---+
	
	assert topology.cabinetise((0,0), (4,4), 2, 2, 4) == (0,0,0)
	assert topology.cabinetise((0,1), (4,4), 2, 2, 4) == (0,0,1)
	assert topology.cabinetise((1,0), (4,4), 2, 2, 4) == (0,0,2)
	assert topology.cabinetise((1,1), (4,4), 2, 2, 4) == (0,0,3)
	
	assert topology.cabinetise((0,2), (4,4), 2, 2, 4) == (0,1,0)
	assert topology.cabinetise((0,3), (4,4), 2, 2, 4) == (0,1,1)
	assert topology.cabinetise((1,2), (4,4), 2, 2, 4) == (0,1,2)
	assert topology.cabinetise((1,3), (4,4), 2, 2, 4) == (0,1,3)
	
	assert topology.cabinetise((2,0), (4,4), 2, 2, 4) == (1,0,0)
	assert topology.cabinetise((2,1), (4,4), 2, 2, 4) == (1,0,1)
	assert topology.cabinetise((3,0), (4,4), 2, 2, 4) == (1,0,2)
	assert topology.cabinetise((3,1), (4,4), 2, 2, 4) == (1,0,3)
	
	assert topology.cabinetise((2,2), (4,4), 2, 2, 4) == (1,1,0)
	assert topology.cabinetise((2,3), (4,4), 2, 2, 4) == (1,1,1)
	assert topology.cabinetise((3,2), (4,4), 2, 2, 4) == (1,1,2)
	assert topology.cabinetise((3,3), (4,4), 2, 2, 4) == (1,1,3)
	
	# Supply a system where we must flip the axes for it to work
	assert topology.cabinetise((0,0), (1,2), 2, 1, 2) == (0,0,0)
	assert topology.cabinetise((0,1), (1,2), 2, 1, 1) == (1,0,0)
	
	# Fail if width not divisible by num_cabinets
	with pytest.raises(ValueError):
		topology.cabinetise((0,0), (4,4), 3, 2, 4) == (1,1,3)
	# Fail if height not divisible by frames_per_cabinet
	with pytest.raises(ValueError):
		topology.cabinetise((0,0), (4,4), 2, 3, 4) == (1,1,3)
