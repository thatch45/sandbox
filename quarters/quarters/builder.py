'''
Generates an ArchLinux chroot base for building packages.
'''

import subprocess
import multiprocessing
import os
import tempfile
import time
import random
import shutil
import pickle

class Chroot(object):
    '''
    Makes a chroot
    '''
    def __init__(self):
        self.root = os.path.join('/tmp',
                'quarters-root-' + str(int(time.time()))\
                        + str(random.randint(1000,9999)))
        self.packer = subprocess.Popen('type -p packer',
                shell=True,
                stdout=subprocess.PIPE).communicate()[0].strip()

    def _setup_root(self):
        '''
        Install the root to use for package building
        '''
        r_cmd = 'mkarchroot ' + self.root + ' curl base base-devel'
        subprocess.call(r_cmd, shell=True)
        shutil.copy2(self.packer, os.path.join(self.root, self.packer[1:]))
        shutil.copy2('/etc/resolv.conf',
                os.path.join(self.root, 'etc/resolv.conf'))
        shutil.copy2('/etc/pacman.d/mirrorlist',
                os.path.join(self.root, 'etc/pacman.d/mirrorlist'))

    def clear_root(self):
        '''
        Delete the chroot
        '''
        shutil.rmtree(self.root)

    def setup(self):
        '''
        Setp the chroot
        '''
        if os.path.isdir(self.root):
            self.clear_root()
        self._setup_root()


class AURBuilder(multiprocessing.Process):
    '''
    Builds the named aur package
    '''
    def __init__(self, opts, b_num):
        multiprocessing.Process.__init__(self)
        self.opts = opts
        self.b_num = b_num
        self.chroot = Chroot()
        self.pkg = ''

    def _load_pkg(self):
        '''
        Builds a package in a chroot
        '''
        self.chroot.setup()
        root = os.open('/', os.O_RDONLY)
        os.chroot(self.chroot.root)
        p_cmd = self.chroot.packer + ' -S --noconfirm ' + self.pkg
        pkout = subprocess.Popen(p_cmd,
                shell=True,
                stdout=subprocess.PIPE).communicate()[0]
        os.fchdir(root)
        for i in range(10):
            os.chdir('..')
        os.chroot('.')
        c_cmd = 'find ' + self.chroot.root\
              + '/tmp -name "*.pkg.tar.xz" -exec cp {} '\
              + self.opts['aur_repo'] + ' \;'
        subprocess.call(c_cmd, shell=True)
        self.chroot.clear_root()

    def _notify_built(self):
        '''
        Save the notification pickle
        '''
        notn = str(int(time.time())) + str(random.randint(1000,9999))
        notp = {'type': 'built_package',
                'action': 'rebuild_aur',
                'b_num': self.b_num,
                'state': 'avail'}
        p_loc = os.path.join(self.opts['not_dir'], notn + '.p')
        pickle.dump(notp, open(p_loc, 'w+'))

    def run(self):
        '''
        Build the pkg in this builder chroot
        '''
        self._load_pkg()
        self._notify_built()
