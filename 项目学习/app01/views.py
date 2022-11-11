from ensurepip import bootstrap
from socket import fromshare
from tokenize import endpats
from xml.dom import ValidationErr
from django.shortcuts import render,redirect
from django.urls import is_valid_path
from matplotlib import widgets
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe

from app01.utils.pagination import Pagination
from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5

# Create your views here.
def depart_list(request):
    '''部门列表'''
    # 去数据库获取所有的部门列表
    # [对象，对象，对象]
    queryset = models.Department.objects.all()  
    return render(request, 'depart_list.html', {'queryset': queryset})

def depart_add(request):
    #添加部门
    if request.method == "GET":
        return render(request, "depart_add.html")
    else:
        title = request.POST.get("title")
    
    #保存到数据库
    models.Department.objects.create(title = title)
    
    #重定向回
    return redirect("/depart/list/")

def depart_delete(req):
    '''删除部门'''
    nid = req.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect("/depart/list/")

def depart_edit(req, nid):
    '''修改部门'''
    #根据nid来获取数据
    if req.method == "GET":
        row_object = models.Department.objects.filter(id=nid).first()
    
        return render(req, "depart_edit.html", {"row_object": row_object})
    else:
        title = req.POST.get("title")
        #根据id找到数据中的数据并更新
        models.Department.objects.filter(id=nid).update(title = title)
        return redirect("/depart/list/")

def user_list(request):
    '''用户管理'''
    #获取所有用户列表
    queryset = models.UserInfo.objects.all()
    #for obj in queryset:
        #数据库里所属部门是“department_id_id (第二个的id是自动生成的)”，那么如果用
        #obj.department_id就是自动获取foreign key（django内置）
        
        #print(obj.id,obj.name,obj.get_gender_display(),obj.department_id.title)
    page_obj = Pagination(request, queryset, page_size=2)
    context = {
        "queryset": page_obj.page_queryset,
        "page_string": page_obj.html(),
        }
    
    return render(request, 'user_list.html', context)

def user_add(request):
    if request.method == "GET":
        context = {
            'gender_choices': models.UserInfo.gender_choices,
            'depart_list': models.Department.objects.all()
        }
        return render(request, "user_add.html", context)
    
    user = request.POST.get('user')
    pwd = request.POST.get('password')
    age = request.POST.get('age')
    account = request.POST.get('account')
    ctime = request.POST.get('ctime')
    gender_id = request.POST.get('gender')
    department_id = request.POST.get('department')
    
    models.UserInfo.objects.create(name=user,password=pwd,age=age,account=account,create_time=ctime,gender=gender_id,department_id_id= department_id)

    return redirect("/user/list/")

'''modelform实例'''
from django import forms

class UserModelForm(BootStrapModelForm):
    name = forms.CharField(min_length=3,label="用户名")
    password = forms.CharField(min_length=6,label="密码")
    
    class Meta:
        model = models.UserInfo
        fields = ["name","password","age","account","create_time","gender","department_id"]

def user_modelform_add(request):
    if request.method =="GET":
        
        form = UserModelForm()
        return render(request, "user_modelform_add.html", {"form":form})
    #用POST提交数据,数据校验。
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        #{'name': '123', 'password': '12345', 'age': 12, 'account': Decimal('0'), 'create_time': datetime.datetime(2001, 12, 20, 0, 0, 
        #tzinfo=backports.zoneinfo.ZoneInfo(key='UTC')), 'gender': 1, 'department_id': <Department: 媒体企划>}
        
        #如果数据合法 保存到数据库
        form.save()
        return redirect("/user/list/")
    else:
        #校验失败：
        return render(request, "user_modelform_add.html", {"form":form})
    
def user_edit(request, nid):
    form = UserModelForm()
    row_object = models.UserInfo.objects.filter(id=nid).first()
    
    # 根据ID去数据库获取要编辑的那一行数据
    if request.method == "GET":
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {"form":form})
    
    #将用户新提交的数据更新
    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        #默认保存的是用户输入的所有数据, 如果想要在用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')
    
    return render(request, 'user_edit.html', {"form":form})

def user_delete(request,nid):
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')

def mobile_list(request):
    
    # 方法1
    # q = models.PrettyNum.objects.filter(mobile="18938690936",id=2)
    # print(q)
    
    # 方法2
    # data_dict = {"mobile":"18938690936","id":6}
    # models.PrettyNum.objects.filter(**data_dict)
    # print(data_dict)
    
    
    # models.PrettyNum.object.filter(id=12)           #等于12
    # models.PrettyNum.object.filter(id__gt=12)       #大于12
    # models.PrettyNum.object.filter(id__gte=12)      #大于等于12
    # models.PrettyNum.object.filter(id__lte=12)      #小于等于12
    
        
    data_dict = {}
    search_data = request.GET.get("q","")  # ""为默认值,若搜索为空则把空值返还给前端，然后搜索框里就啥都不显示
    if search_data:
        data_dict["mobile__contains"] = search_data
    res = models.PrettyNum.objects.filter(**data_dict)
    #print(res)
    
    from app01.utils.pagination import Pagination
    # page = int(request.GET.get('page',1))
    # page_size = 10
    # start = (page-1)*page_size
    # end = page*page_size
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by("-level")
    page_object = Pagination(request,queryset,page_size=20)
    
    page_queryset = page_object.page_queryset
    page_string = page_object.html()
    
    context = {
        "queryset":page_queryset, 
        "search_data":search_data, #分完页的数据
        "page_string":page_string   #页码
        }
    
    return render(request, "mobile_list.html", context)

