from rest_framework import status, viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as django_filters
from django.db.models import Q

from .models import HouseForSale, HouseForRent, PropertyImage
from .serializers import PropertyImageUploadSerializer, PropertyImageSerializer, HouseForSaleSerializer, HouseForRentSerializer


class HouseForSaleFilter(django_filters.FilterSet):
    """Custom filter for HouseForSale model"""
    
    # Price range filters
    min_price = django_filters.NumberFilter(field_name="selling_cost", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="selling_cost", lookup_expr='lte')
    
    # Location filters
    city = django_filters.CharFilter(field_name="city", lookup_expr='icontains')
    nghood = django_filters.CharFilter(field_name="nghood", lookup_expr='icontains')
    postal_code = django_filters.NumberFilter(field_name="postal_code")
    
    # Property features filters
    min_beds = django_filters.NumberFilter(field_name="beds", lookup_expr='gte')
    max_beds = django_filters.NumberFilter(field_name="beds", lookup_expr='lte')
    min_baths = django_filters.NumberFilter(field_name="baths", lookup_expr='gte')
    max_baths = django_filters.NumberFilter(field_name="baths", lookup_expr='lte')
    
    # Area filters
    min_construccion = django_filters.NumberFilter(field_name="construccion", lookup_expr='gte')
    max_construccion = django_filters.NumberFilter(field_name="construccion", lookup_expr='lte')
    min_superficie = django_filters.NumberFilter(field_name="superficie", lookup_expr='gte')
    max_superficie = django_filters.NumberFilter(field_name="superficie", lookup_expr='lte')
    
    # Boolean filters
    infonavit = django_filters.BooleanFilter(field_name="infonavit")
    patio = django_filters.BooleanFilter(field_name="patio")
    negociable = django_filters.BooleanFilter(field_name="negociable")
    
    # Garage/Cochera filter
    min_cochera = django_filters.NumberFilter(field_name="cochera", lookup_expr='gte')
    max_cochera = django_filters.NumberFilter(field_name="cochera", lookup_expr='lte')
    
    # Minisplits filter
    min_minisplits = django_filters.NumberFilter(field_name="minisplits", lookup_expr='gte')
    max_minisplits = django_filters.NumberFilter(field_name="minisplits", lookup_expr='lte')
    
    # Status filter
    estatus = django_filters.CharFilter(field_name="estatus", lookup_expr='icontains')
    
    # Payment method filter
    metodo_de_pago = django_filters.CharFilter(field_name="metodo_de_pago", lookup_expr='icontains')
    
    # Services filter
    servicios = django_filters.CharFilter(field_name="servicios", lookup_expr='icontains')

    class Meta:
        model = HouseForSale
        fields = {
            'title': ['icontains', 'exact'],
            'street': ['icontains', 'exact'],
            'number': ['exact', 'gte', 'lte'],
            'selling_cost': ['exact', 'gte', 'lte'],
            'beds': ['exact', 'gte', 'lte'],
            'baths': ['exact', 'gte', 'lte'],
            'construccion': ['exact', 'gte', 'lte'],
            'superficie': ['exact', 'gte', 'lte'],
            'cochera': ['exact', 'gte', 'lte'],
            'minisplits': ['exact', 'gte', 'lte'],
            'created_at': ['date', 'date__gte', 'date__lte'],
            'updated_at': ['date', 'date__gte', 'date__lte'],
        }


class HouseForRentFilter(django_filters.FilterSet):
    """Custom filter for HouseForRent model"""
    
    # Price range filters
    min_rent = django_filters.NumberFilter(field_name="rent_cost", lookup_expr='gte')
    max_rent = django_filters.NumberFilter(field_name="rent_cost", lookup_expr='lte')
    
    # Location filters
    city = django_filters.CharFilter(field_name="city", lookup_expr='icontains')
    nghood = django_filters.CharFilter(field_name="nghood", lookup_expr='icontains')
    postal_code = django_filters.NumberFilter(field_name="postal_code")
    
    # Property features filters
    min_bedrooms = django_filters.NumberFilter(field_name="bedrooms", lookup_expr='gte')
    max_bedrooms = django_filters.NumberFilter(field_name="bedrooms", lookup_expr='lte')
    min_bathrooms = django_filters.NumberFilter(field_name="bathrooms", lookup_expr='gte')
    max_bathrooms = django_filters.NumberFilter(field_name="bathrooms", lookup_expr='lte')
    
    # Boolean filters
    garage = django_filters.BooleanFilter(field_name="garage")
    patio = django_filters.BooleanFilter(field_name="patio")
    petfriendly = django_filters.BooleanFilter(field_name="petfriendly")
    
    # Minisplits filter
    min_minisplits = django_filters.NumberFilter(field_name="minisplits", lookup_expr='gte')
    max_minisplits = django_filters.NumberFilter(field_name="minisplits", lookup_expr='lte')
    
    # Services filter
    included_services = django_filters.CharFilter(field_name="included_services", lookup_expr='icontains')

    class Meta:
        model = HouseForRent
        fields = {
            'title': ['icontains', 'exact'],
            'street': ['icontains', 'exact'],
            'number': ['exact', 'gte', 'lte'],
            'rent_cost': ['exact', 'gte', 'lte'],
            'bedrooms': ['exact', 'gte', 'lte'],
            'bathrooms': ['exact', 'gte', 'lte'],
            'minisplits': ['exact', 'gte', 'lte'],
            'created_at': ['date', 'date__gte', 'date__lte'],
            'updated_at': ['date', 'date__gte', 'date__lte'],
        }


