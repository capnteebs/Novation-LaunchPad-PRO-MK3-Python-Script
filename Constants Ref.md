# Constants Reference

All `midi.*` constants used across FL Studio MIDI scripting modules.

---

## Step Parameters (`pP*`)

| Constant | Value |
|----------|-------|
| `pPitch` | 0 |
| `pVelocity` | 1 |
| `pRelease` | 2 |
| `pFinePitch` | 3 |
| `pPan` | 4 |
| `pModX` | 5 |
| `pModY` | 6 |
| `pShift` | 7 |
| `pRepeat` | 8 |

## Channel Types (`CT_*`)

| Constant | Value |
|----------|-------|
| `CT_Sampler` | 0 |
| `CT_Hybrid` | 1 |
| `CT_GenPlug` | 2 |
| `CT_Layer` | 3 |
| `CT_AudioClip` | 4 |
| `CT_AutoClip` | 5 |

## Global Transport Commands (`FPT_*`)

| Constant | Value | Constant | Value |
|----------|-------|----------|-------|
| `FPT_Jog` | 0 | `FPT_Play` | 10 |
| `FPT_Jog2` | 1 | `FPT_Stop` | 11 |
| `FPT_Strip` | 2 | `FPT_Record` | 12 |
| `FPT_StripJog` | 3 | `FPT_Rewind` | 13 |
| `FPT_StripHold` | 4 | `FPT_FastForward` | 14 |
| `FPT_Previous` | 5 | `FPT_Loop` | 15 |
| `FPT_Next` | 6 | `FPT_Mute` | 16 |
| `FPT_PreviousNext` | 7 | `FPT_Mode` | 17 |
| `FPT_MoveJog` | 8 | `FPT_Undo` | 20 |
| `FPT_UndoUp` | 21 | `FPT_Punch` | 30 |
| `FPT_UndoJog` | 22 | `FPT_PunchIn` | 31 |
| `FPT_PunchOut` | 32 | `FPT_AddMarker` | 33 |
| `FPT_MarkerJumpJog` | 35 | `FPT_MarkerSelJog` | 36 |
| `FPT_Up` | 40 | `FPT_Down` | 41 |
| `FPT_Left` | 42 | `FPT_Right` | 43 |
| `FPT_HZoomJog` | 44 | `FPT_VZoomJog` | 45 |
| `FPT_Snap` | 48 | `FPT_SnapMode` | 49 |
| `FPT_Cut` | 50 | `FPT_Copy` | 51 |
| `FPT_Paste` | 52 | `FPT_Insert` | 53 |
| `FPT_Delete` | 54 | `FPT_NextWindow` | 58 |
| `FPT_WindowJog` | 59 | `FPT_Enter` | 80 |
| `FPT_Escape` | 81 | `FPT_Menu` | 90 |
| `FPT_PatternJog` | 100 | `FPT_TrackJog` | 101 |
| `FPT_ChannelJog` | 102 | `FPT_TempoJog` | 105 |
| `FPT_TapTempo` | 106 | `FPT_NudgeMinus` | 107 |
| `FPT_NudgePlus` | 108 | `FPT_Metronome` | 110 |
| `FPT_WaitForInput` | 111 | `FPT_Overdub` | 112 |
| `FPT_LoopRecord` | 113 | `FPT_StepEdit` | 114 |
| `FPT_CountDown` | 115 | `FPT_ShuffleJog` | 122 |

## REC Event Flags

| Constant | Value |
|----------|-------|
| `REC_UpdateValue` | 1 |
| `REC_GetValue` | 2 |
| `REC_ShowHint` | 4 |
| `REC_UpdatePlugLabel` | 16 |
| `REC_UpdateControl` | 32 |
| `REC_FromMIDI` | 64 |
| `REC_Store` | 128 |
| `REC_SetChanged` | 256 |
| `REC_SetTouched` | 512 |
| `REC_Init` | 1024 |
| `REC_NoLink` | 2048 |
| `REC_InternalCtrl` | 4096 |
| `REC_PlugReserved` | 8192 |
| `REC_Smoothed` | 16384 |
| `REC_NoLastTweaked` | 32768 |
| `REC_NoSaveUndo` | 65536 |
| `REC_InitStore` | `REC_Init \| REC_Store` |
| `REC_Control` | `REC_UpdateValue \| REC_UpdateControl \| REC_ShowHint \| REC_InitStore \| REC_SetChanged \| REC_SetTouched` |
| `REC_MIDIController` | `REC_Control \| REC_FromMIDI` |

## REC Channel Event Offsets

| Constant | Value | Constant | Value |
|----------|-------|----------|-------|
| `REC_Chan_Vol` | 0 | `REC_Chan_Pan` | 1 |
| `REC_Chan_FCut` | 2 | `REC_Chan_FRes` | 3 |
| `REC_Chan_Pitch` | 4 | `REC_Chan_FType` | 5 |
| `REC_Chan_PortaTime` | 6 | `REC_Chan_Mute` | 7 |
| `REC_Chan_FXTrack` | 8 | `REC_Chan_GateTime` | 9 |
| `REC_Chan_Crossfade` | 10 | `REC_Chan_TimeOfs` | 11 |
| `REC_Chan_SwingMix` | 12 | `REC_Chan_SmpOfs` | 13 |
| `REC_Chan_StretchTime` | 14 | `REC_Chan_OfsPan` | 16 |
| `REC_Chan_OfsVol` | 17 | `REC_Chan_OfsPitch` | 18 |
| `REC_Chan_OfsFCut` | 19 | `REC_Chan_OfsFRes` | 20 |

