import os
from pathlib import Path
from decouple import config  # Importing config from decouple
from datetime import timedelta
import ldap
from django_auth_ldap.config import LDAPSearch, ActiveDirectoryGroupType

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

# Allowed hosts
ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')
print("Allowed Hosts:", ALLOWED_HOSTS)  # Debugging allowed hosts


# WEB_HOST = config('WEB_HOST')
WEB_HOST = config('WEB_HOST', default='http://172.25.99.93:8000')

# Application definition
INSTALLED_APPS = [
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    'ticket.apps.TicketConfig',
    'connectivity.apps.ConnectivityConfig',
    'hardware.apps.HardwareConfig',
    'productivity.apps.ProductivityConfig',
    'informatix.apps.InformatixConfig',
    'tracker.apps.TrackerConfig',

    'crispy_forms',  # Crispy Forms
    'multiselectfield',
    'bootstrap_datepicker_plus',
    'ckeditor',
    'notifications',
    'select2',
    'simple_history',
    'user_visit',
    'import_export',
    'admin_interface',
    'colorfield',
    'sslserver',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'user_visit.middleware.UserVisitMiddleware',
    'django_auto_logout.middleware.auto_logout',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = False  # Set to True if you have HTTPS set up

INTERNAL_IPS = [
    "127.0.0.1",
]

ROOT_URLCONF = 'django_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_auto_logout.context_processors.auto_logout_client',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_project.wsgi.application'

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
    }
}

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',                  # Full toolbar with all options
        'height': 160,                      # Default height
        'width': '100%',                    # Ensure the editor takes 100% width for responsiveness
        'resize_enabled': True,             # Allow resizing of the editor
        'autoGrow_onStartup': True,         # Enable auto-grow on startup
        'autoGrow_minHeight': 160,          # Minimum height when auto-grow is enabled
        'autoGrow_maxHeight': 600,          # Maximum height when auto-grow is enabled
        'extraPlugins': 'autogrow',         # Add autogrow plugin to automatically adjust the editor's height
        'removePlugins': 'resize',          # Disable resizing handles to avoid conflicts with autoGrow
        'enterMode': 2,                     # Use <p> tags instead of <br> tags for paragraphs
        'shiftEnterMode': 1,                # Use <div> tags when Shift+Enter is pressed
        'toolbarCanCollapse': True,         # Allow collapsing of the toolbar for a cleaner UI
        'toolbarGroups': [                 # Define toolbar groups for better organization
            {'name': 'basicstyles', 'groups': ['basicstyles', 'cleanup']},
            {'name': 'paragraph', 'groups': ['list', 'blocks', 'align', 'indent']},
            {'name': 'links', 'groups': ['links']},
            {'name': 'insert', 'groups': ['insert']},
            {'name': 'styles', 'groups': ['styles']},
            {'name': 'colors', 'groups': ['colors']},
            {'name': 'tools', 'groups': ['tools']}
        ],
        'extraAllowedContent': 'div[*];section[*];article[*]',  # Allow additional HTML elements
        'stylesSet': [
            {'name': 'Responsive Image', 'element': 'img', 'attributes': {'class': 'img-fluid'}},  # Add a custom style for responsive images
        ],
    },
}


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Directory for collectstatic
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Additional static file directory
]

# Media files (User-uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# Other settings...
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_L10N = False
USE_TZ = False

# Session settings
LOGIN_REDIRECT_URL = 'front'  # Redirect after login
LOGIN_URL = 'login'            # URL for login redirection

# Auto Logout settings
AUTO_LOGOUT = {
    'IDLE_TIME': timedelta(minutes=config('AUTO_LOGOUT_IDLE_TIME', cast=int)),
    'WARNING_TIME': timedelta(minutes=config('AUTO_LOGOUT_WARNING_TIME', cast=int)),
    'MESSAGE': 'Oops! Your session has expired. Please log in again to continue..',
    'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
}

# SMTP Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587  # Use STARTTLS
# EMAIL_USE_TLS = True  # Enable STARTTLS
# EMAIL_USE_SSL = False  # Must be False when using TLS
# EMAIL_HOST_USER = 'mr.fahim.ferdous@gmail.com'
# EMAIL_HOST_PASSWORD = 'uqpw owbe zzqa tokm'  # Use your app-specific password



# Bootstrap Configuration for Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Notifications Configuration
NOTIFICATIONS_SOFT_DELETE = True

# LDAP Authentication Settings
AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# LDAP Configuration
AUTH_LDAP_SERVER_URI = config('AUTH_LDAP_SERVER_URI', default='ldap://localhost:389')
AUTH_LDAP_BIND_DN = config('AUTH_LDAP_BIND_DN', default='')
AUTH_LDAP_BIND_PASSWORD = config('LDAP_BIND_PASSWORD', default='')


AUTH_LDAP_USER_SEARCH = LDAPSearch("OU=,DC=,DC=com",
                                   ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)")

AUTH_LDAP_GROUP_SEARCH = LDAPSearch("OU=,DC=,DC=com",
                                    ldap.SCOPE_SUBTREE, "(objectClass=group)")

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_superuser": "CN=,OU=,OU=,DC=,DC=com",
    "is_staff": "CN=, OU=IT,OU=,DC=,DC=com",
    "is_active": (
        "CN=,OU=,OU=,DC=,DC=com",
        "CN=,OU=,OU=,DC=,DC=com"
    ),
}

AUTH_LDAP_GROUP_TYPE = ActiveDirectoryGroupType(name_attr="cn")
AUTH_PROFILE_MODULE = 'users.Profile'
AUTH_LDAP_MIRROR_GROUPS = True

AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "cn",
    "last_name": "sn",
    "email": "mail",
    "username": "sAMAccountName",
}

AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600
AUTH_LDAP_FIND_GROUP_PERMS = True

# Message Tags for Django messages framework
from django.contrib.messages import constants as messages

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
}
