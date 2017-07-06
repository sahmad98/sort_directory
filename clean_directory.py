#!/usr/bin/env python

import os
from optparse import OptionParser
from ConfigParser import RawConfigParser
import shutil

parser = OptionParser()
config = RawConfigParser(allow_no_value=True)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def pr_waring(text):
    print bcolors.WARNING + '[WARNING] ' + bcolors.ENDC + text

def pr_info(text):
    print bcolors.OKBLUE + '[INFO] ' + bcolors.ENDC + text

def main(directory):
    extension_map = {}
    print 'Sorting Directory: %s' % (directory)
    config.read('extension.cfg')
    for section in config.sections():
        for extension in config.options(section):
            extension_map[extension] = section
    tree = os.walk(directory)
    tree = tree.next()
    files = tree[2]
    dirs = tree[1]
    for f in files:
        ext = f.split('.')[-1]
        ext = ext.lower()
        try:
            file_type = extension_map[ext]
            pr_info('Moving File %s to %s' % (f, file_type))
            if file_type in dirs:
                shutil.move('%s/%s' % (directory, f), '%s/%s/%s'%(directory, file_type, f))
            else:
                os.mkdir('%s/%s' % (directory, file_type))
                shutil.move('%s/%s' % (directory, f), '%s/%s/%s'%(directory, file_type, f))
        except KeyError as e:
            pr_waring('Unknown File extension %s' % (ext))

if __name__ == '__main__':
    parser.add_option('-d', '--directory', dest = 'directory', help='Path to directory to sort', default='.')
    (option, args) = parser.parse_args()
    directory = option.directory  
    main(directory)  