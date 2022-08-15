


from django.shortcuts import render,redirect
from accounts.models import Account,UserProfile
from cart.models import Cart,CartItem
from category.models import Category
from category.forms import CategoryForm
from django.template.defaultfilters import slugify
from django.contrib import messages
from store.models import Product,Variation,ProductGallery
from store.forms import ProductForm,VariationForm
from orders.models import Order,OrderProduct,Payment
from django.db.models import Sum
from django.contrib.auth.decorators import login_required 
from django.db.models.functions import TruncMinute
import datetime
from django.core.paginator import Paginator
from django.db.models import Q



# Create your views here.

def admin_login(request):
    return render(request,'adminpanel/admin_accounts/admin_login.html')

@login_required(login_url="login")
def user_accounts_table(request,id):
    if request.user.is_superadmin:
        active_users = Account.objects.all().filter(is_admin=False,is_active=True)
        banned_users = Account.objects.all().filter(is_admin = False, is_active =False)
        context  = {
            'active_users' : active_users,
            'banned_users' : banned_users,
        }
        if id==1:
            return render(request,'adminpanel/admin_accounts/accounts.html',context)
        else:
            return render(request,'adminpanel/admin_accounts/banned_accounts.html',context)    

    else:
        return redirect ('home')        

@login_required(login_url="login")
def ban_user(request,id):
    if request.user.is_superadmin:
        user           = Account.objects.get(id=id)
        user.is_active = False
        user.save()
        return redirect('user_accounts_table',id=1)
    else:
         return redirect ('home')

@login_required(login_url="login")         
def unban_user(request,id):
    if request.user.is_superadmin:
        user           = Account.objects.get(id=id)
        user.is_active = True
        user.save()
        return redirect('user_accounts_table',id=2)    
    else:
        return redirect ('home')

@login_required(login_url="login")        
def cart_table(request,id):
    if request.user.is_superadmin:
        carts = Cart.objects.all()
        cart_items = CartItem.objects.all().filter(is_active=True)
        context = {
            'carts' : carts,
            'cart_items' : cart_items,
            
        }
        if id== 1:
            return render(request,'adminpanel/cart_table/cart.html', context)
        else:
            return render(request,'adminpanel/cart_table/cart_items.html', context)  
    else:
        return redirect ('home')          


@login_required(login_url="login")
def category_table(request,id):
    if request.user.is_superadmin:
        category =Category.objects.all()
        context = {
            'category' : category,
        }
        return render(request,'adminpanel/category_table/category.html',context)
    else:
         return redirect ('home')              

@login_required(login_url="login")
def add_category(request):
    if request.user.is_superadmin:
        form = CategoryForm()
        if request.method == 'POST':
            form = CategoryForm(request.POST, request.FILES)
            if form.is_valid():
                category = form.save()
                category_name = form.cleaned_data['category_name']
                slug = slugify(category_name)
                category.slug = slug
                category.save()
                messages.success(request,'New category added successfully')
                return redirect('category_table',id=1)
        context = {
            'form' : form,
        }        
        return render (request,'adminpanel/category_table/add_category.html',context)

    else:
        return redirect ('home')    

@login_required(login_url="login")
def edit_category(request,id):
    if request.user.is_superadmin:
        category = Category.objects.get(id=id)
        if request.method == 'POST':
            form = CategoryForm(request.POST, request.FILES, instance = category)
            if form.is_valid():
                
                category_name = form.cleaned_data['category_name']
                slug = slugify(category_name)
                category.slug = slug
                category.save()
                messages.success(request,'category editted successfully')
                return redirect('category_table',id=1)
        else:
            form = CategoryForm(instance=category)

        context = {
            'form' : form,
        }        
        return render (request,'adminpanel/category_table/add_category.html',context)
    else:
        return redirect ('home')     

