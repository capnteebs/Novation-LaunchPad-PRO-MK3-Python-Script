# name=Launchpad Pro Mk3

import midi
import device
import channels
import patterns
import transport
import general

"""
#----------------------------------------CLASSES----------------------------------------#
"""

class Color:
	OFF     = 0x00
	WHITE   = 0x03
	RED     = 0x05
	ORANGE  = 0x09
	YELLOW  = 0x0D
	LIME    = 0x11
	GREEN   = 0x15
	MINT    = 0x19
	EMERALD = 0x1D
	AQUA    = 0x21
	CYAN    = 0x25
	BLUE    = 0x29
	INDIGO  = 0x2D
	VIOLET  = 0x31
	MAGENTA = 0x35
	PINK    = 0x39

class Animation:
	SOLID    = 0
	FLASHING = 1
	PULSING  = 2

# Button CCs in Programmer Mode. Press = value 127, release = 0.
# Shift-modified labels are noted in comments where applicable.
class Button:
	# Top row (mode / function strip)
	SHIFT            = 90
	LEFT             = 91   # Navigation
	RIGHT            = 92   # Navigation
	SESSION          = 93
	NOTE             = 94
	CHORD            = 95
	CUSTOM           = 96
	SEQUENCER        = 97   # Standalone Sequencer
	PROJECTS         = 98   # Save (w/ Shift)
	LOGO             = 99   # Novation logo (top-right)

	# Left column (top -> bottom)
	UP               = 80   # Navigation
	DOWN             = 70   # Navigation
	CLEAR            = 60
	DUPLICATE        = 50   # Double (w/ Shift)
	QUANTISE         = 40   # Record Quantise (w/ Shift)
	FIXED_LENGTH     = 30
	PLAY             = 20
	RECORD           = 10   # Capture MIDI (w/ Shift)

	# Right column (top -> bottom) - Scene Launch / Sequencer steps
	PATTERNS         = 89
	STEPS            = 79
	PATTERN_SETTINGS = 69
	VELOCITY         = 59
	PROBABILITY      = 49
	MUTATION         = 39
	MICRO_STEP       = 29
	PRINT_TO_CLIP    = 19

	# Bottom: Track Select (thin row above the labeled row)
	TRACK_SELECT_1   = 101
	TRACK_SELECT_2   = 102
	TRACK_SELECT_3   = 103
	TRACK_SELECT_4   = 104
	TRACK_SELECT_5   = 105
	TRACK_SELECT_6   = 106
	TRACK_SELECT_7   = 107
	TRACK_SELECT_8   = 108

	TRACK_SELECTS = [101, 102, 103, 104, 105, 106, 107, 108]

	# Bottom: Ableton Track Controls (labeled row). Shift function in comment.
	RECORD_ARM       = 1    # Undo
	MUTE             = 2    # Redo
	SOLO             = 3    # Click
	VOLUME           = 4    # (•)
	PAN              = 5    # (••)
	SENDS            = 6    # Tap
	DEVICE           = 7    # Tempo
	STOP_CLIP        = 8    # Swing

	# Note: the Setup button (bottom-left, unmarked in programmer mode) does
	# NOT send MIDI - it is the hardware switch used to enter/exit modes.