## Pickup Modes (`PIM_*`)

| Constant | Value |
|----------|-------|
| `PIM_None` | 0 |
| `PIM_AlwaysPickup` | 1 |
| `PIM_FollowGlobal` | 2 |

## Snap Modes

| Constant | Value | Constant | Value |
|----------|-------|----------|-------|
| `Snap_Line` | 0 | `Snap_Cell` | 1 |
| `Snap_None` | 3 | `Snap_SixthStep` | 4 |
| `Snap_FourthStep` | 5 | `Snap_ThirdStep` | 6 |
| `Snap_HalfStep` | 7 | `Snap_Step` | 8 |
| `Snap_SixthBeat` | 9 | `Snap_FourthBeat` | 10 |
| `Snap_ThirdBeat` | 11 | `Snap_HalfBeat` | 12 |
| `Snap_Beat` | 13 | `Snap_Bar` | 14 |

## PME Flags

| Constant | Value |
|----------|-------|
| `PME_System` | 2 |
| `PME_System_Safe` | 4 |
| `PME_PreviewNote` | 8 |
| `PME_FromHost` | 16 |
| `PME_FromMIDI` | 32 |

## Window Constants (`wid*`)

| Constant | Value |
|----------|-------|
| `widMixer` | 0 |
| `widChannelRack` | 1 |
| `widPlaylist` | 2 |
| `widPianoRoll` | 3 |
| `widBrowser` | 4 |
| `widPlugin` | 5 |
| `widPluginEffect` | 6 |
| `widPluginGenerator` | 7 |

## Playlist Tool Constants (`EETool_*`)

| Constant | Value |
|----------|-------|
| `EETool_Pencil` | 0 |
| `EETool_Brush` | 1 |
| `EETool_Del` | 2 |
| `EETool_IP` | 3 |
| `EETool_Sel` | 4 |
| `EETool_Zoom` | 5 |
| `EETool_Cut` | 6 |
| `EETool_Play` | 7 |
| `EETool_Slip` | 8 |
| `EETool_Mute` | 9 |
| `EETool_Step` | 10 |

## Live Block Status Flags

| Constant | Value |
|----------|-------|
| `LB_Status_Filled` | 1 |
| `LB_Status_Scheduled` | 2 |
| `LB_Status_Playing` | 4 |

## Live Loop Modes

| Constant | Value |
|----------|-------|
| `LiveLoop_Stay` | 0 |
| `LiveLoop_OneShot` | 1 |
| `LiveLoop_MarchWrap` | 2 |
| `LiveLoop_MarchStay` | 3 |
| `LiveLoop_MarchStop` | 4 |
| `LiveLoop_Random` | 5 |
| `LiveLoop_ExRandom` | 6 |

## Live Trigger Modes

| Constant | Value |
|----------|-------|
| `LiveTrig_Retrigger` | 0 |
| `LiveTrig_Hold` | 1 |
| `LiveTrig_HMotion` | 2 |
| `LiveTrig_Latch` | 3 |

## Live Snap Constants

| Constant | Value |
|----------|-------|
| `LiveSnap_Off` | 0 |
| `LiveSnap_Fourth` | 1 |
| `LiveSnap_Half` | 2 |
| `LiveSnap_One` | 3 |
| `LiveSnap_Two` | 4 |
| `LiveSnap_Four` | 5 |
| `LiveSnap_Auto` | 6 |

## TLC (Trigger Live Clip) Flags

| Constant | Value |
|----------|-------|
| `TLC_MuteOthers` | 1 |
| `TLC_Fill` | 2 |
| `TLC_Queue` | 4 |
| `TLC_GlobalSnap` | 8 |
| `TLC_NoSnap` | 16 |
| `TLC_Release` | 32 |
| `TLC_NoPlayCheck` | 64 |
| `TLC_ColumnMode` | 128 |
| `TLC_WeakColumnMode` | 256 |
| `TLC_TriggerCheckColumnMode` | 512 |
| `TLC_TrackSnap` | 0 |
| `TLC_SubNum_Normal` | 0 |
| `TLC_SubNum_ClipPos` | 65536 |
| `TLC_SubNum_GroupNum` | 131072 |
| `TLC_SubNum_Read` | 196608 |
| `TLC_SubNum_Leave` | 262144 |
| `TLC_NoHardwareUpdate` | 1073741824 |
| `TLC_SecondPass` | 2147483648 |

## Mixer Position Functions

| Command | Arguments | Returns | Description |
|---------|-----------|---------|-------------|
| `mixer.getSongStepPos` | `-` | `int` | Returns current song step position. |
| `mixer.getSongTickPos` | `(int mode=ST_Int)` | `int/float` | Returns song tick position. `ST_Int`=0, `ST_Beat`=1, `ST_PGB`=2. |
| `mixer.getCurrentTempo` | `(int asInt=0)` | `int/float` | Returns current tempo (BPM). |
| `mixer.setCurrentTempo` | `float/int tempo`, `(int asInt=0)` | `-` | Sets current tempo. |
| `mixer.getRecPPS` | `-` | `int` | Returns recording PPS (positions per second). |