@login_required(login_url="login")
def delete_category(request,id):
    if request.user.is_superadmin:
        category = Category.objects.get(id=id)
        category.delete()
        return redirect ('category_table',id=1)
    else:
        return redirect ('home')       

@login_required(login_url="login")
def store_table(request,id):
    if request.user.is_superadmin:
        products = Product.objects.all()
        variations =Variation.objects.all()

        context = {
            'products' : products,
            'variations' : variations,
        }
        if id==1:
            return render(request,'adminpanel/store_table/products.html',context)
        else:
            return render(request,'adminpanel/store_table/variations.html',context)

    else:
        return redirect ('home')              

@login_required(login_url="login")
def add_product(request):
    if request.user.is_superadmin:
        form = ProductForm()
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid()   :
                product = form.save(commit=False)
                product_name = form.cleaned_data['product_name']
                slug = slugify(product_name)
                product.slug = slug
                product.save()

                images = request.FILES.getlist('images')
                for image in images:
                    ProductGallery.objects.create(
                        image = image,
                        product = product,
                    )

                messages.success(request,'New product added successfully')
                return redirect('store_table',id=1)
        else:
            form = ProductForm()
        context = {
            'form' : form,
        }
        return render(request,'adminpanel/store_table/add_product.html',context)

    else:
        return redirect('home')

@login_required(login_url="login")
def edit_product(request,id):
    if request.user.is_superadmin:
        product = Product.objects.get(id=id)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance = product)
            if form.is_valid():
                
                product_name = form.cleaned_data['product_name']
                slug = slugify(product_name)
                product.slug = slug
                product.save()
                messages.success(request,'product editted successfully')
                return redirect('store_table',id=1)
        else:
            form = ProductForm(instance=product)

        context = {
            'form' : form,
        }        
        return render (request,'adminpanel/store_table/add_product.html',context)
    else:
        return redirect('home')    

@login_required(login_url="login")
def delete_product(request,id):
    if request.user.is_superadmin:
        product = Product.objects.get(id=id)
        product.delete()
        return redirect ('store_table',id=1)
    else:
        return redirect('home') 



@login_required(login_url="login")
def add_variation(request):
    if request.user.is_superadmin:
        form = VariationForm()
        if request.method == 'POST':
            form = VariationForm(request.POST)
            if form.is_valid():
                variation = form.save()
                
                variation.save()
                messages.success(request,'New variation added successfully')
                return redirect('store_table',id=2)
        

        else:
            form = VariationForm()
        context = {
            'form' : form,
        }        
        return render (request,'adminpanel/store_table/add_variation.html',context)        
    else:
        return redirect('home')    

@login_required(login_url="login")
def edit_variation(request,id):
    if request.user.is_superadmin:
        variation = Variation.objects.get(id=id)
        if request.method =='POST':
            form = VariationForm(request.POST,instance=variation)
            if form.is_valid():
                form.save()
                return redirect('store_table',id=2)
        else:
            form = VariationForm(instance=variation)
        context = {
            'form' : form,
        }
        return render (request,'adminpanel/store_table/add_variation.html',context)
    else:
        return redirect ('home')

@login_required(login_url="login")
def delete_variaton(request,id):
    if request.user.is_superadmin:
        variation = Variation.objects.get(id=id)
        variation.delete()
        return redirect('store_table',id=2)
    else:
        return redirect ('home')


