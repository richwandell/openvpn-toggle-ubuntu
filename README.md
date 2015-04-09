# A toggle switch for OpenVPN

OpenVPN Toggle is a tray icon for Ubuntu that will allow you to use your openvpn configuration with an on / off switch through the Ubuntu system tray.

# First Steps
1. Download your openvpn client file and move it to /root/client.ovpn
2. Create nopasswd sudo access for your account 
3. Create a un:pw file for the openvpn connection in /root/openvpn-creds.conf


### Installation

```sh
$ git clone https://github.com/richwandell/openvpn-toggle-ubuntu.git ~/apps/systray-openvpn
$ cp ~/apps/systray-openvpn/openvpn.conf ~/.config/upstart
```