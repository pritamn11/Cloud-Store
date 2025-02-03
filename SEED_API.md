# In the Django shell, we can create a regular user like this

```
python manage.py shell
```

```
from accounts.models import User
```

```
from your_app_name.models import CustomUser

# Create a regular user
user = User.objects.create_user(
    first_name='John',
    last_name='Doe',
    email='johndoe@example.com',
    password='securepassword123'
)
print(user)
```

```
# Create a superuser
superuser = User.objects.create_superuser(
    first_name='Admin',
    last_name='User',
    email='admin@example.com',
    password='adminpassword123'
)
print(superuser)
```

# API Documentation

## User Registration
**Endpoint:** `http://127.0.0.1:8000/api/auth/register/`

**Request Method:** `POST`

**Request Body:**
```json
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@example.com",
    "password": "securepassword123",
    "password2": "securepassword123",
    "terms_agreement": true
}
```

---

## User Login
**Endpoint:** `http://localhost:8000/api/auth/login/`

**Request Method:** `POST`

**Request Body:**
```json
{
    "email": "johndoe@example.com",
    "password": "securepassword123"
}
```

---

## User Logout
**Endpoint:** `http://localhost:8000/api/auth/logout/`

**Request Method:** `POST`

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
}
```

---

## Password Reset Request
**Endpoint:** `http://localhost:8000/api/auth/password-reset-request/`

**Request Method:** `POST`

**Request Body:**
```json
{
    "email": "johndoe@example.com"
}
```

---

## Password Reset Confirmation
**Endpoint:** `http://localhost:8000/api/auth/password-reset-confirm/<uidb64>/<token>/`

### GET Request
**Response:**
```json
{
    "message": "Credentials validated successfully",
    "data": {
        "token": "<token>",
        "uidb64": "<uidb64>"
    }
}
```

### POST Request
**Request Body:**
```json
{
  "password": "new_password",
  "confirm_password": "new_password"
}

```

## Folder Creation

**Endpoint:** `POST http://localhost:8000/api/folders/create/`

## Request Headers
```
Authorization: Bearer <access_token>
```

## Request Body
To create a new folder:
```json
{
    "name": "FOLDER NAME",
    "size": 1024
}
```

##### Creating a Folder Inside Another Folder
If you want to create a folder within an existing folder:
```json
{
    "name": "My Documents",
    "parent_folder": 1,
    "size": 1024
}
```
- **`parent_folder`**: The ID of the folder where the new folder should be created.

## Folder List

**Endpoint:** `GET http://localhost:8000/api/folders/list/`

**Endpoint:** `GET http://localhost:8000/api/folders/list/?parent_folder=1`

## Request Headers
```
Authorization: Bearer <access_token>
```

## Rename a Folder

**Endpoint:** `PATCH http://localhost:8000/api/folders/`

```json
{
    "name": "New Folder Name"
}
```

## Delete a Folder

**Endpoint:** `DELETE http://localhost:8000/api/folders/<folder_id>/`


---
