from sys import platform
try:
    from pync import Notifier
except Exception:
    pass
import subprocess

class Notifier(object):
    ''' Class to determine what notifier to use '''
    def __init__(self):
        self.notifier = None
        if platform == 'linux':
            self.notifier = self.linux_notifier
        else:
            self.notifier = self.mac_notifier

    @staticmethod
    def linux_notifier(**kwargs):
        subprocess.Popen(['notify-send', kwargs.get('title', ''), kwargs.get('message')])
        return

    @staticmethod
    def mac_notifier(*kwargs):
        Notifier.notify(
            kwargs.get('message', ''),
            open=kwargs.get('link', ''),
            title=kwargs.get('title', '')
        )
        return

    def send_notification(self, **kwargs):
        self.notifier(**kwargs)
