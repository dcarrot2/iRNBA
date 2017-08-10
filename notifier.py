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
    def linux_notifier(*args):
        subprocess.Popen(['notify-send', args[0], args[1]])
        return

    @staticmethod
    def mac_notifier(title, message, link):
        Notifier.notify(
            message,
            open=link,
            title=title
        )
        return

    def send_notification(self, **kwargs):
        self.notifier(*(kwargs.values()))
