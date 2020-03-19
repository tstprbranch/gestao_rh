from django.urls import path
from .views import (
    HoraExtraList,
    # HoraExtraEdit,
    # HoraExtraDelete,
    # HoraExtraNovo
)


urlpatterns = [
    path('', HoraExtraList.as_view(), name='list_hora_extra'),
    # path('', HoraExtraEdit.as_view(), name='edit_hora_extra'),
    # path('', HoraExtraDelete.as_view(), name='delete_hora_extra'),
    # path('', HoraExtraNovo.as_view(), name='novo_hora_extra'),
]
