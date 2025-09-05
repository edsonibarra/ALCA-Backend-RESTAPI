from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from api.views import CreateUserView, me
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from owner.views import OwnerViewSet
from property import views
from django.conf.urls.static import static



router = DefaultRouter()
router.register(r'houses-for-sale', views.HouseForSaleViewSet)
router.register(r'owners', OwnerViewSet)
# router.register(r'houses-for-rent', views.HouseForRentViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/register/", CreateUserView.as_view(), name="register"),
    path("api/me/", me, name="me"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
