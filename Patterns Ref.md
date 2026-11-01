# Patterns Module

Controls FL Studio patterns — selection, properties, length, and groups.

---

## Current Pattern

| Command | Arguments | Returns | Description |
|---------|-----------|---------|-------------|
| `patternNumber` | `-` | `int` | Returns the current pattern number. |
| `patternCount` | `-` | `int` | Returns the number of patterns. |
| `patternMax` | `-` | `int` | Returns the maximum pattern number. |
| `jumpToPattern` | `int index` | `-` | Jump to pattern at index. |

## Pattern Properties

| Command | Arguments | Returns | Description |
|---------|-----------|---------|-------------|
| `getPatternName` | `int index` | `string` | Returns pattern name. |
| `setPatternName` | `int index`, `string name` | `-` | Sets pattern name. |
| `getPatternColor` | `int index` | `int` | Returns pattern color. |
| `setPatternColor` | `int index`, `int color` | `-` | Sets pattern color. |
| `getPatternLength` | `int index` | `int` | Returns pattern length in beats. |
| `setPatternLength` | `int index`, `int length` | `-` | Sets pattern length in beats. (v39+) |
| `incrementPatternLength` | `int index`, `int offset` | `-` | Increments pattern length by offset beats. (v39+) |
| `isPatternDefault` | `int index` | `int` | Returns 1 if pattern is default (empty/unchanged). |

## Pattern Selection

| Command | Arguments | Returns | Description |
|---------|-----------|---------|-------------|
| `isPatternSelected` | `int index` | `int` | Returns 1 if selected in Picker panel. |
| `selectPattern` | `int index`, `(int value=-1)`, `(int preview=0)` | `-` | Select pattern in Picker panel. `value`: 1=select, 0=deselect, -1=toggle. |
| `selectAll` | `-` | `-` | Select all patterns. |
| `deselectAll` | `-` | `-` | Deselect all patterns. |

## Pattern Operations

| Command | Arguments | Returns | Description |
|---------|-----------|---------|-------------|
| `clonePattern` | `(int index=-1)` | `-` | Clone selected pattern(s). |
| `movePattern` | `(int direction=1)` | `-` | Move selected pattern(s). 1=up, -1=down. |
| `findFirstNextEmptyPat` | `int flags`, `(int x=-1)`, `(int y=-1)` | `-` | Find first empty pattern (`FFNEP_*` flags). |
| `burnLoop` | `int index`, `(int storeUndo=1)`, `(int updateUi=1)` | `-` | Burn loop. |
| `getBlockSetStatus` | `int left`, `int top`, `int right`, `int bottom` | `int` | Returns block set status. |
| `ensureValidNoteRecord` | `int index`, `(int playNow=0)` | `-` | Ensure valid note for pattern recording. |

## Pattern Groups

| Command | Arguments | Returns | Description |
|---------|-----------|---------|-------------|
| `getActivePatternGroup` | `-` | `int` | Returns active pattern group index (-1 = "All patterns"). |
| `getPatternGroupCount` | `-` | `int` | Returns number of pattern groups. |
| `getPatternGroupName` | `int index` | `str` | Returns pattern group name. |
| `getPatternsInGroup` | `int index` | `tuple[int, ...]` | Returns tuple of pattern indices in group. |
