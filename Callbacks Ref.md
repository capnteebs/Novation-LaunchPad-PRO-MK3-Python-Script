# Callback Functions (Script Events)

Functions FL Studio calls on your script in response to events.

---

## Lifecycle

| Callback | Arguments | Description |
|----------|-----------|-------------|
| `OnInit` | `-` | Called when script starts. |
| `OnDeInit` | `-` | Called before script stops. |
| `OnFirstConnect` | `-` | Device connected for the first time. |

## MIDI Input

Called in order — set `eventData.handled = True` to stop propagation.

| Callback | Arguments | Description |
|----------|-----------|-------------|
| `OnMidiIn` | `eventData` | **First** callback when MIDI received. Only raw data available. |
| `OnMidiMsg` | `eventData` | Processes messages not handled by `OnMidiIn`. Parsed data available. |
| `OnSysEx` | `eventData` | SysEx messages not handled by `OnMidiIn`. |
| `OnNoteOn` | `eventData` | Note-on messages not handled by `OnMidiMsg`. |
| `OnNoteOff` | `eventData` | Note-off messages not handled by `OnMidiMsg`. |
| `OnControlChange` | `eventData` | CC messages not handled by `OnMidiMsg`. |
| `OnProgramChange` | `eventData` | Program change messages. |
| `OnPitchBend` | `eventData` | Pitch bend messages. |
| `OnKeyPressure` | `eventData` | Key (polyphonic) aftertouch. |
| `OnChannelPressure` | `eventData` | Channel aftertouch. |
| `OnMidiOutMsg` | `eventData` | Short MIDI output from MIDI Out plugin. |

### `eventData` Properties

| Property | Type | R/W | Description |
|----------|------|-----|-------------|
| `handled` | bool | R/W | Set True to stop event propagation. |
| `timestamp` | time | R | Event timestamp. |
| `status` | int | R/W | MIDI status byte. |
| `data1` | int | R/W | First data byte. |
| `data2` | int | R/W | Second data byte. |
| `port` | int | R | MIDI input port number. |
| `note` | int | R/W | MIDI note number. |
| `velocity` | int | R/W | Note velocity. |
| `pressure` | int | R/W | Aftertouch pressure. |
| `progNum` | int | R | Program change number. |
| `controlNum` | int | R | CC control number. |
| `controlVal` | int | R | CC control value. |
| `pitchBend` | int | R | Pitch bend value. |
| `sysex` | bytes | R/W | SysEx message data. |
| `isIncrement` | bool | R/W | Whether value is an increment. |
| `res` | float | R/W | MIDI resolution. |
| `inEv` | int | R/W | Original MIDI event value. |
| `outEv` | int | R/W | Output event value. |
| `midiId` | int | R/W | MIDI message type identifier. |
| `midiChan` | int | R/W | MIDI channel (0-based). |
| `midiChanEx` | int | R/W | Extended MIDI channel. |
| `pmeFlags` | int | R | Permission/mode event flags (`PME_*`). |

## Timing & Beat Events

| Callback | Arguments | Description |
|----------|-----------|-------------|
| `OnIdle` | `-` | Called periodically. Use for small UI tasks (meters, LEDs). |
| `OnUpdateBeatIndicator` | `int value` | Fires when beat indicator changes. `0`=off, `1`=bar (beat 1), `2`=beat (other beats). |
| `OnUpdateMeters` | `-` | Called to update peak meters. Must enable with `device.setHasMeters()` in `OnInit`. |

## State Changes

| Callback | Arguments | Description |
|----------|-----------|-------------|
| `OnRefresh` | `int flags` | FL Studio state changed. Flags are bitmask of `HW_Dirty_*` constants. |
| `OnDoFullRefresh` | `-` | Like `OnRefresh` but requires a complete UI update. |
| `OnProjectLoad` | `int status` | Project load: 0=start, 100=success, 101=error. |
| `OnDirtyChannel` | `int index`, `int flag` | Channel changed. `flag`: 0=new, 1=delete, 2=replace, 3=rename, 4=select. |
| `OnDirtyMixerTrack` | `int index` | Mixer track changed. `index=-1` = all tracks. |

### `OnRefresh` Flags (`HW_Dirty_*`)

| Constant | Value | Description |
|----------|-------|-------------|
| `HW_Dirty_Mixer_Sel` | 1 | Mixer selection changed. |
| `HW_Dirty_Mixer_Display` | 2 | Mixer display changed. |
| `HW_Dirty_Mixer_Controls` | 4 | Mixer controls changed. |
| `HW_Dirty_RemoteLinks` | 16 | Remote control links changed. |
| `HW_Dirty_FocusedWindow` | 32 | Focused window changed. |
| `HW_Dirty_Performance` | 64 | Performance mode changed. |
| `HW_Dirty_LEDs` | 256 | LEDs need update (play/stop/record/active window). |
| `HW_Dirty_RemoteLinkValues` | 512 | Remote link values changed. |
| `HW_Dirty_Patterns` | 1024 | Patterns changed. |
| `HW_Dirty_Tracks` | 2048 | Tracks changed. |
| `HW_Dirty_ControlValues` | 4096 | Control values changed. |
| `HW_Dirty_Colors` | 8192 | Colors changed. |
| `HW_Dirty_Names` | 16384 | Names changed. |
| `HW_Dirty_ChannelRackGroup` | 32768 | Channel rack group changed. |
| `HW_ChannelEvent` | 65536 | Channel event. |

## Performance & Display

| Callback | Arguments | Description |
|----------|-----------|-------------|
| `OnUpdateLiveMode` | `int lastTrack` | Performance mode state changed. |
| `OnDisplayZone` | `-` | Playlist display zone changed. |
| `OnWaitingForInput` | `-` | FL Studio enters waiting-for-input mode. |
| `OnSendTempMsg` | `string message`, `int duration` | Hint message sent for controller display. |
