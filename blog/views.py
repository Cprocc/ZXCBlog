from django.shortcuts import render
from .models import Article, Category, Banner, Tag, Link
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import markdown


def index(request):
    """
    获取到所有的category，嵌入到index页面中
    轮播图片banner
    首页推荐位recommend_id=2,推荐三篇
    最新文章，根据时间排序推荐三篇
    热门推荐位recommend_id=1，推荐三篇
    热门文章排行，order by views
    :param request:
    :return:
    """
    all_category = Category.objects.all()
    pic_list = Banner.objects.filter(is_active=True)[0:4]
    index_recommend = Article.objects.filter(recommend=2)[:3]
    new_article = Article.objects.all().order_by('-id')[0:10]
    hot_recommend = Article.objects.filter(recommend=1)[:3]
    hot_rank = Article.objects.all().order_by('views')[0:5]
    tags = Tag.objects.all()
    link_list = Link.objects.all()

    context = {
        'all_category': all_category,
        'banner': pic_list,
        'index_recommend': index_recommend,
        'new_article': new_article,
        'hot_recommend': hot_recommend,
        'hot_rank': hot_rank,
        'tags': tags,
        'link': link_list,

    }
    return render(request, 'index.html', context)


# 列表页
def page_list(request, lid):
    list = Article.objects.filter(category_id=lid)  # 获取通过URL传进来的lid，然后筛选出对应文章
    cname = Category.objects.get(id=lid)  # 获取当前文章的栏目名
    remen = Article.objects.filter(recommend__id=2)[:6]  # 右侧的热门推荐
    allcategory = Category.objects.all()  # 导航所有分类
    tags = Tag.objects.all()  # 右侧所有文章标签
    page = request.GET.get('page')  # 在URL中获取当前页面数
    paginator = Paginator(list, 5)  # 对查询到的数据对象list进行分页，设置超过5条数据就分页
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'list.html', locals())


# 内容页
def show(request, sid):
    show = Article.objects.get(id=sid)  # 查询指定ID的文章
    show.body = markdown.markdown(show.body, extensions=[
                                                    'markdown.extensions.extra',
                                                    'markdown.extensions.toc',
                                                    'markdown.extensions.codehilite',
                                                        ], safe_mode=True, enable_attributes=False)  # markdown转html
    allcategory = Category.objects.all()  # 导航上的分类
    tags = Tag.objects.all()  # 右侧所有标签
    remen = Article.objects.filter(recommend=2)[:6]  # 右侧热门推荐
    hot = Article.objects.all().order_by('?')[:10]  # 内容下面的您可能感兴趣的文章，随机推荐
    previous_blog = Article.objects.filter(created_time__gt=show.created_time, category=show.category.id).first()
    next_blog = Article.objects.filter(created_time__lt=show.created_time, category=show.category.id).last()
    show.views = show.views + 1
    show.save()
    return render(request, 'show.html', locals())


# 标签页
def tag(request, tag):
    list = Article.objects.filter(tags__name=tag)  # 通过文章标签进行查询文章
    remen = Article.objects.filter(recommend__id=2)[:6]
    allcategory = Category.objects.all()
    tname = Tag.objects.get(name=tag)  # 获取当前搜索的标签名
    page = request.GET.get('page')
    tags = Tag.objects.all()
    paginator = Paginator(list, 5)
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'tags.html', locals())


# 搜索页
def search(request):
    ss = request.GET.get('search')  # 获取搜索的关键词
    list = Article.objects.filter(title__icontains=ss)  # 获取到搜索关键词通过标题进行匹配
    remen = Article.objects.filter(recommend__id=2)[:6]
    allcategory = Category.objects.all()
    page = request.GET.get('page')
    tags = Tag.objects.all()
    paginator = Paginator(list, 10)
    try:
        list = paginator.page(page)  # 获取当前页码的记录
    except PageNotAnInteger:
        list = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        list = paginator.page(paginator.num_pages)  # 如果用户输入的页数不在系统的页码列表中时,显示最后一页的内容
    return render(request, 'search.html', locals())


# 关于我们
def about(request):
    allcategory = Category.objects.all()
    return render(request, 'page.html', locals())


# 可以进行的优化
def global_variable(request):
    allcategory = Category.objects.all()
    remen = Article.objects.filter(tui__id=2)[:6]
    tags = Tag.objects.all()
    return locals()
