#!/usr/bin/env python

"""
A model of a SpiNNaker system's boards and their positions.

Generally sets of boards are represented as a list [(board, position), ...]
where position is a coordinate in some coordinate system.
"""

import topology



class Board(object):
	"""
	Represents a SpiNNaker board in a complete system.
	"""
	
	def __init__(self):
		
		# References to other boards in the system which lie at the end of a wire
		# connected to a particular port.
		self.connection = {
			topology.NORTH      : None,
			topology.NORTH_EAST : None,
			topology.EAST       : None,
			topology.SOUTH      : None,
			topology.SOUTH_WEST : None,
			topology.WEST       : None,
		}
	
	
	def connect_wire(self, other, direction):
		"""
		Connect a wire between this board and another for the given direction.
		"""
		# Ensure it isn't already connected
		assert(self.follow_wire(direction) is None)
		assert(other.follow_wire(topology.opposite(direction)) is None)
		
		self.connection[direction] = other
		other.connection[topology.opposite(direction)] = self
	
	
	def follow_wire(self, direction):
		"""
		Follow the wire going in the given direction from this board.
		"""
		return self.connection[direction]
	
	
	def follow_packet(self, in_wire_side, packet_direction):
		"""
		Follow the path of a packet which entered in to the board via the wire
		in_wire_side following packet_direction through the chips in the board.
		Returns a tuple (next_in_wire_side, next_board).
		"""
		
		# Mapping of {(in_wire_side, packet_direction) : out_wire_side,...}
		out_sides = {
			(topology.SOUTH_WEST, topology.EAST)       : topology.EAST,
			(topology.WEST,       topology.EAST)       : topology.NORTH_EAST,
			
			(topology.SOUTH_WEST, topology.NORTH_EAST) : topology.NORTH,
			(topology.SOUTH,      topology.NORTH_EAST) : topology.NORTH_EAST,
			
			(topology.SOUTH,      topology.NORTH)      : topology.WEST,
			(topology.EAST,       topology.NORTH)      : topology.NORTH,
		}
		# Opposite cases are simply inverted versions of the above...
		for (iws, pd), ows in out_sides.items():
			out_sides[( topology.opposite(iws)
			          , topology.opposite(pd)
			          )] = topology.opposite(ows)
		
		out_wire_side = out_sides[(in_wire_side, packet_direction)]
		
		return (topology.opposite(out_wire_side), self.follow_wire(out_wire_side))
		
	
	
	def __repr__(self):
		return "Board()"




def create_threeboards(width = 1, height = None):
	"""
	Returns a set boards containing width x height threeboards. If height is not
	specified, height = width. Links the boards together in a torus.
	"""
	
	height = width if height is None else height
	
	boards = {}
	
	# Create the boards
	for coord in topology.threeboards(width, height):
		boards[coord] = Board()
	
	# Link the boards together
	for coord in boards:
		for direction in [ topology.EAST
		                 , topology.NORTH_EAST
		                 , topology.NORTH
		                 ]:
			# Get the coordinate of the neighbour in each direction
			n_coord = topology.to_xy(
			            topology.wrap_around(
			              topology.add_direction(list(coord)+[0], direction), (width, height)))
			
			# Connect the boards together
			boards[coord].connect_wire(boards[n_coord], direction)
	
	return [(b, c) for (c, b) in boards.iteritems()]


def follow_wiring_loop(start_board, direction):
	"""
	Follows the 'direction' edge until it gets back to the starting board. Yields
	each board along the way.
	
	Generates a sequence of boards that were traversed.
	"""
	yield(start_board)
	cur_board = start_board.follow_wire(direction)
	while cur_board != start_board:
		yield(cur_board)
		cur_board = cur_board.follow_wire(direction)


def follow_packet_loop(start_board, in_wire_side, direction):
	"""
	Follows the path of a packet entering on in_wire_side of start_board
	travelling in the direction given.
	
	Generates a sequence of (in_wire_side, board) tuples that were traversed.
	"""
	yield(in_wire_side, start_board)
	in_wire_side, cur_board = start_board.follow_packet(in_wire_side, direction)
	while cur_board != start_board:
		yield(in_wire_side, cur_board)
		in_wire_side, cur_board = cur_board.follow_packet(in_wire_side, direction)


def rhombus_to_rect(boards, bounds):
	r"""
	Takes a rhombus of boards with the bottom left corner at (0,0) (e.g. from
	create_threeboards) and produces a rectangular arrangement with all
	coordinates positive like so::
		
		_________         ___   ______             _________
		\        \        \  | |      \           |         |
		 \        \   -->  \ | |       \      --> |         |
		  \._______\        \| |._______\ .       |.________|
		   |                             /;\       |
		 (0,0)               \___________/       (0,0)
	"""
	width, height = bounds
	
	out = []
	for board, (old_x,old_y) in boards:
		# Wrap the elements
		new_x = old_x + (0 if old_x >= 0 else width*2)
		new_y = old_y + (0 if old_x >= 0 else width)
		out.append((board, (new_x, new_y)))
	
	return out