class prettyModelForm(BootStrapModelForm):
    #验证：方式1（字段+正则）
    # mobile = forms.CharField(
    #     label = "手机号",
    #     validators=[RegexValidator(r'^1[3-9]9\d{9}$','手机号格式错误')],
    # )
    
    class Meta:
        model = models.PrettyNum
        fields = ["mobile","price","level","status"]
        #fields = "__all__"
        
            
    # 验证：方式2(钩子方法)
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        if len(txt_mobile) != 11:
            raise ValidationError("格式错误")
        
        return txt_mobile
      
def mobile_add(request):
    if request.method == "GET":
        form = prettyModelForm()
        return render(request, "pretty_add.html",{"form":form})
    
    form = prettyModelForm(data=request.POST)
    if form.is_valid():
       
        print(form.cleaned_data)
        #如果数据合法 保存到数据库
        form.save()
        return redirect("/mobile/list/")
    else:
        #校验失败：
        return render(request, "pretty_add.html", {"form":form})

class prettyModelFormEdit(forms.ModelForm):
    #mobile = forms.CharField(disabled=True,label="手机号")
    class Meta:
        model = models.PrettyNum
        fields = ["mobile","price","level","status"]
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
        #循环找到所有插件。添加class=form-control
        for name, field in self.fields.items():
            field.widget.attrs = {"class":"form-control","placeholder":field.label}
            
    # 验证：方式2(钩子方法)
    def clean_mobile(self):
        txt_mobile = self.cleaned_data["mobile"]
        
        #当前编辑的哪一行的id
        #id=self.instance.pk   pk:primary key
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        
        elif len(txt_mobile) != 11:
           raise ValidationError("格式错误")
        
        return txt_mobile
      
def mobile_edit(request, nid):
    '''编辑靓号'''
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == "GET":
        form = prettyModelFormEdit(instance=row_object)
        return render(request, "pretty_edit.html", {"form":form})
    
    form = prettyModelFormEdit(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect("/mobile/list/")

    return render(request,"pretty_edit.html", {"form":form})

def mobile_delete(request, nid):
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect("/mobile/list/") 


def admin_list(request):
    
    # 检查用户是否已经登录，已登录，继续向下走。未登录，跳转回登陆界面。
    # 用户发来请求，获取cookie随机字符串，拿着随机字符串看看session中有没有。
    # request.session["info"]
    info = request.session.get("info")
    if not info:  #若没登陆
        return redirect("/login/" )
    
    data_dict = {}
    search_data = request.GET.get('q',"")
    if search_data:
        data_dict["username__contains"] = search_data
        
    queryset = models.Admin.objects.filter(**data_dict)
    page_object = Pagination(request,queryset)
    context = {
        'queryset':page_object.page_queryset,
        "page_string":page_object.html(),
        "search_data":search_data
        }
    return render(request, 'admin_list.html',context)

class AdminModelForm(BootStrapModelForm):
    
    confirm_password = forms.CharField(
        label="确认密码",
        widget = forms.PasswordInput
        )
    
    class Meta:
        model = models.Admin
        fields = ["username","password","confirm_password"]
        widgets = {
            "password":forms.PasswordInput(render_value=True) #render_value=True:如果密码输入不一致，会在输入框中保留原输入的密码
            }
    
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)  #md5 import from utils.encrypt.py,一个用于加密的函数
        #basically就是要先把输入的密码加密，再存入到数据库
    
    #钩子函数，用于确认密码
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password")) #这里同样需要比较confirm_pwd的加密版，不然永远和pwd不一致
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm   #这里要return confirm, which is 用户输入的密码，因为这样会将return的值保存到数据库
        
class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        fields = ['username']

class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget = forms.PasswordInput
        )
    class Meta:
        model = models.Admin
        fields = ["password","confirm_password"]
        widgets = {
            "password":forms.PasswordInput(render_value=True)      #render_value=True:如果密码输入不一致，会在输入框中保留原输入的密码
            }
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        md5_pwd = md5(pwd)
        #md5 import from utils.encrypt.py,一个用于加密的函数
        #basically就是要先把输入的密码加密，再存入到数据库
        
        #新功能：去数据库校验当前密码和新输入的密码是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk,password = md5_pwd).exists()
        if exists:
            raise ValidationError("不能与以前的密码相同")
        return md5_pwd 

    #钩子函数，用于确认密码
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get("password")
        confirm = md5(self.cleaned_data.get("confirm_password")) #这里同样需要比较confirm_pwd的加密版，不然永远和pwd不一致
        if confirm != pwd:
            raise ValidationError("密码不一致")
        return confirm   #这里要return confirm, which is 用户输入的密码，因为这样会将return的值保存到数据库


def admin_add(request):
    '''添加管理员'''
    title = "新建管理员"
    if request.method == "GET":
        form = AdminModelForm()
        return render(request,"change.html", {"title":title,"form":form})
    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    
    return render(request, 'change.html', {"title":title,"form":form})

def admin_edit(request, nid):
    '''编辑管理员'''
    title = "编辑管理员"
    #对象/None
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        #进入错误界面
        #return render(request, "error.html",{"msg":"数据不存在"})
        return redirect('/admin/list/')
    if request.method == "GET":
        form = AdminEditModelForm(instance=row_object)
        return render(request, 'change.html', {"form":form,"title":title})
    
    form = AdminEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    
    return render(request, 'change.html', {"form":form,"title":title})

def admin_delete(request, nid):
    '''管理员删除'''
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')

def admin_reset(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        #进入错误界面
        #return render(request, "error.html",{"msg":"数据不存在"})
        return redirect('/admin/list/')
    title = "重置密码 - {}".format(row_object.username)
    
    if request.method == "GET":   
        form = AdminResetModelForm()
        return render(request, 'change.html', {"form":form,"title":title})
    
    form = AdminResetModelForm(data=request.POST, instance = row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {"form":form,"title":title})
