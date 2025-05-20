# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Product,Category
from .serializers import ProductSerializer, CategorySerializer

from django.http import JsonResponse
from django.http import Http404
from django.db.models import Q

def latest_products(request):
    response = JsonResponse({"products": [...]})
    response["Access-Control-Allow-Origin"] = "*"
    return response

class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
class ProductSearchView(APIView):
    def post(self, request):
        try:
            query = request.data.get('query', '').strip()
            if not query:
                return Response({"results": [], "message": "Empty query provided"}, status=status.HTTP_200_OK)
            
            # 查询名称或描述中包含关键词的产品
            products = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
            serializer = ProductSerializer(products, many=True)
            return Response({
                "results": serializer.data,
                "message": f"Found {len(serializer.data)} products",
                "query": query
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "error": f"Search failed: {str(e)}",
                "query": query
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
