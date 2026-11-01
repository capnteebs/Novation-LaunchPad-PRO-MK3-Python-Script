# Channels Module

Allows you to control FL Studio Channels.

> `index` respects channel groups, `indexGlobal` is the global index.

---

## Channel Selection

| Command | Arguments | Returns | Description | Version |
|---------|-----------|---------|-------------|---------|
| `selectedChannel` | `(int canBeNone=0)`, `(int offset=0)`, `(int indexGlobal=0)` | `int` | Returns index (respecting groups) of the first selected channel. Returns 0 when no selection (or -1 if `canBeNone` is 1). Use `offset` to find other selected channels. Set `indexGlobal` to 1 to return global index. | 5 |
| `channelNumber` | `(int canBeNone=0)`, `(int offset=0)` | `int` | Returns `indexGlobal` of the first selected channel. Returns -1 when no selection (or 0 if `canBeNone` is 1). Use `offset` to find other selected channels. | 1 |
| `channelCount` | `(int globalCount*=0)` | `int` | Returns number of channels respecting groups. Set `globalCount` to 1 to get count of all channels. | 1, *3 |
| `isChannelSelected` | `int index`, `(bool useGlobalIndex*=False)` | `int` | Returns True if channel at `index` is selected. | 1, *33 |
| `selectOneChannel` | `int index`, `(bool useGlobalIndex*=False)` | `-` | Select channel at `index` exclusively. | 8, *33 |
| `selectChannel` | `int index`, `(int value=-1)`, `(bool useGlobalIndex*=False)` | `-` | Toggle selection of channel at `index`. Set `value` to 1 (select) or 0 (deselect) to not toggle. | 1, *33 |
| `selectAll` | `-` | `-` | Select all channels in the current channel group. | 1 |
| `deselectAll` | `-` | `-` | Deselect all channels in the current channel group. | 1 |

## Channel Properties

| Command | Arguments | Returns | Description | Version |
|---------|-----------|---------|-------------|---------|
| `getChannelName` | `int index`, `(bool useGlobalIndex*=False)` | `string` | Returns the name of channel at `index`. | 1, *33 |
| `setChannelName` | `int index`, `string name`, `(bool useGlobalIndex*=False)` | `-` | Changes the name of channel at `index` to `name`. | 1, *33 |
| `getChannelColor` | `int index`, `(bool useGlobalIndex*=False)` | `int` | Returns the color of channel at `index`. | 1, *33 |
| `setChannelColor` | `int index`, `int color`, `(bool useGlobalIndex*=False)` | `-` | Changes the color of channel at `index` to `color`. | 1, *33 |
| `getChannelType` | `int index`, `(bool useGlobalIndex*=False)` | `int` | Returns the type of channel. | 19, *33 |
| `getChannelIndex` | `int index` | `int` | Returns `indexGlobal` for channel at `index` (respecting groups). | 1 |
| `getChannelMidiInPort` | `int index`, `(bool useGlobalIndex*=False)` | `int` | Returns MIDI port for channel at `index`. Special values: `-3` = touch keyboard, `-2` = selected channel only, `-1` = typing keyboard. | 1, *33 |
| `getTargetFxTrack` | `int index`, `(bool useGlobalIndex*=False)` | `int` | Returns target FX track for channel at `index`. | 1, *33 |
| `setTargetFxTrack` | `int channelIndex`, `int mixerIndex`, `(bool useGlobalIndex*=False)` | `-` | Routes channel at `channelIndex` to mixer track at `mixerIndex`. | 28, *33 |

## Volume, Pan, Pitch

| Command | Arguments | Returns | Description | Version |
|---------|-----------|---------|-------------|---------|
| `getChannelVolume` | `int index`, `(int useDb*=0)`, `(bool useGlobalIndex**=False)` | `float` | Returns normalized volume (0 to 1.0) of channel at `index`. Set `useDb` to 1 for dB. | 1, *14, **33 |
| `setChannelVolume` | `int index`, `float volume`, `(int pickupMode*=PIM_None)`, `(bool useGlobalIndex**=False)` | `-` | Changes volume for channel at `index` (0 to 1.0). Use `pickupMode` to override FL default pickup option. | 1, *13, **33 |
| `getChannelPan` | `int index`, `(bool useGlobalIndex*=False)` | `float` | Returns pan value for channel at `index` (-1.0 to +1.0). | 1, *33 |
| `setChannelPan` | `int index`, `float pan`, `(int pickupMode*=PIM_None)`, `(bool useGlobalIndex**=False)` | `-` | Changes pan value of channel at `index` (-1.0 to +1.0). Use `pickupMode` to override FL default pickup option. | 1, *13, **33 |
| `getChannelPitch` | `int index`, `(int mode=0)`, `(bool useGlobalIndex*=False)` | `float/int` | Returns pitch value (-1.0 to +1.0). `mode=1` for semitones, `mode=2` for pitch range. | 8, *33 |
| `setChannelPitch` | `int index`, `float value`, `(int pitchUnit=0)`, `(int pickupMode*=PIM_None)`, `(bool useGlobalIndex**=False)` | `-` | Changes pitch value (-1.0 to +1.0). `pitchUnit=1` for semitones, `pitchUnit=2` for pitch range. Use `pickupMode` to override FL default pickup option. | 8, *13, **33 |

