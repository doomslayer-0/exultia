# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import socket
import subprocess
from libqtile import qtile
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
#from typing import List  # noqa: F401

from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration


mod = "mod4"
terminal = "kitty"
fileman = "nemo"
browser = "firefox"
browser2 = "brave"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    #Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    #Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "f", lazy.spawn(browser), desc="Spawn the browser of choice"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc='Run Launcher'),
    Key([mod, "Shift"], "d", lazy.spawn("rofi -show run"), desc='Run Desktop Launcher'),
    Key([mod], "Space", lazy.spawn("rofi -show window"), desc='Manage open windows'),
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Print Screen"),
    Key([mod], "e", lazy.spawn(fileman), desc="Open File Manager"),
    Key([mod, "Shift"], "Return", lazy.spawn("alacritty"), desc="Open Alacritty"),
    Key([mod, "Shift"], "k", lazy.spawn("poweroff"), desc="Shutdown"),
    Key([mod, "Control", "Shift"], "k", lazy.spawn("systemctl reboot"), desc="Reboot"),
    Key([mod, "mod1"], "k", lazy.spawn("systemctl suspend"), desc="Sleep"),
    Key([mod, "Shift"], "f", lazy.spawn(browser2), desc="Open Brave"),
    Key([], "XF86AudioMute", lazy.spawn("amixer set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer set Master 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer set Master 5%+")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([mod], "p", lazy.spawn("pavucontrol -t 1"), desc='Accurate volume control')
]

groups = [Group("", layout='monadtall', matches=[Match(wm_class=["vscodium", "VSCodium"])]),
          Group("󰈹", layout='monadtall', matches=[Match(wm_class=["firefox", "LibreWolf", "qutebrowser"])]),
          Group("", layout='monadtall', matches=[Match(wm_class=["Alacritty"])]),
          Group("", layout='monadtall', matches=[Match(wm_class=["nemo"])]),
          Group("", layout='monadtall', matches=[Match(wm_class=["ONLYOFFICE Desktop Editors"])]),
          #Group("CHAT", layout='monadtall'),
          Group("󰎄", layout='monadtall', matches=[Match(wm_class=["clementine", "elisa"])]),
          Group("", layout='monadtall', matches=[Match(wm_class=["virtualbox"])]),
          Group("", layout='monadtall', matches=[Match(wm_class=["lutris", "Steam", "doometernalxvk64.exe", "ru-turikhay-tlauncher-bootstrap-Bootstrap", "Minecraft* 1.19.4"])])]

# Allow MODKEY+[0 through 9] to bind to groups, see https://docs.qtile.org/en/stable/manual/config/groups.html
# MOD4 + index Number : Switch to Group[index]
# MOD4 + shift + index Number : Send active window to another Group
from libqtile.dgroups import simple_key_binder
dgroups_key_binder = simple_key_binder("mod4")

layout_theme = {"border_width": 2,
                "margin": 2,
                "border_focus": "ffb5c7",
                "border_normal": "74c7ec"
                }

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Stack(num_stacks=2),
    layout.Bsp(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.TreeTab(
         font = "JetBrainsMono Nerd Font",
         fontsize = 10,
         sections = ["FIRST", "SECOND", "THIRD", "FOURTH"],
         section_fontsize = 10,
         border_width = 2,
         bg_color = "181825",
         active_bg = "ffb5c7",
         active_fg = "000000",
         inactive_bg = "f5c2e7",
         inactive_fg = "181825",
         padding_left = 0,
         padding_x = 0,
         padding_y = 5,
         section_top = 10,
         section_bottom = 20,
         level_shift = 8,
         vspace = 3,
         panel_width = 200
         ),
    layout.Floating(**layout_theme)
]

colors = [["#1e1e2e", "#1e1e2e"],
          ["#181825", "#181825"],
          ["#cdd6f4", "#cdd6f4"],
          ["#f38ba8", "#f38ba8"],
          ["#a6e3a1", "#a6e3a1"],
          ["#fab387", "#fab387"],
          ["#74c7ec", "#74c7ec"],
          ["#ffb5c7", "#ffb5c7"],
          ["#89b4fa", "#89b4fa"],
          ["#b4befe", "#b4befe"]]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

