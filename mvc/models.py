from django.db import models, connection
import time
import PIL
from django.contrib import admin
from django.utils import timesince, html
from django.utils.encoding import python_2_unicode_compatible
from tmitter.utils import formatter, function


# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField('用户名', max_length=20)
    password = models.CharField('密码', max_length=100)
    realname = models.CharField('姓名', max_length=20)
    email = models.CharField('Email')
    area = models.ForeignKey(Area, verbose_name='地区')
    face = models.ImageField('头像', upload_to='face/%Y/%m/%d', default='', blank=True)
    url = models.CharField('个人主页', max_length=200, default='', blank=True)
    about = models.TextField('关于我', max_length=1000, default='', blank=True)
    addtime = models.DateTimeField('注册时间', auto_now=True)
    friend = models.ManyToManyField('self', verbose_name='好友')

    def __str__(self):
        return self.realname

    def addtime_format(self):
        return self.addtime.strftime('%Y-%m-%d %H:%M:%S')

    def user_save(self, modify_pwd=True):            # 新增，修改函数
        if modify_pwd:
            self.password = function.md5_encode(self.password)
        self.about = formatter.substr(self.about, 20, True)
        super(User, self).save()

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = u'用户'