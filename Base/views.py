import os.path
from Recipes.settings import MEDIA_ROOT

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy, resolve

from notifications.signals import notify

from .models import *
from .forms import *
# Create your views here.

def index(request):
    recipes = Recipe.objects.all().order_by('-created')[:4]
    viewed_recipes = [Recipe.objects.get(id=recipe[0]) for recipe in request.session.get('viewed_recipes', [])]
    context = {'recipes':recipes,
               'viewed_recipes':viewed_recipes
               }
    print(viewed_recipes)
    return render(request, 'Base/recipe_list.html', context)

def get_by_type(request, type):
    recipes = Recipe.objects.filter(dish_type=type)
    context = {'recipes':recipes,
               'order_by':type,
               'message':'Here are results for {}'.format(type)}
    if len(recipes) == 0:
        message = 'There are no dishes for this type yet'
        context['message'] = message
    return render(request, 'Base/recipe_list.html', context)

@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(user=request.user)
    context = {'recipes': recipes}
    if len(recipes) == 0:
        message = 'You dont have any personal recipe'
        context = {'recipes': recipes,
                    'message':message}

    return render(request, 'Base/my_recipes.html', context)

def recipe_view(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    try:
        comments = Comment.objects.filter(recipe=recipe)
    except Comment.DoesNotExist:
        comments = []
    if request.user.is_authenticated:
        max_viewed_recipes = 5
        viewed_recipes = request.session.get('viewed_recipes', [])
        viewed_recipe = [recipe.id, recipe.title]

        if viewed_recipe in viewed_recipes:
            viewed_recipes.pop(viewed_recipes.index(viewed_recipe))
        viewed_recipes.insert(0, viewed_recipe)
        viewed_recipes = viewed_recipes[:max_viewed_recipes]

        request.session['viewed_recipes'] = viewed_recipes
    if recipe is not None:
        return render(request, 'Base/recipe_details.html', {'recipe':recipe, 'comments':comments})

@login_required(login_url='')
def create_view(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.user = request.user
            new_user.save()
        return redirect('my_recipes')
    else:
        form = RecipeForm()

    return render(request, 'Base/recipe_create.html', {"form":form})

@login_required
def edit_view(request, pk):
    if request.method == 'POST':
        form = EditRecipeForm(request.POST, instance=get_object_or_404(Recipe, pk=pk))
        if form.is_valid():
            edited = form.save(commit=False)
            edited.user = request.user
            edited.save()
        return redirect('home')
    else:
        form = EditRecipeForm(instance=get_object_or_404(Recipe, pk=pk))

    return render(request, 'Base/recipe_create.html', {'form':form})

@login_required
def delete_view(request, pk):
    obj = get_object_or_404(Recipe, pk=pk)

    ## We should check if this recipe is in recently viewed recipes
    this_recipe = [obj.pk, obj.title]
    viewed_recipes = request.session.get('viewed_recipes', [])
    if request.user == obj.user:
        for i in viewed_recipes:
            if i == this_recipe:
                viewed_recipes.pop(viewed_recipes.index(i))
                break
        obj.delete()
        request.session['viewed_recipes'] = viewed_recipes
    else:
        messages.error(request, 'this post doesnt belong to you')
    return redirect('my_recipes')

def search_results(request):
    if request.method == 'POST':
        url = resolve(request.path_info)
        print(url)
        searched = request.POST.get('search')
        if searched == '':
            recipes = []
        else:
            recipes = Recipe.objects.filter(title__icontains=searched)
        return render(request, 'Base/search-results.html', {'searched':searched,
                                                            'recipes':recipes})
    else:
        return render(request, 'Base/search-results.html', {})

#### User auth section
class MyLogin(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    form_class = AuthForm
    def get_default_redirect_url(self):
        return reverse_lazy('home')



def register_user(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            if form.clean():
                form.save()
                new_user = authenticate(request,
                                        username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'])
                login(request, new_user)
                return redirect('home')
        else:
            messages.error(request, 'Unsuccsessful registration')
    else:
        form = UserRegister()

    return render(request, 'registration/registration.html', {'form':form})
####


## USER PROFILE ######
@login_required
def user_profile(request):
    user = Profile.objects.get(user_id=request.user.pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
        return redirect('profile', request.user.pk)
    else:
        form = ProfileForm()
    return render(request, 'Base/profile.html', {'user':user,
                                                 'form':form})
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()

        return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'Base/Edit_profile.html', {'form':form})

########

## Comment Section
@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            recipe = Recipe.objects.get(pk=pk)

            new_comment = form.save(commit=False)
            new_comment.user = request.user.profile
            new_comment.recipe = recipe
            new_comment.save()

            ## notification
            notific = Notification.objects.create(
                user = Profile.objects.get(user = recipe.user),
                message = f'{request.user.profile} commented on your post',
                post = recipe
            )
            notific.save()
        return redirect('recipe_details', pk)
    else:
        form = CommentForm()
    return render(request, 'Base/create_comment.html', {'form':form})

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():
            form.save()
        return redirect('recipe_details', comment.recipe.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'Base/create_comment.html', {'form':form})

@login_required
def delete_comment(request, pk):

    comment = get_object_or_404(Comment, pk=pk)
    recipe_pk = comment.recipe.pk
    if request.user.profile == comment.user:
        comment.delete()
    else:
        messages.error(request, 'this comment doesnt belong to you')
    return redirect('recipe_details', recipe_pk)


## Notification

@login_required
def recipe_view_for_notification(request, post_pk, notification_pk):
    recipe = Recipe.objects.get(pk=post_pk)
    notificaiton = Notification.objects.get(pk=notification_pk)
    if notificaiton is not None:
        notificaiton.delete()

    try:
        comments = Comment.objects.filter(recipe=recipe)
    except Comment.DoesNotExist:
        comments = []

    if request.user.is_authenticated:
        max_viewed_recipes = 5
        viewed_recipes = request.session.get('viewed_recipes', [])
        viewed_recipe = [recipe.id, recipe.title]

        if viewed_recipe in viewed_recipes:
            viewed_recipes.pop(viewed_recipes.index(viewed_recipe))
        viewed_recipes.insert(0, viewed_recipe)
        viewed_recipes = viewed_recipes[:max_viewed_recipes]

        request.session['viewed_recipes'] = viewed_recipes
    if recipe is not None:
        return render(request, 'Base/recipe_details.html',
                      {'recipe': recipe, 'comments': comments})
