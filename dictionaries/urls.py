from rest_framework.routers import SimpleRouter

from dictionaries import views

router = SimpleRouter()
router.register('institution_typs', views.InstitutionTypeView, basename='institution_type_view')
router.register('organization_typs', views.OrganizationTypeView, basename='organization_type_view')
router.register('egrul_statuses', views.EgrulStatusView, basename='egrul_status_view')
router.register('rubpnubp_statuses', views.RubpnubpStatusView, basename='rubpnubp_status_view')
router.register('chapters_bk', views.ChapterBKView, basename='chapter_bk_view')
router.register('industry_specific_typings', views.IndustrySpecificTypingView,
                basename='industry_specific_typing_view')
router.register('budget_levels', views.BudgetLevelView, basename='budget_level_view')

urlpatterns = router.urls
