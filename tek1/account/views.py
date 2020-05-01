from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from account.forms import RecepSignUpForm , AdminSignUpForm,VisitorForm , FilterForm
from account.models import User,Temp,Visitor_perma
from django.views import View
from rest_framework import mixins,status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
import io
from account.serializer import TempSerializer
from django.http import StreamingHttpResponse
from rest_framework.renderers import JSONRenderer
from .decorators import admin_required,recep_required
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from datetime import date
import datetime
import logging
from django.contrib.auth.decorators import login_required
from djqscsv import render_to_csv_response
from datetime import timedelta
from django.utils import timezone
import logging
logger=logging.getLogger(__name__)

class RecepSignUpView(CreateView):
    """
    Create new Receptionist ids.
    """
    model = User
    form_class = RecepSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'RECEPTIONIST'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        logger.info("New Receptionist Signup")
        return redirect('account_app:dash')

class AdminSignUpView(CreateView):
    """
    Create new Admin ids.
    """
    model = User
    form_class = AdminSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'ADMIN'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        logger.info("New Admin Signup")
        return redirect('account_app:dash')

@admin_required()
def change_password(request):
    """
    Used for changing the password of User.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            logger.info("Password Changed")
            return redirect('account_app:home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

def home(request):
    """
    Render's Home Page.
    """
    logger.info("Home page is opened")
    return render(request, 'home.html')

def about(request):
    """
    Render's About Page.
    """
    logger.info("About page is opened")
    return render(request, 'about.html')

def support(request):
    """
    Render's Support Page.
    """
    logger.info("Support page is opened")
    return render(request, 'support.html')

def team(request):
    """
    Render's Team Page.
    """
    logger.info("Team page is opened")
    return render(request, 'Team.html')

def dashboard(request):
    """
    Render's dashboard Page of admin and receptionist.
    """
    if request.user.is_superuser:
        logger.info("Admin Dashboard is opened")
        return render(request, 'admin-dashboard.html')
    if request.user.is_recep:
        logger.info("Receptionist Dashboard is opened")
        return render(request, 'recep-dashboard.html')

def not_found(request):
    """
    If User is not found through Phone No.
    """
    logger.info("search by wrong number")
    return render(request, 'NotFound.html')


@api_view(['GET', 'POST','DELETE'])
def user_list(request):
    """
    List all user details.
    """
    # snippets = Temp.objects.all()   // used in delete request
    if request.method == 'GET':
        snippets = Temp.objects.all()
        serializer = TempSerializer(snippets, many=True)
        print("Get req--")
        logger.info("Api for details of visitor is called")
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TempSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Api for posting deatails of visitor is called")
            return Response(serializer.data, status=201)
        logger.info("Api for posting deatails of visitor is wrong")
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        # print(Temp.uid)
        snippet = Temp.objects.get(pk=uid)
    except snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TempSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        snippet.delete()
        print("Deleted---\n")
        return HttpResponse(status=204)


# @admin_required
class HomePageView(TemplateView):
    logger.info("Generate Report Page is opened")
    template_name = 'search.html'


class SearchResultsView(ListView):
    model = Visitor_perma
    template_name = 'search_result.html'

    def get_queryset(self):
        query  =self.request.GET.get('name')
        query2 =self.request.GET.get('dat1')
        query3 = timezone.now().date() - timedelta(days=8)
        query4 = timezone.now().date() - timedelta(days=15)
        query5 =self.request.GET.get('dat2')
        print(query)
        if query=="":
            qu =Visitor_perma.objects.filter(Q(name__iexact=query) | Q(date__gte=query2, date__lt=query5))
            logger.info("Report Generated by date of visitors.")
        else:
            qu =Visitor_perma.objects.filter(Q(name__iexact=query) & Q(date__gte=query2, date__lt=query5))
            logger.info("Report Generated by name and date both of visitors.")
        return qu

def csv_view(request):
    qu = Visitor_perma.objects.all()
    logger.info("Download the data of all Visitors")
    return render_to_csv_response(qu)

@recep_required
def display(request):
    instance = Temp.objects.all().last()
    form = FilterForm(request.POST or None,instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            visit= form.save(commit=False)
            visit1 = Visitor_perma(name=form.cleaned_data['name'],pincode=form.cleaned_data['pincode'],phone=form.cleaned_data['phone'],dob=form.cleaned_data['dob'], uid=form.cleaned_data['uid'], address=form.cleaned_data['address'],purpose=form.cleaned_data['purpose'])
            visit1.save()
            visit.save()
            logger.info("Form is saved of "+form.cleaned_data['name']+".")
        return redirect('account_app:dash')
    return render(request,'home2.html',{'form':form})

@recep_required
def get_queryset2(request):
    query = request.GET.get('q')
    print(query)
    instance = Visitor_perma.objects.filter(phone=query).last()
    if instance==None:
        return redirect('account_app:not_found')
    form = FilterForm(request.POST or None ,instance =instance)
    if request.method =='POST':
        if form.is_valid():
            visit= form.save(commit=False)
            visit1 = Visitor_perma(name=form.cleaned_data['name'],pincode=form.cleaned_data['pincode'],dob=form.cleaned_data['dob'], date=form.cleaned_data['date'], uid=form.cleaned_data['uid'], address=form.cleaned_data['address'],purpose=form.cleaned_data['purpose'],whoto=form.cleaned_data['whoto'],email=form.cleaned_data['email'],phone=form.cleaned_data['phone'])
            visit1.save()
            visit.save()
            logger.info("Visitor Registration done.")
            return redirect('account_app:dash')
        else:
            print(form.errors)
    return render(request,'search2.html',{'form':form})

@recep_required
def main(request):
    return render(request,'main.html')

# @recep_required
class HomePage2View(TemplateView):
    template_name = 'home1.html'
