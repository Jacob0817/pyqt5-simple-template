import os, sys
o_path = os.getcwd() 
sys.path.append(o_path)
from utils.settings import sync_db
from utils.users.models import User, Group, Auth, AuthPermission
from peewee import SqliteDatabase
#from playhouse.migrate import *

def run_create():
    '''创建表'''
    sync_db.connect()

    Group.create_table()
    Auth.create_table()
    AuthPermission.create_table()
    User.create_table()
    sync_db.close()

if __name__ == '__main__':
    run_create()