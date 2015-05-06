"""Data structure which defines the physical dimensions of a set of cabinets."""

class Cabinet(object):
	"""Data structure which defines the physical dimensions of a set of
	cabinets."""
	
	def __init__(self,
	             board_dimensions,
	             board_wire_offset_south_west, board_wire_offset_north_east,
	             board_wire_offset_east, board_wire_offset_west,
	             board_wire_offset_north, board_wire_offset_south,
	             inter_board_spacing,
	             boards_per_frame, frame_dimensions, frame_board_offset,
	             inter_frame_spacing,
	             frames_per_cabinet, cabinet_dimensions, cabinet_frame_offset,
	             inter_cabinet_spacing):
		"""Create a new Cabinet structure with the specified measurements (all in
		meters).
		
		Parameters
		----------
		board_dimensions : (w, h, d)
			Physical board dimensions in meters.
		board_wire_offset_south_west : (x, y, z)
			Physical offset of the South West connector from board right-top-front
			corner in meters. Others are similar.
		inter_board_spacing : float
			Physical spacing between each board in a frame in meters.
		boards_per_frame : int
			Number of boards in each frame.
		frame_dimensions : (w, h, d)
			Frame physical dimensions in meters.
		frame_board_offset : (x, y, z)
			Physical offset of the right-most board from the right-top-front corner of
			a frame in meters.
		inter_frame_spacing : float
			Physical spacing between frames in a cabinet in meters.
		frames_per_cabinet : int
			Number of frames per cabinet.
		cabinet_dimensions : (w, h, d)
			Cabinet physical dimensions in meters.
		cabinet_frame_offset : (x, y, z)
			Physical offset of the top frame from the right-top-front corner of a
			cabinet in meters.
		inter_cabinet_spacing : float
			Physical spacing between each cabinet in meters.
		"""
		self.board_dimensions             = board_dimensions
		
		self.board_wire_offset_south_west = board_wire_offset_south_west
		self.board_wire_offset_north_east = board_wire_offset_north_east
		self.board_wire_offset_east       = board_wire_offset_east
		self.board_wire_offset_west       = board_wire_offset_west
		self.board_wire_offset_north      = board_wire_offset_north
		self.board_wire_offset_south      = board_wire_offset_south
		
		self.inter_board_spacing          = inter_board_spacing
		
		self.boards_per_frame             = boards_per_frame
		self.frame_dimensions             = frame_dimensions
		self.frame_board_offset           = frame_board_offset
		self.inter_frame_spacing          = inter_frame_spacing
		
		self.frames_per_cabinet           = frames_per_cabinet
		self.cabinet_dimensions           = cabinet_dimensions
		self.cabinet_frame_offset         = cabinet_frame_offset
		self.inter_cabinet_spacing        = inter_cabinet_spacing
		
		# Check that all values are positive that are meant to be...
		for field in ["board_dimensions",
		              "board_wire_offset_south_west",
		              "board_wire_offset_north_east",
		              "board_wire_offset_east",
		              "board_wire_offset_west",
		              "board_wire_offset_north",
		              "board_wire_offset_south",
		              "inter_board_spacing",
		              "boards_per_frame",
		              "frame_dimensions",
		              "frame_board_offset",
		              "inter_frame_spacing",
		              "frames_per_cabinet",
		              "cabinet_dimensions",
		              "cabinet_frame_offset",
		              "inter_cabinet_spacing"]:
			value = getattr(self, field)
			if type(value) is tuple:
				if not all(v >= 0.0 for v in value):
					raise ValueError("{} must be positive".format(field))
			elif value < 0.0:
				raise ValueError("{} must be positive".format(field))
		
		# Check all board wires are within the bounds of the board
		for wire in ["board_wire_offset_south_west",
		             "board_wire_offset_north_east",
		             "board_wire_offset_east",
		             "board_wire_offset_west",
		             "board_wire_offset_north",
		             "board_wire_offset_south"]:
			if any(v > m for (v, m)
			       in zip(getattr(self, wire), self.board_dimensions)):
				raise ValueError("{} must be within bounds of board".format(wire))
		
		# Check boards fit in the frame
		if any(v > m for (v, m)
		       in zip(self.frame_board_offset_opposite, self.frame_dimensions)):
			raise ValueError("boards must be within bounds of a frame")
		
		# Check frames fit in the cabinet
		if any(v > m for (v, m)
		       in zip(self.cabinet_frame_offset_opposite, self.cabinet_dimensions)):
			raise ValueError("frames must be within bounds of a cabinet")
	
	
	@property
	def frame_board_offset_opposite(self):
		"""The distance of the left-bottom-back corner of the boards from the
		right-top-front corner of the frame."""
		
		return (# X
		        ((((self.board_dimensions[0] + self.inter_board_spacing) *
		           self.boards_per_frame) - self.inter_board_spacing)
		         + self.frame_board_offset[0]),
		        # Y
		        self.board_dimensions[1] + self.frame_board_offset[1],
		        # Z
		        self.board_dimensions[2] + self.frame_board_offset[2])
	
	
	@property
	def cabinet_frame_offset_opposite(self):
		"""The distance of the left-bottom-back corner of the frames from the
		right-top-front corner of the cabinets."""
		
		return (# X
		        self.frame_dimensions[0] + self.cabinet_frame_offset[0],
		        # Y
		        ((((self.frame_dimensions[1] + self.inter_frame_spacing) *
		           self.frames_per_cabinet) - self.inter_frame_spacing)
		         + self.cabinet_frame_offset[1]),
		        # Z
		        self.frame_dimensions[2] + self.cabinet_frame_offset[2])