class HouseForSaleViewSet(viewsets.ModelViewSet):
    queryset = HouseForSale.objects.all()
    serializer_class = HouseForSaleSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    # Configure filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = HouseForSaleFilter
    
    # Search fields - allows searching across multiple text fields
    search_fields = [
        'title', 'street', 'nghood', 'city', 'comments', 
        'estatus', 'servicios', 'metodo_de_pago'
    ]
    
    # Ordering fields - allows sorting by these fields
    ordering_fields = [
        'selling_cost', 'beds', 'baths', 'construccion', 'superficie',
        'created_at', 'updated_at', 'cochera', 'minisplits'
    ]
    
    # Default ordering
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Optionally restricts the returned houses to a given user,
        by filtering against a `owner` query parameter in the URL.
        """
        queryset = HouseForSale.objects.all()
        owner_id = self.request.query_params.get('owner_id', None)
        if owner_id is not None:
            queryset = queryset.filter(owner__id=owner_id)
        return queryset

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_images(self, request, pk=None):
        """
        Upload multiple images to a HouseForSale
        Endpoint: POST /houses-for-sale/{id}/upload_images/
        """
        house = self.get_object()
        files = request.FILES.getlist("images")  # multiple files

        if not files:
            return Response({"error": "No images provided"}, status=status.HTTP_400_BAD_REQUEST)

        created_images = []
        content_type = ContentType.objects.get_for_model(HouseForSale)

        for img_file in files:
            serializer = PropertyImageUploadSerializer(
                data={
                    "image": img_file,
                    "content_type": "house_for_sale",
                    "object_id": house.id,
                    "is_main": request.data.get("is_main", False),
                    "caption": request.data.get("caption", ""),
                    "order": request.data.get("order", 0),
                },
                context={"request": request},
            )
            serializer.is_valid(raise_exception=True)
            image = serializer.save()
            created_images.append(image)

        return Response(
            PropertyImageSerializer(created_images, many=True, context={"request": request}).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['get'])
    def search_by_location(self, request):
        """
        Custom search endpoint for location-based filtering
        Endpoint: GET /houses-for-sale/search_by_location/?city=...&nghood=...
        """
        city = request.query_params.get('city', None)
        nghood = request.query_params.get('nghood', None)
        postal_code = request.query_params.get('postal_code', None)
        
        queryset = self.get_queryset()
        
        if city:
            queryset = queryset.filter(city__icontains=city)
        if nghood:
            queryset = queryset.filter(nghood__icontains=nghood)
        if postal_code:
            queryset = queryset.filter(postal_code=postal_code)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def price_range(self, request):
        """
        Get houses within a specific price range
        Endpoint: GET /houses-for-sale/price_range/?min_price=...&max_price=...
        """
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        
        queryset = self.get_queryset()
        
        if min_price:
            queryset = queryset.filter(selling_cost__gte=min_price)
        if max_price:
            queryset = queryset.filter(selling_cost__lte=max_price)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class HouseForRentViewSet(viewsets.ModelViewSet):
    queryset = HouseForRent.objects.all()
    serializer_class = HouseForRentSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    
    # Configure filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = HouseForRentFilter
    
    # Search fields
    search_fields = [
        'title', 'street', 'nghood', 'city', 'comments', 
        'included_services'
    ]
    
    # Ordering fields
    ordering_fields = [
        'rent_cost', 'bedrooms', 'bathrooms', 'minisplits',
        'created_at', 'updated_at'
    ]
    
    # Default ordering
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Optionally restricts the returned houses to a given user,
        by filtering against a `owner` query parameter in the URL.
        """
        queryset = HouseForRent.objects.all()
        owner_id = self.request.query_params.get('owner_id', None)
        if owner_id is not None:
            queryset = queryset.filter(owner__id=owner_id)
        return queryset

    @action(detail=False, methods=['get'])
    def search_by_location(self, request):
        """
        Custom search endpoint for location-based filtering
        Endpoint: GET /houses-for-rent/search_by_location/?city=...&nghood=...
        """
        city = request.query_params.get('city', None)
        nghood = request.query_params.get('nghood', None)
        postal_code = request.query_params.get('postal_code', None)
        
        queryset = self.get_queryset()
        
        if city:
            queryset = queryset.filter(city__icontains=city)
        if nghood:
            queryset = queryset.filter(nghood__icontains=nghood)
        if postal_code:
            queryset = queryset.filter(postal_code=postal_code)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def rent_range(self, request):
        """
        Get houses within a specific rent range
        Endpoint: GET /houses-for-rent/rent_range/?min_rent=...&max_rent=...
        """
        min_rent = request.query_params.get('min_rent', None)
        max_rent = request.query_params.get('max_rent', None)
        
        queryset = self.get_queryset()
        
        if min_rent:
            queryset = queryset.filter(rent_cost__gte=min_rent)
        if max_rent:
            queryset = queryset.filter(rent_cost__lte=max_rent)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
