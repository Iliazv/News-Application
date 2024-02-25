import json
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_GET, require_POST
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status
from django.shortcuts import render
from django.core import paginator
from django.core.paginator import Paginator

from .models import New
from .serializers import NewSerializer

TAG_CHOICES = (
        ('политика', 'Политика'),
        ('наука', 'Наука'),
        ('спорт', 'Спорт'),
        ('экономика', 'Экономика'),
        ('религия', 'Религия'),
        ('туризм', 'Туризм'),
        ('технологии', 'Технологии'),
        ('россия', 'Россия'),
        ('общество', 'Общество'),
        ('европа', 'Европа'),
)

NEWS_COUNT_PER_PAGE = 3


def new_all(request):
    """Вывод списка всех элементов по 3 штуки с помощью пагинации"""
    tags = TAG_CHOICES
    all_news = New.objects.all()
    paginator = Paginator(all_news, per_page=NEWS_COUNT_PER_PAGE)
    page_num = int(request.GET.get("page", 1))
    if page_num > paginator.num_pages:
        raise Http404
    new_list = paginator.page(page_num)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'news/posts-new.html', {'new_list': new_list, 'tags': tags})
    return render(request, 'news/index.html', {'new_list': new_list, 'tags': tags})

def new_find(request, tag):
    """Вывод списка элементов с определенным тегом по 3 штуки с помощью пагинации"""
    tags = TAG_CHOICES
    all_news = New.objects.all()
    lst = []
    for new in all_news:
        tag_list = [tag.tag for tag in new.tags.all()]
        if tag in tag_list:
            lst.append(new)

    paginator = Paginator(lst, per_page=NEWS_COUNT_PER_PAGE)
    page_num = int(request.GET.get("page", 1))
    if page_num > paginator.num_pages:
        raise Http404
    new_list = paginator.page(page_num)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'news/posts-new.html', {'new_list': new_list, 'tags': tags, 'tag': tag})
    return render(request, 'news/filtered.html', {'new_list': new_list, 'tags': tags, 'tag': tag})

def new_page(request, pk):
    """Открываем выбранную страницу и записываем просмотр (если он еще не был засчитан)"""
    new_item = New.objects.get(pk=pk)
    total_likes = new_item.total_likes
    total_dislikes = new_item.total_dislikes
    try:
        request.session[f'new is {new_item}']
    except:
        request.session[f'new is {new_item}'] = 'new viewed'
        new_item.view_count += 1
        new_item.save()
    context = {'new_item': new_item, 'total_likes': total_likes, 'total_dislikes': total_dislikes}
    return render(request, 'news/new_page.html', context)

def statistic_page(request):
    """Открываем страницу со статистикой по просмотрам"""
    new_list = New.objects.all()
    context = {'new_list': new_list}
    return render(request, 'news/statistic_page.html', context)

def submit_like(request):
    """Представление вызываемое из Ajax запроса для добавления лайка пользователем"""
    data = {}
    user = request.user
    pk = request.POST.get('primary_key')
    new = get_object_or_404(New, pk=pk)
    if new.dislike_count.filter(id=user.id).exists():
        new.dislike_count.remove(request.user)
        new.like_count.add(request.user)
    else:
        new.like_count.add(request.user)

    data['likes'] = new.like_count.count()
    data['dislikes'] = new.dislike_count.count()
    return JsonResponse(data)

def submit_dislike(request):
    """Представление вызываемое из Ajax запроса для добавления дизлайка пользователем"""
    data = {}
    user = request.user
    pk = request.POST.get('primary_key')
    new = get_object_or_404(New, pk=pk)
    if new.like_count.filter(id=user.id).exists():
        new.like_count.remove(request.user)
        new.dislike_count.add(request.user)
    else:
        new.dislike_count.add(request.user)

    data['likes'] = new.like_count.count()
    data['dislikes'] = new.dislike_count.count()
    return JsonResponse(data)

class GetNewAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            new = New.objects.get(pk=pk)
            serializer = NewSerializer(new)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)

get_new = GetNewAPI.as_view()

class CreateNewAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = NewSerializer
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
create_new = CreateNewAPI.as_view()

class DeleteNewAPI(APIView):
    permission_classes = (AllowAny,)
    serializer_class = NewSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            new = New.objects.filter(pk=pk)
            new.delete()
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
delete_new = DeleteNewAPI.as_view()