from django.contrib import messages
from django.contrib.sites import requests
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.permissions import AllowAny

import requests
from django.core.paginator import Paginator,EmptyPage,InvalidPage

from .serializers import *
from .models import *

from .forms import *

# Create your views here.

class RecipeCreateView(generics.ListCreateAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipiesSerializers


    permission_classes = [AllowAny]


class RecipeDetails(generics.RetrieveAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipiesSerializers



class RecipeUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipiesSerializers



class RecipiesDelete(generics.DestroyAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipiesSerializers


class RecipiesSearchViewSet(generics.ListAPIView):
    queryset = Recipes.objects.all()
    serializer_class = RecipiesSerializers

    def get_queryset(self):
        name=self.kwargs.get('Name')
        return Recipes.objects.filter(Name__icontains=name)



# def create_recipe(request):
#     if request.method=='POST':
#         form = RecipesForm(request.POST,request.FILES)
#         if form.is_valid():
#             try:
#                 form.save()
#                 api_url='https://127.0.0.1:8000/create/'
#                 data=form.cleaned_data
#                 print(data)
#                 response= requests.post(api_url,data=data,files={'Recip_img':request.FILES['Recip_img']})
#
#                 if response.status_code == 400:
#                     messages.success(request,'Recpes insertrd successfully')
#
#                 else:
#                     messages.error(request,f'error{response.status_code}')
#
#             except requests.RequestException as e:
#                 messages.error(request,f'Error During API Request {str(e)}')
#
#         else:
#             messages.error(request,'Form is not Valid')
#
#     else:
#         form=RecipesForm()
#         return render(request,'create-recipe.html',{'form':form})


def create_recipe(request):
    if request.method == 'POST':
        form = RecipesForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                api_url = 'http://127.0.0.1:8000/create/'
                data = form.cleaned_data
                print(data)
                response = requests.post(api_url, data=data, files={'Recip_img': request.FILES['Recip_img']})

                if response.status_code == 400:
                    messages.success(request, 'Recipe inserted successfully')
                    return redirect('/')
                else:
                    messages.error(request, f'Error {response.status_code}')
            except requests.RequestException as e:
                messages.error(request, f'Error during Api request {str(e)}')
        else:
            messages.error(request, 'Form is not valid')
            # Return the form with errors
            return render(request, 'create-recipe.html', {'form': form})
    else:
        form = RecipesForm()
    return render(request, 'create-recipe.html', {'form': form})

def update_detail(request,id):
    api_url=f'http://127.0.0.1:8000/details/{id}/'
    response=requests.get(api_url)
    if response.status_code == 200:
        data=response.json()
        ingredients=data['Descriptions'].split('.')
    return render(request,'recipe_update.html',{'recipes':data,'ingredients':ingredients})

def update_recipe(request,id):
    if request.method == 'POST':
        name = request.POST['Name']
        prep_time = request.POST['Prep_time']
        difficulty = request.POST['Difficulty']
        vegetarian = request.POST.get('Vegetarian', 'false')
        if vegetarian == 'true':
            vegetarian=True
        else:
            vegetarian=False

        print('Image Url',request.FILES.get('Recip_img'))
        description= request.POST['Descriptions']

        api_url=f'http://127.0.0.1:8000/update/{id}/'

        data = {

            'Name': name,
            'Prep_time': prep_time,
            'Difficulty':difficulty,
            'vegetarian':vegetarian,
            'Descriptions': description
        }

        files = {'Recip_img': request.FILES.get('Recip_img')}

        response = requests.put(api_url, data=data , files=files)
        if response.status_code == 200:
            messages.success(request,'recipe updated successfully')
            return redirect('/')
        else:
            messages.error(request,f'Error submitting data to the REST API : {response.status_code}')
    return render(request,'recipe_update.html')
#
# def index(request):
#     if request.method == 'POST':
#         search= request.POST['search']
#
#         api_url=f'https://127.0.0.1:8000/search/{search}/'
#
#         try:
#             response = requests.get(api_url)
#
#             print(response.status_code)
#
#             if response.status_code == 200:
#                 data= response.json()
#             else:
#                 data=None
#         except requests.RequestException as e:
#             data=None
#
#         return render(request, 'index.html',{'data':data})
#     else:
#         api_url='https://127.0.0.1:8000/create/'
#
#         try:
#            response= requests.get(api_url)
#
#            if response.status_code == 200:
#                data= response.json()
#                orginal_data=data
#
#                paginator = Paginator(orginal_data,6)
#
#                try:
#                    page=int(request.GET.get('page',1))
#
#                except:
#                    page = 1
#
#                try:
#                    recipes=paginator.page(page)
#
#                except (EmptyPage.InvalidePage):
#                    recipes= Paginator.page(paginator.num_pages)
#
#                context ={
#                    'orginal_data':orginal_data,
#                    'recipes':recipes
#                }
#                return render(request,'index.html',context)
#            else:
#                return render(request,'index.html',{'error_message':f'Erroe:{response.status_code}'})
#         except requests.RequestException as e:
#             return render(request,'index.html',{'eror_message':f'Error:{str(e)}'})
#     return render(request, 'index.html')


def index(request):
    if request.method=='POST':
        search=request.POST['search']
        api_url = f'http://127.0.0.1:8000/search/{search}'
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                return render(request, 'index.html', {'data': data})
            else:
                return render(request, 'index.html', {'error_message': f'Error: {response.status_code}'})
        except requests.RequestException as e:
            return render(request, 'index.html', {'error_message': f'Error: {str(e)}'})
    else:
        api_url = f'http://127.0.0.1:8000/create/'
        try:
            response=requests.get(api_url)
            if response.status_code == 200:
                data=response.json()
                orginal_data=data
                paginator=Paginator(orginal_data,4)
                try:
                    page=request.GET.get('page',1)
                except:
                    page=1
                try:
                    recipes=paginator.page(page)
                except (EmptyPage,InvalidPage):
                    recipes=paginator.page(paginator.num_pages)
                context={
                    'original_data':orginal_data,
                    'recipes':recipes
                }
                return render(request,'index.html',context)
            else:
                return render(request,'index.html',{'error_message':f'Error:{response.status_code}'})
        except requests.RequestException as e:
            return render(request,'index.html',{'error_message':f'Error:{str(e)}'})



def recipe_fetch(request, id):
    api_url = f'http://127.0.0.1:8000/details/{id}/'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        ingredients = data['Descriptions'].split('.')
        return render(request, 'recipe_fetch.html', {'recipes': data, 'ingredients': ingredients})
    return render(request, 'recipe_fetch.html')



def recipe_delete(request,id):
    api_url = f'http://127.0.0.1:8000/delete/{id}/'

    response=requests.delete(api_url)

    if response.status_code == 200:
        print(f'iteam with id{id} has been deleted')

    else:
        print(f'failed to delete iteam. status code{ response.status_code}')

    return redirect('/')





