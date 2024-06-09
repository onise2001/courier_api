from rest_framework.filters import BaseFilterBackend


class MyParcelsFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = queryset.filter(reciever=request.user)
        return queryset
    


class PendingParcelsFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = queryset.filter(status="Pending")
        return queryset