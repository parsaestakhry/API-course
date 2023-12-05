from .models import MenuItem
from .serializers import MenuItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category
from .serializers import CategorySerializer
from rest_framework.decorators import renderer_classes, throttle_classes
from rest_framework_csv.renderers import CSVRenderer
from django.core.paginator import Paginator, EmptyPage
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .throttles import TenCallsPerMinute

# Create your views here.


# using decorators we determine the access of the request
@api_view(["GET", "POST"])
# a view to see the items of the menu
def menu_items(request):
    # if the client request is GET
    if request.method == "GET":
        # save all the objects of the model also their foreign keys in a variable called items
        # filtering based on query parameters
        items = MenuItem.objects.select_related("category").all()
        category_name = request.query_params.get("category")
        to_price = request.query_params.get("to_price")
        search = request.query_params.get("search")
        ordering = request.query_params.get("ordering")
        perpage = request.query_params.get("perpage", default=1)
        page = request.query_params.get("page", default=1)

        # checking the condition if the paramater exists
        # then filter based on the parameter
        if search:
            items = items.filter(title__startswith=search)
        # if there's a category name :
        if category_name:
            items = items.filter(category__title=category_name)
        # lte less than equal to the value to_price
        if to_price:
            items = items.filter(price__lte=to_price)

        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)

            # serialize all the objects of the model passing it to its model serializer and the request
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []

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


class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ["price", "inventory"]
    search_fields = ["title", "category__title"]


@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message": "some secret message"})


@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    return Response({"message": "for managers"})


@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message": "successful"})


@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
    return Response({"message": "successful for logged users only"})


class MenuItemViewSet(viewsets.ModelViewSet):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_throttles(self):
        if self.action == 'create':
            throttle_classes = [UserRateThrottle]
        else:
            throttle_classes = []
        return [throttle() for throttle in throttle_classes]
