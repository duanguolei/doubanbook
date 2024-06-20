"""
code speace
@Time    : 2024/4/10 13:51
@Author  : 泪懿:dgl
@File    : base.py
"""
import os.path

from django.shortcuts import render
from book.uitls import utils,encrypt
def index(request):

    return render(request,'index.html')


import uuid

from book.forms.base import RegisterModelFrom,LoginModelForm
from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse,HttpResponse
from django.conf import settings
from book import models
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q
from book.uitls.captacher import get_img_code
import datetime
def register(request):

    if request.method=='GET':
        form =RegisterModelFrom(request)

        return render(request,'register.html',{"form":form})

    else:
        form = RegisterModelFrom(request,request.POST)
        if form.is_valid():
            form.save()

            return JsonResponse(
                {'status':True,'data':'/',
                 }
            )
        else:
            return JsonResponse(
                {'status':False,'error':form.errors}
            )





def login(request):
    if request.method=='GET':

        form=LoginModelForm(request)
        return  render(request,'login.html',{'form':form})
    else:
        form=LoginModelForm(request,data=request.POST)
        if form.is_valid():
            mobile_phone=form.cleaned_data['mobile_phone']
            password=form.cleaned_data['password']

            user_Obj=models.Userinfo.objects.filter(Q(email=mobile_phone)|Q(mobile_phone=mobile_phone)|Q(username=mobile_phone)).filter(password=password).first()
            if user_Obj:
                request.session['user_id']=user_Obj.id
                request.session.set_expiry(60*60*24*7)
                return JsonResponse(
                {'status': True, 'data': "/"}
            )
            else:
                form.add_error('username', '用户名或密码错误')
                return JsonResponse({"status": False, 'error': form.errors})

        return JsonResponse({"status": False, 'error': form.errors})

def captch(request):
    """
    生成图片验证码
    :param request:
    :return:
    """
    code,img=get_img_code()
    request.session['captch_code']=code
    request.session.set_expiry(60)

    from io import BytesIO
    stram=BytesIO()
    img.save(stram,'png')

    return HttpResponse(
        stram.getvalue()
    )

def logout(request):
    if request.manage.level:
        request.session.flush()
        request.manage=None
        return redirect('book:manage_login')
    else:
        request.manage = None
        request.session.flush()
        return redirect('book:login')

@csrf_exempt
def persion(request):
    if request.method=='GET':
        return render(request,'persion.html')
    else:
        email=request.POST.get('email')
        name=request.POST.get('name')
        user=request.manage.user
        if user:
            if email:
                if user.email==email:
                    return JsonResponse({'status': False, 'error': '邮箱没有改动'})

                if models.Userinfo.objects.filter(email=email,).exists():
                    return JsonResponse({'status':False,'error':'邮箱已存在'})

            if name:
                user.username=name
            user.save()
            return JsonResponse({'status':True})

        return JsonResponse({'status':False})

@csrf_exempt
def upload(request):

    if request.method=='POST':
        type=request.POST.get('type')
        user=request.manage.user
        if type=='useravator':
            foloder = 'avatars'
            imge = request.FILES.get('image')
            if not imge:
                return JsonResponse({'status': False})

            name = imge.name.rsplit('.')[-1]
            name = encrypt.uid(name) + '.jpg'

            utils.save_image(byte_data=imge.read(), filename=name, folder=foloder)
            user.avator = os.path.join(foloder, name)
            user.save()
        if type=='bookavator':
            if request.manage.level:
                foloder = 'bookimage'
                book_id=request.POST.get('bookid')


                imge = request.FILES.get('image')
                if not imge:
                    return JsonResponse({'status': False})


                name = imge.name.rsplit('.')[-1]
                name = encrypt.uid(name) + '.jpg'

                utils.save_image(byte_data=imge.read(), filename=name, folder=foloder)

                book=models.BookInfo.objects.filter(id=book_id).first()

                if book:
                    book.booklogo= os.path.join(foloder, name)
                    book.save()
                else:

                    return JsonResponse({'status': False})
        if type=='avator':
            if request.manage.level:
                foloder = 'avatars'
                id=request.POST.get('userid')
                imge = request.FILES.get('image')
                if not imge:
                    return JsonResponse({'status': False})

                name = imge.name.rsplit('.')[-1]
                name = encrypt.uid(name) + '.jpg'
                user=models.Userinfo.objects.filter(id=id).first()
                utils.save_image(byte_data=imge.read(), filename=name, folder=foloder)
                user.avator = os.path.join(foloder, name)
                user.save()

        return JsonResponse({'status': True})

