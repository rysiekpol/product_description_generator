## Run project

```bash
docker compose --env-file config/settings/.env.dev up --build
```

Then head to localhost. Thanks to nginx you don't have to use ports.

## Environment

Environment should have at least:

```
SECRET_KEY=super-secret-key
DATABASE_USER=user
DATABASE_PASSWORD=123
DATABASE_NAME=psql_db
DATABASE_HOST=db
DATABASE=postgres
DATABASE_URL=postgres://user:123@db:5432/psql_db
ALLOWED_HOSTS='[
    "localhost",
    "127.0.0.1",
    "0.0.0.0"
]'
```

## User URLs

-   **Password Reset:** POST `user/password/reset/` - Initiates the password reset process.
-   **User Login:** POST `user/login/` - Handles user login functionality.
-   **Logout:** POST `user/logout/` - Logs out the currently authenticated user.
-   **User Registration:** POST `user/register/` - Handles user registration.
-   **User Details:** GET/PUT `user/details/` - Retrieves details of the currently authenticated user.
-   **Certain User Details:** GET `user/details/<int:pk>/` - Retrieves details of a specific user.
-   **Password Change:** POST `user/password/change/` - Handles user password change.
-   **Email Verification:** POST `user/verify-email/` - Verifies user email address.
-   **Resend Email Verification:** POST `user/resend-email/` - Resends the verification email.
-   **Password Reset Confirm:** POST `user/password/reset/confirm/<uidb64>/<token>/` - Confirms the password reset request.
-   **Email Confirmation:** POST `user/confirm-email/<key>/` - Confirms the user's email address.

### JWT Authentication URLs (if enabled)

-   **Token Verify:** GET `user/token/verify/` - Verifies the authenticity of an access token.
-   **Token Refresh:** POST `user/token/refresh/` - Generates a new access token using a refresh token.

## Product URLs

-   **Search Product By Name:** GET `product/search/<str:name>` - Retrieve a list of products matching a partial name.
-   **Product Details By ID:** GET/PUT `product/details/<int:pk>/` - Retrieve details of a specific product.
-   **Create a Product:** POST `product/create/` - Create a new product.
-   **All Products** GET `product/details` - Retrieve a list of all products in database with pagination

## Other URLs

-   **Admin Site:** `admin/` - Provides access to the Django administration site.
