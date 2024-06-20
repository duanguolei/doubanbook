"""
code speace
@Time    : 2024/4/13 11:13
@Author  : 泪懿:dgl
@File    : manager.py
"""

from book.forms.manager import UserLoginModelForm,BookModelForm,UserModelForm
from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse
from book import models
from book.models import User
from django.db.models import Count, Case, When, IntegerField,CharField
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.views.decorators.csrf import csrf_exempt
from book.uitls import utils
import string
import random

def manage_login(request):
    if request.method=='GET':
        if request.manage.level:
            return redirect(reverse('book:manage_login'))
        else:
            form=UserLoginModelForm(request)
            return render(request,'manage/manage_login.html',{"form":form})
    else:
        form = UserLoginModelForm(request,request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            user_Obj = User.objects.filter(username=username).first()
            if user_Obj:
                request.session['user_id'] = user_Obj.id
                request.session['level']=1
                request.session.set_expiry(60 * 60 * 24 * 7)

                return JsonResponse(
                    {'status': True, 'data': "/manage"}
                )
            else:
                form.add_error('username', '用户名或密码错误')
                return JsonResponse({"status": False, 'error': form.errors})

        return JsonResponse({"status": False, 'error': form.errors})

@csrf_exempt
def manage(request):
    if not request.manage.level:

        return redirect(reverse('book:manage_login'))


    if request.method=='GET':


        user_count=models.Userinfo.objects.count()
        book_count=models.BookInfo.objects.count()
        return render(request, 'manage/manage.html',
                  {
                      'user_count':user_count,
                      'book_count':book_count
                  })

    else:
        #柱状图类别数量
        top_tagnames = models.BookInfo.objects.values('tagname').annotate(count=Count('tagname')).order_by('-count')[:10]
        categories=[]
        tag_data=[
            {'name':'类别数量',
             'data':[]
             }
        ]
        for item in top_tagnames:
            categories.append(item['tagname'])
            tag_data[0]['data'].append(item['count'])


        #评分占比饼状图
        rating_distribution = models.BookInfo.objects.annotate(
            rating_range=Case(
                When(rating__gte=0, rating__lt=6, then=1),
                When(rating__gte=6, rating__lt=7, then=2),
                When(rating__gte=7, rating__lt=8, then=3),
                When(rating__gte=8, rating__lt=9, then=4),
                When(rating__gte=9, rating__lt=10, then=5),

                output_field=IntegerField()
            )
        ).values('rating_range').annotate(count=Count('id'))

        filtered_pie_datas=[]

        vating_dict={
            1:"0-6",
            2:"6-7",
            3:'7-8',
            4:'8-9',
            5:'9-10'
        }

        # 打印不同范围内的图书分布占比
        for distribution in rating_distribution:
            range_name = distribution['rating_range']
            if range_name:

                d={
                    'name':vating_dict[range_name],
                    'y':distribution['count']
                }
                filtered_pie_datas.append(d)


        #环形图数据处理,中外书籍

        bookvalues=models.BookInfo.objects.all()
        chinese_count=0
        foreigner_count=0
        for item in bookvalues:
            chinese_falge=True
            #通过isbn 判断 中国区号是7 就是978 7
            ISBN=item.isbn
            if ISBN:
                if not str(ISBN).startswith('9787'):
                    chinese_falge=False

            if chinese_falge:
                chinese_count+=1
            else:
                foreigner_count+=1

        print('中国书籍',chinese_count,foreigner_count)

        autor_data=[
            [
                '中国书籍',chinese_count
            ],
            [
                '外国书籍',foreigner_count
            ]
        ]
        #热度横向柱状图

        top_book=bookvalues.annotate(count=Count('doubanreview')).order_by('-count')[:20]
        top_book_name=[

        ]
        top_book_value=[]
        for book in top_book:
            top_book_name.append(book.name)
            top_book_value.append(book.count)

        hote_data={'name':top_book_name,
            'data':top_book_value

                   }

        #词云图
        min_count=5000
        word_data=[]
        review_word_dict=utils.get_review_word_dict()

        for key,value in review_word_dict.items():
            value=int(value)
            if value>min_count:
                if key not in string.punctuation and len(key)>1 and not str(key).isdigit():
                    random_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
                    word_data.append({
                        'name': key,
                        'value': value,
                        'label': {
                            'color': random_color
                        }
                    })


        return JsonResponse({'status':True,
                             'pie_data':filtered_pie_datas,
                             'categories':categories,
                             'tag_data':tag_data,
                             'hote_data':hote_data,
                             'autor_data':autor_data,
                             "word_data":word_data
                             })

def manage_book(request):
    if not request.manage.level:
        return redirect(reverse('book:manage_login'))
    if request.method=='GET':

        form=BookModelForm()
        return render(request,'manage/manage_book.html',{'form':form})
    else:
        form = BookModelForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"status": True})
        else:
            return JsonResponse({"status": False, 'error': form.errors})

