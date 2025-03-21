from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from event.forms import EventModelForm, CategoryModelForm
from event.models import Event, Category
from datetime import date
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# user checking function
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_organizer(user):
    return user.groups.filter(name='Organizer').exists()

def is_participant(user):
    return user.groups.filter(name='Participant').exists()



# views container
def homepage(request):
    if request.method=='POST':
        keyword = request.POST.get('keyword')
    else:
        keyword = 'a'
    events = Event.objects.filter(Q(name__icontains=keyword)|Q(description__icontains=keyword)|Q(location__icontains=keyword))
    group = request.user.groups.first()
    role = group.name if group else "No Role"
    context = {
        'events': events,
        'role':role
    }
    return render(request, 'homepage.html', context)
        
@login_required(login_url='log-in')
def dashboard(request):
    counts = Event.objects.aggregate(
        total = Count('id'),
        today = Count('id', filter=Q(date=date.today())),
        upcoming = Count('id', filter=Q(date__gt = date.today())),
        past = Count('id', filter=Q(date__lt = date.today()))
    )
    category_count = Category.objects.all().count()
    total_participants = User.objects.count()
    total_groups = Group.objects.count()
    rsvp_count = request.user.rsvp_events.all().count()

    events = None
    categories = None
    users = None
    groups = None
    type = request.GET.get('type')
    if type=='total_events':
        events = Event.objects.all()
        section_title = "Total Events "
    elif type=='today':
        events = Event.objects.filter(date=date.today())
        section_title = "Today's Events "
    elif type=='upcoming':
        events = Event.objects.filter(date__gt=date.today())
        section_title = "Upcoming Events"
    elif type=='past':
        events = Event.objects.filter(date__lt=date.today())
        section_title = "Past Events "
    elif type=='booked_events':
        if is_participant(request.user):
            events = list(request.user.rsvp_events.all())
            section_title = "Booked Events"
        else:
            return redirect('no-permission')
    elif type=='categories':
        if is_admin(request.user) or is_organizer(request.user):
            categories = Category.objects.all()
            section_title = "Categories"
        else:
            return redirect('no-permission')
    elif type=='users':
        if is_admin(request.user):
            users = User.objects.all()
            section_title = "User List"
        else:
            return redirect('no-permission')
    elif type=='groups':
        groups = Group.objects.all()
        section_title = "Group"
    else:
        events = Event.objects.filter(date=date.today())
        section_title = "Today's Events"
        if len(events)==0:
            events = Event.objects.all()
            section_title = "Total Events"

    context = {
        'section_title':section_title,
        'total_participants':total_participants,
        'category_count':category_count,
        'total_groups': total_groups,
        'rsvp_count': rsvp_count,
        'counts':counts,
        'users':users,
        'events':events,
        'categories': categories,
        'groups': groups,
    }

    if(is_admin(request.user)):
        context['role'] = 'Admin'
        return render(request, 'dashboard/admin_dashboard.html', context)
    if(is_organizer(request.user)):
        context['role'] ='Organizer'
        return render(request, 'dashboard/organizer_dashboard.html', context)
    elif(is_participant(request.user)):
        context['role'] = 'Participant'
        return render(request, 'dashboard/participant_dashboard.html', context)
    else:
        return redirect('no-permission')

@login_required(login_url='log-in')
def event_details(request, id):
    event = Event.objects.get(id=id)
    participants = None
    if is_admin(request.user):
        participants = event.participants.all()
    context = {
        'event':event,
        'participants':participants
    }
    return render( request, 'event_details.html', context)


class CreateEvent(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'event.add_event'
    login_url = 'log-in'
    model = Event
    form_class = EventModelForm
    template_name = 'create.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, "Event was created Successfully!")
        return super().form_valid(form)


class DeleteEvent(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'event.delete_event'
    login_url = 'log-in'
    def get(self, request, event_id):
        event = Event.objects.get(id=event_id)
        event.delete()
        messages.success(request, "Event was deleted successfully!")
        return redirect('dashboard')


class UpdateEvent(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'event.change_event'
    login_url = 'log-in'
    model = Event
    form_class = EventModelForm
    template_name = 'update.html'
    success_url = reverse_lazy('dashboard')
    pk_url_kwarg = 'event_id'

    def form_valid(self, form):
        messages.success(self.request, "Event was updated successfully!")
        return super().form_valid(form)

class CreateCategory(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'event.add_category'
    login_url = 'log-in'
    model = Category
    form_class = CategoryModelForm
    template_name = 'create.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, "A new category was successfully created!")
        return super().form_valid(form)

class DeleteCategory(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = 'log-in'
    permission_required = 'event.delete_category'
    def post(self, request, *args, **kwargs):
        category_id = kwargs.get('category_id')
        category = Category.objects.get(id=category_id)
        category.delete()
        messages.success(self.request, "Category was deleted successfully!" )
        return redirect('dashboard')

@login_required(login_url='log-in')
@permission_required(perm='event.change_category', login_url='no-permission')
def update_category(request, category_id):
    category = Category.objects.get(id=category_id)
    if request.method == 'POST':
        category_form = CategoryModelForm(request.POST, instance=category)
        if category_form.is_valid():
            category_form.save()
            messages.success(request, "Category Updated successfully!")
            return redirect('dashboard')
    else:
        category_form = CategoryModelForm(instance=category)
        context = {
            'category_form': category_form
        }
        return render(request, 'update.html', context)
    return redirect('dashboard')

@login_required(login_url='log-in')
def book_event(request, event_id):
    event = Event.objects.get(id=event_id)
    user = request.user
    if event.participants.filter(id=user.id).exists():
        messages.error(request, 'You already book this Event!')
        return redirect('homepage')
    else:
        event.participants.add(user)
        messages.success(request, 'Event Book successfully!')
        return redirect('homepage')