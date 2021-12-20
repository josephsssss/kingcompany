from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, UpdateView
from accounts.forms import ProfileForm
from accounts.models import Profile

# @login_required
# def profile(request):
#     return render(request, 'accounts/profile.html')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'


profile = ProfileView.as_view()



# 클래스 뷰는 경계가 확실할 때 좋지만, 모호할 땐 산으로 간다
# class ProfileUpdateView(UpdateView):
#     model = ProfileView
#     form_class =ProfileForm


@login_required
def profile_edit(request):
    try:
        profile = request.user.profile
        # Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':                    # 프로필 필히 인스턴스로 지정
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
    else:               # 인스턴스로 지정
        form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_form.html',{
        'form': form,
    })


def signup(request):
    pass


def logout(request):
    pass




