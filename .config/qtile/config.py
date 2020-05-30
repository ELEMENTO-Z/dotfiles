# -*- coding: utf-8 -*-
#     ___  _   _ _
#    / _ \| |_(_) | ___
#   | | | | __| | |/ _ \
#   | |_| | |_| | |  __/
#    \__\_\\__|_|_|\___|
#
#   A customized qtile config by me CaptainEureka
#   Email: captaineureka@gmail.com
#   GitHub: CaptainEureka
#
# The following comments are the copyright and licensing information from the default
# qtile config. Copyright (c) 2010 Aldo Cortesi, 2010, 2014 dequis, 2012 Randall Ma,
# 2012-2014 Tycho Andersen, 2012 Craig Barnes, 2013 horsik, 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.

# IMPORTS
import os
import re
import socket
import subprocess
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from typing import List  # noqa: F401

##### DEFINING SOME VARIABLES #####
mod = "mod4"                                     # Sets mod key to SUPER/WINDOWS
alt = "mod1"                                     # Sets Alt key
myTerm = "kitty"                                 # My terminal of choice
myConfig = "/home/mk/.config/qtile/config.py"    # The Qtile config file location

##### KEYBINDINGS #####
keys = [
    # The essentials
    Key(
        [mod], "Return",
        lazy.spawn(myTerm),
        desc='Launches Terminal'
    ),
    Key(
        [mod, "shift"], "Return",
        lazy.spawn("rofi-appsmenu"),
        desc='Rofi Run Launcher'
    ),
    Key(
        [mod], "Tab",
        lazy.next_layout(),
        desc='Toggle through layouts'
    ),
    Key(
        [mod, "shift"], "q",
        lazy.window.kill(),
        desc='Kill active window'
    ),
    Key(
        [mod, "shift"], "r",
        lazy.restart(),
        desc='Restart Qtile'
    ),
    Key(
        [mod, "shift"], "c",
        lazy.shutdown(),
        desc='Shutdown Qtile'
    ),
    # Switch focus of monitors
    Key([mod], "period",
        lazy.next_screen(),
        desc='Move focus to next monitor'
        ),
    Key([mod], "comma",
        lazy.prev_screen(),
        desc='Move focus to prev monitor'
        ),
    # Window controls
    Key(
        [mod], "k",
        lazy.layout.down(),
        desc='Move focus down in current stack pane'
    ),
    Key(
        [mod], "j",
        lazy.layout.up(),
        desc='Move focus up in current stack pane'
    ),
    Key(
        [mod, "shift"], "k",
        lazy.layout.shuffle_down(),
        desc='Move windows down in current stack'
    ),
    Key(
        [mod, "shift"], "j",
        lazy.layout.shuffle_up(),
        desc='Move windows up in current stack'
    ),
    Key(
        [mod], "h",
        lazy.layout.grow(),
        lazy.layout.increase_nmaster(),
        desc='Expand window (MonadTall), increase number in master pane (Tile)'
    ),
    Key(
        [mod], "l",
        lazy.layout.shrink(),
        lazy.layout.decrease_nmaster(),
        desc='Shrink window (MonadTall), decrease number in master pane (Tile)'
    ),
    Key(
        [mod], "n",
        lazy.layout.normalize(),
        desc='normalize window size ratios'
    ),
    Key(
        [mod], "m",
        lazy.layout.maximize(),
        desc='toggle window between minimum and maximum sizes'
    ),
    Key(
        [mod, "shift"], "f",
        lazy.window.toggle_floating(),
        desc='toggle floating'
    ),
    # Stack controls
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate(),
        lazy.layout.flip(),
        desc='Switch which side main pane occupies (XmonadTall)'
    ),
    Key(
        [mod], "space",
        lazy.layout.next(),
        desc='Switch window focus to other pane(s) of stack'
    ),
    Key(
        [mod, "control"], "Return",
        lazy.layout.toggle_split(),
        desc='Toggle between split and unsplit sides of stack'
    ),
    # Rofi scripts launched with ALT + CTRL + KEY
    Key(
        [alt, "control"], "e",
        lazy.spawn("rofi-config-menu"),
        desc='Rofi script for editing config files'
    ),
    Key(
        [alt, "control"], "w",
        lazy.spawn("setbg ~/Downloads"),
        desc='Set wallpaper with Sxiv and xwallpaper'
    ),
    Key(
        [alt, "control"], "b",
        lazy.spawn("bwmenu"),
        desc='Bitwarden menu with Rofi'
    ),
    Key(
        [alt, "control"], "p",
        lazy.spawn("rofi-powermenu sysicons"),
        desc='Rofi power menu (shutdown, reboot, lock, logoff)'
    ),
    Key(
        [alt, "control"], "s",
        lazy.spawn("rofi-search"),
        desc='Rofi DuckDuckGo Search'
    )
    # Key(
    #     "Print",
    #     lazy.spawn("rofi-maim"),
    #     desc='Rofi screenshot utility'
    # ),
    # Key(
    #     "XF86MonBrightnessUp",
    #     lazy.spawn("notipy-light -A 10"),
    #     desc='Increase Brightness'
    # ),
    # Key(
    #     "XF86MonBrightnessDown",
    #     lazy.spawn("notipy-light -U 10"),
    #     desc='Decrease Brightness'
    # )
]