@login_required(login_url="login")
def order_table(request,id):
    if request.user.is_superadmin:
        orders = Order.objects.filter(is_ordered=True,status='New')
        accepted_orders = Order.objects.filter(is_ordered=True,status='Accepted')
        completed_orders = Order.objects.filter(is_ordered=True,status="Completed")
        cancelled_orders = Order.objects.filter(is_ordered=True,status="Cancelled")
        order_products = OrderProduct.objects.all()
        payments = Payment.objects.all()
        context = {
            'orders' : orders,
            'order_products' : order_products,
            'payments' : payments,
            'accepted_orders' : accepted_orders,
            'completed_orders' : completed_orders,
            'cancelled_orders' : cancelled_orders,
        }

        if id==1:
            return render (request,'adminpanel/order_table/orders.html',context)
        elif id==2:
            return render(request,'adminpanel/order_table/accepted_orders.html',context)
        elif id==3:
            return render(request,'adminpanel/order_table/completed_orders.html',context)
        elif id==4:
            return render(request,'adminpanel/order_table/cancelled_orders.html',context)
        else:
            return render(request,'adminpanel/order_table/payments.html',context)
    else:
        return redirect('home')
    
@login_required(login_url="login")    
def order_accepted(request,order_id):
    if request.user.is_superadmin:
        order = Order.objects.get(id=order_id)
        order.status = 'Accepted'
        order.save()
        return redirect('order_table', id=1)
    else:
        return redirect('home')

@login_required(login_url="login")
def order_completed(request, order_id):
    if request.user.is_superadmin:
        order = Order.objects.get(id=order_id)
        order.status = 'Completed'
        order.save()
        return redirect('order_table', id=2)
    else:
        return redirect('home')


@login_required(login_url="login")
def order_cancelled(request,order_id):
    if request.user.is_superadmin:
        order=Order.objects.get(id=order_id)
        order.status = 'Cancelled'
        order.save()
        return redirect('order_table',id=1 )
    else:
        return render(request,'adminpanel/order_table/order_cancelled.html')

@login_required(login_url="login")
def admin_order_detail(request, order_id):
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
    return render(request,'adminpanel/order_table/admin_order_detail.html',context)

@login_required(login_url="login")
def adminpanel(request):
    if request.user.is_superadmin:
        total_revenue = Order.objects.filter(is_ordered = True).aggregate(sum = Sum('order_total'))['sum']


        total_cost= (total_revenue * .80)
        total_profit = total_revenue - total_cost  
        chart_year = datetime.date.today().year
        chart_month = datetime.date.today().month
     
        #getting daily revenue
        daily_revenue = Order.objects.filter(                     
            created_at__year=chart_year,created_at__month=chart_month
        ).order_by('created_at').annotate(day=TruncMinute('created_at')).values('day').annotate(sum=Sum('order_total')).values('day','sum')

        day=[]
        revenue=[]
        for i in daily_revenue:
            day.append(i['day'].minute)
            revenue.append(int(i['sum']))
        
        userprofile = UserProfile.objects.get(user=request.user)
       
        context = {
            'total_revenue' : total_revenue,
            'total_cost' : total_cost,
            'total_profit' : total_profit,
            'day' : day,
            'revenue' : revenue,
            'userprofile' : userprofile,
        }
        return render (request,'adminpanel/adminpanel.html',context)
    else:
        return redirect('adminlogin')

def variationsearch(request):
    variations=[]
    if 'keywordss' in request.GET:
        keywordss=request.GET['keywordss']
    
        if keywordss:
            variations=Variation.objects.order_by('-created_date').filter(Q(variation_category_icontains=keywordss)|Q(variation_value_icontains=keywordss))
        context={
            'variations':variations,
        }
    return render(request,'adminpanel/store_table/variations.html',context)


def productsearch(request):
    products=[]
    if 'keywords' in request.GET:
        keywords=request.GET['keywords']
    
        if keywords:
            products=Product.objects.order_by('-created_date').filter(Q(product_name__icontains=keywords))
            paginator = Paginator(products,3)
            page = request.GET.get('page')
            #paged_proucts = paginator.get_page(page)

            product_count = products.count()
        else:
            products = Product.objects.all()
            paginator = Paginator(products,9)
            page = request.GET.get('page')
           # paged_proucts = paginator.get_page(page)

            product_count = products.count()
        context={
            'products':products,
            'product_count' : product_count,
        }
        return render(request,'adminpanel/store_table/products.html',context)
    