## Mute / Solo

| Command | Arguments | Returns | Description | Version |
|---------|-----------|---------|-------------|---------|
| `isChannelMuted` | `int index`, `(bool useGlobalIndex*=False)` | `int` | Returns True if channel at `index` is muted. | 1, *33 |
| `muteChannel` | `int index`, `(int value=-1)`, `(bool useGlobalIndex*=False)` | `-` | Toggles mute state of channel at `index`. Set `value` to 1 (mute) or 0 (unmute) to not toggle. | 1, *33 |
| `isChannelSolo` | `int index`, `(bool useGlobalIndex*=False)` | `int` | Returns True if channel at `index` is soloed. | 1, *33 |
| `soloChannel` | `int index`, `(int value*=-1)`, `(bool useGlobalIndex**=False)` | `-` | Toggles solo state of channel at `index`. Set `value` to 1 (solo) or 0 (unsolo) to not toggle. | 1, *30, **33 |

## Channel Events

| Command | Arguments | Returns | Description | Version |
|---------|-----------|---------|-------------|---------|
| `getRecEventId` | `int index`, `(bool useGlobalIndex*=False)` | `int` | Returns eventID for channel at `index`. Use with `processRECEvent`. | 1 |
| `incEventValue` | `int eventId`, `int step`, `(float res*)` | `int` | Returns event value increased by `step`. Use `res` to specify increment resolution (default 1/24). Use result as new value in `processRECEvent`. | 1, *20 |

**Example** - increase volume of first channel:
```python
step = 1
eventId = midi.REC_Chan_Vol + channels.getRecEventId(0)
newValue = channels.incEventValue(eventId, step)
general.processRECEvent(eventId, newValue, midi.REC_UpdateValue | midi.REC_UpdateControl)
```

## Channel Grid Bits

| Command | Arguments | Returns | Description | Version |
|---------|-----------|---------|-------------|---------|
| `isGridBitAssigned` | `int index`, `(bool useGlobalIndex*=False)` | `int` | Returns 1 when grid bit for channel at `index` is assigned. | 30, *33 |
| `getGridBit` | `int index`, `int position`, `(bool useGlobalIndex*=False)` | `int` | Returns grid bit at `position` for channel at `index`. | 1, *33 |
| `setGridBit` | `int index`, `int position`, `int value`, `(bool useGlobalIndex*=False)` | `-` | Set grid bit value at `position` for channel at `index`. | 1, *33 |
| `getStepParam` | `int step`, `int param`, `int offset`, `int startPos`, `(int padsStride=16)`, `(bool useGlobalIndex*=False)` | `int` | Get step parameter for step at `step`. | 1, *33 |
| `getCurrentStepParam` | `int index`, `int step`, `int param`, `(bool useGlobalIndex=False)` | `int` | Get current step parameter for channel at `index` and step at `step`. | 1 |
| `setStepParameterByIndex` | `int index`, `int patNum`, `int step`, `int param`, `int value`, `(bool useGlobalIndex=False)` | `-` | Set current step parameter for channel at `index` and step at `step`. | 1 |
| `getGridBitWithLoop` | `int index`, `int position`, `(bool useGlobalIndex*=False)` | `int` | Get grid bit with loop for channel at `index`. | 1, *33 |

## Editor / UI

| Command | Arguments | Returns | Description | Version |
|---------|-----------|---------|-------------|---------|
| `showGraphEditor` | `bool temporary`, `int param`, `int step`, `int index`, `(bool useGlobalIndex*=False)` | `-` | Show graph editor for channel at `index` and step at `step`. Set `temporary` to False to keep open. | 1, *20 |
| `isGraphEditorVisible` | `-` | `bool` | Returns whether the graph editor is currently visible. | - |
| `showEditor` | `int index`, `(int value*=-1)`, `(bool useGlobalIndex**=False)` | `-` | Show/hide editor (plugin window) for channel at `index`. Set `value` to 1 (show) or 0 (hide). | 1, *3, **33 |
| `focusEditor` | `int index`, `(bool useGlobalIndex*=False)` | `-` | Focus editor (plugin window) for channel at `index`. | 1, *33 |
| `showCSForm` | `int index`, `(int state*=1)`, `(bool useGlobalIndex**=False)` | `-` | Show channel settings (or plugin window) for channel at `index`. `state`: 0 (close), 1 (open), -1 (toggle). | 1, *9, **33 |

## Misc

| Command | Arguments | Returns | Description | Version |
|---------|-----------|---------|-------------|---------|
| `midiNoteOn` | `int indexGlobal`, `int note`, `int velocity`, `(int channel=-1)` | `-` | Set MIDI note for channel at `indexGlobal`. | 1 |
| `getActivityLevel` | `int index`, `(bool useGlobalIndex*=False)` | `float` | Returns activity level for channel at `index`. | 9, *33 |
| `isHighLighted` | `-` | `int` | Returns True when red highlight rectangle is active in channel rack. | 1 |
| `quickQuantize` | `int index`, `(int startOnly=1)`, `(bool useGlobalIndex*=False)` | `-` | Perform quick quantize for channel at `index`. | 9, *33 |
| `rerollLoopStarterLoop` | `int index`, `(bool useGlobalIndex=True)` | `-` | Same as clicking the dice button on Loopstarter audio loop channels. | 39 |