##### GROUPS #####
group_names = [("일", {'layout': 'monadtall'}),
               ("이", {'layout': 'monadtall'}),
               ("삼", {'layout': 'monadtall'}),
               ("사", {'layout': 'monadtall'}),
               ("오", {'layout': 'floating'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    # Switch to another group
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))
    # Send current window to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))

##### DEFAULT THEME SETTINGS FOR LAYOUTS #####
layout_theme = {"border_width": 0,
                "margin": 20,
                "border_focus": "82aaff",
                "border_normal": "383e5c"
                }

##### THE LAYOUTS #####
layouts = [
    # layout.MonadWide(**layout_theme),
    # layout.Bsp(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
    layout.Floating(**layout_theme)
]

##### COLORS #####
colors = [["#131421", "#131421"],  # panel background
          ["#383e5c", "#383e5c"],  # background for current screen tab
          ["#c8d3f5", "#c8d3f5"],  # font color for group names
          ["#ff5370", "#ff5370"],  # border line color for current tab
          ["#c597f9", "#c597f9"],  # border line color for other tab and odd widgets
          ["#82aaff", "#82aaff"],  # color for the even widgets
          ["#fca7ea", "#fca7ea"]]  # window name

##### PROMPT #####
prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="SF Pro Display",
    fontsize=22,
    padding=4,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

##### WIDGETS #####

def init_widgets():
    widgets_list = [
        widget.Sep(
            linewidth=0,
            padding=10,
            foreground=colors[2],
            background=colors[0]
        ),
        widget.GroupBox(font="SF Pro Display",
                        fontsize=22,
                        margin_y=3,
                        margin_x=0,
                        padding_y=20,
                        padding_x=20,
                        borderwidth=3,
                        active=colors[2],
                        inactive=colors[2],
                        rounded=True,
                        highlight_color=colors[1],
                        highlight_method="line",
                        this_current_screen_border=colors[5],
                        this_screen_border=colors[4],
                        other_current_screen_border=colors[0],
                        other_screen_border=colors[0],
                        foreground=colors[2],
                        background=colors[0]
                        ),
        widget.Sep(
            linewidth=0,
            padding=1200,
            foreground=colors[2],
            background=colors[0]
        ),
        widget.Clock(
            font="SF Pro Display Bold",
            foreground=colors[2],
            background=colors[0],
            format="%a, %H:%M"
        ),
        widget.Spacer(
            background=colors[0]
        ),
        # widget.TextBox(
        #     text=" ",
        #     padding=4,
        #     font="Feather",
        #     foreground=colors[2],
        #     background=colors[0],
        #     fontsize=20
        # ),
        widget.Notify(
            foreground=colors[2],
            foreground_low=colors[2],
            foreground_urgen=colors[3],
            background=colors[0],
            padding=8
        ),
        widget.CheckUpdates(
            execute='kitty',
            foreground=colors[2],
            background=colors[0],
            padding=4,
            colour_no_updates=colors[2],
            colour_have='ff5370',
            display_format='  {updates}',
            font='Feather'
        ),
        # widget.TextBox(
        #     text="  ",
        #     font="Feather",
        #     fontsize=24,
        #     foreground=colors[2],
        #     background=colors[0],
        #     padding=2
        # ),
        widget.Volume(
            foreground=colors[2],
            background=colors[0],
            padding=4,
            theme_path='/usr/share/icons/Papirus-Dark/16x16/panel'
        ),
        widget.BatteryIcon(
            foreground=colors[2],
            background=colors[0],
            padding=4,
            theme_path='/usr/share/icons/Papirus-Dark/16x16/panel'
        ),
        widget.Battery(
            foreground=colors[2],
            background=colors[0],
            low_foreground=colors[3],
            format='{percent:2.0%}'
        ),
        widget.Wlan(
            interface='wlp58s0',
            foreground=colors[2],
            background=colors[0],
            padding=8,
            format=' ',
            disconnected_message=' ',
            mouse_callbacks={'Button1': 'kitty'}
        ),
        widget.CurrentLayoutIcon(
            custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
            foreground=colors[2],
            background=colors[0],
            padding=0,
            scale=0.5
        ),
        widget.Sep(
            linewidth=0,
            padding=10,
            foreground=colors[0],
            background=colors[0]
        )
    ]
    return widgets_list

# SCREENS ##### (TRIPLE MONITOR SETUP)


def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets(),
                               opacity=0.70, size=54, margin=[10, 20, 0, 20]))]


if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets()

##### DRAG FLOATING WINDOWS #####
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

##### FLOATING WINDOWS #####
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
],
border_width=0)
auto_fullscreen = True
focus_on_window_activation = "smart"

##### STARTUP APPLICATIONS #####
@hook.subscribe.startup_once
def start_once():
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
wmname = "LG3D"