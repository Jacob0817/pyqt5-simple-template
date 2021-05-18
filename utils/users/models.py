import os, sys
from utils.settings import sync_db
from peewee import *
from datetime import datetime
from bcrypt import hashpw, gensalt

class BaseModel(Model):
    create_time = DateTimeField(default=datetime.now, verbose_name="Time of user creation", help_text='Time of user creation')
    update_time = DateTimeField(default=datetime.now, verbose_name='Time of amendment', help_text='Time of amendment')

    class Meta:
        database = sync_db

    def save(self, *args, **kwargs):
        if self._get_pk_value() is None:
            self.create_time = datetime.now()
        self.update_time = datetime.now()
        return super(BaseModel, self).save(*args, **kwargs)
    
    def update(self, *args, **kwargs):
        self.update_time = datetime.now()
        return super(BaseModel, self).update(*args, **kwargs)

class PasswordHash(bytes):
    def check_password(self, password):
        password = password.encode('utf-8')
        return hashpw(password, self) == self


class PasswordField(BlobField):
    def __init__(self, iterations=12, *args, **kwargs):
        if None in (hashpw, gensalt):
            raise ValueError('Missing library required for PasswordField: bcrypt')
        self.bcrypt_iterations = iterations
        self.raw_password = None
        super(PasswordField, self).__init__(*args, **kwargs)

    def db_value(self, value):
        """Convert the python value for storage in the database."""
        if isinstance(value, PasswordHash):
            return bytes(value)

        if isinstance(value, str):
            value = value.encode('utf-8')
        salt = gensalt(self.bcrypt_iterations)
        return value if value is None else hashpw(value, salt)

    def python_value(self, value):
        """Convert the database value to a pythonic value."""
        if isinstance(value, str):
            value = value.encode('utf-8')

        return PasswordHash(value)


class Group(BaseModel):
    group_type_choices = (
        ('SuperAdmin', '超级管理员'),
        ('Admin', '管理员'),
        ('NormalUser', '普通用户'),
    )
    group_type = CharField(max_length=128, choices=group_type_choices, verbose_name='用户组类型')
    group_type_cn = CharField(max_length=128, verbose_name='用户组类型_cn')

    class Meta:
        table_name = 'Group'


class Auth(BaseModel):
    auth_type = CharField(max_length=128, verbose_name='权限名称')

    class Meta:
        db_table = 'Auth'


class AuthPermission(BaseModel):
    object_name = CharField( max_length=128, verbose_name='功能名称')
    object_name_cn = CharField(max_length=128, verbose_name='功能名称_cn')
    auth = ForeignKeyField(Auth, on_delete='CASCADE', verbose_name='权限组', related_name='auth_permissions')
    auth_list = SmallIntegerField(default=0, verbose_name='查看')
    auth_create = SmallIntegerField(default=0, verbose_name='新增')
    auth_update = SmallIntegerField(default=0, verbose_name='修改')
    auth_destroy = SmallIntegerField(default=0, verbose_name='删除')

    class Meta:
        db_table = 'AuthPermission'


class User(BaseModel):
    # 管理员时使用账户密码登录
    username = CharField(max_length=32, default='', verbose_name='用户账号')
    password = PasswordField(default='000000', verbose_name="密码")
    email = CharField(default='', verbose_name='用户邮箱')
    gender = IntegerField(choices=((0, '未知'), (1, '男'), (2, '女')), default=0, verbose_name='性别')
    is_freeze = IntegerField(default=0, choices=((0, '否'),(1, '是')),  verbose_name='是否冻结')
    # is_admin = BooleanField(default=False, verbose_name='是否管理员')
    group = ForeignKeyField(Group, on_delete='RESTRICT', verbose_name='用户组')
    # 组权分离后 当有权限时必定为管理员类型用户，否则为普通用户
    auth = ForeignKeyField(Auth, on_delete='RESTRICT', null=True, verbose_name='权限组')
    # 当auth被删除时，当前user的auth会被保留，但是auth下的auth_permissions会被删除，不返回
    last_login_time = DateTimeField(null=True, verbose_name='上次登录时间')

    class Meta:
        db_table = 'User'
