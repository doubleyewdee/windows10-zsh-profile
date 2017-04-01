#!/usr/bin/env python3

import hashlib
import optparse
import os
import shutil
import sys

def get_file_digest(fname):
    hasher = hashlib.sha256()
    with open(fname, 'rb') as fp:
        hasher.update(fp.read())
    return hasher.hexdigest()

def prompt_install(dest):
    resp = input('Update {0}? [y/N] '.format(dest))
    return resp.lower() == 'y'

def install_one_file(src, dest, options):
    '''
    Potentially install a file by determining if it does not match the source's hash or does
    not exist, respecting input options for verbosity/no-op/auto-install.
    '''

    update = False
    
    src_hash = get_file_digest(src)

    if not os.path.exists(dest):
        if options.verbose:
            print('Destination {0} does not exist.'.format(dest))
        update = True
    else:
        if not os.path.isfile(dest):
            print('Destination {0} exists but is not a file. Giving up for now. Blame the author.')
            return

        dest_hash = get_file_digest(dest)
        if dest_hash != src_hash:
            print('Destination {0} hash ({1}) does not match source hash ({2})'.format(dest, dest_hash, src_hash))
            update = True
        elif options.verbose:
            print('Destination {0} hash ({1}) matches source hash ({2})'.format(dest, dest_hash, src_hash))
    
    if options.no_update:
        return
    if update and not options.auto_update:
        update = prompt_install(dest)
    
    if update:
        if options.verbose:
            print('Updating {0} from {1}'.format(dest, src))
        shutil.copy(src, dest)

def install_one_dir(src, dest, options, dot_prefix = False):
    '''
    Potentially replicate a directory (recursively) while respecting options for verbosity etc
    '''

    if options == None:
        options = object()
        options.no_update = True
        options.verbose = False
        options.auto_update = False

    walk = False
    if not os.path.exists(dest):
        if options.verbose:
            print('Destination directory {0} does not exist.'.format(dest))
        create = not options.no_update
        if not options.auto_update and create:
            create = prompt_install(dest)

        if create:
            # sooo yeah idk if 755 is right but fuck it let's do this.
            if options.verbose:
                print('Creating directory {0}', dest)
            os.mkdir(dest, mode=0o755)
            walk = True
    elif not os.path.isdir(dest):
        print('Destination {0} exists but is not a directory. Giving up for now. Blame the author.')
        return
    else:
        walk = True
    
    if not walk:
        return

    for item in os.listdir(src):
        item_abs = os.path.join(src, item)
        if dot_prefix:
            dest_abs = os.path.join(dest, '.' + item)
        else:
            dest_abs = os.path.join(dest, item)

        if os.path.isfile(item_abs):
            install_one_file(item_abs, dest_abs, options)
        elif os.path.isdir(item_abs):
            install_one_dir(item_abs, dest_abs, options)

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-n', '--no-update', action='store_true', dest='no_update',
                      help='Do not update any files, only report on possible changes.')
    parser.add_option('-y', '--auto-update', action='store_true', dest='auto_update',
                      help='Automatically update all files without matching checksums.')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose',
                      help='Produce verbose output.')

    src_dir = os.path.join(os.path.dirname(__file__), 'src')
    home_dir = os.getenv('HOME')
    if home_dir == None or len(home_dir) < 1:
        raise Exception('Could not find home directory from $HOME ???')
    
    (options, args) = parser.parse_args(sys.argv)
    print('Installing files from {0} -> {1}'.format(src_dir, home_dir))
    install_one_dir(src_dir, home_dir, options, dot_prefix = True)
