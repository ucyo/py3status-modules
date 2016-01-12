# -*- coding: utf-8 -*-
"""
Display volume level by color

Configuration parameters:
    - cache_timeout : how often we refresh this module in seconds
    - colors : color range to use
    - text : text to display
    - text_muted : text to display if muted
    - taskbar : 'true' if notifaction @taskbar
@author Cayoglu
"""

# import your useful libs here
from time import time
import subprocess as sp


class Py3status:

    # available configuration parameters
    cache_timeout = 1
    colors = '#FF0000,#E31C00,#C73800,#AB5400,#8F7000,#738C00,#57A800,#3BC400,#1FE000,#00FF00'
    text = "VOL"
    text_muted = "VOL (muted)"
    taskbar = 'true'

    def on_click(self, i3s_output_list, i3s_config, event):
        f = ['']
        a = ['i3-sensible-terminal','-e','alsamixer']
        b = ['amixer','set','-D','pulse','Master','toggle']
        c = ['killall','alsamixer']
        d = ['amixer','set','Master','10%+']
        e = ['amixer','set','Master','10%-']
        commands = [f,a,b,c,d,e]

        com = commands[event["button"]]
        sp.Popen(com,stdout=open('/dev/null','w'),stderr=open('/dev/null','w'),close_fds=True)
        with open('/tmp/tmp.txt','w') as fl:
            if event['button'] in [3,4,5]: fl.write(str(self.vol)+'%')

    def _muted(self):
        try:
            muted = sp.check_output(["amixer", "get", "Master", "-M"]).split("Mono:")[1].split()[5][1:-1]
        except:
            muted = sp.check_output(["amixer", "get", "Master", "-M"]).split("Mono:")[1].split()[4][1:-1]

        if self.vol == 0 or muted == 'off':
            return True
        else:
            return False

    def _set_color(self, i3s_config):
        if isinstance(self.colors,str): self.colors = self.colors.split(',')
        if len(self.colors)<=1: 
            self.colors = [
                    i3s_config['color_bad'],
                    i3s_config['color_degraded'],
                    i3s_config['color_good']
                    ]

        color_nr = int(self.percentage*len(self.colors)-0.01) if not self.muted else 0
        return self.colors[color_nr]
    
    def uc_volume(self, i3s_output_list, i3s_config):
        try:
            self.vol = int(sp.check_output(["amixer", "get", "Master", "-M"]).split("Mono:")[1].split()[4][1:-2])
        except:
            self.vol = int(sp.check_output(["amixer", "get", "Master", "-M"]).split("Mono:")[1].split()[2][1:-2])

        self.muted = self._muted()
        self.percentage = float(self.vol)/100.0

        full_text = self.text if self.vol > 0 and not self.muted else self.text_muted
        color = self._set_color(i3s_config)

        response = {
            'cached_until': time() + self.cache_timeout,
            'full_text': full_text,
            'color' : color
        }
        return response

if __name__ == "__main__":
    from time import sleep
    x = Py3status()
    config = {
        'color_bad': '#FF0000',
        'color_degraded': '#FFFF00',
        'color_good': '#00FF00'
    }
    while True:
        print(x.uc_volume([], config))
        sleep(1)
