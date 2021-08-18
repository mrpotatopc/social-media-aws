from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import TemplateView,DetailView,ListView,View
import time
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy,reverse
from .models import subscription , post , post_image , user_image , post_comment , post_video ,user_name, user_donate_link, user_premium
from django.utils import timezone
from django.shortcuts import redirect
from user_messages import api
from django.contrib.auth.decorators import login_required
#https://www.youtube.com/watch?v=_HbEl-2n5AQ&t=12663s 2:22:06 1:14:41
import stripe

stripe.api_key = "sk_test_51I1haxG0GeyoyF7Bk7xGq95uBSWVLZQBLPFyJsZ0xCp8P6ACnZenN5Mr8BQRHMy9QgejmDhjwvhxfGeMvQ1ksy1N00H3JQ8qAB"


class RedirectToPreviousMixin:

    default_redirect = '/'

    def get(self, request, *args, **kwargs):
        request.session['previous_page'] = request.META.get('HTTP_REFERER', self.default_redirect)
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.session['previous_page']

def HomePageView(request):
    usr = str(request.user)
    if usr != "AnonymousUser":
        myrecent = post.objects.filter(author=request.user)
        mysubs = subscription.objects.filter(subscriber=request.user)
    else:
        myrecent = ""
        mysubs = ""

    subslst = []
    for x in mysubs:
        author = x.author
        subslst.append(author)

    mysubpost = post.objects.filter(author__in=subslst)
    Post = post.objects.order_by('-id')

    context={
        'myrecents':myrecent,
        'mysubposts':mysubpost,
        'posts':Post,

    }
    try:
        return render(request, 'home/home.html',context)
    except ValueError:
        time.sleep(2)
        return render(request, 'home/home.html',context)

def PostDetailView(request,id):
    Post = post.objects.get(id=id)
    Post_image = post_image.objects.filter(post=Post)
    video = post_video.objects.filter(post=Post)
    comment = post_comment.objects.filter(post=Post)
    author = Post.author
    usr = str(request.user)
    if usr != "AnonymousUser":
        if subscription.objects.filter(subscriber=request.user,author=author).exists():
            is_sub = True
            sub = subscription.objects.get(subscriber=request.user,author=author)
            sub_id = sub.id
        else:
            sub_id = 0
            is_sub = False
    else:
        sub_id = 0
        is_sub = False

    context={
        'post':Post,
        'Post_images':Post_image,
        'is_sub':is_sub,
        'sub_id':sub_id,
        'comments':comment,
        'videos':video,

    }
    try:
        return render(request, 'home/post.html',context)
    except ValueError:
        time.sleep(2)
        return redirect(reverse('home:post', args=[Post.id]))


class SubscriptionListView(LoginRequiredMixin,ListView):
    model = subscription
    context_object_name = "subscriptions"
    template_name = "home/subscriptionlist.html"

    def get_queryset(self):
        usr = self.request.user
        return subscription.objects.filter(subscriber=usr)

class SubscribersListView(LoginRequiredMixin,ListView):
    model = subscription
    context_object_name = "subscriptions"
    template_name = "home/subscriberlist.html"

    def get_queryset(self):
        usr = self.request.user
        return subscription.objects.filter(author=usr)

class UsersListView(ListView):
    model = User
    context_object_name = "users"
    template_name = "home/userslist.html"

    def get_queryset(self):
        return User.objects.order_by("-id")

def UserDetailView(request,id):
    u = User.objects.get(id=id)
    Post = post.objects.filter(author=u)


    usr = str(request.user)
    if usr != "AnonymousUser":
        if subscription.objects.filter(subscriber=request.user,author=id).exists():
            is_sub = True
            sub = subscription.objects.get(subscriber=request.user,author=id)
            sub_id = sub.id
        else:
            sub_id = 0
            is_sub = False
    else:
        sub_id = 0
        is_sub = False

    context={
        'User':u,
        'posts':Post,
        'is_sub':is_sub,
        'sub_id':sub_id

    }

    return render(request, 'home/user.html',context)

@login_required
def unsubscribe(request,id):
    query = subscription.objects.get(id=id)
    query.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def subscribe(request,id1):
    usr = request.user
    subscriber = usr
    author = User.objects.get(id=id1)
    sub = subscription(author=author, subscriber=subscriber)
    sub.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class PostDelete(LoginRequiredMixin,RedirectToPreviousMixin,DeleteView):
    model = post
    action = 'delete post'
    template_name = "home/deletepost.html"

class PostCreateView(LoginRequiredMixin,TemplateView):
    template_name = "home/createpost.html"

