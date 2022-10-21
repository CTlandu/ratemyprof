from django.db import models

# Create your models here.
class Department(models.Model):
    '''部门表'''
    #id = models.BigAutoField(primary_key=True)
    title = models.CharField(verbose_name="部门名",max_length=32)
    
    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(max_length=64)
    age = models.IntegerField()
    account = models.DecimalField(verbose_name="账户余额",max_digits=10,decimal_places=2, default=0)
    #create_time = models.DateTimeField(verbose_name="入职时间")
    create_time = models.DateField(verbose_name="入职时间")
    
    #on_delete.CASCADE: 级联删除
    #on_delete.SET_NULL: 置空
    department_id = models.ForeignKey(verbose_name="部门",to="Department",to_field="id",null = True, blank = True, on_delete=models.SET_NULL)
    #利用元组来做choice
    gender_choices = (
        (1,"男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别",choices=gender_choices)

class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    price = models.IntegerField(verbose_name="价格")
    level_choices = (
        (1, "1级别"),
        (2, "2级别"),
        (3, "3级别"),
        (4, "4级别")
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    status_choices = (
        (1,"已经占用"),
        (2, "未占用")
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)
    
    