## Run project

```bash
docker compose --env-file config/settings/.env.dev up --build
```

Then head to localhost. Thanks to nginx you don't have to use ports.

## Environment

Environment should have at least:

```
SECRET_KEY=change-me
DATABASE_USER=db_user
DATABASE_PASSWORD=123
DATABASE_NAME=db_name
DATABASE_HOST=db_host
DATABASE=postgres
DATABASE_URL=postgres://db_user:123@db_host:5432/db_name
PORT=5000
USE_R2=False
API_KEY=imagga_api_key
API_SECRET=imagga_secret_key

AWS_STORAGE_BUCKET_NAME=bucket_name
AWS_S3_ENDPOINT_URL=https://58c7cbdb377fbe3f750e2b8fa96052eb.r2.cloudflarestorage.com
AWS_S3_ACCESS_KEY_ID=bucket_access_key
AWS_S3_SECRET_ACCESS_KEY=bucket_secret_key

RABBITMQ_DEFAULT_USER=random_user
RABBITMQ_DEFAULT_PASS=secret_pass
CELERY_BROKER_URL=amqp://random_user:secret_pass@rabbitmq//

ALLOWED_HOSTS='[
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
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
-   **Product Description** GET `product/descriptions/<int:pk>/`- Generate description for image

## Other URLs

-   **Admin Site:** `admin/` - Provides access to the Django administration site.
