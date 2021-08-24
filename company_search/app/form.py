from django import forms


# 继承forms.Form
class LoginForm(forms.Form):
    # 如果为空则报错
    username = forms.CharField(label="用户账号：", min_length=3, required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}))
    pwd = forms.CharField(label="用户密码：", min_length=3, required=True,
                          widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
