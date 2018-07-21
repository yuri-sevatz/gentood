import os
import multiprocessing
import subprocess


class Portage:
    @staticmethod
    def emerge(*args):
        params = ['emerge']
        for arg in args:
            if type(arg) is list:
                params += list(arg)
            else:
                params.append(arg)
        subprocess.check_call(params)


class Kernel:
    def __init__(self, src):
            self._src = os.path.join(src, '')

    @property
    def path(self):
            return self._src

    @property
    def binary(self):
            return os.path.join(self.path, 'arch/x86/boot/bzImage')

    @property
    def config(self):
            return os.path.join(self.path, '.config')

    @staticmethod
    def target():
            return Kernel(os.path.realpath('/usr/src/linux'))

    @staticmethod
    def running():
            return Kernel('/usr/src/linux-' + str(subprocess.check_output(['uname', '-r']).decode('utf-8').splitlines()[0]))

    def configure(self, kernel):
            subprocess.check_call(['cp', '-v', kernel.config, '/usr/src/linux/'])
            subprocess.check_call(['make', '-C', self.path, 'oldconfig'])

    def compile(self):
            subprocess.check_call(['make', '-C', self.path, '-j', str(multiprocessing.cpu_count() + 1)])
            subprocess.check_call(['make', '-C', self.path, 'modules_install'])

    def install(self):
            subprocess.check_call(['make', '-C', self.path, 'install'])
            subprocess.check_call(['genkernel', '--install', '--no-ramdisk-modules', 'initramfs'])
            subprocess.check_call(['grub-mkconfig', '-o', '/boot/grub/grub.cfg'])
