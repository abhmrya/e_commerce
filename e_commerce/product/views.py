# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required, user_passes_test
# from django.contrib import messages
# from django.http import HttpResponse

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status

# from .models import (
#     Product, Profile, Cart, Sale, Rating,
#     CartItem, Backgroundimg, Specialproduct
# )

# from .forms import ProductForm, Profileform
# from .serializers import ProductSerializer

# from reportlab.lib.pagesizes import A4
# from reportlab.lib import colors
# from reportlab.lib.units import mm
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_RIGHT
# import io


# # ------------------ STAFF DECORATOR ------------------
# def staff_required(view_func):
#     return login_required(user_passes_test(lambda u: u.is_staff)(view_func))


# # ------------------ PROFILE EDIT ------------------
# def profile_edit(request, id):
#     profile = get_object_or_404(Profile, pk=id)
#     form = Profileform(instance=profile)
#     return render(request, 'profile_edit.html', {'form': form, 'profile': profile})


# # ------------------ PRODUCT API EDIT ------------------
# @api_view(['PUT', 'PATCH'])
# def edit_product_api(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     serializer = ProductSerializer(product, data=request.data, partial=True)

#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # ------------------ PRODUCT EDIT PAGE ------------------
# @staff_required
# def edit_product(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     form = ProductForm(instance=product)
#     return render(request, 'edit_product.html', {'form': form, 'product': product})


# # ------------------ DELETE API ------------------
# @api_view(['DELETE'])
# def delete_product_api(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     product.delete()
#     return Response({"detail": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)


# # ------------------ HOME ------------------
# def index(request):
#     return render(request, 'index.html', {
#         'products': Product.objects.all(),
#         'background': Backgroundimg.objects.all(),
#         'specials': Specialproduct.objects.all()
#     })


# # ------------------ DELETE CONFIRM ------------------
# @staff_required
# def delete_product(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     return render(request, 'confirm_delete.html', {'product': product})


# # ------------------ ADD TO CART ------------------
# @login_required
# def add_to_cart(request, product_id):
#     profile, _ = Profile.objects.get_or_create(user=request.user)
#     product = get_object_or_404(Product, id=product_id)

#     cart, _ = Cart.objects.get_or_create(user=profile)

#     cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
#     if not created:
#         cart_item.quantity += 1

#     cart_item.save()
#     cart.update_totals()

#     return redirect('index')


# # ------------------ VIEW CART ------------------
# @login_required
# def view_cart(request):
#     profile, _ = Profile.objects.get_or_create(user=request.user)
#     cart = Cart.objects.filter(user=profile).first()

#     return render(request, 'cart.html', {
#         'cart_items': cart.cartitem_set.select_related('product') if cart else [],
#         'total': cart.total_price if cart else 0
#     })


# # ------------------ REMOVE CART ITEM ------------------
# @login_required
# def remove_from_cart(request, product_id):
#     profile, _ = Profile.objects.get_or_create(user=request.user)
#     cart = Cart.objects.filter(user=profile).first()

#     if cart:
#         item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
#         if item:
#             item.delete()
#             cart.update_totals()

#     return redirect('view_cart')


# # ------------------ PRODUCTS ------------------
# def product_list(request):
#     return render(request, 'product_list.html', {
#         'products': Product.objects.all()
#     })


# def product_detail(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     return render(request, 'product_detail.html', {
#         'product': product,
#         'user': request.user
#     })


# # ------------------ PROFILE ------------------
# def profile_details(request, id):
#     profile = get_object_or_404(Profile, pk=id)
#     return render(request, "profile.html", {"profile": profile})


# # ------------------ ORDER ------------------
# def order_details_view(request, id):
#     profile, _ = Profile.objects.get_or_create(user=request.user)
#     cart = Cart.objects.filter(user=profile).first()

#     if not cart:
#         messages.error(request, "No cart found.")
#         return redirect('index')

#     return render(request, 'order_details.html', {
#         'profile': profile,
#         'cart': cart,
#         'items': cart.cartitem_set.all(),
#     })


# # ------------------ PDF INVOICE ------------------
# @login_required
# def download_invoice(request, id):
#     profile, _ = Profile.objects.get_or_create(user=request.user)
#     cart = Cart.objects.filter(user=profile).first()

#     if not cart:
#         return HttpResponse("No cart found")

#     items = cart.cartitem_set.select_related('product')

#     buffer = io.BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=A4)
#     styles = getSampleStyleSheet()
#     story = []

#     story.append(Paragraph("INVOICE", styles['Title']))
#     story.append(Spacer(1, 10))

#     story.append(Paragraph(f"Name: {profile.user.username}", styles['Normal']))
#     story.append(Paragraph(f"Email: {profile.user.email}", styles['Normal']))
#     story.append(Paragraph(f"Address: {profile.address}", styles['Normal']))
#     story.append(Spacer(1, 10))

#     data = [['Product', 'Qty', 'Price']]

#     for item in items:
#         data.append([
#             item.product.product_name,
#             str(item.quantity),
#             f"{item.product.final_rupees * item.quantity}"
#         ])

#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
#     ]))

