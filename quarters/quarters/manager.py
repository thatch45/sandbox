'''
Manage the processes running the actions.
'''

import multiprocessing
import os
import time
import subprocess

import quarters.builder as builder
import quarters.tasks as tasks

class Manager(object):
    '''
    Manage the worker processes.
    '''
    def __init__(self, opts):
        self.opts = opts
        self.workers = self.__init_procs()
        self.tasks = tasks.Tasks(opts)
        self.actions = {'aur': [],
                        'aur_repo': False,
                        'svn': [],
                        'svn_repo': False}

    def __init_procs(self):
        '''
        Set up the worker processes
        '''
        aur = []
        svn = []
        for num in range(0, self.opts['builders']):
            aur.append(builder.AURBuilder(self.opts, num))
            #svn.append(builder.SVNBuilder(self.opts, num))

        return {'aur': aur,
                'svn': svn}

    def _get_running(self):
        '''
        Detreminte what processes are availabe, and how many are running.
        '''
        running = {'aur': 0,
                   'svn': 0}
        for build in self.workers['aur']:
            if build.is_alive():
                running['aur'] += 1
        for build in self.workers['svn']:
            if build.is_alive():
                running['svn'] += 1
        return running

    def _load_actions(self):
        '''
        Load and start the processes
        '''
        for task in self.tasks.tasks:
            if task['action'] == 'build_aur_pkg':
                self.actions['aur'].append(task['name'])
            elif task['action'] == 'rebuild_aur':
                self.actions['aur_repo'] = True

    def _build_repo(self, repo):
        '''
        Cleans out old files and rebuilds the repo
        '''
        # This can be made a LOT better!
        files = {}
        old = []
        for fn_ in os.listdir(self.opts[repo]):
            if not fn_.endswith('pkg.tar.xz'):
                continue
            lst = fn_.split('-')
            ver = lst[-3] + '-' + lst[-2]
            name = fn_[:fn_.index(ver)][:-1]
            if files.has_key(name):
                files[name].append(ver)
            else:
                files[name] = [ver]
        for key in files:
            if len(files[key]) == 1:
                continue
            files[key].sort()
            while len(files[key]) > 1:
                old.append(key + '-' + files[key].pop(0))
        for fn_ in old:
            path = os.path.join(self.opts[repo], fn_)
            os.remove(path)
        db_path = os.path.join(self.opts[repo], repo[:-5] + '.db.tar.gz')
        if os.path.isfile(db_path):
            os.remove(db_path)
        r_cmd = 'repo-add -q ' + db_path + ' ' + os.path.join(self.opts[repo],
                '*')
        subprocess.call(r_cmd, shell=True)

    def _run_actions(self):
        '''
        Figure out how many actions are required, divide them up to the
        seperate builders.
        '''
        avail = 0
        if self.actions['aur_repo']:
            self._build_repo('aur_repo')
            self.actions['aur_repo'] = False
        running = self._get_running()
        active = 0
        for key in running:
            active += running[key]
        if active < self.opts['builders']:
            avail = self.opts['builders'] - active
        else:
            return
        while avail:
            aur = len(self.actions['aur'])
            svn = len(self.actions['svn'])
            if self.actions['aur']:
                for ind in range(0, len(self.workers['aur'])):
                    if self.actions['aur']:
                        if not self.workers['aur'][ind].is_alive():
                            if self.workers['aur'][ind].exitcode != None:
                                self.workers['aur'][ind] = builder.AURBuilder(self.opts, ind)
                            self.workers['aur'][ind].pkg = self.actions['aur'].pop(0)
                            self.workers['aur'][ind].start()
                            avail -= 1
            if self.actions['svn']:
                for build in self.workers['svn']:
                    if self.actions['svn']:
                        if not build.is_alive():
                            build.pkg = self.actions['svn'].pop(0)
                            build.start()
                            avail -= 1
            if aur + svn == 0:
                return

    def serve(self):
        '''
        Start working!
        '''
        start = 0
        while True:
            if time.time() - self.opts['aur_wait'] * 60 > start:
                self.tasks.parse_aur()
                start = time.time()
            self.tasks.parse_tasks()
            self._load_actions()
            self._run_actions()
            time.sleep(self.opts['poll_wait'] * 60)


