'''
Reads the upstream scm.
'''

import os
import sys
import subprocess

class ArchSVN:
    '''
    Reads SVN repos.
    '''
    def __init__(self, opts):
        '''
        Pass the options structure, we want those in here.
        '''
        self.opts = opts
        self.svn_repos = self.__gen_svn_repos()
        
        {'packages': 'svn://svn.archlinux.org/packages',
         'community': 'svn://svn.archlinux.org/community'}

    def __gen_svn_repos(self):
        '''
        Generate the svn repos
        '''
        svn_repos = {}
        if self.opts['core_pkg']:
            svn_repos['packages'] = 'svn://svn.archlinux.org/packages'
        if self.opts['community_pkg']:
            svn_repos['community'] = 'svn://svn.archlinux.org/community'
        if self.opts['svn_repos']:
            for key in self.opts['svn_repos']:
                svn_repos[key] = self.opts['svn_repos'][key]
        return svn_repos

    def _update_repos(self):
        '''
        Check the state of the svn repositories
        '''
        up = set()
        co = set()
        fresh = {}
        if not os.path.isdir(self.opts['svn_root']):
            os.makedirs(self.opts['svn_root'])
        for key in self.svn_repos:
            if os.path.isdir(os.path.join(self.opts['svn_root'], key)):
                up.add(key)
            else:
                co.add(key)
        cwd = os.getcwd()
        os.chdir(self.opts['svn_root'])
        for key in up:
            os.chdir(os.path.join(self.opts['svn_root'], key))
            subprocess.getoutput(['svn', 'up'])
        os.chdir(self.opts['svn_root'])
        for key in co:
            subprocess.getoutput('svn co ' + self.svn_repos[key])
        os.chdir(cwd)