def init_widgets_list():
    widgets_list = [
        widget.Sep(
            linewidth = 0,
            padding = 12,
            foreground = colors[2],
            background = colors[0]
            ),
        widget.TextBox(
                text='',
                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("rofi -show run")},
                font = "Ubuntu Nerd Font",
                fontsize = 19,
                foreground = "3daee9",
                background = colors[0],
                padding=1
                ),
        widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[2],
                background = colors[0]
                ),
                #widget.GroupBox(
                        #font = "JetBrainsMono Nerd Font Bold",
                        #fontsize = 13,
                        #margin_y = 3,
                        #margin_x = 0,
                        #padding_y = 5,
                        #padding_x = 3,
                        #borderwidth = 3,
                        #active = colors[7],
                        #inactive = colors[6],
                        #rounded = False,
                        #highlight_color = colors[1],
                        #highlight_method = "line",
                        #this_current_screen_border = colors[6],
                        #this_screen_border = colors [4],
                        #other_current_screen_border = colors[6],
                        #other_screen_border = colors[4],
                        #foreground = colors[2],
                        #background = colors[0]
                        #),
        widget.GroupBox(
                font = "Ubuntu Nerd Font",
                fontsize = 16,
                padding_y = 0,
                padding_x = 3,
                borderwidth = 3,
                highlight_method = "text",
                active = colors[6],
                block_highlight_text_color=colors[6],
                inactive = colors[2],
                rounded = False,
                highlight_color = colors[2],
                this_current_screen_border = colors[7],
                this_screen_border = colors [4],
                        #other_current_screen_border = colors[6],
                        #other_screen_border = colors[4],
                        #foreground = colors[2],
                background = colors[0]
                ),        
        widget.TextBox(
                text = '|',
                font = "JetBrainsMono Nerd Font Bold",
                background = colors[0],
                foreground = '474747',
                padding = 2,
                fontsize = 14
                ),
        widget.CurrentLayoutIcon(
                custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                foreground = colors[2],
                background = colors[0],
                padding = 0,
                scale = 0.7
                ),
        widget.CurrentLayout(
                foreground = colors[7],
                background = colors[0],
                padding = 5,
                decorations=[
                    BorderDecoration(
                        colour = colors[7],
                        border_width = [0, 0, 2, 0],
                        padding_x = 0,
                        padding_y = None
                    )
                ],
                ),
        widget.TextBox(
                text = '|',
                font = "JetBrainsMono Nerd Font Bold",
                background = colors[0],
                foreground = '474747',
                padding = 2,
                fontsize = 14
                ),
        widget.WindowName(
                foreground = colors[6],
                background = colors[0],
                padding = 0,
                #decorations=[
                    #BorderDecoration(
                        #colour = colors[6],
                        #border_width = [0, 0, 2, 0],
                        #padding_x = 0,
                        #padding_y = None
                    #)
                #],
                ),
        #widget.Sep(
                #linewidth = 0,
                #padding = 6,
                #foreground = colors[0],
                #background = colors[0]
                #),
        #widget.Systray(
                #background = colors[0],
                #padding = 5
                #),
        widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[0],
                background = colors[0]
                ),
                #widget.Net(
                        #interface = "enp4s0",
                        #format = 'Net: {down} ↓↑ {up}',
                        #foreground = colors[3],
                        #background = colors[0],
                        #padding = 5,
                        #decorations=[
                            #BorderDecoration(
                                #colour = colors[3],
                                #border_width = [0, 0, 2, 0],
                                #padding_x = 5,
                                #padding_y = None,
                            #)
                        #],
                        #),
        widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[0],
                background = colors[0]
                ),
        widget.CheckUpdates(
                font = "Ubuntu Nerd Font",
                fontsize = 14,
                update_interval = 10,
                distro = "Arch_checkupdates",
                display_format = "  {updates}",
                foreground = colors[6],
                colour_have_updates = colors[6],
                colour_no_updates = colors[2],
                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("kitty -e paru")},
                padding = 5,
                background = colors[0],
                decorations=[
                    BorderDecoration(
                        colour = colors[6],
                        border_width = [0, 0, 2, 0],
                        padding_x = 0,
                        padding_y = None
                    )
                ],
                ),
        widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[0],
                background = colors[0]
                ),
        widget.GenPollText(
                update_interval=1, 
                func=lambda: subprocess.check_output("/home/alexandre/.local/bin/kernel.sh").decode("utf-8"),
                font = "Ubuntu Nerd Font",
                background = colors[0],
                foreground = colors[7],
                padding = 2,
                fontsize = 15,
                decorations=[
                    BorderDecoration(
                        colour = colors[7],
                        border_width = [0, 0, 2, 0],
                        padding_x = 0,
                        padding_y = None
                    )
                ],
                ),
        widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[0],
                background = colors[0]
                ),
        widget.CPU(
                font = "Ubuntu Nerd Font",
                fontsize = 14,
                foreground = colors[6],
                background = colors[0],
                        #mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("kitty -e ...")},
                threshold = 90,
                fmt = '  {}',
                padding = 5,
                decorations=[
                    BorderDecoration(
                        colour = colors[6],
                        border_width = [0, 0, 2, 0],
                        padding_x = 0,
                        padding_y = None,
                    )
                ],
                ),
        widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[0],
                background = colors[0]
                ),
        widget.ThermalSensor(
                font = "Ubuntu Nerd Font",
                fontsize = 14,
                foreground = colors[7],
                background = colors[0],
                        #mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("kitty -e ...")},
                threshold = 90,
                fmt = ' {}',
                padding = 5,
                decorations=[
                    BorderDecoration(
                        colour = colors[7],
                        border_width = [0, 0, 2, 0],
                        padding_x = 0,
                        padding_y = None,
                    )
                ],
                ),
        widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[0],
                background = colors[0]
                ),
        widget.Memory(
                font = "Ubuntu Nerd Font",
                fontsize = 14,
                foreground = colors[6],
                background = colors[0],
                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn("kitty -e htop")},
                fmt = '{}',
                padding = 5,
                decorations=[
                    BorderDecoration(
                        colour = colors[6],
                        border_width = [0, 0, 2, 0],
                        padding_x = 5,
                        padding_y = None,
                    )
                ],
                ),
        widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[0],
                background = colors[0]
                ),
        widget.Volume(
                font = "Ubuntu Nerd Font",
                fontsize = 14,
                foreground = colors[7],
                background = colors[0],
                fmt = ' {}',
                padding = 5,
                decorations=[
                    BorderDecoration(
                        colour = colors[7],
                        border_width = [0, 0, 2, 0],
                        padding_x = 0,
                        padding_y = None,
                    )
                ],
                ),
        widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[0],
                background = colors[0]
                ),
        widget.KeyboardLayout(    
            font = "Ubuntu Nerd Font",
            fontsize = 14,
            foreground = colors[6],
            background = colors[0],
            fmt = '󰌌 {}',
            padding = 5,
            decorations=[
                BorderDecoration(
                    colour = colors[6],
                    border_width = [0, 0, 2, 0],
                    padding_x = 0,
                    padding_y = None,
                )
            ],
            ),
        widget.Sep(
                linewidth = 0,
                padding = 6,
                foreground = colors[0],
                background = colors[0]
                ),
        widget.Clock(
                font = "Ubuntu Nerd Font",
                fontsize = 14,
                foreground = colors[7],
                background = colors[0],
                format = " %a, %d %B %H:%M ",
                decorations=[
                BorderDecoration(
                    colour = colors[7],
                    border_width = [0, 0, 2, 0],
                    padding_x = 0,
                    padding_y = None,
                    )
                ],

                ),
            ]        
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    del widgets_screen1[9:10]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2                 # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=1.0, size=20)),
            Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup
def autostart():
        home = os.path.expanduser('~')
        subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "qtile"
