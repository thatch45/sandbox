'''
The chroot module creates a chrooted install of Arch
'''
import os
import sys
import subprocess
import tempfile
import configparser

class Chroot(object):
    '''
    Builds a chrooted install of Archlinux
    '''
    def __init__(self, opts):
        '''
        Creates s chroot instance
        '''
        self.opts = opts
        self.root = self.__setup_root()
        self.conf = self.__get_conf()

    def __setup_root(self):
        '''
        Prepare the chroot directory
        '''
        chroot = self.opts['chroot_dir']
        if chroot:
            if os.path.isdir(chroot):
                for file in os.listdir(chroot):
                    err = 'The chroot dir ' + chroot + ' is not empty, '\
                        + 'select an empty directory'
                    sys.stderr.write(err + '\n')
                    sys.exit(42)
            os.makedirs(chroot)
            os.makedirs(os.path.join(chroot, 'var/lib/pacman'))
            return chroot
        chroot = tempfile.mkdtemp()
        os.makedirs(os.path.join(chroot, 'var/lib/pacman'))
        return chroot

    def __get_conf(self):
        '''
        Gets the configuration items from the config file, these are returned
        as a dict. The dict contains pkg, rootpw, crypt_rootpw, overlay
        '''
        conf = {}
        parser = configparser.ConfigParser()
        parser.read(self.opts['config'])
        if parser.has_section('conf'):
            if parser.has_option('conf', 'pkg'):
                conf['pkg'] = parser.get('conf', 'pkg')
            else:
                conf['pkg'] = 'base'
            if parser.has_option('conf', 'rootpw'):
                conf['rootpw'] = parser.get('conf', 'rootpw')
            if parser.has_option('conf', 'crypt_rootpw'):
                conf['crypt_rootpw'] = parser.get('conf', 'crypt_rootpw')
            if parser.has_option('conf', 'overlay'):
                conf['overlay'] = parser.get('conf', 'overlay')
        else:
            conf['pkg'] = 'base'

        return conf

    def make_chroot(self):
        '''
        Runs pacman to prepare the chroot
        '''
        p_cmd = 'pacman -Sy --noconfirm -r ' + self.root + ' ' conf['pkg']
        subprocess.call(p_cmd, shell=True)
