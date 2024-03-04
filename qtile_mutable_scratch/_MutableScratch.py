import libqtile
import libqtile.config
from libqtile.lazy import lazy
from libqtile.log_utils import logger

# For type hints
from libqtile.core.manager import Qtile
from libqtile.group import _Group
from libqtile.backend import base
from collections.abc import Callable


class MutableScratch(object):
    """For creating a mutable scratch workspace (similar to i3's scratch functionality)"""


    def __init__(self, win_attr: str='mutscratch', group_name: str=''):
        """

        Parameters
        ----------
        win_attr : str
            Attribute added to the qtile.window object to determine whether the
            window is a part of the MutableScratch system
        group_name : str
            Name of the group that holds the windows added to the scratch space
        """

        self.win_attr: str = win_attr
        self.scratch_group_name: str = group_name

        self.win_stack: list = [] # Equivalent of focus_history


    def qtile_startup(self):
        """Initialize MutableScratch group on restarts

        Put
            hook.subscribe.startup_complete(<MutScratch>.qtile_startup)
        in your config.py to initialize the windows in the MutScratch group
        """

        qtile = libqtile.qtile
        group = qtile.groups_map[self.scratch_group_name]

        for win in group.windows:
            win.floating = True
            setattr(win, self.win_attr, True)

        self.win_stack = group.windows.copy()


    def add_current_window(self) -> Callable:
        """Add current window to the MutableScratch system"""
        @lazy.function
        def _add_current_window(qtile: Qtile):
            win: base.Window = qtile.current_window
            win.hide()
            win.floating = True
            setattr(win, self.win_attr, True)

            win.togroup(self.scratch_group_name)
            self.win_stack.append(win)

        return _add_current_window


    def remove_current_window(self) -> Callable:
        """Remove current window from MutableScratch system"""
        @lazy.function
        def _remove(qtile: Qtile):
            win = qtile.current_window
            setattr(win, self.win_attr, False)

            if win in self.win_stack:
                self.win_stack.remove(win)
        return _remove


    def toggle(self) -> Callable:
        """Toggle between hiding/showing MutableScratch windows

        If current window is in the MutableScratch system, hide the window. If
        it isn't, show the next window in the stack.
        """
        @lazy.function
        def _toggle(qtile: Qtile):
            win: base.Window = qtile.current_window
            if getattr(win, self.win_attr, False):
                self._push(win)
            else:
                self._pop(qtile)
        return _toggle


    def _push(self, win: base.Window) -> None:
        """Hide and push window to stack

        Parameters
        ----------
        win : libqtile.backend.base.Window
            Window to push to the stack
        """
        win.togroup(self.scratch_group_name)
        win.keep_above(False)
        self.win_stack.append(win)


    def _pop(self, qtile: Qtile) -> None:
        """Show and pop window from stack

        Parameters
        ----------
        qtile : libqtile.qtile
            qtile root object
        win : libqtile.backend.base.Window
            Window to pop from stack
        """
        scratch_group: _Group = qtile.groups_map[self.scratch_group_name]
        if set(self.win_stack) != set(scratch_group.windows):
            logger.warning(f"{self}'s win_stack and {scratch_group}'s windows have mismatching windows: "
                           f"{set(self.win_stack).symmetric_difference(set(scratch_group.windows))}")
            self.win_stack = scratch_group.windows.copy()
        if self.win_stack:
            win = self.win_stack.pop(0)
            win.togroup(qtile.current_group.name)
            win.keep_above(True)
