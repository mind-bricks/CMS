DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'e_cms',
        'USER': 'e_root',
        'PASSWORD': 'XXXX',
        'HOST': 'localhost',
        'PORT': '3306',
        'ATOMIC_REQUESTS': True,
        'OPTIONS': {
            'init_command':
                'SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED'
        }
    },
}

UMS_OAUTH2 = {
    'CLIENT_ID': 'L8GNY78qYX1caGrsGw0mwh70ZSuqSbBtY3013jgX',
    'CLIENT_SECRET':
        'h3uIhoazt4AuRW5yGowcjdKu3nUrvxsJUA0zIosvieRwpGGT8tUxD49KpNor79Ju7oV'
        'jcfVM1uwhDybC8aSJleWwkOh2pqMA2W9JgyZdtnDwKxCKZ1zVdGHP9H3XRFy4',
    'URL_SCHEME': 'http',
    'URL_DOMAIN': 'localhost:8000',
    'LOGIN_PATH': 'oauth2/token/',
    'INTROSPECT_PATH': 'oauth2/introspect/',
}
