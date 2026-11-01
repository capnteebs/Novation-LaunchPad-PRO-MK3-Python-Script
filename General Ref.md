# General Module

Undo history, timing/timebase, project info, and utility functions.

---

## Undo

| Command | Arguments | Returns | Description |
|---------|-----------|---------|-------------|
| `saveUndo` | `string undoName`, `int flags`, `(int updateHistory=1)` | `-` | Save undo history point (`UF_*` flags). |
| `undo` | `-` | `int` | Undo (Ctrl+Z). |
| `undoUp` | `-` | `int` | Move up one undo level. |
| `undoDown` | `-` | `int` | Move down one undo level. |
| `undoUpDown` | `int offset` | `int` | Move by offset in undo history. |
| `restoreUndoLevel` | `int level` | `-` | Restore to specific undo point. |
| `getUndoLevelHint` | `-` | `string` | Returns hint for current undo level. |
| `getUndoHistoryPos` | `-` | `int` | Returns undo history position. |
| `getUndoHistoryCount` | `-` | `int` | Returns undo history count. |
| `getUndoHistoryLast` | `-` | `int` | Returns last undo history position. |
| `setUndoHistoryPos` | `int index` | `-` | Sets undo history position. |
| `setUndoHistoryCount` | `int value` | `-` | Sets undo history count. |
| `setUndoHistoryLast` | `int index` | `-` | Sets last undo history position. |

## Timing / Timebase

| Command | Arguments | Returns | Description |
|---------|-----------|---------|-------------|
| `getRecPPB` | `-` | `int` | Returns timebase x numerator (ticks per bar). |
| `getRecPPQ` | `-` | `int` | Returns timebase (PPQ — pulses per quarter note). |
| `setRecPPQ` | `int ppq` | `-` | Sets timebase. |
| `setNumerator` | `int numerator` | `-` | Sets time signature numerator. |
| `setDenominator` | `int denominator` | `-` | Sets time signature denominator. |

## Metronome

| Command | Arguments | Returns | Description |
|---------|-----------|---------|-------------|
| `getUseMetronome` | `-` | `int` | Returns 1 if metronome is enabled. |
| `getPrecount` | `-` | `int` | Returns precount value. |

## Project Info

| Command | Arguments | Returns | Description |
|---------|-----------|---------|-------------|
| `getProjectTitle` | `-` | `string` | Returns project title. |
| `getProjectAuthor` | `-` | `string` | Returns project author. |
| `getProjectGenre` | `-` | `string` | Returns project genre. |
| `getVersion` | `-` | `int` | Returns API version number. |
| `getChangedFlag` | `-` | `int` | Returns: 0=clean, 1=dirty, 2=dirty but clean for autosave. |

## Utility

| Command | Arguments | Returns | Description |
|---------|-----------|---------|-------------|
| `processRECEvent` | `int eventId`, `int value`, `int flags` | `-` | Process a REC event. **Deprecated as of v38.** |
| `safeToEdit` | `-` | `int` | Returns 1 when safe to use setter functions. |
| `dumpScoreLog` | `int time`, `(int silent=0)` | `-` | Dump score log. |
| `clearLog` | `-` | `-` | Clear log. |
