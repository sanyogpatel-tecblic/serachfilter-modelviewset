from .models import Product,Category,Book
from .serializer import ProductSerializer,CategorySerializer,BookSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.request import Request 
from fuzzywuzzy import fuzz
from rest_framework.viewsets import ModelViewSet



@api_view(['GET'])
def GetAllcategory(request):
    category = Category.objects.all()
    serializer = CategorySerializer(category, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def AddCategory(request):
    data = request.data
    serializer = CategorySerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response("Category Added", status=201)
    else:
        return Response(serializer.errors, status=400)

@api_view(['POST'])
def AddProduct(request):
    data = request.data
    serializer = ProductSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response("Product Added", status=201)
    else:
        return Response(serializer.errors, status=400)   
        
@api_view(['GET'])
def GetAllproduct(request):
    product = Product.objects.all()
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def Searchproduct(request: Request):
    if request.method == 'GET':
        search = request.query_params.get('product')
        
        words = search.split()
        word_queries = []
        for word in words:
            q = Q(name__icontains=word) | Q(category_id__category__icontains=word)

            fuzzy_q = Q(name__icontains=word) | Q(category_id__category__icontains=word)
            products_with_fuzzy = Product.objects.filter(fuzzy_q)
            for product in products_with_fuzzy:
                if fuzz.partial_ratio(word, product.name.lower()) >= 60:
                    q |= Q(name__iexact=product.name)
                elif fuzz.partial_ratio(word, product.category_id.category.lower()) >= 60:
                    q |= Q(category_id__category__iexact=product.category_id.category)

            word_queries.append(q)

        phrase_query = Q(name__icontains=search) | Q(category_id__category__icontains=search)
        products_with_fuzzy_phrase = Product.objects.filter(phrase_query)
        for product in products_with_fuzzy_phrase:
            if fuzz.partial_ratio(search, product.name.lower()) >= 60:
                phrase_query |= Q(name__iexact=product.name)
            elif fuzz.partial_ratio(search, product.category_id.category.lower()) >= 60:
                phrase_query |= Q(category_id__category__iexact=product.category_id.category)
                
        word_query = Q()
        for query in word_queries:
            word_query |= query
            
        query = word_query | phrase_query

        products = Product.objects.filter(query)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

from django.core.paginator import Paginator,EmptyPage

@api_view(['GET'])
def SearchFilter(request: Request):
    if request.method == 'GET':
        search = request.query_params.get('product')
        price_filter = request.query_params.get('price')
        category_filter = request.query_params.get('category')
        records_per_page = request.query_params.get('records', 5) 
        page_number = request.query_params.get('pageno', 1) 

        query = Q()
        if search:
            query |= Q(name__icontains=search) | Q(category_id__category__icontains=search)

        if price_filter:
            min_price, max_price = map(int, price_filter.split('-'))
            query |= Q(price__gte=min_price, price__lte=max_price)

        if category_filter:
            query &= Q(category_id__category__icontains=category_filter)

        products = Product.objects.filter(query)

        paginator = Paginator(products, records_per_page)
        try:
            paginated_products = paginator.page(page_number)
        except EmptyPage:
            paginated_products = paginator.page(paginator.num_pages)

        serializer = ProductSerializer(paginated_products, many=True)
        return Response(serializer.data)
    

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
