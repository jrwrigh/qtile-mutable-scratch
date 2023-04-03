# qtile MutableScratch

![PyPI](https://img.shields.io/pypi/v/qtile-mutable_scratch)

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

See [repository README for most up-to-date documentation](https://github.com/jrwrigh/qtile-mutable-scratch).

## Installation

You can now install via `pip`:
```
pip install qtile_mutable_scratch
```

## Setup

Put the following default configuration in your `config.py`:
```python
import qtile_mutable_scratch
from libqtile.config import EzKey
from libqtile import hook
...

mutscr = qtile_mutable_scratch.MutableScratch()
groups.append(Group('')) # Must be after `groups` is created

keys.extend( [
    EzKey('M-S-<minus>', mutscr.add_current_window()),
    EzKey('M-C-<minus>', mutscr.remove_current_window()),
    EzKey('M-<minus>',   mutscr.toggle()),
] )

hook.subscribe.startup_complete(mutscr.qtile_startup)
```

Each `MutableScratch` instance has two parameters to chose from, `scratch_group_name` and
`win_attr`.
It's not necessary to set these, as the default configuration
should work for every configuration.
`scratch_group_name` (default `''`, or the empty name group) sets the name of the group that will old the scratch windows.
`win_attr` (default `mutscratch`) sets the attribute that will be set on each window to tag it as being apart of the `MutableScratch` system.

## Usage

1. Add the current window to the `MutableScratch` group via `MutableScratch.add_current_window()`
    - This will move the window to the invisible group
2. Rotate through windows in the `MutableScratch` group via `MutableScratch.toggle()`
    - If the current window is apart of the `MutableScratch` group, then it will be moved back to the invisible group
    - If the current window is not apart of the `MutableScratch`, then the next `MutableScratch` window in the stack will be moved to the current group
3. To remove a window from the `MutableScratch` group, use `MutableScratch.remove()`

### Hastily thrown together demo video:
It's ugly, but it get's the point across...hopefully.

https://user-images.githubusercontent.com/20801821/147259912-5acec613-239b-4fe3-aebb-9c1820426d2c.mp4


## Implementation Details

### Tracking members of the `MutableScratch` group

This is done by dynamically adding an attribute (by default `mutscratch`) to
the window object that simply stores a boolean.

### Cycling through windows in `MutableScratch`

`MutableScratch` has something similar to qtile's `focus_history` for groups.
It's effectively just a stack of windows belonging to the `MutableScratch` group, where windows are pushed and popped from the stack.
Doing this,`MutableScratch` controls the order in which the windows are stored in the stack.
This ensures that the every window in the `MutableScratch` group can be accessed via toggle.

### Initializing the `MutableScratch` on qtile start

When restarting qtile, the `MutableScratch` instance in `config.py` will be overwritten, losing the stack history and the floating window status of it's windows.
To stop this, we add a `hook` function to `startup_complete` that will reinitialize a new `MutableScratch` instance with the windows that are located in the `MutableScratch.scratch_group_name`.
