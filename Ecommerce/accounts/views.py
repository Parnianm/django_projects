from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm, LoginForm
# verfication Email 
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.urls import reverse
from carts.models import Cart, CartItem
from carts.views import _cart_id
import requests
from urllib.parse import urlparse, parse_qs

User = get_user_model()

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated. You can now login.')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('accounts:register')
        
def reset_password_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/emails/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            email = EmailMessage(
                subject=mail_subject, 
                body=message,
                from_email=None,
                to=[to_email]
            )
            email.content_subtype = 'html'
            email.send()
            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Account with this email does not exist.')

    return render(request, 'accounts/reset_password_request.html')


def reset_password_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            if password == confirm_password:
                user.set_password(password)
                user.save()
                messages.success(request, 'Your password has been reset successfully.')
                return redirect('accounts:login')
            else:
                messages.error(request, 'Passwords do not match.')
        return render(request, 'accounts/reset_password_confirm.html')
    else:
        messages.error(request, 'The reset link is invalid or has expired.')
        return redirect('accounts:reset_password')        

def register_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.username = form.cleaned_data['email'].split('@')[0]
            user.phone_number = form.cleaned_data['phone_number']
            user.is_active = False 
            user.save()

            # ==== User Activation====
            current_site = get_current_site(request)
            mail_subject = 'PLease activate your account'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()

            messages.success(request, "Please check your email to activate your account.")
            return redirect(f"{reverse('accounts:login')}?command=verification&email={email}")
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email = form.cleaned_data['email'],
                # username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user:
                if user.is_active:
                    try:
                        cart = Cart.objects.get(cart_id = _cart_id(request))
                        is_cart_item_exits = CartItem.objects.filter(cart = cart).exists()
                        if is_cart_item_exits:
                            cart_item = CartItem.objects.filter(cart=cart)

                            for item in cart_item:
                                item.user = user
                                item.save()
                    except:
                        pass
                    
                    login(request, user)
                    messages.success(request, "Login successful.")
                    url = request.META.get('HTTP_REFERER')
                    if url:
                        try:
                            query = urlparse(url).query
                            params = parse_qs(query)
                            next_page = params.get('next', [None])[0]
                            if next_page:
                                return redirect(next_page)
                        except Exception:
                            pass

                    return redirect('accounts:dashboard')
                else:
                    messages.warning(request, "Account is not activated. Please check your email.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('accounts:login')


@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})


