from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from .forms import CustomUserCreationForm, AddUserForm
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required
from django.utils import translation
from datetime import date, datetime
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import to_locale, get_language
from account.models import Company


def viewAR(request):
    if translation.LANGUAGE_SESSION_KEY in request.session:
        del request.session[translation.LANGUAGE_SESSION_KEY]
    request.session.modified = True
    user_language = 'ar'
    translation.activate(user_language)
    request.LANGUAGE_CODE = translation.get_language()
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    request.session.modified = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def viewEN(request):
    if translation.LANGUAGE_SESSION_KEY in request.session:
        del request.session[translation.LANGUAGE_SESSION_KEY]
    request.session.modified = True
    user_language = 'en'
    translation.activate(user_language)
    request.LANGUAGE_CODE = translation.get_language()
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    request.LANGUAGE_CODE = translation.get_language()
    request.session.modified = True
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@never_cache
def user_login(request):
    next = request.GET.get('next')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if next:
                    return redirect(next)
                return redirect(reverse('home:homepage'))
            else:
                messages.error(request, 'Inactive Account')
                return render(request, 'login.html')
        else:
            messages.error(request, _(
                'Login Failed, Please Check the Username or Password'))
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


@login_required(login_url='home:user-login')
def homepage(request):
    return render(request, 'index.html', context=None)


@login_required(login_url='home:user-login')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home:user-login'))


def register(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            comp = Company(
                           name = form.cleaned_data.get('company_name'),
                           created_by = user.id,
                           )
            comp.save()
            user.company_id = comp.id
            user.is_staff = True
            user.save(update_fields=['company', 'is_staff'])
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home:user-login'))
            else:
                user_lang=user_lang=to_locale(get_language())
                if user_lang=='ar':
                    messages.error(request, 'This account is deactivated!')
                else:
                    messages.error(request, 'This Account is inactive!')
                return render(request, 'login.html')
    return render(request, 'register.html', {'register_form': form})


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_reset_complete.html'
    title = _('Password reset complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'registration/password_change_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_change_done.html'
    title = _('Password change successful')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
