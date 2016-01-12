# -*- coding: utf-8 -*-
"""
Display notifications in taskbar

One-line summary followed by an empty line.
Multi-line description followed by an empty line.
Configuration parameters:
    - cache_timeout : how often we refresh this module in seconds
    - notify_sec : how long the notification should be displayed in seconds
    - fl : File to read notifications from
@author Cayoglu
"""

# import your useful libs here
from time import time
import os

class Py3status:

    # available configuration parameters
    cache_timeout = 1
    notify_sec = 3
    fl = '/tmp/tmp.txt'

    def uc_notify(self, i3s_output_list, i3s_config):
        last_edit = os.stat(self.fl).st_mtime 
        text = file(self.fl).read().strip('\n') if time()-last_edit<self.notify_sec else ""
        response = {
            'cached_until': time() + self.notify_sec,
            'full_text': text
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
        print(x.uc_notify([], config))
        sleep(1)
