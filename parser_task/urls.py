from rest_framework.routers import SimpleRouter

from parser_task import views

router = SimpleRouter()
router.register('budget', views.BudgetView, basename='budget')

urlpatterns = router.urls
