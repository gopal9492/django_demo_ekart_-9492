from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import user_profiles, user_product, user_cart
from cryptography.fernet import Fernet


fernet_key = settings.FERNET_KEY.encode()
key = Fernet(fernet_key)


def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = user_profiles.objects.get(username=username)
            decrypted_password = key.decrypt(user.password.encode()).decode()
            if password == decrypted_password:
                request.session['user_id'] = user.id
                return redirect('home')
            else:
                error_message = "Invalid username/password."
        except user_profiles.DoesNotExist:
            error_message = "Invalid username/password."
        except Exception as e:
            error_message = "Error decrypting password. Please try again."

        return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')


def signup_page(request):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        encrypted_password = key.encrypt(password.encode()).decode()
        mobile = request.POST['mobile']
        profile_image = request.FILES['img']
        gender = request.POST['gender']
        city = request.POST['city']

        if user_profiles.objects.filter(username=username).exists():
            error_message = "Username already exists. Please choose a different username."
            return render(request, 'signup.html', {'error_message': error_message})

        user_profiles.objects.create(
            fullname=fullname, username=username, email=email, password=encrypted_password,
            mobile=mobile, profile_image=profile_image, gender=gender, city=city)
        messages.success(request, "Successfully Details Stored..")
        return redirect('login')

    return render(request, 'signup.html')


def home(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = user_profiles.objects.get(id=user_id)
    except user_profiles.DoesNotExist:
        return redirect('login')

    category = request.GET.get('category', 'all')

    if category != 'all':
        products = user_product.objects.filter(category=category)
    else:
        products = user_product.objects.all()

    message = request.session.pop('message', '')

    context = {
        'products': products,
        'user': user,
        'message': message,
        'category': category,
    }
    return render(request, 'home.html', context)



def user_profile(request):
    user_id = request.session.get('user_id')
    try:
        user = user_profiles.objects.get(id=user_id)
    except user_profiles.DoesNotExist:
        return HttpResponse('User not found')

    return render(request, 'userprofile.html', {'user': user})


def edit_user_details(request):
    user_id = request.session.get('user_id')
    try:
        user = user_profiles.objects.get(id=user_id)
        user.password = key.decrypt(user.password.encode()).decode()
    except user_profiles.DoesNotExist:
        return HttpResponse('User not found')

    if request.method == 'POST':
        user.fullname = request.POST.get('fullname')
        user.email = request.POST.get('email')
        user.mobile = request.POST.get('mobile')
        user.gender = request.POST.get('gender')
        user.city = request.POST.get('city')
        new_password = request.POST.get('password')
        user.password = key.encrypt(new_password.encode()).decode()
        user.save()
        return redirect('user_profile')

    return render(request, 'edit_user_details.html', {'user': user})


def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    messages.success(request, "Successfully Logged Out..")
    return redirect('login')


def forgot_pwd(request):
    if request.method == 'POST':
        username = request.POST['username']
        try:
            user = user_profiles.objects.get(username=username)
            decrypted_password = key.decrypt(user.password.encode()).decode()
            send_password_email(user, decrypted_password)
            messages.success(request, "Successfully sent password to email.")
            return redirect('login')
        except user_profiles.DoesNotExist:
            messages.error(request, "Username does not exist.")
        except Exception as e:
            messages.error(request, "Error decrypting password. Please try again.")

        return redirect('forgotpwd')

    return render(request, 'forgotpwd.html')


def send_password_email(user, password):
    subject = 'Password Recovery'
    message = f'Hello {user.fullname},\n\n Your password is: {key.decrypt(user.password.encode()).decode()}\n\n Thank you!'
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]

    send_mail(subject, message, from_email, to_email, fail_silently=False)


def cart(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = user_profiles.objects.get(id=user_id)
        cart_items = user_cart.objects.filter(user=user)
    except user_profiles.DoesNotExist:
        return HttpResponse('User not found')

    total_price = sum(item.product.price * item.quantity for item in cart_items)
    cart_items_with_totals = [
        {'item': item, 'total': item.product.price * item.quantity}
        for item in cart_items
    ]

    return render(request, 'cart.html', {'cart_items': cart_items_with_totals, 'total_price': total_price})


def add_to_cart(request, product_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = user_profiles.objects.get(id=user_id)
        product = user_product.objects.get(id=product_id)
        cart_item, created = user_cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    except (user_profiles.DoesNotExist, user_product.DoesNotExist):
        return HttpResponse('User or Product not found')

    category = request.GET.get('category', 'all')
    request.session['message'] = "Your item is added to cart"

    return redirect(f'/home?category={category}')


def remove_from_cart(request, cart_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = user_profiles.objects.get(id=user_id)
        cart_item = user_cart.objects.get(id=cart_id, user=user)
        cart_item.delete()
    except (user_profiles.DoesNotExist, user_cart.DoesNotExist):
        return HttpResponse('User or Cart item not found')

    return redirect('cart')


def payment(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    try:
        user = user_profiles.objects.get(id=user_id)
        cart_items = user_cart.objects.filter(user=user)
    except user_profiles.DoesNotExist:
        return HttpResponse('User not found')

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    user_cart.objects.filter(user=user).delete()

    return render(request, 'payment.html', {'total_price': total_price})
