from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from AppLibrary import models
from AppLibrary.My_form import Register as reg_form
from AppLibrary.My_form import AddBook as addbook_form
from AppLibrary.My_form import AddPub as addpub_form
from AppLibrary.My_form import AddAuth
from AppLibrary.My_Paginator import Paginator


# Create your views here.


def add_data(request):
    """
    初始化增加数据使用, 放开相应注释
    按顺序增加数据
    1. 新社出版社app_publish
    2. 作者详情app_authordetail
    3. 作者app_author
    4. 书app_book
    :param request:
    :return:
    """
    # 书app_book
    # models.Book.objects.create(title="独孤九剑", price=180, publish_id=1, pub_date="2019-1-12")
    # models.Book.objects.create(title="华山剑法", price=100, publish_id=1, pub_date="2018-10-2")
    # models.Book.objects.create(title="挤奶龙爪手", price=200, publish_id=1, pub_date="2019-2-22")
    # models.Book.objects.create(title="冲灵剑法", price=150, publish_id=2, pub_date="2019-3-6")
    # models.Book.objects.create(title="吸星大法", price=190, publish_id=2, pub_date="2019-2-6")
    # models.Book.objects.create(title="葵花宝典", price=280, publish_id=2, pub_date="2018-1-17")
    # models.Book.objects.create(title="乾坤大挪移", price=260, publish_id=3, pub_date="2019-1-6")
    # models.Book.objects.create(title="九阴真经", price=220, publish_id=3, pub_date="2019-3-6")
    # models.Book.objects.create(title="九阳神功", price=230, publish_id=3, pub_date="2019-3-11")
    # models.Book.objects.create(title="九阴白骨爪", price=50, publish_id=3, pub_date="2019-2-7")

    # 出版社app_publish
    # models.Publish.objects.create(name="华山出版社", city="华山", email="hs_111@163.com")
    # models.Publish.objects.create(name="明教出版社", city="泰山", email="ts_222@163.com")
    # models.Publish.objects.create(name="少林出版社", city="嵩山", email="ss_333@163.com")

    # 作者app_author
    # models.Author.objects.create(name='令狐冲', age=25, au_detail_id=1)
    # models.Author.objects.create(name='任我行', age=28, au_detail_id=2)
    # models.Author.objects.create(name='任盈盈', age=35, au_detail_id=3)

    # 作者详情app_authordetail
    # models.AuthorDetail.objects.create(gender=1, tel=13432335433, addr="华山", birthday="1994-5-23")
    # models.AuthorDetail.objects.create(gender=1, tel=13943454554, addr="黑木崖", birthday="1961-8-13")
    # models.AuthorDetail.objects.create(gender=0, tel=13878934322, addr="少林寺", birthday="1996-5-20")

    # book = models.Book.objects.filter(title="九阴白骨爪").first()
    # ling = models.Author.objects.filter(name='令狐冲').first()
    # ren = models.Author.objects.filter(name='任我行').first()
    # ying = models.Author.objects.filter(name='任盈盈').first()
    # book.authors.add(ren.pk, ling.pk)
    # book.authors.clear()
    # book.authors.add(ren.pk)
    return HttpResponse('新增成功！')


# 图书主页
@login_required(login_url='/login/')
def index_book(request):
    books_list = models.Book.objects.all()
    authors = models.Author.objects.all()
    publishs = models.Publish.objects.all()
    current_page = request.GET.get("page", default="1")
    paginator = Paginator(request, current_page, books_list.count(), 10, 11)
    books_list = books_list[paginator.start: paginator.end]
    return render(request, 'index_book.html', {'books_list': books_list,
                                               'authors': authors,
                                               'publishs': publishs,
                                               'paginator': paginator,
                                               'current_page': current_page,
                                               })


# 新增书籍
class AddBook(View):
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        obj = super().dispatch(request, *args, **kwargs)
        return obj

    def get(self, request):
        form = addbook_form()
        authors = models.Author.objects.all()
        publish = models.Publish.objects.all()
        return render(request, 'add_book.html', locals())

    def post(self, request):
        form = addbook_form(request.POST)
        authors = models.Author.objects.all()
        pub = models.Publish.objects.all()

        au_list = request.POST.getlist('author')
        publish = request.POST.get('publish')

        if form.is_valid():
            data = form.cleaned_data
            book_obj = models.Book.objects.create(title=data['title'], price=data['price'], publish_id=publish,
                                                  pub_date=data['pub_date'])
            book_obj.authors.add(*au_list)
            return redirect('/index_book/')
        else:
            return render(request, 'add_book.html', {"form": form, 'authors': authors, 'publish': pub})


