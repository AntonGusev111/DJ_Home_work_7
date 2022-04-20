from rest_framework import response, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer


class DestroyAdv(permissions.BasePermission):
    def destroy(self, request, pk=None):
        if Advertisement.objects.filter(id=request.parser_context['kwargs']['pk']).values()[0][
            'creator_id'] == request.user.id:
            return [IsAuthenticated()]
        else:
            raise ValidationError("it is not you'r adv")
        return response


class AdvertisementViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            if Advertisement.objects.filter(id=self.request.parser_context['kwargs']['pk']).values()[0][
                'creator_id'] == self.request.user.id:
                return [IsAuthenticated()]
            else:
                raise ValidationError("it is not you'r adv")
        if self.action in ['destroy']:
            d = DestroyAdv()
            d.destroy(request=self.request, pk=self.request.parser_context['kwargs']['pk'])
        return []




