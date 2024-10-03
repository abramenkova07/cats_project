from rest_framework import filters


class BreedFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        breed_slug = request.query_params.get('breed')
        if breed_slug:
            queryset = queryset.filter(breed__slug=breed_slug)
        return queryset
