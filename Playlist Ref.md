# Playlist Module

Controls FL Studio playlist tracks, playback position, performance mode, and live clips.

---

## Playback Position

| Command | Arguments | Returns | Description |
|---------|-----------|---------|-------------|
| `getVisTimeBar` | `-` | `int` | Returns the current bar number. |
| `getVisTimeStep` | `-` | `int` | Returns the current step number. |
| `getVisTimeTick` | `-` | `int` | Returns the current tick. |

## Track Management

| Command | Arguments | Returns | Description |
|---------|-----------|---------|-------------|
| `getTrackName` | `int index` | `string` | Returns track name. |
| `setTrackName` | `int index`, `string name` | `-` | Sets track name. |
| `getTrackColor` | `int index` | `int` | Returns track color (RGBA). |
| `setTrackColor` | `int index`, `int color` | `-` | Sets track color. |

## Mute / Solo

| Command | Arguments | Returns | Description |
|---------|-----------|---------|-------------|
| `isTrackMuted` | `int index` | `int` | Returns 1 if muted. |
| `muteTrack` | `int index`, `(int value=-1)`, `(int inGroup=0)` | `-` | Toggle/set mute. `value`: 1=mute, 0=unmute, -1=toggle. |
| `isTrackMuteLock` | `int index` | `int` | Returns 1 if mute is locked. |
| `muteTrackLock` | `int index` | `-` | Toggles mute lock. |
| `isTrackSolo` | `int index` | `int` | Returns 1 if solo'd. |
| `soloTrack` | `int index`, `(int value=-1)`, `(int inGroup=0)` | `-` | Toggle/set solo. |

## Selection

| Command | Arguments | Returns | Description |
|---------|-----------|---------|-------------|
| `isTrackSelected` | `int index` | `int` | Returns 1 if selected. |
| `selectTrack` | `int index` | `-` | Toggle track selection. |
| `selectAll` | `-` | `-` | Select all tracks. |
| `deselectAll` | `-` | `-` | Deselect all tracks. |

## Activity / Meters

| Command | Arguments | Returns | Description |
|---------|-----------|---------|-------------|
| `getTrackActivityLevel` | `int index` | `float` | Activity level (0 if inactive). |
| `getTrackActivityLevelVis` | `int index` | `float` | Visual activity level (normalized). |

## Performance Mode & Live Clips

| Command | Arguments | Returns | Description |
|---------|-----------|---------|-------------|
| `getPerformanceModeState` | `-` | `int` | Returns 1 if playlist is in performance mode. |
| `getLiveLoopMode` | `int index` | `int` | Get live loop mode (`LiveLoop_*` constants). |
| `getLiveTriggerMode` | `int index` | `int` | Get live trigger mode (`LiveTrig_*` constants). |
| `getLivePosSnap` | `int index` | `int` | Get live position snap (`LiveSnap_*` constants). |
| `getLiveTrigSnap` | `int index` | `int` | Get live trigger snap. |
| `getLiveStatus` | `int index`, `(int mode=LB_Status_Default)` | `int` | Get live status for track. |
| `getLiveBlockStatus` | `int index`, `int blockNum`, `(int mode=LB_Status_Default)` | `int` | Get live block status (`LB_Status_*` flags). |
| `getLiveBlockColor` | `int index`, `int blockNum` | `int` | Get live block color. |
| `triggerLiveClip` | `int index`, `int blockNum`, `int flags`, `(float velocity=-1)` | `-` | Trigger live clip. `blockNum=-1` + `TLC_Fill` = stop clips on track. |
| `refreshLiveClips` | `int index`, `int value` | `-` | Refresh live clips for track. |
| `incLivePosSnap` | `int index`, `int value` | `-` | Increment live position snap. |
| `incLiveTrigSnap` | `int index`, `int value` | `-` | Increment live trigger snap. |
| `incLiveLoopMode` | `int index`, `int value` | `-` | Increment live loop mode. |
| `incLiveTrigMode` | `int index`, `int value` | `-` | Increment live trigger mode. |

## Display Zones

| Command | Arguments | Returns | Description |
|---------|-----------|---------|-------------|
| `getDisplayZone` | `-` | `int` | Returns current display zone (0 if none). |
| `lockDisplayZone` | `int index`, `int value` | `-` | Lock display zone. |
| `liveDisplayZone` | `int left`, `int top`, `int right`, `int bottom`, `(int duration=0)` | `-` | Set display zone with optional temporary duration. |

## Tools

| Command | Arguments | Returns | Description |
|---------|-----------|---------|-------------|
| `selectTool` | `int index` | `-` | Select playlist/piano roll tool (`EETool_*` constants). |
