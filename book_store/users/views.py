from django.shortcuts import render
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    CreateView,
    FormView,
    TemplateView)

from .forms import (
    ProfileUpdateForm,
    UserRegisterForm,
    UserUpdateForm)

# Create your views here.


class SignUpView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'
    success_message = "Now you are registered, try to log in!"


class UserDetailView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = 'users/user_detail.html'


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    login_url = "login"
    form_class = UserUpdateForm
    p_form = ProfileUpdateForm()
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('UserProfile')
    success_message = "Now your profile is updated!"

    def form_valid(self, form):
        self.request.user.username = self.request.POST['username']
        self.request.user.email = self.request.POST['email']
        self.request.user.save()
        return super().form_valid(form)

    def get_initial(self):
        initial = super(UserUpdateView, self).get_initial()
        initial['username'] = self.request.user.username
        initial['email'] = self.request.user.email
        return initial


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    login_url = "login"
    form_class = ProfileUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('UserProfile')
    success_message = "Now you photo is updated"

    def form_valid(self, form):
        if 'image' in self.request.FILES:
            self.request.user.profile.image = self.request.FILES['image']
            self.request.user.profile.save()
            return super().form_valid(form)
        else:
            messages.add_message(self.request, messages.INFO,
                                 'Your profile pic is not change')
            return HttpResponseRedirect(reverse_lazy('UserProfile'))

    def get_initial(self):
        initial = super(ProfileUpdateView, self).get_initial()
        initial['image'] = self.request.user.profile.image
        return initial


#============================================================================================

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('home')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/user_form.html', context)

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse_lazy('index')
        
        else:
            return super().get_success_url()


from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
