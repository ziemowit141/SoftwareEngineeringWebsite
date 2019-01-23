from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, RedirectView
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout
from dissertation.models import Profile, Thesis, Message
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


# GENERIC POINT OF VIEW ###################################################
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
    pattern_name = 'login'

    def get_redirect_url(self, *args, **kwargs):
        """
        Logout user and redirect to target url.
        """
        if self.request.user.is_authenticated:
            logout(self.request)
        return super(LogoutView, self).get_redirect_url(*args, **kwargs)

# STUDENT POINT OF VIEW ###################################################
class SupervisorsList(LoginRequiredMixin, TemplateView):
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


class SupervisorDetail(LoginRequiredMixin, TemplateView):
    template_name = 'dissertation/supervisorDetail.html'

    def get_context_data(self, username):
        profile = Profile.objects.get(user__username=username)
        thesisList = profile.thesisList.all()
        context = {"supervisor" : profile,
                   "thesisList" : thesisList}

        return context  

class AplyingForThesisSuccess(LoginRequiredMixin, TemplateView):
    template_name = 'dissertation/successfullyAplyingForSubject.html'

    def notifySupervisor(self, name, subject):
        sender_ = Profile.objects.get(user__username=self.request.user.username)
        receiver_ = Profile.objects.get(user__username=name)
        Message.objects.create(sender=sender_, receiver=receiver_,
            text="Is sending you supervision request for " + subject)

    def get_context_data(self, username, subject):
        self.notifySupervisor(username, subject)
        context = {}
        return context


# SUPERVISOR POINT OF VIEW ###################################################
class StudentsList(LoginRequiredMixin, TemplateView):
    template_name = 'dissertation/studentsList.html'

    def get_context_data(self, **kwargs):
        allProfiles = Profile.objects.filter(is_reviewer=False)
        myStudents = allProfiles.filter(cooperator__user__username=self.request.user.username)

        context = {"studentsList" : myStudents}

        return context


# class Notifications(LoginRequiredMixin, TemplateView):
#     template_name = 'dissertation/notifications.html'
#
#     def get_context_data(self, **kwargs):
#         myNotifications = Message.objects.filter(receiver__user__username=self.request.user.username)
#         context = {'notifications' : myNotifications}
#
#         return context
class Notifications(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'dissertation/notifications.html'
    context_object_name = 'all_messages'

class AcceptStudent(LoginRequiredMixin, TemplateView):
        template_name = 'dissertation/acceptstudent.html'

        def addstuden(self, student , id):
                    currentProfile = Profile.objects.get(user=self.request.user)
                    studentProfile = Profile.objects.get(user__username=student)
                    studentProfile.cooperator = currentProfile
                    studentProfile.save()
                    Message.objects.get(id=id).delete()
        def get_context_data(self, student,id):
            self.addstuden(student,id)
            context = {}
            return context
# class AcceptStudent(LoginRequiredMixin,RedirectView):
#     permanent = False
#     query_string = True
#     pattern_name = 'notifications'
#
#     def get_context_data(self, student, pk):
#         currentProfile = Profile.objects.get(user=self.request.user)
#         studentProfile = Profile.objects.get(user__username=student)
#         studentProfile.cooperator = currentProfile
#         studentProfile.save()
#         Message.objects.get(pk=pk).delete()

class RejectStudent(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('notifications')