def manage_user(request):
    if not request.manage.level:
        return redirect(reverse('book:manage_login'))
    return render(request,'manage/manage_user.html')


def book_data(request):
    # print(request.manage.level)
    if not request.manage.level:
        return redirect(reverse('book:manage_login'))
    if request.manage.level:
        now_page=request.GET.get('page',0)

        book_data = models.BookInfo.objects.all().annotate(review_count=Count("doubanreview")).order_by('-id').values()
        per_page_num=20

        paginator = Paginator(book_data, per_page_num)

        try:
            contacts = paginator.page(now_page)
        except PageNotAnInteger:
            # 如果用户请求的页码号不是整数，显示第一页
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果用户请求的页码号超过了最大页码号，显示最后一页
            contacts = paginator.page(paginator.num_pages)

        return JsonResponse({'data':list(contacts),'total':len(book_data)})
    return JsonResponse({'data':[]})


def deel_book(request):
    if not request.manage.level:
        return redirect(reverse('book:manage_login'))
    if request.method=='GET':
        if request.manage.level:
            id=request.GET.get('id')
            type=request.GET.get('type')
            if type=='delete':
                book=models.BookInfo.objects.filter(id=id).first()
                book.delete()
                return JsonResponse({"status":True})
            if type=='update':
                request.session['bookid']=id
                title=request.GET.get('title')
                request.session['title']=title
                request.session['bookid']=id
                request.session.set_expiry(60*60)
                return JsonResponse({"status": True})

        else:
            return JsonResponse({'status':False})
    else:
        if request.manage.level:
            type=request.POST.get('type')
            if type=='update':
                id = request.session.get('bookid')
                book = models.BookInfo.objects.filter(id=id).first()

                form=BookModelForm(request.POST,instance=book)
                if form.is_valid():
                    form.save()
                    return JsonResponse({'status': True})
                else:
                    return JsonResponse({'status': False})

        else:
            return JsonResponse({'status': False})


def update_form(request):
    if not request.manage.level:
        return redirect(reverse('book:manage_login'))
    title=request.session.get('title')
    if title=='图书信息更改':
        id = request.session.get('bookid')
        book=models.BookInfo.objects.filter(id=id).first()

        form=BookModelForm(instance=book)
        return render(request,'manage/manage_update.html',{"form":form,'title':title})

    if title=='用户信息更改':
        id = request.session.get('user_update_id')
        user = models.Userinfo.objects.filter(id=id).first()
        form = UserModelForm(instance=user)
        return render(request, 'manage/manage_update.html', {"form": form, 'title': title})

def user_data(request):
    if request.manage.level:
        user_datas=models.Userinfo.objects.all().values().order_by('-id')
        return JsonResponse({'status':True,'data':list(user_datas)})
    else:
        return JsonResponse({"data":[]})

def deel_user(request):
    if request.method=='GET':
        if request.manage.level:
            id = request.GET.get('id')
            type=request.GET.get('type')
            if type=='delete':

                book=models.Userinfo.objects.filter(id=id).first()
                book.delete()
                return JsonResponse({"status":True})
            if type=='update':

                title=request.GET.get('title')
                request.session['title']=title
                request.session['user_update_id']=id
                request.session.set_expiry(60*60)
                return JsonResponse({"status": True})

        else:
            return JsonResponse({'status':False})
    else:
        if request.manage.level:
            type=request.POST.get('type')

            if type=='update':

                id = request.session.get('user_update_id')
                user = models.Userinfo.objects.filter(id=id).first()
                form=UserModelForm(data=request.POST,instance=user)
                if form.is_valid():

                    form.save()

                    return JsonResponse({'status': False})
                else:
                    return JsonResponse({'status': False,'error':form.errors})

        else:
            return JsonResponse({'status': False})