# 编辑书籍
class EditBook(View):
    edit_pk = 0

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        obj = super().dispatch(request, *args, **kwargs)
        return obj

    def get(self, request):
        global edit_pk
        edit_pk = request.GET.get('edit_pk')
        page = request.GET.get('page', "1")
        book_obj = models.Book.objects.filter(pk=edit_pk).first()
        authors = models.Author.objects.all()
        publish = models.Publish.objects.all()
        return render(request, 'edit_book.html', locals())

    def post(self, request):
        page = request.GET.get('page')
        title = request.POST.get('edit_title')
        price = request.POST.get('edit_price')
        au_list = request.POST.getlist('edit_author')
        publish = request.POST.get('edit_pub')
        pub_date = request.POST.get('edit_pub_date')
        try:
            book_obj = models.Book.objects.filter(pk=edit_pk)
            book_obj.update(title=title, price=price, publish_id=publish, pub_date=pub_date)
            book_obj.first().authors.set(au_list)
        except Exception as e:
            print(str(e))
            return redirect('/edit_book/')
        return redirect('/index_book/?page=' + page)


# 删除书籍
@login_required(login_url='/login/')  # auth自带的装饰器，只有登录状态才可以操作
def del_book(request):
    ret = {'status': 1, 'msg': None}
    pk = request.POST.get('books_pk')
    try:
        models.Book.objects.filter(pk=pk).delete()
    except Exception as e:
        ret['status'] = 0
        ret['msg'] = str(e) + '操作失败！'
    return JsonResponse(ret)


# 作者主页
@login_required(login_url='/login/')
def index_author(request):
    author_obj = models.Author.objects.all()
    current_page = request.GET.get("page", default="1")
    paginator = Paginator(request, current_page, author_obj.count(), 10, 11)
    auth_list = author_obj[paginator.start: paginator.end]
    return render(request, 'index_author.html', {'author_obj': author_obj,
                                                 'current_page': current_page,
                                                 'paginator': paginator,
                                                 'publish_list': auth_list})


