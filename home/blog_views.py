from django.shortcuts import render, redirect, get_object_or_404
from . models import Blog, Like, Comment, Subscription
from rest_framework.response import Response
from rest_framework.decorators import api_view
from taggit.models import Tag
from django.core.paginator import Paginator, PageNotAnInteger
from django.db.models import Count, Q
from django.contrib import messages
from django.core.paginator import Paginator
def search(request):
    if request.GET.get('search'):
        q = request.GET.get('search')
        post = Blog.objects.filter(Q(title__icontains=q) | Q(author__icontains=q) | Q(text__icontains=q))
        title = request.GET.get('search')

        if q is not None:
            prop = Paginator(post, 12)
            page = request.GET.get('page')
            page_obj = prop.get_page(page)
            return render(request, 'results.html', {'page_obj': page_obj, "title": title})


@api_view(["POST"])
def letter(request):
    if request.method == "POST":
        email = request.data.get("email")
        if Subscription.objects.filter(email=email).exists():
            return Response({"message": "The email already exist"})
        Subscription.objects.create(email=email)
        return Response({"message": "You have successfully subscribed to our news letter"})

def home_page(request):
    tags = Tag.objects.all()
    visit = None
    recent = Blog.objects.all()[:6]
    if request.session.get('visitors'):
        visit = True
        request.session['visitors'] = int(request.session.get('visitors') + 1)
    else:
        request.session['visitors'] = 1
        visit = False
    return render(request, 'home/index.html', {'recent': recent, 'tags':tags, 'visit': visit})


def detail(request, pk, slug):
    post = get_object_or_404(Blog, pk=pk, slug=slug)
    likes = Like.objects.filter(blog__pk=pk).count()
# List of active comments for this post
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Blog.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-created_on')[:5]
    if request.method == "POST":
        name = request.POST.get("name")
        msg= request.POST.get("msg")
        post = get_object_or_404(Blog, pk=pk, slug=slug)
        new_comment = Comment(name=name, content=msg, blog=post)
        new_comment.save()
        messages.success(request, 'Comment added')

#        return render(request, 'detail.html',
#                  {'post': post,
#                   'similar_posts': similar_posts,
#"likes":likes
#})
    return render(request, 'detail.html',
                  {'post': post,
                   'similar_posts': similar_posts,
"likes":likes
})

@api_view(['POST'])
def like(request):
    post_pk = int(request.data.get('post_pk'))
    post = get_object_or_404(Blog, pk=post_pk)
    if request.method == 'POST':
        like = Like(blog=post)
        like.save()
        data = {'count_likes': Like.objects.filter(blog__pk=post_pk).count()}
        return Response(data)

def tags(request, tag_slug=None):
    object_list = Blog.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 5) # 3 posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                 'tags.html',
                 {'page': page,
                  'posts': posts,
                  'tag': tag})

def search(request):
    if request.GET.get('search'):
        q = request.GET.get('search')
        post = Blog.objects.filter(Q(title__icontains=q) | Q(author__icontains=q) | Q(text__icontains=q))
        title = request.GET.get('search')

        if q is not None:
            prop = Paginator(post, 12)
            page = request.GET.get('page')
            page_obj = prop.get_page(page)
            return render(request, 'results.html', {'page_obj': page_obj, "title": title})

@api_view(["GET"])
def comment(request):
    post_id = request.GET.get("post_id")
    comments = Comment.objects.filter(blog__id=post_id)
    paginate_obj = Paginator(comments, 8)
    results = paginate_obj.get_page(int(request.GET.get("page", 1)))
    data = [{"name": comment.name, "date": comment.date, "content": comment.content} for comment in results]
    data.append({"pagination_info": {"has_prev": results.has_previous(), "has_next": results.has_next(), "page_number": results.number,  "pages": paginate_obj.num_pages}})
    return Response(data)


@api_view(["POST"])
def subscribe(request):
    if request.method == "POST":
        email = request.data.get('email')
        if Subscription.objects.filter(email=email).exists():
            return Response({"data": "Email already exists"})
        Subscription.objects.create(email=email)
        return Response({"data": "Added"})
