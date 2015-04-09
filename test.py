#!/usr/bin/python
from gi.repository import Gtk, GObject
from gi.repository import AppIndicator3 as appindicator
from subprocess import Popen, PIPE
from threading import Thread
import os

current_status = False

def menuitem_response(w, toggle):
    global current_status
    if toggle == True and current_status == False:
        def startOpenVpn():
            p = Popen([
                "sudo",
                "openvpn",
                "--config",
                "/root/client.ovpn",
                "--script-security",
                "2",
                "--auth-user-pass",
                "/root/openvpn-creds.conf"
            ], stdout=PIPE, stdin=PIPE, stderr=PIPE)
            p.communicate()
        Thread(target=startOpenVpn).start()
    else:
        Popen(["sudo", "killall", "-15", "openvpn"]).communicate()



def timeout_callback(on, off, status_button):
    global current_status
    p = Popen(["/sbin/ifconfig", "tun0"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    if err:
        status_button.set_label("Status: %s" % err)
        current_status = False
    else:
        status_button.set_label("Status: %s" % out)
        current_status = True

    GObject.timeout_add_seconds(5, timeout_callback, on, off, status_button)

if __name__ == "__main__":
    ind = appindicator.Indicator.new (
        "example-simple-client",
        "indicator-messages",
        appindicator.IndicatorCategory.COMMUNICATIONS
    )
    ind.set_status(appindicator.IndicatorStatus.ACTIVE)
    ind.set_attention_icon("icon.png")
    ind.set_icon(os.path.dirname(os.path.realpath(__file__))+"/icon.png")
   
    # create a menu
    menu = Gtk.Menu()

    on_button = Gtk.MenuItem("Connect to Home")
    on_button.connect("activate", menuitem_response, True)
    menu.append(on_button)
    on_button.show()

    off_button = Gtk.MenuItem("Disconnect from Home")
    off_button.connect("activate", menuitem_response, False)
    menu.append(off_button)
    off_button.show()

    status_button = Gtk.MenuItem("Status: Disconnected")
    menu.append(status_button)
    status_button.show()
   
    ind.set_menu(menu)

    GObject.timeout_add_seconds(5, timeout_callback, on_button, off_button, status_button)

    Gtk.main()