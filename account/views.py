from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from validate_email import validate_email

from account.forms import UserEditForm
from account.token import account_activation_token
from store.models import Product


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'account/dashboard/edit_details.html', {'user_form': user_form})


@login_required
def delete_user(request):
    user = User.objects.get(username=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, 'account/dashboard/user_wish_list.html', {"wishlist": products})


@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, 'account/dashboard/user_wish_list.html', {"wishlist": products})


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, "You removed " + product.title + " from wishlist")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "Added " + product.title + " to your Wishlist")
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def dashboard(request):
    return render(request, 'account/dashboard/dashboard.html', {})


def register(request):
    if request.method == 'POST':
        context = {'has_error': False, 'data':request.POST}
        fname = request.POST.get('fname')
        lname = request.POST.get('sname')
        username = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('pass')
        password2 = request.POST.get('pass2')

        if len(password) < 6:
            messages.add_message(request, messages.ERROR,
                                 'Password should be at least 8 characters')
            context['has_error'] = True

        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'Password mismatch')
            context['has_error'] = True

        if not validate_email(email):
            messages.add_message(request, messages.ERROR,
                                 'Enter a valid email address')
            context['has_error'] = True

        if not username:
            messages.add_message(request, messages.ERROR,
                                 'Username is required')
            context['has_error'] = True

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR,
                                 'Username is taken, choose another one')
            context['has_error'] = True

        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR,
                                 'Email is taken, choose another one')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'account/register.html', context)

        new_user = User.objects.create_user(username=username, email=email)
        new_user.set_password(password)
        new_user.first_name = fname
        new_user.last_name = lname
        new_user.is_active=False
        new_user.save()
        # Setting-up email
        current_site = get_current_site(request)
        subject = 'Activate your Account'
        message = render_to_string('account/account_activation_email.html',{
            'user': new_user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
            'token': account_activation_token.make_token(new_user),
        })
        new_user.email_user(subject=subject, message=message)
        messages.success(request, 'Account creation was successful, confirm you email using the link send to activate.')
        return redirect('store:all_products')

    return render(request, 'account/register.html')


def account_activate(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    new_user = User.objects.get(pk=uid)
    if new_user is not None and account_activation_token.check_token(new_user, token):
        new_user.is_active = True
        new_user.save()
        login(request, new_user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/activation_invalid.html')


def loginn(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        password = request.POST.get('pass')

        user = authenticate(request, username=uname, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been successfully logged in')
            return redirect('store:all_products')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('account:login-page')

    return render(request, 'account/login.html', {})


def logoutuser(request):
    logout(request)
    return redirect('store:all_products')
