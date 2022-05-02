from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from . forms import UserRegisterForm
from django.utils.text import slugify
from django.shortcuts import render, redirect, redirect, get_object_or_404


from .models import Lender
from product.models import Product
from .forms import ProductForm

def become_lender(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            lender = Lender.objects.create(name=user.username, created_by=user)

            return redirect('frontpage')
    else:
        form = UserRegisterForm()

    return render(request, 'lender/become_lender.html', {'form': form})

@login_required
def lender_admin(request):
    lender = request.user.lender
    products = lender.products.all()
    orders = lender.orders.all() 
     
        
    for order in orders:
        order.lender_amount = 0
        order.lender_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.lender == request.user.lender:
                if item.lender_paid:
                    order.lender_paid_amount += item.get_total_price()
                else:
                    order.lender_amount += item.get_total_price()
                    order.fully_paid = False

    return render(request, 'lender/lender_admin.html', {'lender': lender, 'products': products})


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.lender = request.user.lender
            product.slug = slugify(product.title)
            product.save()

            return redirect('lender_admin')
    else:
        form = ProductForm()
    
    return render(request, 'lender/add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    lender = request.user.lender
    product = lender.products.get(pk=pk)

    if request . method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
    

        if form.is_valid():
            form.save()

            return redirect('lender_admin')
    else:
        form = ProductForm(instance=product)
       
        return render(request, 'lender/edit_product.html', {'form': form,  'product': product})

@login_required
def edit_lender(request):
    lender = request.user.lender

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')

        if name:
            lender.created_by.email = email
            lender.created_by.save()

            lender.name = name
            lender.save()

            return redirect('lender_admin')
    
    return render(request, 'lender/edit_lender.html', {'vendor': lender})

def lenders(request):
    lenders = Lender.objects.all()

    return render(request, 'lender/lenders.html', {'lenders': lenders})

def lender(request, lender_id):
    lender = get_object_or_404(Lender, pk=lender_id)

    return render(request, 'lender/lender.html', {'lender': lender})