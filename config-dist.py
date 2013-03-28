#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" Wordpress Deploy configuration """
import os

# Add ssh-reachable hosts here
HOSTS = ['user@host:port']

# Enter where you keep your sourcecode
CODE_DIR_REMOTE="/var/www/wordpress/"
CODE_DIR_LOCAL='%s/dev/wordpress/' % os.getenv('HOME')

# What your git remote location is called
# You'll have to add these to both your local and remote branch!
GIT_REMOTE_NAME = 'remote'

# Fill out these database details
# Currently, there's only two database hosts supported,
# local dev and remote prod (or staging)
DBASE = {
	'local':{
		'host':'localhost',
		'user':'localuser',
		'password':'localpassword',
		'name':'wordpress',
	},
	'remote':{
		'host':'localhost',
		'user':'remoteuser',
		'password':'remotepassword',
		'name':'wordpress',
	}
}