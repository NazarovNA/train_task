from rest_framework.routers import SimpleRouter

from dictionaries import views

router = SimpleRouter()
router.register('institution_type_view', views.InstitutionTypeView, basename='institution_type_view')
router.register('organization_type_view', views.OrganizationTypeView, basename='organization_type_view')
router.register('egrul_status_view', views.EgrulStatusView, basename='egrul_status_view')
router.register('rubpnubp_status_view', views.RubpnubpStatusView, basename='rubpnubp_status_view')
router.register('chapter_bk_view', views.ChapterBKView, basename='chapter_bk_view')
router.register('industry_specific_typing_view', views.IndustrySpecificTypingView,
                basename='industry_specific_typing_view')
router.register('budget_level_view', views.BudgetLevelView, basename='budget_level_view')

urlpatterns = router.urls
