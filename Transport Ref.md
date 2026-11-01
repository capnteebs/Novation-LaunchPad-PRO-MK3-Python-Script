# Transport Module

Handles FL Studio transport (Play, Stop, Pause & Record).

---

## Playback Control

| Command | Arguments | Returns | Description | Version |
|---------|-----------|---------|-------------|---------|
| `start` | `-` | `-` | Initiate playback. | - |
| `stop` | `-` | `-` | Halt playback. | - |
| `record` | `-` | `-` | Toggle recording state. | - |
| `isPlaying` | `-` | `int` | Returns 1 if playback is active. | - |
| `isRecording` | `-` | `int` | Returns 1 if recording is active. | - |

## Loop Mode

| Command | Arguments | Returns | Description | Version |
|---------|-----------|---------|-------------|---------|
| `getLoopMode` | `-` | `int` | Returns current loop mode: `0` = pattern, `1` = song. | - |
| `setLoopMode` | `-` | `-` | Toggles between pattern/song loop modes. | - |

## Song Position

| Command | Arguments | Returns | Description | Version |
|---------|-----------|---------|-------------|---------|
| `getSongPos` | `(int mode)` | `float` | Returns song position. Without mode: normalized 0.0 to 1.0. With mode: see constants below. | - |
| `setSongPos` | `float position`, `(int mode)` | `-` | Sets song position (normalized or formatted). | - |
| `getSongLength` | `int mode` | `int` | Returns song length in the format specified by `mode`. | - |
| `getSongPosHint` | `-` | `string` | Returns a hint string for the current song position. | - |

### Song Position Mode Constants (`SONGLENGTH_*`)

| Constant | Value | Unit |
|----------|-------|------|
| `SONGLENGTH_MS` | 0 | Milliseconds |
| `SONGLENGTH_S` | 1 | Seconds |
| `SONGLENGTH_ABSTICKS` | 2 | Absolute ticks |
| `SONGLENGTH_BARS` | 3 | Bars (BST format) |
| `SONGLENGTH_STEPS` | 4 | Steps (BST format) |
| `SONGLENGTH_TICKS` | 5 | Ticks (BST format) |

## Navigation

| Command | Arguments | Returns | Description | Version |
|---------|-----------|---------|-------------|---------|
| `rewind` | `int startStop`, `(int flags)` | `-` | Rewind song. `SS_Start` (2) to begin, `SS_Stop` (0) to stop. | - |
| `fastForward` | `int speed` | `-` | Fast forward at specified speed. | - |
| `continuousMove` | `int speed`, `int startStop` | `-` | Continuous movement. Positive = forward, negative = backward. | - |
| `continuousMovePos` | `int speed`, `int startStop` | `-` | Alternative continuous movement. `startStop`: 2=start, 0=stop. | - |
| `markerJumpJog` | `int value`, `(int flags)` | `-` | Jump to marker by increment (-1 prev, +1 next). | - |
| `markerSelJog` | `int value`, `(int flags)` | `-` | Select marker by increment. | - |

## Tempo & Beat

| Command | Arguments | Returns | Description | Version |
|---------|-----------|---------|-------------|---------|
| `setPlaybackSpeed` | `float speedMultiplier` | `-` | Set playback speed (0.25 to 4.0, 1.0 = normal). | - |
| `getHWBeatLEDState` | `-` | `int` | Returns the state of the hardware beat LED indicator. | - |
| `globalTransport` | `int command`, `int value`, `(int pmeflags)`, `(int flags)` | `int` | Execute a global transport command using `FPT_*` constants. Pass `eventData.pmeFlags` when calling from within script events. | - |

### StartStop Constants

| Constant | Value |
|----------|-------|
| `SS_Stop` | 0 |
| `SS_StartStep` | 1 |
| `SS_Start` | 2 |
