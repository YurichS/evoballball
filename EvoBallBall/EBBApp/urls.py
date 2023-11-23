from django.urls import path, include
from .views import CategoryListView, RegisterView, ProductDetailView, UpdateUserView, OrderView, OrderDeleteView, \
    OrderUpdateView, OrderDoneView

urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('users/details', UpdateUserView.as_view(), name='user_details'),
    path('order/', OrderView.as_view(), name='order'),
    path('order/<int:product_id>/', OrderUpdateView.as_view(), name='update_order'),
    path('order/delete/<int:order_id>/', OrderDeleteView.as_view(), name='delete_order'),
    path('order/done/', OrderDoneView.as_view(), name='done_order'),
    path('users/', include('django.contrib.auth.urls')),
    path('users/register/', RegisterView.as_view(), name='register'),
    path('<int:id>/<slug:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('<slug:slug>/', CategoryListView.as_view(), name='category'),
]
