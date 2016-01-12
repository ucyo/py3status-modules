# -*- coding: utf-8 -*-
"""
Display free space on disk by color

Configuration parameters:
    - cache_timeout : how often we refresh this module in seconds
    - folder : folder to be calculated
    - full_text : text/icon to indicate folder
    - colors : color range to use
    - window_manager : window manager to start on left click
    - taskbar : 'true' if notification @taskbar
@author Cayoglu 
"""

from time import time
import os
import subprocess


class Py3status:

    # available configuration parameters
    cache_timeout = 300
    folder = '/'
    full_text = None
    colors = '#FF0000,#E31C00,#C73800,#AB5400,#8F7000,#738C00,#57A800,#3BC400,#1FE000,#00FF00'
    window_manager = 'thunar'
    taskbar = "false"

    def on_click(self, i3s_output_list, i3s_config, event):
        FNULL = open('/dev/null', 'w') 
        message = '{} GB ({}%) Free'.format(round(self.abs_gb,2),int(self.percentage*100))
        if event['button']==1:
            subprocess.Popen(
                    [self.window_manager,self.folder],
                    stdout=FNULL,
                    stderr=FNULL,
                    close_fds = True
            )
        elif event['button']==3 and self.taskbar!='true':
            subprocess.Popen(
                    ['notify-send', message],
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
        color_nr = int(self.percentage*len(self.colors))
        return self.colors[color_nr]

    def _get_val(self):
        self.total = float(os.statvfs(self.folder).f_blocks)
        self.free = float(os.statvfs(self.folder).f_bavail)
        self.blocksize = float(os.statvfs(self.folder).f_bsize)
        self.abs_gb = self.free*self.blocksize/1024/1024/1024
        self.percentage = self.free/self.total

        if not self.full_text:
            return '{} ({}%) free'.format(self.folder, int(self.percentage*100))
        else:
            return self.full_text

    def uc_freespace(self, i3s_output_list, i3s_config):
        response = {
            'cached_until': time() + self.cache_timeout,
        }
        
        full_text = self._get_val()
        color = self._set_color(i3s_config)
        
        response['full_text'] = full_text 
        response['color'] = color

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
        print(x.uc_freespace([], config))
        sleep(1)
