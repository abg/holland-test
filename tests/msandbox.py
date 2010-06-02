import os, sys
import logging
import subprocess
from testconfig import config as _config

LOG = logging.getLogger(__name__)

def make_sandbox(name, port=None):
    config = _config['mysql_sandbox']
    dist = config['dist']
    root = config['root']
    datadir = config['datadir']
    port = str(port or config['port'])
    os_user = config['os_user']
    mysql_user = config.get('mysql_user', '')
    mysql_pass = config.get('mysql_password', '')

    sb_args = [
        'make_sandbox',
        dist,
        '-U', os_user,
        '--db_user', mysql_user,
        '--db_password', mysql_pass,
        '--upper_directory',
        os.path.abspath(root),
        '--sandbox_directory',
        name,
        '--datadir_from', 'dir:%s' % datadir,
        '--sandbox_port', port,
        '--no_confirm',
        '--force',
    ]
    LOG.debug("%s", subprocess.list2cmdline(sb_args))
    subprocess.check_call(sb_args, close_fds=True)

def clear_sandbox(name):
    path = sandbox_path(name)
    args = [
        os.path.join(path, 'clear')
    ]
    LOG.debug("%s", subprocess.list2cmdline(args))
    subprocess.check_call(args, close_fds=True)

def delete_sandbox(name):
    config = _config['mysql_sandbox']
    root = config['root']
    path = os.path.join(root, name)

    clear_sandbox(name)
    sb_args = [
        'sbtool',
        '--operation', 'delete',
        '--source_dir', os.path.abspath(path),
    ]
    LOG.debug("%s", subprocess.list2cmdline(sb_args))
    subprocess.check_call(sb_args, close_fds=True)

def copy_sandbox(dstname, srcname='main'):
    srcname = sandbox_path(srcname)

    if not sandbox_exists(dstname):
        make_sandbox(dstname, port=int(_config['mysql_sandbox']['port']) + 1)

    dstname = sandbox_path(dstname)

    sb_args = [
        'sbtool',
        '--operation', 'copy',
        '--source_dir', os.path.abspath(srcname),
        '--dest_dir', os.path.abspath(dstname),
    ]
    LOG.debug("%s", subprocess.list2cmdline(sb_args))
    subprocess.check_call(sb_args, close_fds=True)

def start_sandbox(name):
    name = sandbox_path(name)
    start_script = os.path.join(name, 'start')
    args = [
        start_script,
    ]
    LOG.debug("%s", subprocess.list2cmdline(args))
    subprocess.check_call(args, close_fds=True)

def stop_sandbox(name):
    name = sandbox_path(name)
    stop_script = os.path.join(name, 'stop')
    args = [
        stop_script,
    ]
    LOG.debug("%s", subprocess.list2cmdline(args))
    subprocess.check_call(args, close_fds=True)

def sandbox_exists(name):
    root = _config['mysql_sandbox']['root']
    return os.path.exists(os.path.abspath(os.path.join(root, name)))

def run_script_in_sandbox(name, script):
    name = sandbox_path(name)
    use_script = os.path.join(name, 'use')
    sb_args = [
        os.path.abspath(use_script),
    ]

    if isinstance(script, basestring):
        script = open(script, 'r')

    LOG.debug("%s", subprocess.list2cmdline(sb_args))
    subprocess.check_call(sb_args, stdin=script, close_fds=True)

def sandbox_path(name):
    if name == 'main':
        name = _config['mysql_sandbox']['main']

    root = _config['mysql_sandbox']['root']
    return os.path.abspath(os.path.join(root, name))
