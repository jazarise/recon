# Authentication

ReconX uses **JSON Web Tokens (JWT)** for all API authentication.

## Token Lifecycle
1. **Login**: User provides credentials to `/api/v1/auth/token`.
2. **Access Token**: Short-lived (e.g., 15 minutes) token returned.
3. **Refresh Token**: Long-lived token stored securely (e.g., HttpOnly cookie or secure storage) to request new access tokens without re-authenticating.

## Password Storage
ReconX strictly uses **bcrypt** for password hashing. We never store plain-text passwords or use weak algorithms like MD5/SHA1. Password strength is validated upon registration to prevent trivial dictionary attacks.
