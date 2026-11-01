# Launchpad Pro MK3 — Programmer Mode MIDI Map

Complete MIDI mapping for Programmer Mode. All buttons (everything except the 8x8 grid pads) send CC messages. Only the 8x8 grid pads send Note On/Off.

---

## Full Layout Diagram

`N` = Note On/Off, `C` = CC (Control Change). All on MIDI Channel 1.

```
 [C:99] [C:90] [C:91] [C:92] [C:93] [C:94] [C:95] [C:96] [C:97] [C:98]
  Logo   Shift  Left   Right  Session Note   Chord  Custom Seq    Projects

 [C:80]  N:81   N:82   N:83   N:84   N:85   N:86   N:87   N:88  [C:89]
   Up                                                             Patterns
 [C:70]  N:71   N:72   N:73   N:74   N:75   N:76   N:77   N:78  [C:79]
  Down                                                            Steps
 [C:60]  N:61   N:62   N:63   N:64   N:65   N:66   N:67   N:68  [C:69]
  Clear                                                           PatSettings
 [C:50]  N:51   N:52   N:53   N:54   N:55   N:56   N:57   N:58  [C:59]
  Dupl                                                            Velocity
 [C:40]  N:41   N:42   N:43   N:44   N:45   N:46   N:47   N:48  [C:49]
  Quant                                                           Probability
 [C:30]  N:31   N:32   N:33   N:34   N:35   N:36   N:37   N:38  [C:39]
  FixLen                                                          Mutation
 [C:20]  N:21   N:22   N:23   N:24   N:25   N:26   N:27   N:28  [C:29]
  Play                                                            MicroStep
 [C:10]  N:11   N:12   N:13   N:14   N:15   N:16   N:17   N:18  [C:19]
  Rec                                                             PrintToClip

        [C:101][C:102][C:103][C:104][C:105][C:106][C:107][C:108]
         TrkSel TrkSel TrkSel TrkSel TrkSel TrkSel TrkSel TrkSel
          1      2      3      4      5      6      7      8

         [C:1]  [C:2]  [C:3]  [C:4]  [C:5]  [C:6]  [C:7]  [C:8]
        RecArm  Mute   Solo    Vol    Pan   Sends  Device  Stop
```

---

## 1. 8x8 Pad Grid — Note On/Off

Velocity-sensitive (1-127). Also sends Polyphonic Aftertouch (0xA0).

```
        Col1  Col2  Col3  Col4  Col5  Col6  Col7  Col8
Row 8:   81    82    83    84    85    86    87    88
Row 7:   71    72    73    74    75    76    77    78
Row 6:   61    62    63    64    65    66    67    68
Row 5:   51    52    53    54    55    56    57    58
Row 4:   41    42    43    44    45    46    47    48
Row 3:   31    32    33    34    35    36    37    38
Row 2:   21    22    23    24    25    26    27    28
Row 1:   11    12    13    14    15    16    17    18
```

- **Message:** Note On (0x90) / Note Off (0x80), Channel 1
- **Velocity:** 1-127 (pressure-sensitive)
- **Note number:** row * 10 + col (1-indexed, bottom-left = 11)

## 2. Right Column — CC

One button per row. Values: 127 press, 0 release.

| Row | CC | Label | Shift Label |
|-----|----|-------|-------------|
| 8 | 89 | Patterns | - |
| 7 | 79 | Steps | - |
| 6 | 69 | Pattern Settings | - |
| 5 | 59 | Velocity | - |
| 4 | 49 | Probability | - |
| 3 | 39 | Mutation | - |
| 2 | 29 | Micro Step | - |
| 1 | 19 | Print to Clip | - |

## 3. Left Column — CC

One button per row. Values: 127 press, 0 release.

| Row | CC | Label | Shift Label |
|-----|----|-------|-------------|
| 8 | 80 | Up | - |
| 7 | 70 | Down | - |
| 6 | 60 | Clear | - |
| 5 | 50 | Duplicate | Double |
| 4 | 40 | Quantise | Record Quantise |
| 3 | 30 | Fixed Length | - |
| 2 | 20 | Play | - |
| 1 | 10 | Record | Capture MIDI |

## 4. Top Row — CC

Values: 127 press, 0 release.

| Position | CC | Label | Shift Label |
|----------|-----|-------|-------------|
| - | 90 | Shift | - |
| 1 | 91 | Left | - |
| 2 | 92 | Right | - |
| 3 | 93 | Session | - |
| 4 | 94 | Note | - |
| 5 | 95 | Chord | - |
| 6 | 96 | Custom | - |
| 7 | 97 | Sequencer | - |
| 8 | 98 | Projects | Save |

## 5. Track Select Row — CC

Thin row between grid and bottom labeled row. Values: 127 press, 0 release.

| Position | CC | Label |
|----------|-----|-------|
| 1 | 101 | Track Select 1 |
| 2 | 102 | Track Select 2 |
| 3 | 103 | Track Select 3 |
| 4 | 104 | Track Select 4 |
| 5 | 105 | Track Select 5 |
| 6 | 106 | Track Select 6 |
| 7 | 107 | Track Select 7 |
| 8 | 108 | Track Select 8 |

## 6. Bottom Row — CC

Values: 127 press, 0 release.

| Position | CC | Label | Shift Label |
|----------|-----|-------|-------------|
| 1 | 1 | Record Arm | Undo |
| 2 | 2 | Mute | Redo |
| 3 | 3 | Solo | Click |
| 4 | 4 | Volume | - |
| 5 | 5 | Pan | - |
| 6 | 6 | Sends | Tap |
| 7 | 7 | Device | Tempo |
| 8 | 8 | Stop Clip | Swing |

## 7. Logo Button — CC

| Control | CC |
|---------|----|
| Novation Logo (top-left) | 99 |

---

## LED Feedback

To light any pad or button, send the corresponding message type back to the device:

- **Grid pads (notes 11-88):** Send Note On (0x90) with note number + color value
- **All buttons (CCs):** Send CC (0xB0) with CC number + color value

### Animation Channels

| Channel | Animation |
|---------|-----------|
| 0 (0x90/0xB0) | Solid |
| 1 (0x91/0xB1) | Flashing |
| 2 (0x92/0xB2) | Pulsing |

---

## SysEx

Header: `F0 00 20 29 02 0E`

| Command | SysEx |
|---------|-------|
| Enter Programmer Mode | `F0 00 20 29 02 0E 0E 01 F7` |
| Exit Programmer Mode | `F0 00 20 29 02 0E 0E 00 F7` |

---

## Hex Quick Reference

| Control | Decimal | Hex |
|---------|---------|-----|
| Bottom row CC 1-8 | 1-8 | 0x01-0x08 |
| Left col CC 10-80 | 10,20,...,80 | 0x0A,0x14,0x1E,0x28,0x32,0x3C,0x46,0x50 |
| Shift | 90 | 0x5A |
| Grid bottom-left | 11 | 0x0B |
| Grid bottom-right | 18 | 0x12 |
| Grid top-left | 81 | 0x51 |
| Grid top-right | 88 | 0x58 |
| Right col CC 19-89 | 19,29,...,89 | 0x13,0x1D,0x27,0x31,0x3B,0x45,0x4F,0x59 |
| Top row CC 91-98 | 91-98 | 0x5B-0x62 |
| Logo CC 99 | 99 | 0x63 |
| Track select CC 101-108 | 101-108 | 0x65-0x6C |