# 新增作者 和 作者详情
class AddAuthor(View):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        obj = super().dispatch(request, *args, **kwargs)
        return obj

    def get(self, request):
        form = AddAuth()
        return render(request, 'add_author.html', {'form': form})

    def post(self, request):
        form = AddAuth(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print(data)
            try:
                au_obj = models.AuthorDetail.objects.create(gender=data['gender'], tel=data['tel'], addr=data['addr'],
                                                            birthday=data['birthday'])
                models.Author.objects.create(name=data['name'], age=data['age'], au_detail=au_obj)
                return redirect('/index_author/')
            except Exception as e:
                print(str(e))
        return render(request, 'add_author.html', {'form': form})


# 编辑作者 和 作者详情
class EditAuthor(View):
    edit_pk = 0

    def get(self, request):
        global edit_pk
        edit_pk = request.GET.get('edit_pk')
        au_obj = models.Author.objects.get(pk=edit_pk)
        au_d_obj_pk = models.AuthorDetail.objects.get(pk=au_obj.au_detail_id)

        au_de_obj = models.AuthorDetail.objects.all()
        page = request.GET.get('page')
        return render(request, 'edit_author.html', locals())

    def post(self, request):
        page = request.GET.get('page')
        name = request.POST.get('edit_name')
        age = request.POST.get("edit_age")
        gender = request.POST.get("edit_gender")
        tel = request.POST.get("edit_tel")
        addr = request.POST.get('edit_addr')
        birthday = request.POST.get("edit_bir")
        try:
            models.Author.objects.filter(pk=edit_pk).update(name=name, age=age)
            au_d_id = models.Author.objects.get(pk=edit_pk).au_detail_id
            models.AuthorDetail.objects.filter(pk=au_d_id).update(gender=gender, tel=tel, addr=addr, birthday=birthday)
        except Exception as e:
            print(str(e))
            return redirect('/edit_author/')
        return redirect('/index_author/?page=' + page)


# 删除作者 和 作者详情
@login_required(login_url='/login/')
def del_author(request):
    author_pk = request.POST.get('author_pk')

    ret = {'status': 1, 'msg': None}
    try:
        au_obj = models.Author.objects.filter(pk=author_pk).first()
        au_obj.delete()
        au_det_obj = models.AuthorDetail.objects.filter(pk=au_obj.au_detail_id).first()
        au_det_obj.delete()
    except Exception as e:
        ret['status'] = 0
        ret['msg'] = str(e) + '操作失败！'
    return JsonResponse(ret)


# 出版社主页
@login_required(login_url='/login/')
def index_publish(request):
    publish_obj = models.Publish.objects.all()
    current_page = request.GET.get("page", default="1")
    paginator = Paginator(request, current_page, publish_obj.count(), 10, 11)
    publish_list = publish_obj[paginator.start: paginator.end]
    return render(request, 'index_publish.html', {'publish_obj': publish_obj,
                                                  'current_page': current_page,
                                                  'paginator': paginator,
                                                  'publish_list': publish_list})


# 新增出版社
class AddPub(View):
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        obj = super().dispatch(request, *args, **kwargs)
        return obj

    def get(self, request):
        form = addpub_form()
        return render(request, 'add_publish.html', {'form': form})

    def post(self, request):
        form = addpub_form(request.POST)
        edit_pk = request.POST.get('edit_pk')
        if form.is_valid():
            data = form.cleaned_data
            pub_obj = models.Publish.objects.filter(pk=edit_pk)
            pub_obj.create(**data)
            return redirect('/index_publish/')
        else:
            return render(request, 'add_publish.html', {'form': form})


# 编辑出版社
class EditPub(View):
    edit_pk = 0

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        obj = super().dispatch(request, *args, **kwargs)
        return obj

    def get(self, request):
        global edit_pk
        edit_pk = request.GET.get('edit_pk')
        page = request.GET.get('page', '1')
        pub_obj = models.Publish.objects.get(pk=edit_pk)
        return render(request, 'edit_publish.html', {"pub_obj": pub_obj, "page": page})

    def post(self, request):
        page = request.GET.get('page')
        name = request.POST.get('edit_name')
        city = request.POST.get('edit_city')
        email = request.POST.get("edit_email")
        print(name, city, email)
        try:
            pub_obj = models.Publish.objects.filter(pk=edit_pk)
            pub_obj.update(name=name, city=city, email=email)
        except Exception as e:
            print(str(e))
            return redirect('/edit_publish/')
        return redirect('/index_publish?page=' + page)


# 删除出版社
@login_required(login_url='/login/')
def del_publish(request):
    ret = {'status': 1, 'msg': None}
    pub_pk = request.POST.get('pub_pk')
    try:
        models.Publish.objects.filter(pk=pub_pk).delete()
    except Exception as e:
        ret['status'] = 0
        ret['msg'] = str(e) + '操作失败！'
    return JsonResponse(ret)


# 登录
class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/index_book')
        return render(request, 'login.html')

    def post(self, request):
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        valid_num = request.POST.get('valid_num')
        keep_str = request.session.get('keep_str')

        if keep_str.upper() == valid_num.upper():
            user_obj = authenticate(request, username=user, password=pwd)
            if user_obj is not None:
                auth.login(request, user_obj)
                path = request.GET.get('next') or '/index_book/'
                return redirect(path)
            else:
                return redirect('/login/')
        else:
            return redirect('/login/')


# 注册
class Register(View):
    message = ''

    def get(self, request):
        form = reg_form()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = reg_form(request.POST)
        if form.is_valid():
            data = form.cleaned_data  # 校验成功的值会放在cleaned_data里

            # 写入到数据库
            data.pop('r_password')
            user = User.objects.create_user(**data)
            user.save()
            message = '恭喜您注册成功！即将跳转登录界面...'
            return render(request, 'confirm.html', locals())

        else:
            print(form.errors)
            all_errors = form.errors.get('__all__')
            return render(request, 'register.html', {'form': form, 'all_errors': all_errors})


# 提示页面
def confirm(request):
    return render(request, 'confirm.html')


# 注销
@login_required(login_url='/login/')
def logout(request):
    auth.logout(request)
    return redirect('/login/')


# 验证码那块
def get_random_color():
    """
    获取随机图片颜色
    :return:
    """
    import random
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def valid_img(request):
    # 方式四
    import random
    from io import BytesIO
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (190, 44), get_random_color())  # 新建图片大小为250*40
    draw = ImageDraw.Draw(img)  # 可以在该图片对象上写内容
    font = ImageFont.truetype("statics/font/HYTianYuFengXingTiW-2.ttf", 30)  # 指定字体，需自行下载字体文件

    keep_str = ""
    for i in range(4):  # 获取随机数
        random_num = str(random.randint(0, 9))
        random_low_alpha = chr(random.randint(97, 122))
        random_upper_alpha = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_low_alpha, random_upper_alpha])
        draw.text((18 + i * 35, 0), random_char, get_random_color(), font=font)
        keep_str += random_char

    # 验证码噪点噪线
    width = 250
    height = 40
    for i in range(10):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=get_random_color())

    for i in range(100):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_random_color())

    request.session["keep_str"] = keep_str
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()
    return HttpResponse(data)
