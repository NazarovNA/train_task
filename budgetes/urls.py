from rest_framework.routers import SimpleRouter

from budgetes import views

router = SimpleRouter()
router.register('budget', views.BudgetView, basename='budget')

urlpatterns = router.urls
