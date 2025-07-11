from rest_framework.routers import DefaultRouter
from api.views.book_views import BookViewSet

router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')

urlpatterns = router.urls