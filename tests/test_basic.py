import os, sys
import subprocess
from testconfig import config
from tests.msandbox import copy_sandbox, start_sandbox, stop_sandbox, \
                           delete_sandbox
from holland.core.spool import Spool

def setup():
    pass

def teardown():
    pass

def test_basic():
    """Testing to see if I can connect to the sandbox"""
    import MySQLdb

    c = MySQLdb.connect(unix_socket='/tmp/mysql_sandbox9999.sock',
            user='root')
    z = c.cursor()
    z.execute('SHOW GLOBAL VARIABLES LIKE \'datadir\'')
    z.fetchone()

def test_mysqldump():
    hl_args = [
        'coverage', 'run', '--append',
        '/usr/sbin/holland',
        '--config', os.path.abspath('tests/conf/holland.conf'),
        'backup',
        'default',
    ]
    subprocess.check_call(hl_args, close_fds=True)
    spool = Spool(os.path.abspath('backups'))
    last_backup = [x for x in spool.list_backups('default')][-1]
