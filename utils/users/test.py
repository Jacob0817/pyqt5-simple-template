import os, sys, time, random
o_path = os.getcwd()
sys.path.append(o_path)
from utils.users.models import User, Group, Auth
from utils.settings import sync_db
from peewee_async import Manager

objects = Manager(sync_db)

def create_init_data():
    '''
    生成初始化数据
    '''
    gdatas = [
        {
            'id': -1,
            'group_type': 'SuperAdmin',
            'group_type_cn': '超级管理员'
        },
        {
            'id': 0,
            'group_type': 'Admin',
            'group_type_cn': '管理员'
        },
        {
            'id': 1,
            'group_type': 'NormalUser',
            'group_type_cn': '普通用户'
        }
    ]
    Group.insert_many(gdatas).execute()
    adatas = [
        {
            'id': -1,
            'auth_type': 'SuperAdmin'
        },
        {
            'id': 0,
            'auth_type': 'Admin'
        },
        {
            'id': 1,
            'auth_type': 'DefaultAuthGroup_1'
        },
        {
            'id': 2,
            'auth_type': 'DefaultAuthGroup_2'
        }
    ]
    Auth.insert_many(adatas).execute()
    User.insert(username='sysadmin', password='123456', group=-1, auth=-1).execute()


if __name__ == '__main__':
    start_time = time.time()
    create_init_data()
    print('耗时：', time.time() - start_time)