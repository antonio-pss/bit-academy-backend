from django_filters import rest_framework as filters
from bit_main.models import User


class UserFilter(filters.FilterSet):
    """
    Filtros para o modelo User.
    """
    email = filters.CharFilter(lookup_expr='icontains')  # Filtra por email com busca parcial
    name = filters.CharFilter(lookup_expr='icontains')  # Filtra por nome com busca parcial
    active = filters.BooleanFilter()  # Filtra por usuários ativos/inativos

    class Meta:
        model = User
        fields = ['email', 'username', 'name', 'xp', 'streak', 'created_at', 'active']  # Campos disponíveis para filtragem