from django.shortcuts import render
from rest_framework import generics
from .serializers import CategoryListSerializer, ProductDetailSerializer, OrderSerializer
from .models import Category, Product, Buyer, Comment, Order
from django.contrib.auth import authenticate, login
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserCreationForm, UpdateUserForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

class CategoryListView(generics.GenericAPIView):
    template_name = 'home.html'
    serializer_class = CategoryListSerializer

    def get(self, request, slug=None):
        category = None
        categories = Category.objects.all()
        products = Product.objects.all()
        if slug:
            category = get_object_or_404(Category, slug=slug)
            products = products.filter(category=category)
        return render(request, self.template_name, {'categories': categories, 'products': products})

    def post(self, request):
        categories = Category.objects.all()
        search = request.POST['search']
        products = Product.objects.filter(name__icontains=search)
        return render(request, self.template_name, {'categories': categories, 'products': products})


class RegisterView(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


# class SearchView(generics.GenericAPIView):
#     template_name = 'home.html'
#
#     def post(self, request):
#         categories = Category.objects.all()
#         search = request.POST['search']
#         products = Product.objects.filter(name__icontains=search)
#         return render(request, self.template_name, {'categories': categories, 'products': products})


class ProductDetailView(generics.GenericAPIView):
    serializer_class = ProductDetailSerializer
    template_name = 'product_detail.html'

    def post(self, request, id, slug):
        product = get_object_or_404(Product, id=id, slug=slug)
        user = request.user
        comment_text = request.POST['comment']
        comment = Comment.objects.create(
            product=product,
            comment=comment_text,
            created_by=user
        )
        return redirect('product_detail', id=id, slug=slug)

    def get(self, request, id, slug):
        product = get_object_or_404(Product, id=id, slug=slug)
        comments = Comment.objects.filter(product=product)
        return render(request, self.template_name, {'product': product, 'comments': comments})


class UpdateUserView(generics.GenericAPIView):
    template_name = 'registration/update_user.html'

    def get(self, request):
        context = {
            'form': UpdateUserForm(instance=request.user),
            'orders': Order.objects.filter(user=request.user, status=3)
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return redirect('user_details')


class OrderView(generics.GenericAPIView):
    template_name = 'order.html'

    def get(self, request):
        orders = Order.objects.filter(Q(user=request.user, status=1) | Q(user=request.user, status=2))
        total = 0
        for order in orders:
            total += order.product.price * order.quantity
        return render(request, self.template_name, {'orders': orders, 'total': total})


class OrderDeleteView(generics.GenericAPIView):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        return redirect('order')


class OrderUpdateView(generics.GenericAPIView):
    serializer_class = OrderSerializer

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        order = get_object_or_404(Order, user=request.user, product=product)
        order.quantity = int(request.data['quantity'])
        order.save()
        return redirect('order')

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        Order.objects.create(user=request.user, product=product)
        return redirect('order')


class OrderDoneView(generics.GenericAPIView):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        for order in orders:
            order.status = 2
            order.save()
        return redirect('order')
