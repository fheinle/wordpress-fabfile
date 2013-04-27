#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" deploy wordpress """

# Prereq:
# mysql allows connection from other hosts
# "dumps" directory in cwd

from __future__ import with_statement
import time
import shutil, os

from fabric.api import cd, lcd, local, run, get, put, settings, abort, env
from fabric.contrib.console import confirm

from config import HOSTS, CODE_DIR_LOCAL, \
                   CODE_DIR_REMOTE, DBASE, GIT_REMOTE_NAME
env.hosts = HOSTS

# commands

def dump_local_database():
    """Dump local database and save to dumps folder

    returns dump filename"""
    invocation, filename = _make_db_dump_string(db_location='local')
    local(invocation)
    shutil.move(filename, os.path.join(os.getcwd(), 'dumps'))
    return os.path.join(
        os.getcwd(),
        'dumps',
        os.path.split(filename)[-1]
    )

def dump_remote_database():
    """Dump local database and download to dumps folder

    returns local dump filename"""
    invocation, filename = _make_db_dump_string(db_location='remote')
    run(invocation)
    get(filename, os.path.join(os.getcwd(), 'dumps'))
    return os.path.join(
        os.getcwd(),
        'dumps',
        os.path.split(filename)[-1]
    )

def push_local_code():
    """Push local code to production host with some host in the middle

    shows git status beforehand and asks to continue"""
    with lcd(CODE_DIR_LOCAL):
        local('git status')
        if confirm('Fortfahren?'):
            _push_code_to_host_from_local()
            _pull_code_from_host_to_remote()
        else:
            abort('User abort')

def pull_remote_code():
    """Pull remote code to local dev repo with some host in the middle

    shows git status beforehand and asks to continue"""
    with cd(CODE_DIR_REMOTE):
        run('git status')
        if confirm('Continue?'):
            _push_code_to_host_from_remote()
            _pull_code_from_host_to_local()
        else:
            abort('User abort')

def push_local_database():
    """deploy local database to production host

    changes there will be lost, siteurl and home settings will be corrected"""
    local_database_filename = dump_local_database()
    remote_database_filename = put(local_database_filename, '/tmp/', mode=0400)
    run(_make_db_import_string('remote', remote_database_filename[0]))
    with settings(warn_only=True):
        if run("test -f %s" % os.path.join(
            CODE_DIR_REMOTE,
            'wp_migrate_to_remote.sql')
        ).failed:
            put('wp_migrate_to_remote.sql', CODE_DIR_REMOTE)
    run(_make_db_import_string(
        'remote',
        os.path.join(CODE_DIR_REMOTE, 'wp_migrate_to_remote.sql')
        )
    )

def pull_remote_database():
    """deploy remote database to local dedvelopment host

    changes here will be lost, siteurl and home settings will be corrected"""
    remote_database_filename = dump_remote_database()
    local(_make_db_import_string(
        'local',
        remote_database_filename
        )
    )
    local(_make_db_import_string(
        'local',
        os.path.join(os.getcwd(), 'wp_migrate_to_local.sql')
        )
    )

def sync_uploads():
    """two-way sync wp-content/sync_uploads
    requires unison and configuration! See README"""
    with settings(warn_only=True):
        if local('test -L %s' % os.path.join(
            os.getenv('HOME'),
            '.unison',
            'uploads-sync.prf'
            )
        ).failed:
            _create_unison_profile()
    local('unison -batch uploads-sync')

# {{ helper functions

def _pull_code_from_host_to_remote():
    """pull code from some remote location to remote repo

    has to be defined in your git repo!
    (git remote add)"""
    with cd(CODE_DIR_REMOTE):
        run('git pull %s master' % GIT_REMOTE_NAME)

def _pull_code_from_host_to_local():
    """pull code from some remote location to local repo

    has to be defined in your git repo!
    (git remote add)"""
    with lcd(CODE_DIR_LOCAL):
        run('git pull %s master' % GIT_REMOTE_NAME)

def _push_code_to_host_from_remote():
    """push code on remote location to repo

    has to be defined in your git repo!
    (git remote add)"""
    with cd(CODE_DIR_REMOTE):
        run('git push %s master' % GIT_REMOTE_NAME)

def _push_code_to_host_from_local():
    """push code to some remote location

    has to be defined in your git repo!
    (git remote add)"""
    with lcd(CODE_DIR_LOCAL):
        local('git push %s master' % GIT_REMOTE_NAME)

def _create_unison_profile():
    """creates a new unison profile for uploads sync

    per default uses only the first host from config, if you want more,
    you're free to change the file, as it's not overwritten.

    Creates a symlink to unison's config directory"""
    local_path = CODE_DIR_LOCAL
    remote_path = 'ssh://%s/%s' % (HOSTS[0], CODE_DIR_REMOTE)

    with open('uploads-sync.prf', 'w') as profile:
        for item in (local_path, remote_path):
            profile.write('root = %s\n' % os.path.join(
                item,
                'wp-content/uploads/')
            )
    unison_config_file = os.path.join(
        os.getenv('HOME'),
        '.unison',
        'uploads-sync.prf'
    )
    os.symlink(
        os.path.join(os.getcwd(), 'uploads-sync.prf'),
        unison_config_file
    )

# }} {{ helper helper functions

def _make_db_dump_string(db_location='local'):
    """create mysqldump invocation
    
    returns invocation syntax, dump file path and name
    """
    db_config = DBASE[db_location]
    filename = '/tmp/db-%s-%s-%s.db' % (
        db_config['host'], db_config['name'], time.strftime('%s')
    )
    invoc = 'mysqldump -h%s -u%s -p%s %s > %s' % (
        db_config['host'], db_config['user'],
        db_config['password'], db_config['name'], 
        filename,
    )
    return (invoc, filename)

def _make_db_import_string(db_location='local', dump_filename=''):
    """create mysql invocation

    returns invocation syntax"""
    db_config = DBASE[db_location]
    invoc = "mysql -h%s -u%s -p%s %s<%s" % (
        db_config['host'], db_config['user'],
        db_config['password'], db_config['name'], dump_filename
    )
    return invoc

# EOF }}
#   with settings(warn_only=True):
