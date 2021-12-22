# qtile-MutableScratch

This package is a series of functions and a class to create a "scratch" space
in qtile more similar to i3's. qtile has the `ScratchPad` group type, but the
(documented) purpose is to only host `Dropdown` windows that must be specified
ahead of time.

Instead, what `MutableScratch` does is piggybacks onto an "invisible" qtile
`Group` (ie. a group named `''`) and provide functions to dynamically add and
remove windows to this group. Viewing the "hidden" windows is done via a toggle
function, which cycles through the windows in the Scratch group. All windows
added to the `MutableScratch` group will be automatically converted to
floating. This emulates the scratch functionality of i3 as closely as possible.


## Setup

Put the following default configuration in your `config.py`:
```python
## Setup MutableScratch
mutscr = MutableScratch()
groups.append(Group(''))

keys.extend( [
    EzKey('M-S-<minus>', mutscr.add_current_window()),
    EzKey('M-<minus>',   mutscr.toggle()),
    EzKey('M-C-<minus>', mutscr.remove()),
] )

hook.subscribe.startup_complete(minscr.qtile_startup)
```

## Usage

1. Add the current window to the `MutableScratch` group via `MutableScratch.add_current_window()`
    - This will move the window to the invisible group
2. Rotate through windows in the `MutableScratch` group via `MutableScratch.toggle()`
    - If the current window is apart of the `MutableScratch` group, then it
      will be moved back to the invisible group
    - If the current window is not apart of the `MutableScratch`, then the next
      `MutableScratch` window in the stack will be moved to the current group
3. To remove a window from the `MutableScratch` group, use `MutableScratch.remove()`

## Implementation Details

### Tracking members of the `MutableScratch` group

This is done by adding an attribute to the window object that simply stores a
boolean.

### Cycling through windows in `MutableScratch`

`MutableScratch` has something similar to qtile's `focus_history` for groups.
It's effectively just a stack of windows belonging to the `MutableScratch`
group, where windows are pushed and popped from the stack. This ensures that
the every window in the `MutableScratch` group can be accessed via toggle

### Initializing the `MutableScratch` on qtile start

When restarting qtile, the `MutableScratch` instance in `config.py` will be
overwritten, losing the stack history and the floating