@login_required()
def createpost(request):
    if request.method == 'POST':
        author = request.user
        title = request.POST['title']
        text = request.POST['text']
        images = request.FILES.getlist('images')
        videos = request.FILES.getlist('videos')
        po = post(author=author, title=title, text=text )

        po.save()

        for image in images:
            photo = post_image(
                post=po,
                image=image,
            )
            photo.save()

        for video in videos:
            video = post_video(
                post=po,
                video=video
            )
            video.save()

        query = subscription.objects.filter(author=author)
        not_txt = str(author) + " added a new post " + '"' + str(title) + '"'
        post_url = "/post/" + str(po.id) + "/"
        for x in query:
            usr = x.subscriber
            usr_id = usr.id
            print(usr,usr_id)
            api.info(usr_id, not_txt ,meta={'url': post_url,})


        return redirect(reverse('home:post', args=[po.id]))

@login_required
def createcomment(request,id):
    if request.method == 'POST':
        author = request.user
        p = post.objects.get(id=id)
        text = request.POST['text']

        c = post_comment(post=p, author=author , text=text)
        c.save()

        return redirect(reverse('home:post', args=[id]))

class UserSettings(TemplateView):
    template_name = "home/settings.html"

@login_required
def editusername(request):
    if request.method == 'POST':
        if user_name.objects.filter(user=request.user).exists():
            old_username = user_name.objects.get()
            old_username.delete()
            new_username = user_name(user=request.user,name=request.POST['username'])
            new_username.save()
        else:
            new_username = user_name(user=request.user,name=request.POST['username'])
            new_username.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
         #mosh strodos mosh na hz

@login_required
def edituserava(request):
    if request.method == 'POST':
        if user_image.objects.filter(user=request.user).exists():
            old_img = user_image.objects.get(user=request.user)
            old_img.delete()
            new_img = user_image(user=request.user,image=request.FILES['profilepic'])
            new_img.save()
        else:
            new_img = user_image(user=request.user,image=request.FILES['profilepic'])
            new_img.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def edituserdonatelink(request):
    if request.method == 'POST':
        if user_donate_link.objects.filter(user=request.user).exists():
            old_link = user_donate_link.objects.get(user=request.user)
            old_linke.delete()
            new_link = user_donate_link(user=request.user,link=request.POST['link'])
            new_link.save()
        else:
            new_link = user_donate_link(user=request.user,link=request.POST['link'])
            new_link.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def edituserpassword(request):
    if request.method == 'POST':
        us = request.user.id
        USER = User.objects.get(id=us)
        USER.set_password(request.POST['password'])
        USER.save()
        return redirect(reverse('account_login'))

def PostEdit(request,id):
    p =  post.objects.get(id=id)
    image = post_image.objects.filter(post=p)
    video = post_video.objects.filter(post=p)
    context={
        'post':p,
        'images':image,
        'videos':video

    }
    return render(request, 'home/postedit.html',context)

def PostEditConfirm(request,id):
    if request.method == 'POST':
        po = post.objects.get(id=id)
        title = request.POST['title']
        text = request.POST['text']
        images = request.FILES.getlist('images')
        videos = request.FILES.getlist('videos')

        po.title = title
        po.text = text
        po.save()

        for image in images:
            photo = post_image(
                post=po,
                image=image,
            )
            photo.save()

        for video in videos:
            video = post_video(
                post=po,
                video=video
            )
            video.save()
        return redirect(reverse('home:post', args=[po.id]))

def deleteimage(request,id):
    query = post_image.objects.get(id=id)
    query.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def deletevideo(request,id):
    query = post_video.objects.get(id=id)
    query.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DonationPage(LoginRequiredMixin,TemplateView):
    template_name = "home/donation.html"

@login_required
def Donate(request):
    if request.method == 'POST':
        amount = float(request.POST['amount'])
        description = request.POST['description']
        user = request.user
        cents = int(amount * 100)



        if user_name.objects.filter(user=user).exists():
            uname = user_name.objects.get(user=user)
            username = uname.name
        else:
            username = user.username


        customer = stripe.Customer.create(
            email = user.email,
            name=username,
            source=request.POST['stripeToken']
        )
        charge = stripe.Charge.create(
            customer=customer,
            amount = cents,
            currency='eur',
            description = description
        )
        return redirect(reverse('home:thanks'))

class thanks(TemplateView):
    template_name = "home/thanks.html"

class GetPremiumPage(TemplateView):
    template_name = "home/getpremium.html"

class alreadyHavePremium(TemplateView):
    template_name = "home/alreadyhavepremium.html"

def GetPremium(request):
    if request.method == "POST":
        amount = 300
        description = "premium account"
        user = request.user

        if user_premium.objects.filter(user=user).exists():
            return redirect(reverse('home:alreadyhavepremium'))
        else:
            pass

        customer = stripe.Customer.create(
            email = user.email,
            name = user.username,
            source = request.POST['stripeToken']
        )
        charge = stripe.Charge.create(
            customer=customer,
            amount=amount,
            currency="eur",
            description=description
        )
        premium = user_premium(user=user)
        premium.save()
        return redirect(reverse('home:settings'))
