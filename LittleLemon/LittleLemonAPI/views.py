from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category
from .serializers import CategorySerializer
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from rest_framework.decorators import renderer_classes
from rest_framework_csv.renderers import CSVRenderer
# Create your views here.


@api_view(["GET", "POST"])
def menu_items(request):
    if request.method == "GET":
        items = MenuItem.objects.select_related("category").all()
        serialized_item = MenuItemSerializer(
            items, many=True, context={"request": request}
        )
        return Response(serialized_item.data)
    if request.method == "POST":
        serialized_item = MenuItemSerializer(data=request.data)
        if serialized_item.is_valid(raise_exception=False):
            serialized_item.save()
        return Response(serialized_item.data, status=201)


@api_view()
def single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemSerializer(item, many=False)
    return Response(serialized_item.data)


@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serialized_category = CategorySerializer(category, many=False)
    return Response(serialized_category.data)


@api_view()
@renderer_classes([CSVRenderer])
def menu(request):
    items = MenuItem.objects.select_related("category").all()
    serialized_item = MenuItemSerializer(items, many=True)
    return Response({"data": serialized_item.data}, template_name="menu-items.html")


@api_view(["GET"])
@renderer_classes([CSVRenderer])
def welcome(request):
    data = "<html><body><h1>Welcome To Little Lemon API Project</h1></body></html>"
    return Response(data)
