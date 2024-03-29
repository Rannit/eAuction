#coding=utf-8
from django import forms

#定义注册表单模型
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮件')

#定义登录表单模型
class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码  ',widget=forms.PasswordInput())

#报价
class QuotesForm(forms.Form):
	userid = forms.IntegerField(label='用户ID')
	goodid = forms.IntegerField(label='拍卖品ID')
	quote = forms.FloatField(label='报价')
	time = forms.DateTimeField(label='时间')

#定义地址表单模型
class AddressForm(forms.Form):
    address = forms.CharField(label='地址',max_length=100)
    phone = forms.CharField(label='电话',max_length=15)
