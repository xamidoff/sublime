from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q

from .utils import CardForAuthenticatedUser, get_cart_data
from .models import Category, Product, Review, Order
from .forms import  LoginForm,  RegistrationForm, ReviewForm, ShippingForm, CustomerForm


class ProductList(ListView):
    model = Product
    extra_context = {
        'title': "Sublime. Bosh sahifa"
    }

    template_name = 'store/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = Product.objects.filter(active=True)
        return products

class ProductListByCategory(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'store/category_product_list.html'

    def get_queryset(self):
        sort_field = self.request.GET.get('sort')
        data = []
        category = Category.objects.get(slug=self.kwargs['slug'])
        subcategories = category.subcategory.all()
        products = Product.objects.filter(category__in=subcategories)
        if sort_field:
            products = products.order_by(sort_field)
        return products

    def get_count(self):
        count = []
        category = Category.objects.get(slug=self.kwargs['slug'])
        subcategories = category.subcategory.all()
        products = Product.objects.filter(category__in=subcategories).count()
        count += products
        return count

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(slug=self.kwargs['slug'])
        context['title'] = category.title
        return context


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = Product.objects.get(slug=self.kwargs['slug'])

        products = Product.objects.filter(quantity__gt=0)
        data = []
        for i in range(4):
            from random import randint
            random_index = randint(0, len(products) - 1)
            product = products[random_index]
            if product not in data:
                data.append(product)
        context['products'] = data
        context['reviews'] = Review.objects.filter(product__slug=self.kwargs['slug'], publish=True)
        context['reviews_count'] = Review.objects.filter(product__slug=self.kwargs['slug'], publish=True).count()
        if self.request.user.is_authenticated:
            context['review_form'] = ReviewForm()
        return context


def login_registration(request):
    context = {
        'login_form': LoginForm(),
        'registration_form': RegistrationForm(),
        'title': "Kirish yoki Ro'yhatdan o'tish"
    }
    return render(request, 'store/login_registration.html', context)

def user_login(request):
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('product_list')
    else:
        messages.error(request, "Parol yoki Login noto'g'ri kiritilgan!")
        return redirect('login_registration')

def user_logout(request):
    logout(request)
    return redirect('product_list')

def register(request):
    form = RegistrationForm(data=request.POST)
    if form.is_valid():
        user = form.save()
        messages.success(request, 'Akkaunt yaratildi!')
    else:
        for error in form.errors:
            messages.error(request, form.errors[error][0])
    return redirect('login_registration')


def safe_review(request, product_slug):
    form = ReviewForm(data=request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.author = request.user
        product = Product.objects.get(slug=product_slug)
        review.product = product
        review.save()
    else:
        messages.error('Sizning sharhingiz saqlanmadi')

    return redirect('product_detail', product_slug)


class ReviewsList(ListView):
    model = Review
    context_object_name = 'reviews'

    def reviews_list(self):
        review = Review.objects.filter(product__slug=self.kwargs['slug'],
                                                   publish=True)
        return review


def contact(request):
    context = {
        'title': "Sublime. Bog'lanish"
    }
    return render(request, 'store/contact.html', context)


class SearchResult(ProductList):

    def get_queryset(self):
        word = self.request.GET.get('q')
        products = Product.objects.filter(
            Q(title__icontains=word) | Q(brand__icontains=word), active=True
        )
        return products


def cart(request):
    cart_info = get_cart_data(request)

    context = {
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'order': cart_info['order'],
        'products': cart_info['products'],
        'title': 'Sublime. Savat'
    }

    return render(request, 'store/cart.html', context)


def to_cart(request, product_id, action):
    if request.user.is_authenticated:
        user_cart = CardForAuthenticatedUser(request, product_id, action)
        return redirect('cart')
    else:
        return redirect('login_registration')

def clear_cart(self):
    clear = CardForAuthenticatedUser.get_cart_info(self)['order']
    clear.delete()
    return redirect('product_list')


def checkout(request):
    cart_info = get_cart_data(request)
    context = {
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'order': cart_info['order'],
        'items': cart_info['products'],
        'title': 'Buyurtmani tasdiqlash',
        'customer_form': CustomerForm(),
        'shipping_form': ShippingForm()
    }
    return render(request, 'store/checkout.html', context)






