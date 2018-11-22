from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.views import View
from app.forms import *
import random
import json
import hashlib
import app.zhenzismsclient as smsclient
from django.db.models import Q


def index(request):
    types = Type.objects.all()
    type_id = request.GET.get("type_id", None)
    search = request.GET.get("search", None)
    hot_news = Content.objects.all().order_by("-clicked")[:10]
    if type_id:
        type_id = int(type_id)
        content_list_all = Content.objects.filter(type_id=type_id)
    elif search:
        content_list_all = Content.objects.filter(title__regex="\w*%s\w*" % search)
    else:
        content_list_all = Content.objects.all()
    return render(request, 'index.html', locals())


class Login(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")
        else:
            return render(request, "login.html",{"error": "用户名或密码有误！"})

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class Signup(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            pwd = make_password(request.POST.get("password"))
            UserInfo.objects.create(
                password=pwd,
                username=request.POST.get("username"),
                email=request.POST.get("email"),
                mobile=request.POST.get("mobile"),
                gender=request.POST.get("gender")
            )
            return redirect("/login")
        else:
            return render(request, "signup.html", {"form": form})

class SetUserView(View):
    def get(self, request, user_id):
        user = UserInfo.objects.get(id=user_id)
        return render(request, "setuser.html", locals())

    def post(self, request, user_id):
        user = UserInfo.objects.get(id=user_id)
        form = UserInfoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save(commit=True)
            return redirect("/")
        return render(request, "setuser.html", locals())

@login_required(login_url="/login")
def password_reset(request, user_id):
    if request.method == "GET":
        return render(request, "password_reset.html", locals())
    elif request.method == "POST":
        form = PasswordForm(request.POST)
        if form.is_valid():
            pwd1 = request.POST.get("password")
            pwd2 = request.POST.get("re_password")
            if pwd1 == pwd2:
                user = UserInfo.objects.get(id=user_id)
                user.password = make_password(pwd1)
                user.save()
                return redirect("/login")
    return render(request, "password_reset.html", locals())

def send_dx(mobile):
    yzm = "".join([str(random.randint(0, 9)) for i in range(4)])
    api_url = "http://sms_developer.zhenzikj.com"
    app_id = 100097
    app_secret = "NTI3ZjUyN2EtYjc2Yi00N2FiLTgwYjMtOGQ5MzE2NjJhN2Uz"
    client = smsclient.ZhenziSmsClient(api_url, app_id, app_secret)
    result = client.send(mobile, "您的验证码是%s" % yzm)
    return json.loads(result), yzm

def hash_code(code):
    m = hashlib.md5()
    m.update(code.encode('utf-8'))
    return m.hexdigest()

class ForGetPassword(View):
    def get(self, request):
        form = ForGetPasswordForm()
        return render(request, "forgetpwd.html", locals())

    def post(self, request):
        form = ForGetPasswordForm(request.POST)
        if form.is_valid():
            username = request.POST.get("username")
# 　　通过用户名，邮箱，或手机号来查找用户
            user = UserInfo.objects.get(Q(username=username) | Q(email=username) | Q(mobile=username))
            if user:
                result, yzm = send_dx(user.mobile)  # 找到用户手机号，给用户发送短信
                print(result, yzm)
                if result.get("code") == 0:  # 结果的返回码为0,发送短信成功
                    return redirect('/getyzm/%s/%s' % (user.id, hash_code(yzm)))
        return render(request, "forgetpwd.html", locals())


def getyzm(request, user_id, code):
    if request.method == "GET":
        return render(request, "getyzm.html", locals())

    elif request.method == "POST":
        new_code = request.POST.get("new_code")
        user = UserInfo.objects.get(id=user_id)
        if user and code == hash_code(new_code):
            login(request, user)
            return redirect("/password_reset/%s" % user_id)
        else:
            return render(request, "getyzm.html", locals())

class News(View):
    def get(self, request, content_id):
        types = Type.objects.all()
        contents= Content.objects.get(id=content_id)
        contents.clicked = int(contents.clicked) + 1
        contents.save()
        form = CommentForm()
        comments = Comment.objects.filter(news_id=contents, restore=None)
        hot_news = Content.objects.all().order_by("-clicked")[:10]
        return render(request, "news.html", locals())

    def post(self, request, content_id):
        form = CommentForm(request.POST)
        ip = request.META['REMOTE_ADDR']
        if form.is_valid():
            if request.user.id:
                restore = request.POST.get("restore", None)
                if restore:
                    Comment.objects.create(
                        user_id=request.user,
                        news_id=Content.objects.get(id=content_id),
                        content=request.POST.get("content"),
                        restore=Comment.objects.get(id=request.POST.get("restore")),
                        restore_user=UserInfo.objects.get(id=request.POST.get("restore_user")),
                        ip=ip,
                    )
                else:
                    Comment.objects.create(
                        user_id=request.user,
                        news_id=Content.objects.get(id=content_id),
                        content=request.POST.get("content"),
                        ip=ip,
                    )
            else:
                return HttpResponse("登陆后才能评论！")
        return redirect("/news/%s" % content_id)