# 8x8 pad grid uses Note On / Note Off (not CC) in Programmer Mode.
# Note number = row*10 + col, where row 1 = bottom, col 1 = left.
# Bottom-left pad = 11, top-right pad = 88.
class Pad:
	@staticmethod
	def note(row, col):
		"""1-indexed (row, col). row 1 = bottom, col 1 = left."""
		return row * 10 + col

	@staticmethod
	def row_col(note):
		"""Inverse of note(): returns (row, col) for a pad note number."""
		return (note // 10, note % 10)

	# Useful corner / edge references
	BOTTOM_LEFT  = 11
	BOTTOM_RIGHT = 18
	TOP_LEFT     = 81
	TOP_RIGHT    = 88

# Grid view state
class State:
	stepOffset    = 0   # first visible step index (scrolls by 1)
	channelOffset = 0   # first visible channel index (scrolls by 1)
	playheadStep  = -1  # last drawn playhead step (-1 = none)
	padState      = {}  # (row, col) -> (animation, color) — dedup cache
	buttonColors  = {}  # cc -> color — tracks each button's resting color
	trackSelState = {}  # i -> (animation, color) — dedup cache for track select
	shiftHeld     = False
	editMode      = None     # None or a PARAM_MODES key string
	editSelection = None     # (ch, step) — the step being edited
	# Per-refresh cached values (set once per refreshGrid call)
	_numCh       = 0
	_patSteps    = 0
	_chColors    = {}   # ch -> padColor
	_chMuted     = {}   # ch -> bool

# Step parameter editing modes — each defines behavior for the track select picker
PARAM_MODES = {
	'velocity': {
		'param': 1,        # pVelocity
		'values': [16, 32, 48, 64, 80, 96, 112, 127],
		'centered': False,
		'center': None,
		'color': Color.RED,
		'button': 4,       # Button.VOLUME
	},
	'pan': {
		'param': 4,        # pPan
		'values': [0, 18, 36, 55, 73, 91, 109, 128],
		'centered': True,
		'center': 64,
		'color': Color.VIOLET,
		'button': 5,       # Button.PAN
	},
	'release': {
		'param': 2,        # pRelease
		'values': [16, 32, 48, 64, 80, 96, 112, 127],
		'centered': False,
		'center': None,
		'color': Color.EMERALD,
		'button': 59,      # Button.VELOCITY (right col)
	},
	'pitch': {
		'param': 3,        # pFinePitch
		'values': [0, 18, 36, 55, 73, 91, 109, 128],
		'centered': True,
		'center': 64,
		'color': Color.LIME,
		'button': 39,      # Button.MUTATION (right col)
	},
	'shift': {
		'param': 7,        # pShift (micro-timing)
		'values': None,    # computed dynamically per step
		'centered': False,
		'center': None,
		'color': Color.INDIGO,
		'button': 29,      # Button.MICRO_STEP (right col)
	},
	'repeat': {
		'param': 8,        # pRepeat
		'values': [0, 2, 4, 6, 8, 10, 12, 14],
		'centered': False,
		'center': None,
		'color': Color.PINK,
		'button': 49,      # Button.PROBABILITY (right col)
	},
}

# Reverse lookup: button CC -> mode name
PARAM_BUTTON_MAP = {mode['button']: name for name, mode in PARAM_MODES.items()}

def getEditValues():
	"""Return the picker values for the current edit mode.
	Most modes use static 8 values. Shift mode computes per-step:
	normal = 8 binary subdivisions (1/8), shift held = 6 triplet subdivisions (1/6, 1/3)."""
	mode = PARAM_MODES[State.editMode]
	if State.editMode == 'shift' and State.editSelection is not None:
		step = State.editSelection[1]
		ppq = general.getRecPPQ()
		ticksPerStep = ppq // 4
		base = step * ticksPerStep
		if State.shiftHeld:
			# Triplet grid: 6 positions (1/6 step)
			increment = max(1, ticksPerStep // 6)
			return [base + i * increment for i in range(6)]
		else:
			# Binary grid: 8 positions (1/8 step)
			increment = max(1, ticksPerStep // 8)
			return [base + i * increment for i in range(8)]
	return mode['values']

"""
#----------------------------------------HELPER METHODS----------------------------------------#
"""
# Streamlined Midi Message sending to Device
#	- command  = message type (Note On, CC, etc)
#	- channel  = MIDI channel (0-2 maps to Animation: Solid/Flashing/Pulsing)
#	- data1    = note number or CC number
#	- data2    = color/velocity value
def SendMIDI(command, channel, data1, data2):
	status = command | channel
	message = status + (data1 << 8) + (data2 << 16)
	device.midiOutMsg(message)

def SendCC(cc, color, animation=Animation.SOLID):
	"""Light a CC button (all non-pad buttons). Tracks resting color for press feedback."""
	if color != Color.OFF:
		State.buttonColors[cc] = color
	SendMIDI(midi.MIDI_CONTROLCHANGE, animation, cc, color)

def lightButtons(color=Color.WHITE):
	"""Light all non-pad buttons. Pass Color.OFF to turn them off."""
	# Top row
	for cc in [Button.SHIFT, Button.LEFT, Button.RIGHT, Button.SESSION,
			   Button.NOTE, Button.CHORD, Button.CUSTOM, Button.SEQUENCER,
			   Button.PROJECTS, Button.LOGO]:
		SendCC(cc, color)

	# Left column
	for cc in [Button.UP, Button.DOWN, Button.CLEAR, Button.DUPLICATE,
			   Button.QUANTISE, Button.FIXED_LENGTH, Button.PLAY, Button.RECORD]:
		SendCC(cc, color)

	# Right column
	for cc in [Button.PATTERNS, Button.STEPS, Button.PATTERN_SETTINGS,
			   Button.VELOCITY, Button.PROBABILITY, Button.MUTATION,
			   Button.MICRO_STEP, Button.PRINT_TO_CLIP]:
		SendCC(cc, color)

	# Track select row
	for cc in [Button.TRACK_SELECT_1, Button.TRACK_SELECT_2, Button.TRACK_SELECT_3,
			   Button.TRACK_SELECT_4, Button.TRACK_SELECT_5, Button.TRACK_SELECT_6,
			   Button.TRACK_SELECT_7, Button.TRACK_SELECT_8]:
		SendCC(cc, color)

	# Bottom row
	for cc in [Button.RECORD_ARM, Button.MUTE, Button.SOLO, Button.VOLUME,
			   Button.PAN, Button.SENDS, Button.DEVICE, Button.STOP_CLIP]:
		SendCC(cc, color)

# Approximate RGB values for each Launchpad palette color
PALETTE = [
	((255, 255, 255), Color.WHITE),
	((255,   0,   0), Color.RED),
	((255, 127,   0), Color.ORANGE),
	((255, 255,   0), Color.YELLOW),
	((127, 255,   0), Color.LIME),
	((  0, 255,   0), Color.GREEN),
	((  0, 255, 127), Color.MINT),
	((  0, 200,  80), Color.EMERALD),
	((  0, 255, 255), Color.AQUA),
	((  0, 127, 255), Color.CYAN),
	((  0,   0, 255), Color.BLUE),
	(( 63,   0, 255), Color.INDIGO),
	((127,   0, 255), Color.VIOLET),
	((255,   0, 255), Color.MAGENTA),
	((255,   0, 127), Color.PINK),
]

def flColorToPad(flColor):
	"""Map FL Studio channel color to nearest Launchpad palette color.
	Strips the gray component and normalizes to full saturation before
	matching, so muted/pastel FL colors still hit the right hue."""
	b =  flColor        & 0xFF
	g = (flColor >>  8) & 0xFF
	r = (flColor >> 16) & 0xFF

	mx = max(r, g, b)
	mn = min(r, g, b)

	# Too gray to determine a hue — just call it white
	if mx == 0 or (mx - mn) < 30:
		return Color.WHITE

	# Remove gray component, stretch to full saturation
	span = mx - mn
	r = int((r - mn) * 255 / span)
	g = int((g - mn) * 255 / span)
	b = int((b - mn) * 255 / span)

	best = Color.WHITE
	bestDist = float('inf')
	for (pr, pg, pb), padColor in PALETTE:
		dist = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
		if dist < bestDist:
			bestDist = dist
			best = padColor
	return best

def velocityToColor(vel):
	"""Map a velocity value (0-127) to a cool-to-hot color."""
	if vel < 20:
		return Color.BLUE
	elif vel < 40:
		return Color.CYAN
	elif vel < 60:
		return Color.GREEN
	elif vel < 80:
		return Color.YELLOW
	elif vel < 100:
		return Color.ORANGE
	else:
		return Color.RED

def valueToButton(val, values):
	"""Given a param value, return the closest button index (0-7)."""
	best = 0
	bestDist = abs(val - values[0])
	for i in range(1, 8):
		dist = abs(val - values[i])
		if dist < bestDist:
			bestDist = dist
			best = i
	return best

def refreshEditDisplay():
	"""Update track select row to show the current param value for the selected step."""
	if State.editMode is None or State.editSelection is None:
		for i in range(8):
			SendCC(Button.TRACK_SELECTS[i], Color.OFF)
		State.trackSelState.clear()
		return

	mode = PARAM_MODES[State.editMode]
	values = getEditValues()
	ch, step = State.editSelection
	val = channels.getCurrentStepParam(ch, step, mode['param'])
	activeBtn = valueToButton(val, values)

	if mode['centered']:
		isCentered = val == mode['center']
		for i in range(8):
			cc = Button.TRACK_SELECTS[i]
			if isCentered:
				SendCC(cc, Color.OFF)
			elif val < mode['center']:
				if i == activeBtn:
					SendCC(cc, Color.WHITE, Animation.PULSING)
				elif activeBtn < i <= 3:
					SendCC(cc, Color.WHITE)
				else:
					SendCC(cc, Color.OFF)
			else:
				if i == activeBtn:
					SendCC(cc, Color.WHITE, Animation.PULSING)
				elif 4 <= i < activeBtn:
					SendCC(cc, Color.WHITE)
				else:
					SendCC(cc, Color.OFF)
	else:
		numValues = len(values)
		for i in range(8):
			cc = Button.TRACK_SELECTS[i]
			if i >= numValues:
				SendCC(cc, Color.OFF)
			elif i == activeBtn:
				SendCC(cc, Color.WHITE, Animation.PULSING)
			elif i < activeBtn:
				SendCC(cc, Color.WHITE)
			else:
				SendCC(cc, Color.OFF)
	State.trackSelState.clear()

"""
#----------------------------------------MAPPING----------------------------------------#
"""
def channelForRow(row):
	"""Row 8 (top) = first visible channel, Row 1 (bottom) = 8th."""
	return (8 - row) + State.channelOffset

def stepForCol(col):
	"""Col 1 (left) = first visible step."""
	return (col - 1) + State.stepOffset

"""
#----------------------------------------GRID DISPLAY----------------------------------------#
"""
def _cacheChannelInfo():
	"""Precompute per-channel data once per refresh cycle."""
	State._numCh = channels.channelCount()
	pat = patterns.patternNumber()
	State._patSteps = patterns.getPatternLength(pat) * 4
	State._chColors.clear()
	State._chMuted.clear()
	for i in range(8):
		ch = i + State.channelOffset
		if ch < State._numCh:
			State._chMuted[ch] = channels.isChannelMuted(ch)
			if State.editMode is None:
				State._chColors[ch] = flColorToPad(channels.getChannelColor(ch))

def refreshGrid():
	"""Redraw all 64 pads based on current view, preserving playhead."""
	_cacheChannelInfo()
	for row in range(1, 9):
		for col in range(1, 9):
			refreshPad(row, col)

def refreshPad(row, col):
	"""Redraw a single pad, accounting for playhead and pattern bounds. Only sends MIDI if state changed."""
	ch = channelForRow(row)
	step = stepForCol(col)
	isPlayhead = (step == State.playheadStep)
	outOfBounds = (ch >= State._numCh) or (step >= State._patSteps)

	if outOfBounds:
		if isPlayhead:
			anim = Animation.PULSING
			color = Color.BLUE
		elif ch < State._numCh:
			anim = Animation.SOLID
			color = Color.WHITE - 2  # dim white — valid channel, past pattern end
		else:
			anim = Animation.SOLID
			color = Color.OFF        # no channel here
	elif channels.getGridBit(ch, step):
		isEditSelected = State.editMode is not None and State.editSelection == (ch, step)
		if State.editMode == 'velocity':
			vel = channels.getCurrentStepParam(ch, step, 1)
			padColor = velocityToColor(vel)
			anim = Animation.PULSING if isEditSelected else Animation.SOLID
		elif State.editMode is not None:
			# Any other param edit mode — selected step pulses mode color
			if isEditSelected:
				padColor = PARAM_MODES[State.editMode]['color']
				anim = Animation.PULSING
			else:
				padColor = State._chColors.get(ch, Color.WHITE)
				anim = Animation.SOLID
		else:
			# Normal mode
			padColor = State._chColors.get(ch, Color.WHITE)
			if State._chMuted.get(ch, False):
				padColor = padColor + 2
			anim = Animation.PULSING if channels.isChannelSelected(ch) else Animation.SOLID
		color = Color.WHITE if isPlayhead else padColor
	elif isPlayhead:
		anim = Animation.PULSING
		color = Color.BLUE
	else:
		anim = Animation.SOLID
		color = Color.OFF

	# Only send if this pad's state actually changed
	key = (row, col)
	state = (anim, color)
	if State.padState.get(key) != state:
		State.padState[key] = state
		SendMIDI(midi.MIDI_NOTEON, anim, Pad.note(row, col), color)

def refreshColumn(col):
	"""Redraw an entire column (used when playhead moves)."""
	_cacheChannelInfo()
	for row in range(1, 9):
		refreshPad(row, col)

def refreshTrackSelect():
	"""Update track select buttons to show channel colors, highlight selected. Cached."""
	if State.editMode is not None:
		refreshEditDisplay()
		return
	numCh = State._numCh if State._numCh > 0 else channels.channelCount()
	for i in range(8):
		cc = Button.TRACK_SELECTS[i]
		ch = i + State.channelOffset
		if ch < numCh:
			color = State._chColors.get(ch, flColorToPad(channels.getChannelColor(ch)))
			if State._chMuted.get(ch, channels.isChannelMuted(ch)):
				color = color + 2
			anim = Animation.PULSING if channels.isChannelSelected(ch) else Animation.SOLID
		else:
			color = Color.OFF
			anim = Animation.SOLID

		state = (anim, color)
		if State.trackSelState.get(i) != state:
			State.trackSelState[i] = state
			SendCC(cc, color, anim)

def clearGrid():
	"""Turn off all 64 pads."""
	State.padState.clear()
	for row in range(1, 9):
		for col in range(1, 9):
			SendMIDI(midi.MIDI_NOTEON, Animation.SOLID, Pad.note(row, col), Color.OFF)

"""
#----------------------------------------PLAYHEAD----------------------------------------#
"""
def getPlayheadStep():
	"""Compute current step position in pattern from absolute ticks."""
	absTicks = transport.getSongPos(2)  # SONGLENGTH_ABSTICKS
	ppq = general.getRecPPQ()           # ticks per quarter note
	ticksPerStep = ppq // 4             # 16th note resolution

	pat = patterns.patternNumber()
	patSteps = patterns.getPatternLength(pat) * 4  # beats * 4 = 16th-note steps

	if patSteps <= 0 or ticksPerStep <= 0:
		return -1

	return int(absTicks / ticksPerStep) % patSteps

def updatePlayhead():
	"""Move the playhead column to the current step position. Only active in pattern mode."""
	if not transport.isPlaying() or transport.getLoopMode() == 1:
		if State.playheadStep != -1:
			oldCol = (State.playheadStep - State.stepOffset) + 1
			State.playheadStep = -1
			if 1 <= oldCol <= 8:
				refreshColumn(oldCol)
		return

	step = getPlayheadStep()
	if step == State.playheadStep:
		return

	oldStep = State.playheadStep
	State.playheadStep = step

	# Clear previous playhead column if visible
	oldCol = (oldStep - State.stepOffset) + 1
	if 1 <= oldCol <= 8:
		refreshColumn(oldCol)

	# Draw new playhead column if visible
	newCol = (step - State.stepOffset) + 1
	if 1 <= newCol <= 8:
		refreshColumn(newCol)

"""
#----------------------------------------INPUT HANDLING----------------------------------------#
"""
def OnMidiMsg(event):
	# Pad press (Note On, channel 0)
	if event.midiId == midi.MIDI_NOTEON and event.midiChan == 0:
		row, col = Pad.row_col(event.data1)
		if 1 <= row <= 8 and 1 <= col <= 8 and event.data2 > 0:
			onPadPress(row, col, event.data2)
		event.handled = True

	# Button press/release (CC, channel 0)
	elif event.midiId == midi.MIDI_CONTROLCHANGE and event.midiChan == 0:
		cc = event.data1
		if cc == Button.SHIFT:
			State.shiftHeld = event.data2 > 0
		elif event.data2 > 0:
			color = State.buttonColors.get(cc, Color.WHITE)
			SendMIDI(midi.MIDI_CONTROLCHANGE, Animation.SOLID, cc, color - 1)
			onButtonPress(cc)
		else:
			# Release — restore resting color
			color = State.buttonColors.get(cc, Color.WHITE)
			SendMIDI(midi.MIDI_CONTROLCHANGE, Animation.SOLID, cc, color)
		event.handled = True

def onPadPress(row, col, velocity=100):
	"""Toggle a step or set velocity depending on mode."""
	ch = channelForRow(row)
	step = stepForCol(col)

	if ch >= channels.channelCount():
		return

	if State.editMode is not None:
		# Step param editing — only interact with active steps
		if channels.getGridBit(ch, step):
			mode = PARAM_MODES[State.editMode]
			if State.editMode == 'velocity' and State.editSelection == (ch, step):
				# Velocity: re-tap selected step sets value from pad pressure
				pat = patterns.patternNumber()
				channels.setStepParameterByIndex(ch, pat, step, mode['param'], velocity)
				if not transport.isPlaying():
					channels.midiNoteOn(channels.getChannelIndex(ch), 60, velocity)
				refreshPad(row, col)
				refreshEditDisplay()
			else:
				# Select this step (or switch selection)
				prevSelection = State.editSelection
				State.editSelection = (ch, step)
				if prevSelection and prevSelection != (ch, step):
					prevRow = 8 - (prevSelection[0] - State.channelOffset)
					prevCol = (prevSelection[1] - State.stepOffset) + 1
					if 1 <= prevRow <= 8 and 1 <= prevCol <= 8:
						refreshPad(prevRow, prevCol)
				refreshPad(row, col)
				refreshEditDisplay()
	else:
		current = channels.getGridBit(ch, step)
		channels.setGridBit(ch, step, int(not current))
		if not current and not transport.isPlaying():
			channels.midiNoteOn(channels.getChannelIndex(ch), 60, velocity)
		refreshPad(row, col)

def onButtonPress(cc):
	"""Handle navigation and function buttons."""
	if cc == Button.DOWN:
		if State.shiftHeld:
			numCh = channels.channelCount()
			if State.channelOffset + 8 < numCh:
				State.channelOffset = min(State.channelOffset + 8, max(numCh - 8, 0))
				refreshGrid()
		elif State.channelOffset + 8 < channels.channelCount():
			State.channelOffset += 1
			refreshGrid()
	elif cc == Button.UP:
		if State.shiftHeld:
			State.channelOffset = max(State.channelOffset - 8, 0)
			refreshGrid()
		elif State.channelOffset > 0:
			State.channelOffset -= 1
			refreshGrid()
	elif cc == Button.PLAY:
		transport.start()
	elif cc == Button.RECORD:
		transport.record()
	elif cc == Button.RECORD_ARM:
		general.undo()
	elif cc == Button.MUTE:
		if State.shiftHeld:
			general.undoUp()  # redo
		else:
			ch = channels.selectedChannel()
			if ch >= 0:
				channels.muteChannel(ch)
	elif cc == Button.SOLO:
		if State.shiftHeld:
			transport.globalTransport(midi.FPT_Metronome, 1)
		else:
			ch = channels.selectedChannel()
			if ch >= 0:
				channels.soloChannel(ch)
	elif cc in PARAM_BUTTON_MAP:
		modeName = PARAM_BUTTON_MAP[cc]
		if State.editMode == modeName:
			# Toggle off
			State.editMode = None
			State.editSelection = None
			SendCC(cc, Color.WHITE)
		else:
			# Switch to this mode (turn off previous)
			if State.editMode is not None:
				SendCC(PARAM_MODES[State.editMode]['button'], Color.WHITE)
			State.editMode = modeName
			State.editSelection = None
			SendCC(cc, PARAM_MODES[modeName]['color'], Animation.PULSING)
		State.padState.clear()
		State.trackSelState.clear()
		refreshGrid()
		refreshTrackSelect()
	elif cc == Button.SENDS:
		if State.shiftHeld:
			transport.globalTransport(midi.FPT_TapTempo, 1)
	elif cc == Button.DUPLICATE:
		patterns.clonePattern()
	elif cc == Button.LEFT:
		if State.shiftHeld:
			pat = patterns.patternNumber()
			if pat > 1:
				patterns.jumpToPattern(pat - 1)
				State.stepOffset = 0
				refreshGrid()
		elif State.stepOffset > 0:
			State.stepOffset -= 1
			refreshGrid()
	elif cc == Button.RIGHT:
		if State.shiftHeld:
			pat = patterns.patternNumber()
			if pat < patterns.patternCount():
				patterns.jumpToPattern(pat + 1)
				State.stepOffset = 0
				refreshGrid()
		else:
			State.stepOffset += 1
			refreshGrid()
	elif cc == Button.CLEAR:
		pat = patterns.patternNumber()
		patSteps = patterns.getPatternLength(pat) * 4
		if State.shiftHeld:
			# Clear ALL channels in pattern
			for ch in range(channels.channelCount()):
				for step in range(patSteps):
					channels.setGridBit(ch, step, 0)
		else:
			# Clear selected channel only
			ch = channels.selectedChannel()
			if ch >= 0:
				for step in range(patSteps):
					channels.setGridBit(ch, step, 0)
		refreshGrid()
	elif cc in Button.TRACK_SELECTS:
		btnIndex = cc - Button.TRACK_SELECT_1
		if State.editMode is not None and State.editSelection is not None:
			# Set param value for the selected step
			mode = PARAM_MODES[State.editMode]
			values = getEditValues()
			if btnIndex >= len(values):
				return  # button beyond available values
			ch, step = State.editSelection
			newVal = values[btnIndex]
			# Centered modes: pressing active button resets to center
			if mode['centered']:
				currentVal = channels.getCurrentStepParam(ch, step, mode['param'])
				currentBtn = valueToButton(currentVal, values)
				if currentVal != mode['center'] and btnIndex == currentBtn:
					newVal = mode['center']
			pat = patterns.patternNumber()
			channels.setStepParameterByIndex(ch, pat, step, mode['param'], newVal)
			# Preview sound for velocity changes
			if State.editMode == 'velocity' and not transport.isPlaying():
				channels.midiNoteOn(channels.getChannelIndex(ch), 60, newVal)
			refreshPad(8 - (ch - State.channelOffset), (step - State.stepOffset) + 1)
			refreshEditDisplay()
		else:
			ch = btnIndex + State.channelOffset
			if ch < channels.channelCount():
				channels.selectOneChannel(ch)
				refreshTrackSelect()

"""
#----------------------------------------CALLBACKS----------------------------------------#
"""
def OnInit():
	State.stepOffset = 0
	State.channelOffset = 0
	State.playheadStep = -1
	State.padState = {}
	State.trackSelState = {}
	State.editMode = None
	State.editSelection = None
	lightButtons(Color.OFF)  # start with everything off
	# Modifier
	SendCC(Button.SHIFT, Color.WHITE)
	# Navigation — cyan
	SendCC(Button.UP, Color.CYAN)
	SendCC(Button.DOWN, Color.CYAN)
	SendCC(Button.LEFT, Color.CYAN)
	SendCC(Button.RIGHT, Color.CYAN)
	# Transport
	SendCC(Button.PLAY, Color.GREEN)
	SendCC(Button.RECORD, Color.RED)
	# Channel controls
	SendCC(Button.MUTE, Color.YELLOW)
	SendCC(Button.SOLO, Color.AQUA)
	SendCC(Button.CLEAR, Color.ORANGE)
	SendCC(Button.DUPLICATE, Color.WHITE)
	SendCC(Button.RECORD_ARM, Color.WHITE)
	# Step param mode buttons
	for name, mode in PARAM_MODES.items():
		SendCC(mode['button'], Color.WHITE)
	# Misc
	SendCC(Button.SENDS, Color.WHITE)
	SendCC(Button.LOGO, Color.WHITE)
	# Track select — colored per channel
	refreshTrackSelect()
	refreshGrid()
	print("LaunchPad Initialized")

def OnDeInit():
	clearGrid()
	lightButtons(Color.OFF)


def OnIdle():
	updatePlayhead()
	refreshGrid()       # poll grid state every tick — cache makes this cheap
	refreshTrackSelect()

def OnUpdateBeatIndicator(value):
	updatePlayhead()
	if value == 1:     # bar start (beat 1) — bright flash
		SendCC(Button.LOGO, Color.GREEN)
	elif value == 2:   # other beats — dim flash
		SendCC(Button.LOGO, Color.WHITE)

def OnRefresh(flags):
	refreshGrid()
