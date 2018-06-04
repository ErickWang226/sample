from django.shortcuts import render
from django.forms.models import modelform_factory
from myapp.models import UserInfo
# Create your views here.
def home(request):
    return render(request, 'home.html')

def form_create(request):
    UserFrom = modelform_factory(UserInfo, fields=('user_name', 'user_col', 'user_int'))
    if request.method == 'POST':
        form = UserFrom(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'result.html')
    else:
        form = UserFrom()
    return render(request, 'userform.html', {'form':UserFrom()})
