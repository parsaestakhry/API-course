from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category
from .serializers import CategorySerializer
from rest_framework.decorators import renderer_classes
from rest_framework_csv.renderers import CSVRenderer

# Create your views here.


# using decorators we determine the access of the request
@api_view(["GET", "POST"])
# a view to see the items of the menu
def menu_items(request):
    # if the client request is GET
    if request.method == "GET":
        # save all the objects of the model also their foreign keys in a variable called items
        items = MenuItem.objects.select_related("category").all()
        # filtering based on the categories
        category_name = request.query_params.get("category")
        # filtering on price
        to_price = request.query_params.get("to_price")
        search = request.query_params.get("search")
        if search:
            items = items.filter(title__startswith=search)
        # if there's a category name :
        # double underscore because category is related to another model
        if category_name:
            items = items.filter(category__title=category_name)
        # lte less than equal to the value to_price
        if to_price:
            items = items.filter(price__lte=to_price)
            # serialize all the objects of the model passing it to its model serializer and the request
        serialized_item = MenuItemSerializer(
            items, many=True, context={"request": request}
        )
        # return the data of the serialized items
        return Response(serialized_item.data)

    # if the client method is POST
    if request.method == "POST":
        # the data passed into the serializer will be the data of the request that client has sent storing it in a variable
        serialized_item = MenuItemSerializer(data=request.data)
        # if the data is valid it will be saved
        if serialized_item.is_valid(raise_exception=False):
            serialized_item.save()
        # returning the data that has been recieved from a client and a status code that it has been created
        return Response(serialized_item.data, status=201)


@api_view()
def single_item(request, id):
    # another way of getting a single item and exception in the same method
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
