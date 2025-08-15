from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.template.loader import get_template
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
import os
import tempfile
from weasyprint import HTML
from .models import (Product,Profile,Cart,Sale,Rating,CartItem,Backgroundimg,Specialproduct,)
from .forms import ProductForm, Profileform
from .serializers import ProductSerializer


def staff_required(view_func):
    return login_required(user_passes_test(lambda u: u.is_staff)(view_func))


def profile_edit(request, id):
    profile = get_object_or_404(Profile, pk=id)
    form = Profileform(instance=profile)
    return render(request, 'profile_edit.html', {'form': form, 'profile': profile})


@api_view(['PUT', 'PATCH'])
def edit_product_api(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    serializer = ProductSerializer(product, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        print("Validation errors:", serializer.errors)  # <-- add this to debug
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@staff_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form,'product': product})

@api_view(['DELETE'])
def delete_product_api(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    product.delete()
    print("delete api run")
    return Response({"detail": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)


def index(request):
    background = Backgroundimg.objects.all()
    products = Product.objects.all()
    specials=Specialproduct.objects.all()
    return render(request, 'index.html', {'products': products,'background':background,'specials':specials})



@staff_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # if request.method == "POST":
    #     product.delete()
    #     return redirect('index')
    return render(request, 'confirm_delete.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    profile = Profile.objects.get(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=profile)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    cart.update_totals()

    return redirect('index')

@login_required
def view_cart(request):
    profile = Profile.objects.get(user=request.user)
    cart = Cart.objects.filter(user=profile).first()

    cart_items = cart.cartitem_set.select_related('product') if cart else []
    total = cart.total_price if cart else 0

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
    })

@login_required
def remove_from_cart(request, product_id):
    profile = Profile.objects.get(user=request.user)
    cart = Cart.objects.filter(user=profile).first()
    if cart:
        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if cart_item:
            cart_item.delete()
            cart.update_totals()
    return redirect('view_cart')

# product/views.py
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product,'user': request.user})

def profile_details(request, id):
    profile = Profile.objects.get(pk=id)
    return render(request, 'profile.html', {'profile': profile})



def order_details_view(request, id):
    profile = get_object_or_404(Profile, user=request.user)
    cart = Cart.objects.filter(user=profile).first()

    if not cart:
        messages.error(request, "No cart found.")
        return redirect('home')

    return render(request, 'order_details.html', {
        'profile':profile,
        'cart': cart,
        'items': cart.cartitem_set.all(),
    })


@login_required
def download_invoice(request, id):
    profile = get_object_or_404(Profile, user=request.user)
    cart = Cart.objects.filter(user=profile).first()
    items = cart.cartitem_set.all()
    template = get_template('invoice.html')
    html_string = template.render({'cart': cart, 'items': items, 'profile': profile})
    html = HTML(string=html_string)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice_{cart.id}.pdf'
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as output:
        temp_filename = output.name
    html.write_pdf(target=temp_filename)
    with open(temp_filename, 'rb') as f:
        response.write(f.read())
    os.remove(temp_filename)
    return response