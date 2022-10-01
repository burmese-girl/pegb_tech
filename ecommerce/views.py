from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from . import forms
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model, login as auth_login, logout
from django.http import HttpResponse
from . import models
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from django.utils.translation import gettext_lazy as _
from django.views.generic import View, UpdateView
# email sending
from django.core.mail import send_mail
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.views import generic
from django.core.files.storage import FileSystemStorage
import json
from decimal import *
from django.utils import timezone
from datetime import datetime
import pytz

# Create your views here.
# def index(request):
#     # return render(request, "index.html", {})
#     if request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('user:profile'))
#     return HttpResponseRedirect(reverse(settings.LOGIN_URL))


def index(request):
    # print("**** Home Page **** ")
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('user:login'))
    product_list = models.Product.objects.filter(is_sale=True)
    category_obj = models.ProductCategory.objects.all()
    frozen_foods = []
    fresh_produce = []
    computers = home_appliances = noddles = seafood = bags = rice = fruits = oil = general = categ_list = []
    for categ in category_obj:
        categ_list.append(categ)
    print("* Length of Category List *  ", len(categ_list))
    for prod in product_list:
        if prod.category_id.name == "frozen_foods":
            categ_id = prod.category_id.id
            frozen_foods = models.Product.objects.filter(
                is_sale=True, category_id=categ_id)[:4]
            # computers.append(prod)
        elif prod.category_id.name == 'fresh_produce':
            categ_id = prod.category_id.id
            fresh_produce = models.Product.objects.filter(
                is_sale=True, category_id=categ_id)[:4]

        else:
            general.append(prod)

    if 'btn-search' in request.POST:
        search_input = request.POST.get('search')
        product_list = models.Product.objects.filter(
            name__icontains=search_input, is_sale=True)
        print("****** Item Count : ", len(product_list))
        count = len(product_list)
        return render(request, 'product_search.html',
                      {'product_list': product_list, 'count': count, 'search_item': search_input})

    return render(request, 'products.html',
                  {'frozen_foods': frozen_foods, 'fresh_produce': fresh_produce, 'categ_list': categ_list, })


def login(request):
    form = forms.AuthenticateExtraForm(request, data=request.POST)

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:profile'))

    if request.method != 'POST':
        form = forms.AuthenticateExtraForm(request)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print("User login ::::", user)

        if user is not None:
            if user.userprofile.active_user:
                auth_login(request, user)
                print("Login Successfully!")
            else:
                html = "<h2 style='background-color:yellow;'> This account is not activate. Please activate your email " \
                       "first!</h2> "
                return HttpResponse(html)

        else:
            html = "<h2 style='background-color:yellow;'> Authentication Error! Check username & password again " \
                   "!</h2> "
            return HttpResponse(html)

        return HttpResponseRedirect(reverse('user:profile'))

    return render(request, "login.html", {
        'form': form,

    })


def profile(request):
    print("reached profile. :")

    try:
        user = models.UserProfile.objects.get(user=request.user)
    except:
        return HttpResponseRedirect(reverse(settings.LOGIN_URL))

    if request.method != 'POST':
        profile_form = forms.ProfileForm(instance=user, initial={'first_name': request.user.first_name,
                                                                 'last_name': request.user.last_name})
        return render(request, "profile.html", {'form': profile_form, })
    return HttpResponseRedirect(reverse('user:profile'))


def register(request):
    if request.method != 'POST':
        form = forms.SignupForm()
        return render(request, 'signup.html', {'form': form})

    register_form = forms.SignupForm(request.POST)
    if not register_form.is_valid():
        return render(request, 'signup.html', {"form": register_form})
    transaction.atomic()

    try:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        residential_country = request.POST.get('residential_country')
        nationality = request.POST.get('nationality', '')
        user = User.objects.create_user(username=email, email=email)
        user.is_active = True
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        if password:
            user.set_password(password)
        user.save()
        print("User =============")
        print(user)

        profile, created = models.UserProfile.objects.get_or_create(
            user_id=user.pk, dob=dob)  # requried field=dob
        profile.gender = gender
        profile.dob = dob
        profile.name = first_name + " " + last_name
        profile.residential_country = residential_country
        profile.nationality = nationality
        profile.active_user = False
        profile.created_user = "Admin Site"
        profile.save()
        print("Profile =============")
        print(profile)
        # For Email Sending
        # user = register_form.save(commit=False)
        # user.is_active = False  # Deactivate account till it is confirmed
        # user.save()
        current_site = get_current_site(request)
        subject = 'Activate Your Account'
        data = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        }
        message = render_to_string('account_activation_email.html', data)
        # user.email_user(subject, message)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail(subject, message, email_from, recipient_list)
        context = data
        messages.success(
            request, 'Please Confirm your email to complete registration.')
        return render(request, 'email_confirmation.html', context)

    except ValueError:
        print
        transaction.rollback()
        messages.add_message(request, messages.INFO, _('Registration failed.'))
        return render(request, 'signup.html', {
            'form': forms.RegistrationForm(request.POST),

        })

    return HttpResponseRedirect(reverse('user:profile'))


