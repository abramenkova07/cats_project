from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BreedViewSet, CatViewSet, ScoreViewSet


router = DefaultRouter()
router.register('breeds', BreedViewSet, basename='breeds')
router.register('cats', CatViewSet, basename='cats')
router.register('scores', ScoreViewSet, basename='scores')
router.register(
    'scores',
    ScoreViewSet,
    basename='scores'
)

urlpatterns = [
    path(
        'auth/', include(
            [
                path('', include('djoser.urls')),
                path('', include('djoser.urls.jwt'))
            ]
        )
    ),
    path('', include(router.urls))
]
