'''
Creates an image file and formats it
'''
import subprocess
import sys
import os
import configparser
import collections

class Image(object):
    '''
    Create a virtual machine image and mounts it to the chroot directory.
    '''
    def __init__(self, opts):
        '''
        Instansiates the object used 
        '''
        self.lfs = ['ext2', 'ext3', 'ext4', 'reiserfs', 'xfs', 'jfs']
        self.opts = self.__setup_root(opts)
        self.conf, self.disk = self.__get_config()
        self.node = self.__init_image()

    def __setup_root(self, opts):
        if opts['chroot_dir']:
            err = 'For virtual machine images a temporary chroot dir is '\
                + 'created, please execute without the --chroot-dir option'
            sys.stderr.write(err, '\n')
            sys.exit(43)
        opts['chroot_dir'] = tempdir.mkdtemp()
        return opts

    def __get_config(self):
        '''
        Parses out the values from the configuration file pertinant to image
        creation.
        Returns a tuple of 2 dict objects, the first is the configuration
        values, the second is the values for the disk partitioning.
        '''
        formats = ['qcow2',
                   'raw']
        conf = {}
        disk = {}
        parser = configparser.ConfigParser()
        if parser.has_option('disk', 'format'):
            fmt = parser.get('disk', 'format')
            if not formats.count(fmt):
                conf['format'] = 'qcow2'
            else:
                conf['format'] = fmt
        else:
            conf['format'] = 'qcow2'
        if parser.has_option('disk', 'size'):
            size = parser.get('disk', 'size')
            if not ['K', 'M', 'G', 'T'].count(size[-1]):
                size = size + 'G'
            conf['size'] = size
        else:
            conf['size'] = '20G'
        if parser.has_section('disk'):
            for opt in parser.options('disk'):
                if opt == 'format' or opt == 'size':
                    continue
                vals = (opt.split('_'))
                if disk.has_key(vals[0]):
                    disk[vals[0]][vals[1]] = parser.get('disk', opt)
                else:
                    disk[vals[0]] = {vals[1]: parser.get('disk', opt)}
        return conf, disk

    def __sfdisk_cmd(self):
        '''
        Returns the sfdisk command used to partition the disk.
        '''
        # TODO - Error checking, if the parts are bigger than the disk
        # TODO - Verify that the size values are formated propperly
        parts = {}
        s_cmd = 'sfdisk -L -uM NODE << EOF\n'
        for key in self.disk:
            if key.startswith('p'):
                parts[key] = self.disk[key]
        parts = collections.OrderedDict(sorted(parts.items(), key=lambda t: t[0]))
        for key in parts:
            size = parts[key][size]
            fs = parts[key][fs]
            mode = ''
            if size.endswith('G'):
                size = str(int(size[:-1]) * 1024)
            elif size.endswith('T'):
                size = str(int(size[:-1]) * 1024 * 1024)
            elif size.endswith('M'):
                size = size[:-1]
            elif size.endswith('K'):
                print('Get out, K? No, I refuse!', file=sys.stderr)
                sys.exit(-42)
            elif size == 'rest':
                size = ''
            if self.lfs.count(fs):
                mode = 'L'
            elif fs == 'swap':
                mode = 'S'
            elif fs == 'pv':
                mode = '8e'
            s_cmd += ',' + size + ',' + mode + '\n'
        s_cmd += 'EOF'
        return s_cmd

    def __init_image(self):
        '''
        Initial setup of the image, this involves the creation of the image
        through the making available of the image via qemu-nbd
        Returns the node where the image is available.
        '''
        # TODO - Add error cheching for all paths
        # TODO - Make sure the nbd is cleaned up if the process fails!
        node = '/dev/nbd9'
        i_cmd = 'qemu-img create -f ' self.conf['format'] + ' '\
              + self.opts['output'] + ' ' + self.conf['size']
        subprocess.call(i_cmd, shell=True)
        m_cmd = 'modprobe nbd max_part=63'
        b_cmd = 'qemu-nbd -c ' + node + ' ' + self.opts['output']
        subprocess.call(m_cmd, shell=True)
        subprocess.call(b_cmd, shell=True)
        return node

    def part_disk(self, sf_cmd):
        '''
        Partitions the disk
        Takes the sfdisk command and the node location
        '''
        sf_cmd = sf_cmd.replace('NODE', self.node)
        subprocess.call(sf_cmd, shell=True)

    def mkfs_all(self):
        '''
        Creates filesystems on the disks, this includes setting up of all lvm
        settings.
        '''
        # TODO - I'm sure this could be done faster, but the data sets are
        # always very small - but - I'm sure this can be done faster
        parts = {}
        vgs = {}
        lvs = {}
        tomount = []
        for key in self.disk:
            if key.startswith('p'):
                parts[key] = self.disk[key]
        for key in self.disk:
            if key.startswith('v'):
                vgs[key] = self.disk[key]
        for key in self.disk:
            if key.startswith('l'):
                lvs[key] = self.disk[key]
        for key in parts:
            self.mkfs(self.node + part, parts[key]['fs'])
            if parts[key].has_key('mount'):
                tomount.append((self.node + key, parts[key]['mount']))
        for key in vgs:
            self.mk_vol(key.split('_')[1], vgs[key][key.split('_')[1]].split(','))
        for key in lvs:
            self.mk_lv(lvs[key]['name'], lvs[key]['size'], lvs[key]['vg'])
            self.mkfs(os.path.join('/dev', lvs[key]['vg'], lvs[key]['name']),
                      lvs[key]['fs'])
            tomount.append((os.path.join('/dev',
                lvs[key]['vg'],
                lvs[key]['name']),
                    lks[key]['mount']))
        


    def mkfs(self, part, fs):
        '''
        Creates a single filesystem on the passed partition
        '''
        cmd = ''
        if self.lfs.count(fs):
            cmd = 'mkfs.' + fs + ' ' + part
        elif fs == 'pv':
            cmd = 'pvcreate ' + part
        elif fs == 'swap':
            cmd = 'mkswap ' + part
        else:
            print('Invalid filesystem ' + fs + ' specified.', file=sys.stderr)
            sys.exit(-42)
        subprocess.call(cmd, shell=True)

    def mk_vol(self, name, pvs):
        '''
        Creates a volume group, all physical volumes must be present and the
        volume group name must be available
        '''
        cmd = ['vgcreate', name].extend(pvs)
        subprocess.call(cmd)
        
    def mk_lv(self, name, size, vg):
        '''
        Creates the logical volume
        '''
        cmd = 'lvcreate -l ' + size + ' -n ' + name + ' ' + vg
        subprocess.call(cmd, shell=True)

    def mount(self, device, mountpoint):
        '''
        Mounts a single device
        '''
        mountpoint = os.path.join(self.opts['chroot_dir'], mountpoint)
        if not os.path.isdir(mountpoint):
            os.makedirs(mountpoint)
        m_cmd = 'mount ' + device + ' ' + mountpoint
        subprocess.call(m_cmd, shell=True)