def logout(request):
    form = forms.AuthenticateExtraForm(request)
    # import pdb;pdb.set_trace()
    auth.logout(request)

    return render(request, "logout.html", {'form': form, })


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.userprofile.email_confirmed = True
            user.userprofile.active_user = True
            user.userprofile.save()
            user.save()
            auth_login(request, user)
            messages.success(request, 'Your account have been confirmed.')
            return HttpResponseRedirect(reverse("user:profile"))
        else:
            messages.warning(
                request, 'The confirmation link was invalid, possibly because it has already been used.')
            return HttpResponseRedirect(reverse(settings.LOGIN_URL))


def product_category(request, *args, **kwargs):
    print("** Product Category **")
    if request.method != 'POST':
        if kwargs and 'pk' in kwargs:
            product_list = models.Product.objects.filter(
                is_sale=True, category_id=kwargs['pk'])
            category_name = models.ProductCategory.objects.filter(
                id=kwargs['pk'])
            if category_name:
                category_name = category_name[0].complete_name
            if product_list:
                return render(request, 'product_categories.html',
                              {'product_list': product_list, 'category_name': category_name})
            else:
                return render(request, "404.html")


def product_details(request, *args, **kwargs):
    print(" Product details")
    if request.method != 'POST':
        if kwargs and 'pk' in kwargs:
            product_detail = models.Product.objects.filter(
                is_sale=True, id=kwargs['pk'])
            qty = 1
            if product_detail:
                return render(request, 'product_details.html', {'product': product_detail[0], 'qty': qty, })
            else:
                return render(request, "404.html")

    if request.method == 'POST':
        if 'btn-search' in request.POST:
            search_input = request.POST.get('search')
            product_list = models.Product.objects.filter(
                name__icontains=search_input, is_sale=True)
            count = len(product_list)
            return render(request, 'product_search.html',
                          {'product_list': product_list, 'count': count, 'search_item': search_input})


class CartListView(generic.ListView):
    model = models.Product
    context_object_name = 'cart_list'
    queryset = []
    # queryset = models.Product.objects.filter()[:2]
    template_name = 'cart_list.html'

    def get(self, request):
        # print("***Cart request.method:::: {0}\n ***self.queryset :::::::{1}".format(request.method, self.queryset))
        return render(request, 'cart_list.html', {'cart_list': self.queryset})


def order(request):
    form = forms.AuthenticateExtraForm(request)
    if not request.user.is_authenticated:
        return render(request, 'login.html', {'form': form})

    if request.method == "POST":
        order_form = forms.OrderConfirmedForm()
        if request.method == 'POST' and 'myfile' in request.FILES:
            order_form = forms.OrderConfirmedForm(
                initial={'payment_type': 'Other_Payment'})
            image_file = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(image_file.name, image_file)
            uploaded_file_url = fs.url(filename)
            print("Storage URL", uploaded_file_url)
            return render(request, 'order_confirm.html', {'form': order_form,
                                                          'uploaded_file_url': uploaded_file_url
                                                          })
        return render(request, 'order_confirm.html', {'form': order_form})
    return render(request, 'order_list.html', )


class SuccessOrderView(generic.ListView):
    model = models.Order
    context_object_name = 'order'
    queryset = []
    template_name = 'order_success.html'

    def get(self, request):
        print(
            "\n  ******** SelfConfirmedOrder ******* {0} \n".format(self.queryset))
        return render(request, 'order_success.html', {'order': self.queryset})
