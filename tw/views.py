from django.shortcuts import render
from .models import Twitter
from .forms import TwitterForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


def twit_list(request):
    twits = Twitter.objects.all().order_by('-created_at')
    return render(request, 'twit_list.html', {'twits':twits})


@login_required
def twit_create(request):
    if request.method == "POST":
      form = TwitterForm(request.POST, request.FILES)
      if form.is_valid():
          twit = form.save(commit=False)
          twit.user = request.user
          twit.save()
          return redirect('twit_list')
    else:
        form = TwitterForm()
    return render(request, 'twit_form.html', {'form':form})

@login_required
def twit_edit(request, twit_id):
    twit = get_object_or_404(Twitter, pk= twit_id, user= request.user)
    if request.method == "POST":
        form = TwitterForm(request.POST, request.FILES, instance=twit)
        if form.is_valid():
            twit = form.save(commit=False)
            twit.user = request.user
            twit.save()
            return redirect('twit_list')
    else:
        form = TwitterForm(instance=twit)
    return render(request, 'twit_form.html', {'form':form})

@login_required
def twit_delete(request, twit_id):
   twit = get_object_or_404(Twitter, pk=twit_id, user = request.user)
   if request.method == "POST":
       twit.delete()
       return redirect('twit_list')
   return render(request, 'twit_confirm_delete.html', {'twit':twit})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('twit_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html',{'form':form})


def search_twit(request):
    query = request.GET.get('q', '')
    if query:
        results = Twitter.objects.filter(text__icontains=query)
    else:
        results = Twitter.objects.none()
    return render(request, 'search_twit.html', {'results': results, 'query': query})

   
