import libqtile
from libqtile.lazy import lazy
from libqtile.log_utils import logger
import libqtile.window


class MutableScratch(object):
    """For creating a mutable scratch workspace (similar to i3's scratch functionality)"""


    def __init__(self, win_attr: str='mutscratch', grp_name: str=''):
        """

        Parameters
        ----------
        win_attr : str
            Attribute added to the qtile.window object to determine whether the
            window is a part of the MutableScratch system
        grp_name : str
            Name of the group that holds the windows added to the scratch space
        """

        self.win_attr = win_attr
        self.grp_name = grp_name

        self.win_stack = [] # Equivalent of focus_history


    def add_current_window(self):
        """Add current window to the MutableScratch system"""
        @lazy.function
        def _add_current_window(qtile):
            win = qtile.current_window
            win.hide()
            win.floating = True
            setattr(win, self.win_attr, True)

            win.togroup(self.grp_name)
            self.win_stack.append(win)

        return _add_current_window


    def qtile_startup(self):
        """Initialize MutableScratch group on restarts

        Put
            hook.subscribe.startup_complete(<MutScratch>.qtile_startup)
        in your config.py to initialize the windows in the MutScratch group
        """

        qtile = libqtile.qtile
        group = qtile.groups_map[self.grp_name]

        wins = list(group.windows)
        for win in wins:
            win.floating = True
            setattr(win, self.win_attr, True)

        self.win_stack = list(group.windows)


    def remove(self):
        """Remove current window from MutableScratch system"""
        @lazy.function
        def _remove(qtile):
            win = qtile.current_window
            setattr(win, self.win_attr, False)

            if win in self.win_stack:
                self.win_stack.remove(win)
        return _remove


    def toggle(self):
        """Toggle between hiding/showing MutableScratch windows

        If current window is in the MutableScratch system, hide the window. If
        it isn't, show the next window in the stack.
        """
        @lazy.function
        def _toggle(qtile):
            win = qtile.current_window
            if getattr(win, self.win_attr, False):
                self._push(win)
            else:
                self._pop(qtile, win)
        return _toggle


    def _push(self, win: libqtile.window.Window):
        """Hide and push window to stack

        Parameters
        ----------
        win : libqtile.window.Window
            Window to push to the stack
        """
        win.togroup(self.grp_name)
        self.win_stack.append(win)


    def _pop(self, qtile, win: libqtile.window.Window):
        """Show and pop window from stack

        Parameters
        ----------
        qtile : libqtile.qtile
            qtile root object
        win : libqtile.window.Window
            Window to pop from stack
        """
        group = qtile.groups_map[self.grp_name]
        if set(self.win_stack) != group.windows:
            logger.warning(f"{self}'s win_stack and {group}'s windows have mismatching windows: "
                           f"{set(self.win_stack).symmetric_difference(group.windows)}")
            self.win_stack = list(group.windows)
        if self.win_stack:
            win = self.win_stack.pop(0)
            win.togroup(qtile.current_group.name)
