from django.views.generic import CreateView, FormView, View, DetailView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import render, HttpResponseRedirect
from .forms import CustomUserCreationForm, AccountEditForm

class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


class AccountEditView(LoginRequiredMixin, FormView):
    form_class = AccountEditForm
    template_name = 'accounts/account_edit.html'
    success_url = reverse_lazy('account_edit')

    def get_initial(self):
        account = self.request.user
        initial = {
            'username': account.username,
            'display_name': account.display_name,
            'email': account.email,
        }
        return initial

    def get_form_kwargs(self):
        kwargs = super(AccountEditView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class AccountDeleteView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/account_delete.html')

    def post(self, request):
        account = request.user
        account.delete()
        return HttpResponseRedirect(reverse_lazy('login'))


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    context_object_name = 'account'
    template_name = 'accounts/account_detail.html'