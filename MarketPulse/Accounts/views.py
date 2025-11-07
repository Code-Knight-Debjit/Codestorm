from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProductForm, ShopOwnerForm, SignUpForm
from django.contrib.auth.decorators import login_required
from .models import Product, ShopOwner, Consumer
import csv
import json
from .myBERT import ReviewAnalyzer
from google import genai

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shops_detail')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('shop')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def home(request):
    return render(request, 'MarketPulse/index.html')

@login_required
def shops_detail(request):
    if request.method == 'POST':
        form = ShopOwnerForm(request.POST)
        if form.is_valid():
            shop_owner = form.save(commit=False)
            shop_owner.user = request.user
            shop_owner.save()
            return redirect('shop')
    else:
        form = ShopOwnerForm()

    return render(request, 'Accounts/shop_details.html', {'form': form})

@login_required
def shop(request):
    products = Product.objects.filter(shop_owner__user=request.user).all()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.shop_owner = request.user.shopowner
            product.save()
            return redirect('shop')
    else:
        form = ProductForm()
    return render(request, 'MarketPulse/shops.html', {'form': form, 'products': products})


def upload_review_csv(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        comments_json = request.POST.get('comments')

        if comments_json:
            comments = json.loads(comments_json)
            print(f"Product {product_id} → Comments:", comments)

            analyzer = ReviewAnalyzer()
            for comment in comments:
                analyzer.analyze(comment)
        
            summary = analyzer.get_summary()
            print(f"Product {product_id} → Summary:", summary)

            # You can store or process these comments later
            # Example:
            # for comment in comments:
            #     Review.objects.create(product_id=product_id, comment=comment)
        client = genai.Client(api_key="AIzaSyA7eJBsIw_hmuZBicfb5jUGjxCaB2zbiYk")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"Summarize the following reviews: {summary}"
        )
        print(response.text)

        return render(request,"MarketPulse/Report.html",{"report_data": json.dumps(summary), "summary": response.text,})
    return redirect('shop')
