from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from Keepsake.models import Customer, Product, Order, Review
from django.utils import timezone

#Homepage
def Homepage(request):
    user_name = request.session.get('user_name')
    return render(request, "Homepage.html", {'user_name': user_name})

#Register User and Login
def Register(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        phone_no = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']

        existing_customer = Customer.objects.filter(User_Name=user_name).values()

        if existing_customer.count() == 0:
            new_customer = Customer(
                User_Name=user_name,
                Phone_No=phone_no,
                Email=email,
                Password=password,
                Address=address
            )
            new_customer.save()
            context = {
                'message': "Your account was successfully created"
            }
        else:
            context = {
                'message': "Username " + existing_customer[0]['User_Name'] + " already exists"
            }
    else:
        context = {
            'message': ''
        }
        
    return render(request, 'Profile.html', context)

def Login(request):
    if request.session.get('user_name'):
        return redirect('Homepage')
    return render(request, "Login.html") 

def LoginSubmit(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        password = request.GET.get('password')

        customer = Customer.objects.filter(User_Name=username, Password=password).first()

        if customer:
            request.session['user_name'] = username
            return HttpResponseRedirect(reverse('Homepage') + '?user_name=' + username)
        else:
            return render(request, "Login.html", {'error': 'Invalid User ID or Password'})
    else:
        return render(request, "Login.html")

def Logout(request):
    if 'user_name' in request.session:
        del request.session['user_name']
    return HttpResponseRedirect(reverse('Homepage'))

def Register(request):
    if request.method == 'POST':
        user_name = request.POST['username']
        phone_no = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']

        existing_customer = Customer.objects.filter(User_Name=user_name).exists()

        if not existing_customer:
            new_customer = Customer(
                User_Name=user_name,
                Phone_No=phone_no,
                Email=email,
                Password=password,
                Address=address
            )
            new_customer.save()
            context = {
                'message': "Your account was successfully created"
            }
        else:
            context = {
                'message': "Username " + user_name + " already exists"
            }
    else:
        context = {
            'message': ''
        }
    
    return render(request, 'Profile.html', context)

def UpdateProfile(request):
    if request.method == 'POST':
        user_name = request.session.get('user_name')
        if user_name:
            customer = Customer.objects.get(User_Name=user_name)
            
            customer.Phone_No = request.POST.get('phone', customer.Phone_No)
            customer.Email = request.POST.get('email', customer.Email)
            customer.Address = request.POST.get('address', customer.Address)
            
            customer.save()
            context = {
                'message': 'Profile updated successfully'
            }
            return render(request, 'UpdateProfile.html', context)
        else:
            return HttpResponseForbidden('User not authenticated')
    else:
        user_name = request.session.get('user_name')
        if user_name:
            customer = Customer.objects.get(User_Name=user_name)
            context = {
                'user_name': user_name,
                'customer': customer ,
            }
            return render(request, 'UpdateProfile.html', context)
        else:
            return HttpResponseForbidden('User not authenticated')

def DeleteProfile(request):
    user_name = request.session.get('user_name')
    if user_name:
        try:
            customer = Customer.objects.get(User_Name=user_name)
            customer.delete()
            del request.session['user_name']  
            return redirect('Homepage')  # Redirect to homepage 
        except Customer.DoesNotExist:
            return redirect('Login')  # if customer doesn't exist
    else:
        return redirect('Login')  # if user is not authenticated

#Product
def Catalogue(request):
    user_name = request.session.get('user_name')
    return render(request,"Catalogue.html", {'user_name': user_name})

def Birthday(request):
    user_name = request.session.get('user_name')
    products = Product.objects.filter(Category='Birthday').values()
    return render(request, "Birthday.html", {'products': products,'user_name': user_name})

def Anniversary(request):
    user_name = request.session.get('user_name')
    products = Product.objects.filter(Category='Anniversary').values()
    return render(request, "Anniversary.html", {'products': products,'user_name': user_name})

def Graduation(request):
    user_name = request.session.get('user_name')
    products = Product.objects.filter(Category='Graduation').values()
    return render(request, "Graduation.html", {'products': products,'user_name': user_name})

def AllOrder(request):
    user_name = request.session.get('user_name')
    orders = Order.objects.filter(User_Name=user_name).select_related('Product_Name')
    return render(request, "AllOrder.html", {'orders': orders,'user_name': user_name})

def Update_Order(request, Product_Name):
    user_name = request.session.get('user_name')
    if not user_name:
        return redirect('Login')

    try:
        product = Product.objects.get(Product_Name=Product_Name)
    except Product.DoesNotExist:
        return render(request, "Order.html", {'error': f'Product "{Product_Name}" does not exist.', 'user_name': user_name})

    try:
        customer = Customer.objects.get(User_Name=user_name)
    except Customer.DoesNotExist:
        return render(request, "Order.html", {'error': f'Customer "{user_name}" does not exist.', 'user_name': user_name})

    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        shipping_address = request.POST['shipping_address']
        total_price = quantity * product.Price

        if quantity > product.Stock:
            return render(request, "Order.html", {'product': product, 'user_name': user_name, 'error': 'Not enough stock available.'})

        Order.objects.create(
            Product_Name=product,
            User_Name=customer,
            Quantity=quantity,
            Total_Price=total_price,
            Order_Date=timezone.now(),
            Shipping_Address=shipping_address,
        )

        product.Stock -= quantity
        product.save()

        return redirect('Catalogue')

    return render(request, "Order.html", {'product': product, 'user_name': user_name})

def Delete_Order(request, order_id):
    user_name = request.session.get('user_name')

    if not user_name:
        return redirect('Login')

    try:
        order = Order.objects.get(Order_ID=order_id, User_Name__User_Name=user_name)
    except Order.DoesNotExist:
        return render(request, "Order.html", {'error': f'Order "{order_id}" does not exist for user "{user_name}".', 'user_name': user_name})

    if request.method == 'POST':
        order.Product_Name.Stock += order.Quantity
        order.Product_Name.save()

        order.delete()

        return redirect('AllOrder')

    return render(request, "Order.html", {'order': order, 'user_name': user_name})

#Review
def create_review(request):
    user_name = request.session.get('user_name')
    products = Product.objects.all()
    if request.method == 'POST':
        product_name = request.POST['product_name']
        order_id = request.POST['order_id']
        description = request.POST['description']
        rate = request.POST['rate']
        
        try:
            order = Order.objects.get(pk=order_id)
            product = Product.objects.get(pk=product_name)
            review = Review(Product_Name=product, Order_ID=order, Description=description, Rate=rate)
            review.save()
            return redirect('review_list')
        except Order.DoesNotExist:
            return render(request, 'create_review.html', {
                'products': products,
                'error_message': 'Order ID does not exist.'
            })
    
    return render(request, 'create_review.html', {'products': products, 'user_name': user_name})

def update_review(request, review_id):
    user_name = request.session.get('user_name')
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return HttpResponse("Review does not exist.")
    
    products = Product.objects.all()

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        order_id = request.POST.get('order_id')
        description = request.POST.get('description')
        rate = request.POST.get('rate')

        try:
            product = Product.objects.get(Product_Name=product_name)
            order = Order.objects.get(Order_ID=order_id)
            review.Product_Name = product
            review.Order_ID = order
            review.Description = description
            review.Rate = rate
            review.save()
            return redirect('review_list')
        except Product.DoesNotExist:
            return HttpResponse("Product does not exist.")
        except Order.DoesNotExist:
            return HttpResponse("Order does not exist.")
    return render(request, 'update_review.html', {'review': review, 'products': products, 'user_name': user_name})

def delete_review(request, review_id):
    user_name = request.session.get('user_name')
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return HttpResponse("Review does not exist.")
    
    if request.method == 'POST':
        review.delete()
        return redirect('review_list')
    return render(request, 'delete_review.html', {'review': review, 'user_name': user_name})

def review_list(request):
    user_name = request.session.get('user_name')
    reviews = Review.objects.all()
    return render(request, 'review_list.html', {'reviews': reviews, 'user_name': user_name})