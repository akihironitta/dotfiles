import subprocess

from libqtile import bar, hook, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal


@hook.subscribe.screen_change
def adjust_display(event=None):
    script_path = os.path.expanduser("/home/nitta/bin/disphome")
    subprocess.call([script_path])


def get_display_num_names():
    cmd = "xrandr --listmonitors"
    output = subprocess.getoutput(cmd)
    info = []
    for line in output.split("\n"):
        info.append(line.strip().split()[-1])
    n_displays = int(info[0])
    display_names = info[1:]
    return n_displays, display_names


# (3, ['eDP-1', 'DP-1-1', 'DP-1-3'])
num_displays, display_names = get_display_num_names()

display0, display1, display2 = None, None, None

if num_displays == 3:
    display0, display1, display2 = display_names
elif num_displays == 2:
    display0 = display_names[0]
    display1 = display_names[1]
elif num_displays == 1:
    display0 = display_names[0]


mod = "mod4"  # Super key
alt = "mod1"  # Alt key
terminal = guess_terminal()
colors = {
    "green": "#59D77C",
    "dark_green": "#007E24",
    "red": "#FF6622",
    "black": "#000000",
}

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "Tab", lazy.layout.next()),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left()),
    Key([mod, "control"], "l", lazy.layout.grow_right()),
    Key([mod, "control"], "j", lazy.layout.grow_down()),
    Key([mod, "control"], "k", lazy.layout.grow_up()),
    Key([mod], "n", lazy.layout.normalize()),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.next_screen()),
    # Toggle between different layouts as defined below
    Key([mod, "control"], "period", lazy.next_layout()),
    # Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "period", lazy.spawncmd()),
    Key([mod, "control"], "r", lazy.restart()),
    # audio
    Key([mod, "control"], "minus", lazy.spawn("amixer sset Master,0 5%-")),
    Key([mod, "control"], "equal", lazy.spawn("amixer sset Master,0 5%+")),
    Key([mod, "control"], "m", lazy.spawn("amixer sset Master,0 toggle")),
    # backlight
    # Key([mod], "minus", lazy.spawn("asdfasdf")),
    # Key([mod], "equal", lazy.spawn("asdfasdf")),
]

# (group name, key)
group_configs = [
    ("www", "u"),
    ("dev", "i"),
    ("chat", "o"),
    ("mail", "p"),
]

groups = []
for name, key,  in group_configs:
    groups.append(Group(name))
    keys.append(Key([mod], key, lazy.group[name].toscreen(toggle=False)))
    keys.append(Key([mod, "shift"], key, lazy.window.togroup(name, switch_group=False)))

groups.append(
    ScratchPad(
        "scratchpad",
        [DropDown("term", "terminator", opacity=0.8, height=1.0, width=1.0, x=0.0, y = 0.0)],
    )
)

keys.append(
    Key([alt], "space", lazy.group["scratchpad"].dropdown_toggle("term"))
)
    
border_kwargs = dict(
    # margin=[0, 1, 0, 1],
    margin=0,
    border_width=3,
    border_focus=colors["green"],
    border_normal=colors["black"],
)

layouts = [
    layout.Max(),
    layout.Stack(
        autosplit=False,
        fair=False,
        num_stacks=2,
        **border_kwargs,
    ),
]

widget_defaults = dict(
    font="mono",
    # font="sans",
    fontsize=18,
    padding=3,
    foreground=colors["green"],
    border_color=colors["green"],
    fill_color=colors["green"],
    graph_color=colors["green"],
    cursor_color=colors["green"],
    active_color=colors["green"],
    type="box",
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(f"{display0} {display1}"),
                
                widget.GroupBox(),
              
                widget.Sep(linewidth=3),
                widget.CurrentLayoutIcon(),
                widget.CurrentLayout(),
                
                widget.Sep(linewidth=3),
                widget.Prompt(cursorblink=0.3, prompt=">"),

                widget.Spacer(),
                
                # TODO: Unify the color configuration with `widget_defaults`
                widget.Sep(linewidth=3),
                widget.TextBox("CPU"),
                widget.ThermalSensor(tag_sensor="temp1", threshold=60, foreground_alert=colors["red"], foreground=colors["green"]),
                widget.CPU(format="{freq_current}/{freq_max}GHz {load_percent:3.0f}%"),
                widget.CPUGraph(),

                widget.Sep(linewidth=3),
                widget.Memory(format="{MemUsed:5.0f}/{MemTotal:5.0f}{mm}"),
                widget.MemoryGraph(),
                widget.Memory(format="{SwapUsed:5.0f}/{SwapTotal:5.0f}{ms}"),
                widget.SwapGraph(),
                
                widget.Sep(linewidth=3),
                widget.Wlan(interface="wlp2s0", format="{essid}({percent:4.0%})"),
                widget.Net(format="RX{down}"),
                widget.NetGraph(bandwidth_type="down"),
                widget.Net(format="TX{up}"),
                widget.NetGraph(bandwidth_type="up"),

                widget.Sep(linewidth=3),
                widget.TextBox("BAT"),
                widget.Battery(
                    charge_char="*",
                    discharge_char=":",
                    empty_char="x",
                    full_char="=",
                    unknown_char="?",
                    # format="{char} {percent:2.0%} {hour:d}:{min:02d} {watt:.2f}W",
                    format="{char}{percent:2.0%}",
                    low_foreground=colors["red"],
                ),
                
                widget.Sep(linewidth=3),
                widget.TextBox("BL"),
                widget.Backlight(backlight_name="intel_backlight"),
                
                widget.Sep(linewidth=3),
                widget.TextBox("Vol"),
                widget.Volume(),
                
                widget.Sep(linewidth=3),
                widget.Systray(),

                # See /usr/share/zoneinfo/ for other timezones.
                widget.Sep(linewidth=3),
                widget.Clock(format="%m/%d(%a) %H:%M", timezone="Asia/Tokyo"),
                # widget.Sep(linewidth=3),
                # widget.Clock(format="NY%H:%M", timezone="America/New_York"),
                # widget.Sep(linewidth=3),
                # widget.Clock(format="CZ%H:%M", timezone="Europe/Prague"),
            ],
            24,
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(f"{display2}"),
                widget.GroupBox(),
                widget.Sep(linewidth=3),
                widget.CurrentLayoutIcon(),
                widget.CurrentLayout(),
            ],
            24,
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class="confirmreset"),  # gitk
    Match(wm_class="makebranch"),  # gitk
    Match(wm_class="maketag"),  # gitk
    Match(wm_class="ssh-askpass"),  # ssh-askpass
    Match(title="branchdialog"),  # gitk
    Match(title="pinentry"),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
