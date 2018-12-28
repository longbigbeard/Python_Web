from django.shortcuts import render
from django.http import HttpResponse , JsonResponse, StreamingHttpResponse
from django.http.request import QueryDict
from django.views.decorators.http import require_http_methods
from django.template import loader
from django.views.generic import View, TemplateView, ListView
from .models import Article
import json, csv

from django.core.paginator import Page, Paginator




def index(request):
    result = request.GET.get('username', default="qqqwwww")
    print(result)
    return HttpResponse("success")


# @require_http_methods(['GET', 'POST'])
# def add_article(request):
#     if request.method == 'GET':
#         return render(request, 'add_article.html')
#     else:
#         title = request.POST.get('title')
#         content = request.POST.get('content')
#         tags = request.POST.getlist('tags')
#         print(title)
#         print(content)
#         print(tags)
#         return HttpResponse('success')


def index1(request):
    response = HttpResponse("<h1>hello world! 大师傅士大夫士大夫</h1>", content_type='text/plain;charset=utf-8')
    response['X-Token'] = "hellos"
    response.status_code = 400
    response.write("abc")
    return response


def Json_response(request):
    # person = {
    #     'name': "明",
    #     'age': 18,
    #     'height': 190
    # }
    # # person_str = json.dumps(person)
    # # response = HttpResponse(person_str, content_type='application/json')
    # # return HttpResponse(response)
    # response = JsonResponse(person)
    # return response

    person = [
        {
            'name': "明",
            'age': 18,
            'height': 190
        },
        {
            'name': "明",
            'age': 18,
            'height': 190
        }
    ]
    response = JsonResponse(person, safe=False)
    return response


def index2(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment;filename='abc.csv"
    writer = csv.writer(response)
    writer.writerow(['username', 'age'])
    writer.writerow(['hello ', 'age', 10])

    return response


def template_csv(request):
    context = {
        'rows': [
            ['hello', 12],
            ['world', 23],
        ]
    }
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment;filename='abc.csv"
    template = loader.get_template('templaye.txt')
    csv_template = template.render(context)
    response.content = csv_template
    return response


def large_csv(request):
    response = StreamingHttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment;filename='large_abc.csv'"
    rows = ("Row {}, {}\n".format(row, row) for row in range(0, 100000))
    response.streaming_content = rows
    return response


class BookListView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('success')


class AddBookView(View):
    def get(self, request, *args, **kwargs):
        return  render(request, 'add_article.html')

    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        content = request.POST.get("content")
        args = request.POST.getlist("tags")
        print(title,content,args)
        return HttpResponse("success")
    def http_method_not_allowed(self, request, *args, **kwargs):
        return HttpResponse("你请求的方法不存在！")



class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        content = {
            'phone': "111111"
        }
        return content


def add_article(request):
    articles = []
    for x in range(0, 102):
        article = Article(title='标题：%s' % x, content='内容：%s' % x)
        articles.append(article)
    # article = Article(title='标题：', content='内容：')
    # article.save()
    # articles.append(article)
    # print(article)
    # print(articles)
    Article.objects.bulk_create(articles)
    return HttpResponse("插入成功")



class ArticleListView(ListView):
    model = Article
    template_name = 'article_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    ordering = 'create_time'

    def get_context_data(self,  **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        print("*"*20)
        print(context)
        print("*"*20)
        paginator = context.get('paginator')
        print(paginator.count)
        print(paginator.num_pages)
        print(paginator.page_range)
        page_obj = context.get('page_obj')
        print(page_obj.has_next())
        print(page_obj.next_page_number)
        paginator_data = self.get_pagination_data(paginator, page_obj)
        context.update(paginator_data)
        return context

    def get_pagination_data(self, paginator, page_obj, around_count=2):
        current_page = page_obj.number
        num_page = paginator.num_pages

        left_has_more = False
        right_has_more = False

        if current_page <= around_count + 2:
            left_page = range(1, current_page)
        else:
            left_has_more = True
            left_page = range(current_page-around_count, current_page)
        if current_page >= num_page-around_count-1:
            right_page = range(current_page+1, num_page+1)
        else:
            right_has_more = True
            right_page = range(current_page+1, current_page+3)
        return {
            'left_pages': left_page,
            'right_pages': right_page,
            'current_page': current_page,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
        }



    # def get_queryset(self):
    #     return Article.objects.filter(id__lte=9)

