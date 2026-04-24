import email
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Entry,Address,Order,OrderItem,admin
from django.db.models import Sum,FloatField
import uuid,random,string
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.core.mail import send_mail


def entry(request):

    if not request.session.get('admin_logged_in'):
        return redirect('admin_login')

    if request.method == "POST":
        Entry.objects.create(
            name=request.POST['name'],
            description=request.POST['description'],
            price=request.POST['price'],
            image=request.POST['image'],
            size=request.POST['size'],
            flavour=request.POST['flavour'],
            category=request.POST['category']
        )
        return redirect('entry')

    return render(request, 'entry.html')



def product(request):
        product=Entry.objects.all()
        if request.method == "POST":
             name = request.POST.get('name')
             description = request.POST.get('description')
             price = request.POST.get('price')
             image = request.POST.get('image')
             size = request.POST.get('size')
             flavour = request.POST.get('flavour')
             category = request.POST.get('category')

             Entry.objects.create(
                 name=name,
                description=description,
                price=price,
                image=image,
                size=size,
                flavour=flavour,
                category=category 
            )
             return redirect('product') 
        return render(request, "product.html", {'data': product})



def edit(request, product_id):
    product = get_object_or_404(Entry, product_id=product_id)

    if request.method == "POST":
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.image = request.POST['image']
        product.size = request.POST['size']
        product.flavour = request.POST['flavour']
        product.category = request.POST['category']
        product.save()
        return redirect('admin_home')

    return render(request, "edit.html", {'product': product})


def delete(request,id):
    if request.method == "POST":
        id = request.POST['id']
        return render(request,"product.html")
    
    product = Entry.objects.get(product_id=id)
    product.delete()
    return redirect('product')


def index(request):
    popular_products = Entry.objects.filter(category="popular")
    main_products = Entry.objects.filter(category="main")
    beverage_products = Entry.objects.filter(category="beverage")

    return render(request, "index.html", {
        "popular_products": popular_products,
        "main_products": main_products,
        "beverage_products": beverage_products,
    })




def total_price(self):
        return self.product.price * self.quantity


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('checkout')



def checkout(request):

    cart = request.session.get('cart', {})
    cart_items = []


    for product_id, quantity in cart.items():
        product = Entry.objects.get(product_id=product_id)  
        cart_items.append({
            'product': product,
            'quantity': quantity,
        })

    total = sum(item['product'].price * item['quantity'] for item in cart_items)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


def update_quantity(request, cart_id):

    cart = request.session.get('cart', {})
    cart_id = str(cart_id)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))

        if quantity > 0:
            cart[cart_id] = quantity
        else:
            cart.pop(cart_id, None)

        request.session['cart'] = cart

    return redirect('checkout')


def remove_from_cart(request, id):

    cart = request.session.get('cart', {})
    id = str(id)

    if id in cart:
        del cart[id]

    request.session['cart'] = cart

    return redirect('checkout')
    


@login_required
def add_address(request):
    if request.method == "POST":
        Address.objects.create(
            user=request.user,
            full_name=request.POST.get("full_name"),
            phone=request.POST.get("phone"),
            address_line=request.POST.get("address_line"),
            street=request.POST.get("street"),
            city=request.POST.get("city"),
            landmark=request.POST.get("landmark"),
            zip_code=request.POST.get("zip_code"),
        )
        return redirect("payment")

    return render(request, "address.html")

@login_required
def edit_address(request, id):

    address = get_object_or_404(Address, id=id, user=request.user)

    if request.method == "POST":
        address.full_name = request.POST.get("full_name")
        address.phone = request.POST.get("phone")
        address.door_number = request.POST.get("door")
        address.street = request.POST.get("street")
        address.city = request.POST.get("city")
        address.zip_code = request.POST.get("zip")
        address.save()

        return redirect('login')

    return render(request, "edit_address.html", {"address": address})


