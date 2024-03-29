"""demo-events-app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path, re_path

from events.views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("api/", include("api.urls")),
    path("", HomeView.as_view()),
]

urlpatterns += i18n_patterns(
    re_path(r"^events/", include("events.urls")),
)


if settings.DEBUG:
    import debug_toolbar
    from django.views import static

    urlpatterns += [
        re_path(
            r"^media/(?P<path>.*)$",
            static.serve,
            {"document_root": settings.MEDIA_ROOT},
        ),
        re_path(
            r"^static/(?P<path>.*)$",
            static.serve,
            {"document_root": settings.STATIC_ROOT},
        ),
    ]
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
