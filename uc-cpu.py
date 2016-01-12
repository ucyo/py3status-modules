# -*- coding: utf-8 -*-
"""
Display CPU usage level by color

Configuration parameters:
    - cache_timeout : how often we refresh this module in seconds
    - colors : color range to use
    - text : text to display
    - taskbar : 'true' if notification @taskbar
!! needs python module : psutil !!!
@author Cayoglu
"""

# import your useful libs here
from time import time
import psutil
import subprocess

class Py3status:

    # available configuration parameters
    cache_timeout = 10
    colors = '#FF0000,#E31C00,#C73800,#AB5400,#8F7000,#738C00,#57A800,#3BC400,#1FE000,#00FF00'
    text = 'CPU'
    taskbar = 'true'

    def on_click(self, i3s_output_list, i3s_config, event):
        FNULL = open('/dev/null', 'w')
        message = '{} {}% used'.format(self.text, round(100-self.percentage,2))
        if self.taskbar!='true':
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
            with open('/tmp/tmp.txt','w') as f:
                f.write(message)
        FNULL.close()


    def _set_color(self, i3s_config):
        if isinstance(self.colors,str): self.colors = self.colors.split(',')
        if len(self.colors)<=1: 
            self.colors = [
                    i3s_config['color_bad'],
                    i3s_config['color_degraded'],
                    i3s_config['color_good']
                    ]

        color_nr = int((self.percentage/100)*len(self.colors))
        return self.colors[color_nr]
    
    def uc_cpu(self, i3s_output_list, i3s_config):
        """
        This method will return an empty text message
        so it will NOT be displayed on your i3bar.
        If you want something displayed you should write something
        in the 'full_text' key of your response.
        See the i3bar protocol spec for more information:
        http://i3wm.org/docs/i3bar-protocol.html
        """
        self.percentage = 100.0 - psutil.cpu_percent(interval=1)
        color = self._set_color(i3s_config)

        response = {
            'cached_until': time() + self.cache_timeout,
            'full_text': self.text,
            'color': color
        }
        return response

if __name__ == "__main__":
    """
    Test this module by calling it directly.
    This SHOULD work before contributing your module please.
    """
    from time import sleep
    x = Py3status()
    config = {
        'color_bad': '#FF0000',
        'color_degraded': '#FFFF00',
        'color_good': '#00FF00'
    }
    while True:
        print(x.uc_cpu([], config))
        sleep(1)
