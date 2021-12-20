from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, ArchiveIndexView, YearArchiveView, CreateView, UpdateView, \
    DeleteView
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from requests import post
from .models import Post
from .forms import PostForm
from django.contrib import messages


# @login_required
# def post_new(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             messages.success(request, '포스팅을 저장했습니다')
#             return redirect(post)
#     else:
#         form = PostForm()
#
#     return render(request, 'instagram/post_form.html', {
#         'form': form,
#         'post': None,
#     })

#로그인 리콰이어드 사용해도 되고, 인자에 로그인 리과이어드 믹스인을 사용하면 된다
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        messages.success(self.request, '포스팅을 저장했습니다')
        return super().form_valid(form)


post_new = PostCreateView.as_view()


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        messages.success(self.reqeust, '포스팅을 수정했습니다')
        return super().form_valid(form)

post_edit = PostUpdateView.as_view()

# @login_required
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#
#     # 장식자로 만들어서 추가하자
#     if post.author != request.user:
#         from django.contrib import messages
#         messages.error(request, '작성자만 추가할 수 있습니다')
#         return redirect(post)
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES, instance=post)
#         if form.is_valid():
#             post = form.save()
#             # messages.success(request, '포스팅을 수정했습니다')
#             return redirect(post)
#     else:
#         form = PostForm(instance=post)
#
#     return render(request, 'instagram/post_form.html', {
#         'form': form,
#         'post': post,
#     })

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    # success_url = '/instagram/'
    # success_url = reverse('instagram:post_list')
    # 리버스가 안되는 이유:
    # 파이썬은 소스가 임포트될 때 한줄 한줄 시작된다. 리버스(석세스 url)은 소스코드가 읽혀질 때 실행된다.
    # 즉 장고 초기화, 프로젝트를 로딩하기 전에 실행된다.
    # 이를 해결하기 위해 메서드로 만들어서 사용할 때 호출해도 되고,
    # def get_success_url(self):
    #     return reverse('instagram:post_list')
    success_url = reverse_lazy('instagram:post_list')
    # 해도 된다


post_delete = PostDeleteView.as_view()


# @login_required
# def post_delete(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == 'POST':
#         post.delete()
#         messages.success(request, '성공적인 삭제')
#         return redirect('instagram:post_list')
#     return render(request, 'instagram/post_confirm_delete.html', {
#       'post': post,
#     })


# post_list = login_required(ListView.as_view(model=Post, paginate_by=10))
@method_decorator(login_required, name='dispatch')
class PostListView(ListView):
    model = Post
    paginate_by = 100


post_list = PostListView.as_view()


# @login_required
# def post_list(request):
#     qs = Post.objects.all()
#     q = request.GET.get('q', '')
#     if q:
#         qs = qs.filter(message__icontains=q)
#
#     # instagram/templates/instagram/post_list.html
#     return render(request, 'instagram/post_list.html', {
#         'post_list': qs,
#         'q': q,
#     })


# def post_detail(request: HttpRequest, pk) -> HttpRequest:
#     post = get_object_or_404(Post, pk=pk)
#
#     # try:
#     #     Post.objects.get(pk=pk)
#     # except Post.DoesNotExist:
#     #     raise Http404
#
#     return render(request, 'instagram/post_detail.html', {'post': post, })
#     return response

# post_detail = DetailView.as_view(
#     model=Post,
#     queryset=Post.objects.filter(is_public=True)
#     )


class PostDetailView(DetailView):
    model = Post
    # queryset = Post.objects.filter(is_public=True)

    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_authenticated:
            qs = qs.filter(is_public=False)
        return qs


post_detail = PostDetailView.as_view()


# def archives_year(request, year):
#     return HttpResponse(f"{year}년 archives")

post_archive = ArchiveIndexView.as_view(model=Post, date_field='created_at', paginate_by=10)

post_archive_year = YearArchiveView.as_view(model=Post, date_field='created_at', make_object_list=True)
