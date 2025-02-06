#!/usr/bin/env python3

import dbus
from dbus.connection import String
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

plan_map = {
    "throughput-performance": ("Performance", "power-profile-performance-symbolic"),
    "balanced": ("Balanced", "power-profile-balanced-symbolic"),
    "powersave": ("Powersaver", "power-profile-power-saver-symbolic")
}

DBusGMainLoop(set_as_default=True)
sys_bus = dbus.SystemBus()
sbus = dbus.SessionBus()

def handle_msg(plan: dbus.String, ok: dbus.Boolean, _):
    if ok:
        show_osd(str(plan))

def show_osd(prof: String):
    if not prof in plan_map:
        pass
    msg, ic = plan_map[prof]
    sbus.call_blocking('org.erikreider.swayosd-server', '/org/erikreider/swayosd', 'org.erikreider.swayosd', 'HandleAction', None, ("CUSTOM-ICON", ic))
    sbus.call_blocking('org.erikreider.swayosd-server', '/org/erikreider/swayosd', 'org.erikreider.swayosd', 'HandleAction', None, ("CUSTOM-MESSAGE", msg))

sys_bus.add_signal_receiver(handle_msg, 'profile_changed', 'com.redhat.tuned.control', 'com.redhat.tuned', '/Tuned')

active_prof = sys_bus.call_blocking('com.redhat.tuned', '/Tuned', 'com.redhat.tuned.control', 'active_profile', None, {})

show_osd(str(active_prof))

mainloop = GLib.MainLoop()
mainloop.run()
