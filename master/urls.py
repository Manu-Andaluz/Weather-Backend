from django.urls import path
from . import views

urlpatterns = [
    path("create-master-password/", views.create_masterkey, name="create_masterkey"),
    path("create-entry/", views.create_entry,name="create-entry"),
    path("retrieve-entries/", views.extract_entries, name="retrieve-entries"),
    path("generate-password/", views.generate_password, name="generate-password"),
    path("delete-entry/",views.delete_entry, name="delete-entry")
]