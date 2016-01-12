# -*- coding: utf-8 -*-
"""
Display battery level by color

Configuration parameters:
    - cache_timeout : how often we refresh this module in seconds
    - colors : color range to use
    - text_ac : text to display on charge
    - text_full : text to display if full
    - text_else : text to display else
    - taskbar : 'true' if notifaction @taskbar
@author Cayoglu
"""
from time import time
import os
import subprocess

class Py3status:

    # available configuration parameters
    cache_timeout = 10
    colors = '#FF0000,#E31C00,#C73800,#AB5400,#8F7000,#738C00,#57A800,#3BC400,#1FE000,#00FF00'
    text_ac = 'ac'
    text_full = 'full'
    text_else = 'else'
    taskbar = 'false'
    
    def on_click(self, i3s_output_list, i3s_config, event):
        FNULL = open('/dev/null', 'w') 
        status = file('/sys/class/power_supply/BAT0/status').read().strip('\n')
        message = '{} {}%'.format(status, int(self.percentage*100))
        
        if self.taskbar != 'true':
            subprocess.Popen(
                    ['notify-send',
                        message,
                        '-t',
                        '1600'
                    ],
                    stdout=FNULL,
                    stderr=FNULL,
                    close_fds = True
            )
        else:
            with open('/tmp/tmp.txt','w') as fl:
                fl.write(message)
        FNULL.close()


    def _on_ac(self):
        ac_path = '/sys/class/power_supply/AC/online'
        if os.path.exists(ac_path) and int(file(ac_path).read().strip('\n'))==1:
            return True
        else:
            return False
    
    def _calc_percentage(self):
        total_path = '/sys/class/power_supply/BAT0/energy_full'
        alt_total_path = '/sys/class/power_supply/BAT0/charge_full_design'
        now_path = '/sys/class/power_supply/BAT0/energy_now'
        alt_now_path = '/sys/class/power_supply/BAT0/charge_now'
        
        
        try:
            self.now = float(file(now_path).read().strip('\n'))
            self.total = float(file(total_path).read().strip('\n'))
        except:
            self.now = float(file(alt_now_path).read().strip('\n'))
            self.total = float(file(alt_total_path).read().strip('\n'))


        return self.now/self.total-0.01

    def _set_color(self, i3s_config):
        if isinstance(self.colors,str): self.colors = self.colors.split(',')
        if len(self.colors)<=1: 
            self.colors = [
                    i3s_config['color_bad'],
                    i3s_config['color_degraded'],
                    i3s_config['color_good']
                    ]

        color_nr = int(self.percentage*len(self.colors))
        print color_nr, self.percentage
        return self.colors[color_nr]

    def _get_text(self):
        if self.ac:
            return self.text_ac
        elif self.percentage > 0.99:
            return self.text_full
        else:
            return self.text_else
        
    def uc_battery(self, i3s_output_list, i3s_config):
        self.ac = self._on_ac()
        self.percentage = self._calc_percentage()
        color = self._set_color(i3s_config)
        text = self._get_text()
        
        response = {
            'cached_until': time() + self.cache_timeout,
            'full_text': text,
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
        print(x.uc_battery([], config))
        sleep(1)
