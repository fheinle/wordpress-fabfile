#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" Wordpress Deploy configuration """
import os

# Add ssh-reachable hosts here
HOSTS = ['user@host:port']

# Enter where you keep your sourcecode
CODE_DIR_REMOTE="/vNar/www/wordpress/"
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

# Queries to run after migrating your database to another host
# changes siteurl and home in wp_config and any embedded urls in posts
# If you want to review or change those, refer to the files
MIGRATE_TO_REMOTE_QUERY = open('wp_migrate_to_remote.sql').read()
MIGRATE_TO_LOCAL_QUERY = open('wp_migrate_to_local.sql').read()