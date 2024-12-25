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

# need to do migration and connect db to postgresql