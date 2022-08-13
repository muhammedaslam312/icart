

from django.shortcuts import get_object_or_404, redirect, render


from orders.models import OrderProduct
from .models import Account, UserProfile 
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm,UserForm,UserProfileForm

#verification email
from django.contrib.sites.shortcuts import get_current_site 
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from store.models import  Product
from home.models import Banner
from cart.models import Cart,CartItem
from cart.views import _cart_id
from orders.models import Order


 
import requests




# Create your views here.

def home(request):

    active_banner = Banner.objects.filter(is_first=True)
    banners = Banner.objects.filter(is_first=False)
    products = Product.objects.all()
    
    

    context ={
        'active_banner' : active_banner,
        'products':products,
        'banners' :banners,
    }

    return render(request,'accounts/index.html',context)


def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = Account.objects.create_user(first_name=first_name,last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            
            user.save()

            #USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'please activate your account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user,
                'domain':current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })  
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'thank you for register with us...verify your email address')
            return redirect('login')

    else:     
         form = RegistrationForm()
    context ={
        'form':form,
    }
    return render(request,'accounts/signup.html',context)  

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:  
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    #getting the product variation by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    #get the cart items for user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                   
                    ex_var_list =[]
                    id =[]
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    #product_variation = [1, 2, 3, 4, 6]    
                    #ex_var_list = [4, 6, 3, 5]
                    
                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()

            except:
                pass
            auth.login(request, user)
            messages.success(request, 'you are now logged in')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                print('query ->', query)
                #next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                print(params)
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
                    
                    
            except:
                return redirect('home')
        else:
            messages.error(request,'invalid login credentials.')    
            return redirect('login')
    return render(request,'accounts/login.html')

@login_required(login_url ='login')
def user_logout(request):
    auth.logout(request)
    messages.success(request, 'you are logged out.')
    return redirect('login')


def activate(request,uidb64,token):
    try:
        uid =  urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError,OverflowError,Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Your account has been successfully activated.')
        return redirect('login')
    else:
        messages.error(request,'Activation failed try again..!')
        return redirect('login')

def forgotPassword(request):
    if request.method == "POST":
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            #reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset link has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'The link has been expired')
        return redirect('login')


def resetPassword(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')

        else:
            messages.error(request, 'Passwords do not match')
            return redirect('resetPassword')

    else:
     return render(request, 'accounts/resetPassword.html')


@login_required(login_url= 'login')
def user_profile(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    UserProfile.objects.get_or_create(user=request.user)
    userprofile = UserProfile.objects.get(user=request.user)
    context = {
        'orders_count' : orders_count,
        'userprofile' : userprofile,
    }
    return render(request,'accounts/dashboard/user_profile.html',context)        

def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders' : orders,
    }
    return render(request,'accounts/dashboard/my_orders.html', context)  

@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'your profile has been updated')
            return redirect('edit_profile')
    else:
        user_form =UserForm(instance=request.user)
        profile_form =UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form' : profile_form,
        'userprofile' :userprofile,
    }            
    return render(request,'accounts/dashboard/edit_profile.html', context)      



def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__iexact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.Logout(request)
                messages.success(request, 'password updated successfuly.')
                return redirect('change_password')
            else:
                messages.success(request, 'Password updated successfully')
                return redirect('change_password')  
        else:          
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request,'accounts/dashboard/change_password.html')    

def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)

    sub_total = 0
    for i in order_detail:
        sub_total += i.product_price * i.quantity
    
    context = {
        'order_detail' : order_detail,
        'order' : order,
        'sub_total' : sub_total,
    }
    return render(request, 'accounts/dashboard/order_detail.html',context)   

def order_track(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    try:
        if order.status == 'Accepted':
            order_detail.is_shipped = True
        else:
            order_detail.is_shipped = False
    except:
        pass
    try:
        if order.status == 'Completed':
            order_detail.is_delivered = True
            order_detail.is_shipped = True
        else:
            order_detail.is_delivered = False
    except:
        pass

    sub_total = 0
    for i in order_detail:
        sub_total += i.product_price * i.quantity
    
    context = {
        'order_detail' : order_detail,
        'order' : order,
        'sub_total' : sub_total,
        'is_shipped': order_detail.is_shipped,
        'is_delivered': order_detail.is_delivered,
    }
    return render(request, 'accounts/dashboard/order_track.html',context)       