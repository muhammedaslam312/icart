from django.shortcuts import render,redirect,get_object_or_404
from store.models import Product
from .models import Wishlist,WishlistItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
 
# create your views here.

def _wishlist_id(request):
    wishlist = request.session.session_key
    if not wishlist:
        wishlist = request.session.create()
    return wishlist



def add_wishlist(request,product_id):
    
    product = Product.objects.get(id= product_id) #get the product
    product_variation = []
    
      
    try:    
        wishlist = Wishlist.objects.get(wishlist_id = _wishlist_id(request))

    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(wishlist_id = _wishlist_id(request))
    wishlist.save()

    is_wishlist_item_exists = WishlistItem.objects.filter(product = product, wishlist = wishlist).exists()
    if is_wishlist_item_exists:
        wishlist_item = WishlistItem.objects.filter(product=product,wishlist=wishlist)
        # existing variations
        # current variations
        # item id
        ex_var_list = []
        id = []
        for item in wishlist_item:
            existing_variation = item.variations.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)

        print(ex_var_list)

        if product_variation in ex_var_list:
            # increase wishlist item quantity
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = WishlistItem.objects.get(product=product, id=item_id)
            item.save()
        else:
            item = WishlistItem.objects.create(product=product,wishlist = wishlist)
            # create a new wishlist item 
            if len(product_variation) > 0:   #product variations
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()

    else:
        wishlist_item = WishlistItem.objects.create(
            product=product,
            wishlist = wishlist,
        )
        if len(product_variation) > 0:   #product variations else case
            wishlist_item.variations.clear()
            wishlist_item.variations.add(*product_variation)
        wishlist_item.save()
    return redirect ('wishlist')

def remove_wishlist_item(request,product_id,wishlist_item_id):
    wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
    product = get_object_or_404(Product,id=product_id)
    wishlist_item = WishlistItem.objects.get(product=product,wishlist=wishlist,id=wishlist_item_id)
    wishlist_item.delete()
    return redirect('wishlist')

@login_required(login_url='login')
def wishlist(request,wishlist_items=None):
    try:
       
        wishlist = Wishlist.objects.get(wishlist_id=_wishlist_id(request))
        wishlist_items = WishlistItem.objects.filter(wishlist=wishlist, is_active = True)
       
       
        

    except ObjectDoesNotExist:
        pass        
    context = {
        'wishlist_items':wishlist_items,
    }
    return render (request,('wishlist.html'),context)