'''
Manages the aif files, takes one as input and modifies it to make the virtual
image.
'''

import os
import sys
import tempfile
import subprocess

class AIF:
    '''
    Manages the aif files, and executes the aif application
    '''
    def __init__(self, opts, nbd):
        self.opts = opts
        self.nbd = nbd
        self.aif, self.target = self.__mk_conf()

    def __mk_conf(self):
        '''
        Generate the configuration file passed to AIF, returns the path to the
        modified aif file
        '''
        target = tempfile.mkdtemp()
        lines = open(self.opts['conf'], 'r').readlines()
        err = 0
        for index in range(0, len(lines)):
            lines[index] = lines[index].replace('GRUB_DEVICE=/dev/sda',
                    'GRUB_DEVICE=' + self.nbd)
            lines[index] = lines[index].replace('GRUB_DEVICE=/dev/vda',
                    'GRUB_DEVICE=' + self.nbd)
            lines[index] = lines[index].replace('/dev/sda ', self.nbd + ' ')
            lines[index] = lines[index].replace('/dev/sda', self.nbd + 'p')
            lines[index] = lines[index].replace('/dev/vda ', self.nbd + ' ')
            lines[index] = lines[index].replace('/dev/vda', self.nbd + 'p')
            if lines[index].count('/dev/vd') or lines[index].count('/dev/sd') or lines[index].count('/dev/hd'):
                print('''References are made in the aif file to a second disk,
                        only one disk is supported, EXITING''',
                        file=sys.stderr)
                sys.exit()
        lines.append('var_TARGET_DIR=' + target  + '\n')
        lines.append('PACMAN_TARGET="pacman --root $var_TARGET_DIR --config /tmp/pacman.conf"\n')
        lines.extend(['\nworker_mkinitcpio ()\n',
        '{\n',
        'sed -i s,MODULES=\\",MODULES=\\"virtio\\ virtio_blk\\ virtio_pci\\ , $var_TARGET_DIR/etc/mkinitcpio.conf\n',
        'run_mkinitcpio\n',
        '}\n'])
        aif = '/tmp/working.aif'
        open(aif, 'w+').writelines(lines)
        return aif, target
            
    def run_aif(self):
        '''
        If this in run without the correct files and ops in place you may
        destroy your system.  YOU HAVE BEEN WARNED!
        '''
        a_cmd = 'aif -p automatic -c ' + self.aif
        subprocess.call(a_cmd, shell=True)
