from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, RedirectView
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from dissertation.models import Profile

class StartView(TemplateView):
    template_name = 'dissertation/start.html'

class LoginView(views.LoginView):
    template_name = 'dissertation/login_form.html'

@login_required
def index(request):
    url = '/dissertation/index/%s/' % request.user.username
    return HttpResponseRedirect(url)

class UserIndexView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'dissertation/index.html'
    redirect_field_name = 'login'

class LogoutView(RedirectView):
    """
    A view that logout user and redirect to homepage.
    """
    permanent = False
    query_string = True
    pattern_name = 'start'

    def get_redirect_url(self, *args, **kwargs):
        """
        Logout user and redirect to target url.
        """
        if self.request.user.is_authenticated:
            logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)


class SupervisorsList(TemplateView):
    template_name = 'dissertation/availableSupervisors.html'

    # def get_context_data(self, **kwargs):
    #     context = super(SupervisorsList, self).get_context_data(**kwargs)
    #     context['supervisorsList'] = Profile.objects.filter(is_reviewer=True)
        
    #     return context

    def get_context_data(self, **kwargs):
        allProfiles = Profile.objects.all()
        allSupervisorProfiles = []

        for profile in allProfiles:
            if profile.is_reviewer:
                allSupervisorProfiles.append(profile)
                print(profile.user.first_name)

        context = {"supervisorsList" : allSupervisorProfiles}

        return context


class SupervisorDetail(TemplateView):
    template_name = 'dissertation/supervisorDetail.html'

    def get_context_data(self, username):
        profile = Profile.objects.get(user__username=username)
        print(profile.user.username)
        context = {"supervisor" : profile}

        return context    
