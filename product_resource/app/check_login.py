from django.shortcuts import render, redirect


def check_login(func):  # 自定义登录验证装饰器
    def warpper(request, *args, **kwargs):
        is_login = request.session.get('is_login', False)
        if is_login:
            res = func(request, *args, **kwargs)
            return res
        else:
            return redirect("login.html")

    return warpper
