E-commerce web application developed using Python and Django. It provides a platform for users to d purchase products online. The application includes features for user authentication, profile management, cart management, and payment processing.

Technologies Used:

Backend: Python, Django
Frontend: HTML, CSS
Database: PostgreSQL

User Authentication

Login: Navigate to the login page (/) and enter your username and password. Implemented validations for both the UI and server-side.

Signup: Navigate to the signup page (/signup/) and fill in your details to create a new account. Implemented validations for both the UI and server-side.

Home: Users can only navigate to the home or dashboard page if they are authenticated or already logged in.

Dashboard Management:

After successfully logging in, navigate to the home page. The homepage is divided into two parts:

User Profile Management

Product Management



1. User Profile Management
   
   a) User Photo or Icon: Users can upload a profile picture or icon which is displayed on their profile.
   
   b) User Full Name: Displays the user's full name prominently on their profile.
   
   c) View Profile: Users can see their profile details by clicking the "View Profile" link.
   
   d) Edit Profile: Users can update their profile information by clicking the "Edit Profile" link.

   
   e) Cart Items:-Cart Management
   
            Add to Cart: Click on the "Add to Cart" button next to a product to add it to your cart.
   
            View Cart: Click on the "Cart Items" link to view items in your cart.
   
            Remove from Cart: Click on the "Remove" link next to an item in your cart to remove it.
   
            Payment Processing
   
                Payment: Navigate to the payment page from your cart to process your payment.
   
   f) Logout: Click the logout link to end the session and redirect to the login page.


   
 2. Product Management
    
    a) Home Page Body: Display available products listed on the home page. Shows product image, name, price, and an "Add to Cart" button.
    
    b) Add To cart: Clicking on the "Add to Cart" button sends the product ID to the cart and displays a popup confirming that the item has been added.
    



    
