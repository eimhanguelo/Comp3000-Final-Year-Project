from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from blog.views import ITUserMixin  # Assuming ITUserMixin is imported from blog.views

from django.http import JsonResponse
from django.core.management import call_command
from django.views import View

class SyncLdapUsersView(View):
    def get(self, request, *args, **kwargs):
        try:
            # Call the command and capture the result message
            result = call_command('sync_ldap_users')
            return JsonResponse({"message": result})
        except Exception as e:
            return JsonResponse({"message": f"Error: {str(e)}"}, status=500)

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views import View

class CustomRegisterView(View):
    template_name = 'users/register.html'

    def get(self, request):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the user with username, password, first_name, and email
            user = form.save(commit=False)  # Don't commit yet to modify fields
            user.first_name = request.POST.get('first_name')  # Get first name from the form data
            user.last_name = request.POST.get('last_name')  # Get first name from the form data
            user.email = request.POST.get('email')  # Get email from the form data
            user.save()  # Now save the user instance with first_name and email

            messages.success(request, f'Account created for {user.username}!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, self.template_name, {'form': form})





# Custom LoginView
class CustomLoginView(LoginView):
    template_name = 'users/login.html'  # Your login template
    redirect_authenticated_user = True  # Redirects authenticated users
    success_url = reverse_lazy('profile')  # Redirect to profile after login
    
    def form_invalid(self, form):
        messages.error(self.request, "Please enter the correct username or password.")
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context

# Autocomplete view for usernames
def autocomplete(request):
    term = request.GET.get('term')  # Get the search term from the GET parameters
    users = User.objects.filter(username__icontains=term)[:10]  # Example query to filter users
    results = [user.username for user in users]  # Extract usernames for autocomplete suggestion
    return JsonResponse(results, safe=False)

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

from django.contrib import messages  # Ensure you import messages

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')  # Success message
            return redirect('profile')  # Redirect to the profile page after a successful update
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'users/profile.html', context)


# User detail view (requires login)
class UserDetailView(ITUserMixin, LoginRequiredMixin, DetailView):
    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context = {
            'ok': User.objects.get(id=user.id),
        }
        return render(request, 'users/user_summary.html', context)

# User list view (requires login)
class UserListView(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        context = {            
            'user_list': User.objects.all()
        }
        return render(request, 'users/all_user_list.html', context)
