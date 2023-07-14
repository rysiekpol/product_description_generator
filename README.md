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

-   **Password Reset:** `user/password/reset/` - Initiates the password reset process.
-   **User Login:** `user/login/` - Handles user login functionality.
-   **Logout:** `user/logout/` - Logs out the currently authenticated user.
-   **User Registration:** `user/register/` - Handles user registration.
-   **User Details:** `user/details/` - Retrieves details of the currently authenticated user.
-   **Certain User Details:** `user/details/<int:pk>/` - Retrieves details of a specific user.
-   **Password Change:** `user/password/change/` - Handles user password change.
-   **Email Verification:** `user/verify-email/` - Verifies user email address.
-   **Resend Email Verification:** `user/resend-email/` - Resends the verification email.
-   **Password Reset Confirm:** `user/password/reset/confirm/<uidb64>/<token>/` - Confirms the password reset request.
-   **Email Confirmation:** `user/confirm-email/<key>/` - Confirms the user's email address.
-   **Account Email Verification Sent:** `user/account-email-verification-sent/` - Notifies the user that the email verification was sent.

### JWT Authentication URLs (if enabled)

-   **Token Verify:** `user/token/verify/` - Verifies the authenticity of an access token.
-   **Token Refresh:** `user/token/refresh/` - Generates a new access token using a refresh token.

## Other URLs

-   **Admin Site:** `admin/` - Provides access to the Django administration site.
