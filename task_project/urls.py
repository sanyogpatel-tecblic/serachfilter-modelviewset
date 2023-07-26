"""
URL configuration for task_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from task_app import views
from rest_framework.routers import DefaultRouter
from task_app.views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product',views.GetAllproduct,name = 'getproducts'),
    path('category',views.AddCategory,name = 'createcategory'),
    path('getcategory',views.GetAllcategory,name = 'getcategory'),
    path('addproduct',views.AddProduct,name = 'createproduct'),
    path('search/',views.Searchproduct,name = 'Searchproduct'),
    path('filter/',views.SearchFilter,name='filter'),
    path('', include(router.urls)),
]
