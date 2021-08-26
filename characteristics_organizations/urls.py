from rest_framework.routers import SimpleRouter

from characteristics_organizations.views import OrganizationView

router = SimpleRouter()
router.register('organization_view', OrganizationView, basename='organization_view')

urlpatterns = router.urls
