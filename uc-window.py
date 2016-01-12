# -*- coding: utf-8 -*-

"""
Display window title in notification bar 

Configuration parameters:
    - cache_timeout : how often we refresh this module in seconds
    - limit : character limit to show
    - color : color of text

@author Cayoglu
"""

# import your useful libs here
from time import time
import subprocess as sp

class Py3status:

    # available configuration parameters
    cache_timeout = 1
    limit = 40
    color = ''

    def on_click(self, i3s_output_list, i3s_config, event):
        self.text = ''
        pass

    def _get_name(self):
        name = sp.check_output(['xdotool','getactivewindow','getwindowname']).strip('\n')
        return name[:self.limit-3]+'...' if len(name) > self.limit else name

    def uc_window(self, i3s_output_list, i3s_config):
        self.text = self._get_name()

        response = {
            'cached_until': time() + self.cache_timeout,
            'full_text': self.text
        }
        if self.color: response['color']=self.color
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
        print(x.uc_window([], config))
        sleep(1)
