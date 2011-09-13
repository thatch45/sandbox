#!/usr/bin/env python2
'''
Return the total size of a passed file type in a specified dir
'''

import os
import re
import optparse

def rummage(path, exper):
    '''
    Walk through the dirs for the specified file
    '''
    size = 0
    for root, dirs, files in os.walk(path):
        for fn_ in files:
            if re.match(exper, fn_):
                size += os.path.getsize(os.path.join(root, fn_))
    return 'Size in MB: {0}'.format(size/1024/1024)


def parse():
    '''
    Parse the command line options
    '''
    parser = optparse.OptionParser()
    parser.add_option('-p',
            '--path',
            dest='path',
            default='.',
            help='The root path to scan')
    parser.add_option('-e',
            '--regex',
            dest='regex',
            default='.*',
            help='The regex to check for')

    options, args = parser.parse_args()
    opts = {
            'path': options.path,
            'regex': options.regex}
    return opts

def main():
    '''
    Run the main man!
    '''
    opts = parse()
    print rummage(opts['path'], opts['regex'])

if __name__ == '__main__':
    main()
