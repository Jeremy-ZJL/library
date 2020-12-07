from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Register(forms.Form):
    username = forms.CharField(max_length=32, min_length=3, label="用户名：",
                               error_messages={'min_length': '不符合长度要求3！', "required": '不能为空！'},
                               widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}))

    password = forms.CharField(max_length=32, min_length=6, label="密 码：",
                               widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}),
                               error_messages={'min_length': '不符合长度要求6！', "required": '不能为空！'})

    r_password = forms.CharField(max_length=32, min_length=6, label="确认密码：",
                                 widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}),
                                 error_messages={'min_length': '不符合长度要求6！', "required": '不能为空！'})

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('该用户已存在！')
        return username

    def clean(self):
        password = self.cleaned_data.get('password')
        r_password = self.cleaned_data.get('r_password')

        # print(password, r_password)

        if password != r_password:
            raise ValidationError('两次密码输入不一致，请重新输入！')
        return self.cleaned_data


class AddBook(forms.Form):
    title = forms.CharField(max_length=32, label="书名：", error_messages={"required": '不能为空！'},
                            widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}))

    price = forms.DecimalField(max_digits=5, decimal_places=2, label='价格：', error_messages={"required": '不能为空！'},
                               widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}))
    pub_date = forms.DateField(label="出版时间：", error_messages={"required": '不能为空！'},
                               widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}))


class AddPub(forms.Form):
    name = forms.CharField(max_length=32, label="出版社：", error_messages={"required": '不能为空！'},
                           widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}))

    city = forms.CharField(max_length=32, label="所在城市：", error_messages={"required": '不能为空！'},
                           widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}))

    email = forms.EmailField(label="Email：", error_messages={"required": '不能为空！'},
                             widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}))


class AddAuth(forms.Form):
    name = forms.CharField(max_length=32, label="姓名：", error_messages={"required": '不能为空！'},
                           widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}))

    age = forms.IntegerField(max_value=100, label='年龄',
                             error_messages={"required": '该字段不能为空', "max_value": '最大不能超过100!', 'invalid': '请填写数字！'},
                             widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}))

    gender = forms.ChoiceField(choices=((0, "女"), (1, "男"), (2, "保密"),), initial=1, label='性别',
                               error_messages={"required": '该字段不能为空'},
                               widget=forms.widgets.Select(attrs={'class': 'form-control', 'autocomplete': "off"}))

    tel = forms.CharField(max_length=32, label="电话：", error_messages={"required": '不能为空！'},
                          widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}))

    addr = forms.CharField(max_length=32, label="住址：", error_messages={"required": '不能为空！'},
                           widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'autocomplete': "off"}))

    birthday = forms.DateField(label='出生日期', error_messages={"required": '不能为空！', "invalid": "请填写正确日期！"},
                               widget=forms.widgets.DateInput(attrs={'class': 'form-control', 'autocomplete': "off"}),
                               input_formats=['%Y-%m-%d'])