#     story.append(table)
#     story.append(Spacer(1, 10))
#     story.append(Paragraph(f"Total: {cart.total_price}", styles['Normal']))

#     doc.build(story)
#     buffer.seek(0)

#     return HttpResponse(buffer, content_type='application/pdf')











from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
# from django.template.loader import get_template
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
# import os
# import tempfile
# from weasyprint import HTML
from .models import (Product,Profile,Cart,Sale,Rating,CartItem,Backgroundimg,Specialproduct,)
from .forms import ProductForm, Profileform
from .serializers import ProductSerializer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
import io


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
    profile, created = Profile.objects.get_or_create(
    user=request.user
)
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
    profile, created = Profile.objects.get_or_create(user=request.user)
    cart = Cart.objects.filter(user=profile).first()

    cart_items = cart.cartitem_set.select_related('product') if cart else []
    total = cart.total_price if cart else 0

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
    })

@login_required
def remove_from_cart(request, product_id):
    profile, created = Profile.objects.get_or_create(
    user=request.user
)
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

from django.shortcuts import get_object_or_404

def profile_details(request, id):
    profile = get_object_or_404(Profile, pk=id)
    return render(request, "profile.html", {"profile": profile})


def order_details_view(request, id):
    profile, created = Profile.objects.get_or_create(user=request.user)
    cart = Cart.objects.filter(user=profile).first()

    if not cart:
        messages.error(request, "No cart found.")
        return redirect('home')

    return render(request, 'order_details.html', {
        'profile':profile,
        'cart': cart,
        'items': cart.cartitem_set.all(),
    })


# @login_required
# def download_invoice(request, id):
#     profile, created = Profile.objects.get_or_create(user=request.user)
#     cart = Cart.objects.filter(user=profile).first()

#     if not cart:
#         return HttpResponse("No cart found")
#     items = cart.cartitem_set.all()
#     template = get_template('invoice.html')
#     html_string = template.render({'cart': cart, 'items': items, 'profile': profile})
#     html = HTML(string=html_string)
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename=invoice_{cart.id}.pdf'
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as output:
#         temp_filename = output.name
#     html.write_pdf(target=temp_filename)
#     with open(temp_filename, 'rb') as f:
#         response.write(f.read())
#     os.remove(temp_filename)
#     return response

@login_required
def download_invoice(request, id):
    profile, created = Profile.objects.get_or_create(user=request.user)
    cart = Cart.objects.filter(user=profile).first()

    if not cart:
        return HttpResponse("No cart found")

    items = cart.cartitem_set.select_related('product').all()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=15*mm, leftMargin=15*mm,
                            topMargin=15*mm, bottomMargin=15*mm)
    styles = getSampleStyleSheet()
    story = []

    # ── Title ──
    title_style = ParagraphStyle('Title', parent=styles['Normal'],
                                  fontSize=24, textColor=colors.HexColor('#1a1a2e'),
                                  fontName='Helvetica-Bold', spaceAfter=4*mm)
    story.append(Paragraph("INVOICE", title_style))
    story.append(Spacer(1, 4*mm))

    # ── Customer Info ──
    info_style = ParagraphStyle('Info', parent=styles['Normal'],
                                 fontSize=9, fontName='Helvetica', spaceAfter=2*mm)
    story.append(Paragraph(f"<b>Name:</b> {profile.user.get_full_name() or profile.user.username}", info_style))
    story.append(Paragraph(f"<b>Email:</b> {profile.user.email}", info_style))
    story.append(Paragraph(f"<b>Address:</b> {profile.address}", info_style))
    story.append(Paragraph(f"<b>Invoice No:</b> INV-{cart.id:05d}", info_style))
    story.append(Spacer(1, 6*mm))

    # ── Items Table ──
    table_data = [['#', 'Product', 'Qty', 'Price', 'Subtotal']]

    for idx, item in enumerate(items, start=1):
        table_data.append([
            str(idx),
            item.product.product_name,
            str(item.quantity),
            f"Rs. {item.product.final_rupees:,}",
            f"Rs. {item.product.final_rupees * item.quantity:,}",
        ])

    table = Table(table_data, colWidths=[10*mm, 80*mm, 20*mm, 35*mm, 35*mm])
    table.setStyle(TableStyle([
        ('BACKGROUND',     (0, 0), (-1, 0),  colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR',      (0, 0), (-1, 0),  colors.white),
        ('FONTNAME',       (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',       (0, 0), (-1, 0),  9),
        ('ALIGN',          (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME',       (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE',       (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ('GRID',           (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
        ('BOTTOMPADDING',  (0, 0), (-1, -1), 5),
        ('TOPPADDING',     (0, 0), (-1, -1), 5),
    ]))
    story.append(table)
    story.append(Spacer(1, 6*mm))

    # ── Total ──
    right_style = ParagraphStyle('Right', parent=styles['Normal'],
                                  fontSize=11, fontName='Helvetica-Bold',
                                  alignment=TA_RIGHT)
    story.append(Paragraph(f"Total: Rs. {cart.total_price:,}", right_style))

    doc.build(story)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice_{cart.id}.pdf'
    return response