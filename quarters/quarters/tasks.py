'''
Parses the present state of resources to determine what needs to be done
'''

import os
import sys
import pickle
import time
import random
import urlgrabber

class Tasks(object):
    '''
    Manage all of the tasks to be executed by quarters.
    '''
    def __init__(self, opts):
        self.opts = opts
        self.aur = {}
        self.gen_repo_data()
        self.tasks = []

    def gen_repo_data(self):
        '''
        Parses the repo directories to acertain the present state of the
        packages, this is run to populate the packages data.
        '''
        for fn_ in os.listdir(self.opts['aur_repo']):
            lst = fn_.split('-')
            ver = lst[-3] + '-' + lst[-2]
            name = fn_[:fn_.index(ver)][:-1]
            self.aur[name] = ver

    def parse_aur(self):
        '''
        Reads the aur file and creates initial tasks for the defined packages.
        '''
        self.gen_repo_data()
        notify = False
        aur = 'http://aur.archlinux.org/rpc.php?type=info&arg='
        for line in open(self.opts['aur_file'], 'r').readlines():
            line = line.strip()
            if line.startswith('#'):
                continue
            data = eval(urlgrabber.urlread(aur + line))
            if data['type'] == 'error':
                # log something
                continue
            if self.aur.has_key(line):
                ver = data['results']['Version']
                if aur[line] < ver:
                    notify = True
            else:
                notify = True
            if notify:
                notp = {'type': 'aur_pkg',
                        'action': 'build_aur_pkg',
                        'name': line}
                notn = str(int(time.time()))\
                     + str(random.randint(1000,9999))
                path = os.path.join(self.opts['not_dir'], notn + 'p')
                pickle.dump(notp, open(path, 'w'))

    def parse_tasks(self):
        '''
        Parses the pickles used to notify the main thread as to the state of
        available resources.
        '''
        for fn_ in os.listdir(self.opts['not_dir']):
            path = os.path.join(self.opts['not_dir'], fn_)
            self.tasks.append(pickle.load(open(path, 'r')))
            os.remove(path)

