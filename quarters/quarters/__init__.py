#!/usr/bin/python2

import quarters.manager as manager

def serve(opts):
    man = manager.Manager(opts)
    man.serve()
