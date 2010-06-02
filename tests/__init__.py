import os, sys
import subprocess
from holland.core.spool import Spool
from testconfig import config
from tests.msandbox import make_sandbox, start_sandbox, delete_sandbox

def setup():
    make_sandbox(config['mysql_sandbox']['main'])
    start_sandbox(config['mysql_sandbox']['main'])

def teardown():
    delete_sandbox(config['mysql_sandbox']['main'])
