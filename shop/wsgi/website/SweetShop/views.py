from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from .forms import UserForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.conf import settings
from SweetShop.models import Product
from SweetShop.models import Basket
from django.core.mail import send_mail


# thi is used when the user calls the origin domain, if the user logged in previously
# and didnt log out they will be kept logged in, so the broswer checks if they are still authenticated
# if they are not, it redirrects them to the login page, if they are still logged in, it redirects them to
# the index page of the website.
# this method is also used when the customer uses the search bar, it checks if the type is query, if it is, it runs that
def index(request):
    if not request.user.is_authenticated():
        return render(request, 'SweetShop/login.html')
    else:
        allProducts = Product.objects.all()
        query = request.GET.get("q")
        if query:
            allProducts = allProducts.filter(
                Q(name__icontains=query)
            ).distinct()
            return render(request, 'SweetShop/index.html', {
                'AllProducts': allProducts
            })
        else:
            return render(request, 'SweetShop/index.html', {'AllProducts': allProducts})

    return render(request, 'SweetShop/login.html')


# this function is called when the submit button is pressed on the register page. here the form is loaded and saved
# the new registered user instance is saved, they are then logged in.
def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                allProducts = Product.objects.all()
                return render(request, 'SweetShop/index.html',{'AllProducts': allProducts})
    context = {
        "form": form,
    }
    return render(request, 'SweetShop/register.html', context)


# this function is called when the user attemps to log in directly from the login page.
# the username and password they enetered into the text boxes are retrived and are then authenticated to see if they
# match an exisiting account. if they do, the user is logged in and there products are loaded onto the index page.
# if there are any errors during this they are redirected back to the login page.
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                allProducts = Product.objects.all()
                return render(request, 'SweetShop/index.html', {'AllProducts': allProducts})
            else:
                return render(request, 'SweetShop/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'SweetShop/login.html', {'error_message': 'Invalid login'})
    return render(request, 'SweetShop/login.html')


# this method is called when the user clicks on the view product's button on the top navigation menu once logged in.
# if successful all the product items are loaded and displayed.
# if this url is entered manually without a user logging in, this method checks if a there is a user logged in so that
# if the user is not logged in they cannot gain accesss
def products(request):
    if not request.user.is_authenticated():
        return render(request, 'SweetShop/login.html')
    else:
        allProducts = Product.objects.all()
        return render(request, 'SweetShop/index.html', {'AllProducts': allProducts})

# this is the method called when the user is browsing through the products on the index page, it is ran when they click
# the image of the item or the view details button of the product they want to view.
# if successful it displays the page displaying that particular
def detail(request, product_id):
    if not request.user.is_authenticated():
        return render(request, 'SweetShop/login.html')
    else:
        user = request.user
        product = get_object_or_404(Product, pk=product_id)
        return render(request, 'SweetShop/details.html', {'Product': product, 'user': user})


# this is the method that is run if the user clicks on the basket button on thenavigation menu.
# it gets the current user that is logged in, filters the objects that exist in Basket the that user id and passes
# displays them in the basket.html
def basket(request):
    if not request.user.is_authenticated():
        return render(request, 'SweetShop/login.html')
    else:
        user = request.user
        realuser = User.objects.filter(id=user.id)
        basketprods = Basket.objects.filter(userID=realuser)
        return render(request, 'SweetShop/basket.html', {'allProducts': basketprods})


# this is the method  called to add prodcuts to the basket. it gets the Product id of the product the user selected and
# also the quantitiy the entered from the ajax. from here  the user instance and selected product instance is loaded and
# these are passed to a Basket instance with the quantity the user entereed and this is saved to the database.
def addtobasket(request):
    if request.method == 'POST' and request.is_ajax():
        pID = request.POST['pro']
        prodquant = request.POST['quant']
        current_user = request.user
        prod = Product.objects.get(id=pID)
        pro = User.objects.get(id=current_user.id)
        bas = Basket(userID=pro, productID=prod, quantity=prodquant)
        bas.save()
        return render(request, 'SweetShop/details.html', {'Product': prod})


# this is the method called to delete an item from the basket. it takes the basketid that is given from the ajax request
# it takes the basketID and filters from the basket instance the object that exist with that id. when found it is
# deleted
def delete_item(request):
    if not request.user.is_authenticated():
        return render(request, 'SweetShop/login.html')
    else:
        if request.method == 'POST' and request.is_ajax():
            basketID = request.POST['bask']
            todel = Basket.objects.get(pk=basketID)
            todel.delete()
            user = request.user
            realuser = User.objects.filter(id=user.id)
            basketprods = Basket.objects.filter(userID=realuser)
            return render(request, 'SweetShop/basket.html', {'allProducts': basketprods})


# this is the method called from the ajax request triggered when a user, changes the quantity value of a item in their
# order, passed to this method is the BasketID and the new quantity entered by the user, a Basket instance is called
# that gets the object of the recieved BasketID, the quantity  of this object is reassigned to the new quantity and
# the changes are saved to the database.
def quantity_update(request):
    if not request.user.is_authenticated():
        return render(request, 'SweetShop/login.html')
    else:
        if request.method == 'POST' and request.is_ajax():
            basketID = request.POST['bask']
            prodquant = request.POST['quant']
            todel = Basket.objects.get(pk=basketID)
            todel.quantity = prodquant
            todel.save()
            user = request.user
            realuser = User.objects.filter(id=user.id)
            basketprods = Basket.objects.filter(userID=realuser)
            return render(request, 'SweetShop/basket.html', {'allProducts': basketprods})


# this is the checkout method called when a the checkout button is clicked on the baskset page, when this is called
# the current logged user is loaded and all of the basket objects which are assosiated with this user are deleted.
# the email of this user is received and then and email is sent to the users email giving them a confirmation of a
# successful checkout.
def checkout(request):
    if not request.user.is_authenticated():
        return render(request, 'SweetShop/login.html')
    else:
        if request.method == 'POST' and request.is_ajax():
            user = request.user
            BasketItems = Basket.objects.filter(userID=user.id)
            message = "Order details : \n"
            for items in BasketItems:
                currentmessage = "\n" + " Product: " + items.productID.name + ", Price: " + items.productID.price+","
                currentmessage = currentmessage + " Quantity: " + items.quantity + "."
                message = message + currentmessage

            for item in BasketItems:
                item.delete()

            realuser = User.objects.filter(id=user.id)
            basketprods = Basket.objects.filter(userID=realuser)
            emailuser = User.objects.get(id=user.id)
            email = emailuser.email
            try:
                send_mail(
                    'The Sweet Tooth Order Complete',
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                   )
                message = "Order Complete!"
                return render(request, 'SweetShop/basket.html', {'allProducts': basketprods,
                                                                 'message': message})
            except:
                return render(request, 'SweetShop/basket.html', {'allProducts': basketprods})


# this is the method which is used to logout the user.
def logout_user(request):
    if not request.user.is_authenticated():
        return render(request, 'SweetShop/login.html')
    else:
        logout(request)
        form = UserForm(request.POST or None)
        context = {
            "form": form,
        }
        return render(request, 'SweetShop/login.html', context)