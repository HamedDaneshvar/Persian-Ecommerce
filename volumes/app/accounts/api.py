from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import serializers
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomUserDetailsSerializer


class UserDetailAPIView(RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            # Handle validation error
            return self.handle_exception(e)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def get_object(self):
        return self.request.user

    def handle_exception(self, exc):
        if isinstance(exc, serializers.ValidationError):
            # Handle validation error response
            return Response(exc.detail, status=status.HTTP_403_FORBIDDEN)

        # For other exceptions, use the default handler
        return super().handle_exception(exc)