def register(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        address_type = request.POST.get("address_type", "home")  

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if Address.objects.filter(email=email).exists():
            messages.error(request, "User already exists")
            return redirect("login")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        Address.objects.create(
            user=user,
            email=email,
            password=password,
            full_name=full_name,
            phone=phone,
            address_type=address_type,   # ✅ save it here
            address_line=request.POST.get("address_line"),
            street=request.POST.get("street"),
            city=request.POST.get("city"),
            landmark=request.POST.get("landmark"),
            zip_code=request.POST.get("zip_code")
        )

        messages.success(request, "Registration successful")
        return redirect("login")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if not user:
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid login details")

    return render(request, "login.html")


def admin_login(request):
    if request.method == "POST":
        admin_email = request.POST.get("admin_email")
        password = request.POST.get("password")

        if admin.objects.filter(admin_email=admin_email, password=password).exists():
            print("successful")

            request.session['admin_logged_in'] = True
            request.session['admin_email'] = admin_email

            return redirect("admin_home")   

        else:
            messages.error(request, "Invalid credentials")

    return render(request, "admin_login.html")


def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')


@login_required(login_url='login')
def payment_page(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('checkout')

    items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Entry.objects.get(product_id=int(product_id))
        subtotal = product.price * quantity
        total += subtotal
        items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    selected_type = request.session.get("selected_address_type", "home")
    selected_address = Address.objects.filter(
        user=request.user, address_type=selected_type
    ).first()

    if not selected_address:
        selected_address = Address.objects.filter(user=request.user).order_by('id').first()

    home_address   = Address.objects.filter(user=request.user, address_type="home").first()
    office_address = Address.objects.filter(user=request.user, address_type="office").first()
    other_address  = Address.objects.filter(user=request.user, address_type="other").first()

    context = {
        "items": items,
        "total": total,
        "home_address": home_address,
        "office_address": office_address,
        "other_address": other_address,
        "selected_address": selected_address,
    }
    return render(request, "payment.html", context)


@login_required(login_url='login')
def update_address(request):

    if request.method == "POST":

        address_type = request.POST.get("address_type")

        address, created = Address.objects.get_or_create(
            user=request.user,
            address_type=address_type
        )

        address.phone = request.POST.get("phone")
        address.address_line = request.POST.get("address_line")
        address.street = request.POST.get("street")
        address.city = request.POST.get("city")
        address.landmark = request.POST.get("landmark")
        address.zip_code = request.POST.get("zip_code")

        address.save()

        request.session['selected_address_type'] = address_type

    return redirect("payment_page")



@login_required(login_url='login')
def place_order(request):

    if request.method != "POST":
        return redirect('checkout')

    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('index')

    total = 0
    order_id = "ORD" + ''.join(random.choices(string.digits, k=6))

    order = Order.objects.create(
        user=request.user,
        order_id=order_id,
        total=0
    )

    order_items_text = ""

    for product_id, quantity in cart.items():
        product = Entry.objects.get(product_id=int(product_id))
        subtotal = product.price * quantity
        total += subtotal

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

        order_items_text += f"{product.name} x{quantity} = ₹{subtotal}\n"

    order.total = total
    order.save()

    request.session['cart'] = {}

    user_email = request.user.email
    user_name  = request.user.first_name or request.user.username

    send_mail(
        subject=f"Order Confirmed! ID: {order_id}",
        message=f"Hi {user_name},\n\nYour order has been placed successfully!\n\nOrder ID: {order_id}\n\nItems:\n{order_items_text}\nTotal: ₹{total}\n\nThank you for ordering from FoodieHub!",
        from_email="manasa.srikath.mails@gmail.com",
        recipient_list=[user_email],
        fail_silently=False,
    )

    send_mail(
        subject="New Order Received",
        message=f"New order placed!\n\nOrder ID: {order_id}\nCustomer: {user_name}\nEmail: {user_email}\n\nItems:\n{order_items_text}\nTotal: ₹{total}",
        from_email="manasa.srikath.mails@gmail.com",
        recipient_list=["manasa.srikath.mails@gmail.com"],
        fail_silently=True,
    )

    order = Order.objects.filter(user=request.user).order_by('-created_at').first()

    return render(request, "payment.html", {
        "order": order
    })

@login_required(login_url='login')
def my_orders(request):

    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    for order in orders:
        order.total_quantity = sum(item.quantity for item in order.items.all())

    return render(request, "orders.html", {"orders": orders})


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile_dashboard(request):
    user = request.user
    address = Address.objects.filter(user=user).order_by('id').first()
    password = None

    if request.method == "POST":
        full_name    = request.POST.get("full_name")
        email        = request.POST.get("email")
        phone        = request.POST.get("phone")
        password     = request.POST.get("password")
        address_line = request.POST.get("address_line")
        street       = request.POST.get("street")
        city         = request.POST.get("city")
        landmark     = request.POST.get("landmark")
        zip_code     = request.POST.get("zip_code")
        address_type = request.POST.get("address_type", "home")

        saved_cart = request.session.get('cart', {})

        if User.objects.filter(username=email).exclude(pk=user.pk).exists():
            messages.error(request, "This email is already registered by another user.")
            return redirect("profile_dashboard")

        name_parts = full_name.split(" ", 1)
        user.first_name = name_parts[0]
        user.last_name  = name_parts[1] if len(name_parts) > 1 else ""
        user.email    = email
        user.username = email

        if password:
            user.set_password(password)

        user.save()

        update_session_auth_hash(request, user)
        request.session['cart'] = saved_cart
        request.session['selected_address_type'] = address_type

        if address:
            address.full_name    = full_name
            address.email        = email
            address.phone        = phone
            address.address_line = address_line
            address.street       = street
            address.city         = city
            address.landmark     = landmark
            address.zip_code     = zip_code
            address.address_type = address_type
            address.save()
        else:
            address = Address.objects.create(
                user=user,
                full_name=full_name,
                email=email,
                password=password if password else "",
                phone=phone,
                address_line=address_line,
                street=street,
                city=city,
                landmark=landmark,
                zip_code=zip_code,
                address_type=address_type,
            )

        messages.success(request, "Profile updated successfully!")

        if saved_cart:
            return redirect("payment_page")
        return redirect("profile_dashboard")

    return render(request, "profile_dashboard.html", {
        "user": user,
        "address": address,
    })

@login_required
def order_details(request, order_id):

    order = Order.objects.get(id=order_id, user=request.user)

    items = order.items.all()

    return render(request, "orders.html", {
        "order": order,
        "items": items
    })
    
@login_required 
def cancel_order(request, order_id): 
    order = Order.objects.get(id=order_id, user=request.user) 
    if order.status == "Pending": order.status = "Cancelled" 
    order.save() 
    return redirect("orders")



def admin_home(request):

    popular_products = Entry.objects.filter(category="popular")
    main_products = Entry.objects.filter(category="main")
    beverage_products = Entry.objects.filter(category="beverage")

    context = {
        "popular_products": popular_products,
        "main_products": main_products,
        "beverage_products": beverage_products
    }

    return render(request, "admin_home.html", context)


def admin_dashboard(request):
    orders = Order.objects.all()

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        orders = orders.filter(created_at__date__range=[start_date, end_date])

    total_users = User.objects.count()
    total_orders = Order.objects.count()
    total_products = Entry.objects.count()

    revenue = Order.objects.aggregate(total=Sum('total'))['total'] or 0

    pending_orders = Order.objects.filter(status="Pending").count()
    completed_orders = Order.objects.filter(status="Completed").count()
    cancelled_orders = Order.objects.filter(status="Cancelled").count()

    context = {
        'orders': orders,
        'total_users': total_users,
        'total_orders': total_orders,
        'total_products': total_products,
        'revenue': revenue,

        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
    }

    return render(request, 'admin_dashboard.html', context)

def order_dashboard(request):
    orders = Order.objects.all()

    return render(request, 'order_dashboard.html', {
        'orders': orders
    })

def order_detail(request, id):
    order = Order.objects.get(id=id)

    return render(request, 'order_detail.html', {
        'order': order
    })

def users(request):
    users = User.objects.all()

    return render(request, 'users.html', {
        'users': users
    })

def order_detail(request):

    return render(request, 'order_detail.html')

def about(request):
    return render(request, "about.html")