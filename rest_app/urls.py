from django.urls import path
from .views import *
from .import views

urlpatterns=[

path('create/',RecipeCreateView.as_view(),name="create-recipe"),

path('details/<int:pk>/',RecipeDetails.as_view(),name="details"),
path('update/<int:pk>/',RecipeUpdateView.as_view(),name="update"),
path('delete/<int:pk>/',RecipiesDelete.as_view(),name="delete"),

path('search/<str:Name>/',RecipiesSearchViewSet.as_view(),name="search"),

path('create_recipe/', views.create_recipe, name='create_recipe'),
path('recipe_fetch/<int:id>/', views.recipe_fetch, name='recipe_fetch'),
path('update_recipe/<int:id>/', views.update_recipe, name='update_recipe'),
path('recipe_delete/<int:id>/', views.recipe_delete, name='recipe_delete'),
path('',views.index,name='index'),
path('update_detail/<int:id>/', views.update_detail,name='update_detail')


]