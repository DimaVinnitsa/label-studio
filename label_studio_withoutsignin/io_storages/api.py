"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import logging
import inspect
import os

from rest_framework import generics
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from drf_yasg import openapi as openapi
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

from core.permissions import (
    BaseRulesPermission,
    IsBusiness,
    get_object_with_permissions,
    all_permissions,
)
from core.utils.common import get_object_with_check_and_log
from core.utils.io import read_yaml
from io_storages.serializers import ImportStorageSerializer, ExportStorageSerializer
from projects.models import Project

logger = logging.getLogger(__name__)


class StorageAPIBasePermission(BaseRulesPermission):
    perm = "projects.change_project"


class ImportStorageListAPI(generics.ListCreateAPIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser)
    permission_required = all_permissions.projects_change
    serializer_class = ImportStorageSerializer

    def get_queryset(self):
        project_pk = self.request.query_params.get("project")
        project = get_object_with_check_and_log(self.request, Project, pk=project_pk)
        self.check_object_permissions(self.request, project)
        ImportStorageClass = self.serializer_class.Meta.model
        return ImportStorageClass.objects.filter(project_id=project.id)


class ImportStorageDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """RUD storage by pk specified in URL"""

    parser_classes = (JSONParser, FormParser, MultiPartParser)
    serializer_class = ImportStorageSerializer
    permission_required = all_permissions.projects_change

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        return super(ImportStorageDetailAPI, self).put(request, *args, **kwargs)


class ExportStorageListAPI(generics.ListCreateAPIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser)
    permission_required = all_permissions.projects_change
    serializer_class = ExportStorageSerializer

    def get_queryset(self):
        project_pk = self.request.query_params.get("project")
        project = get_object_with_check_and_log(self.request, Project, pk=project_pk)
        self.check_object_permissions(self.request, project)
        ImportStorageClass = self.serializer_class.Meta.model
        return ImportStorageClass.objects.filter(project_id=project.id)


class ExportStorageDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """RUD storage by pk specified in URL"""

    parser_classes = (JSONParser, FormParser, MultiPartParser)
    serializer_class = ExportStorageSerializer
    permission_required = all_permissions.projects_change

    @swagger_auto_schema(auto_schema=None)
    def put(self, request, *args, **kwargs):
        return super(ExportStorageDetailAPI, self).put(request, *args, **kwargs)


class ImportStorageSyncAPI(generics.GenericAPIView):

    parser_classes = (JSONParser, FormParser, MultiPartParser)
    permission_required = all_permissions.projects_change
    serializer_class = ImportStorageSerializer

    def get_queryset(self):
        ImportStorageClass = self.serializer_class.Meta.model
        return ImportStorageClass.objects.all()

    def post(self, request, *args, **kwargs):
        storage = self.get_object()
        # check connectivity & access, raise an exception if not satisfied
        storage.validate_connection()
        storage.sync()
        storage.refresh_from_db()
        return Response(self.serializer_class(storage).data)


class StorageValidateAPI(generics.CreateAPIView):
    parser_classes = (JSONParser, FormParser, MultiPartParser)
    permission_classes = (IsBusiness, StorageAPIBasePermission)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        storage = self.serializer_class.Meta.model(**serializer.validated_data)
        storage.validate_connection()
        return Response()


class StorageFormLayoutAPI(generics.RetrieveAPIView):

    parser_classes = (JSONParser, FormParser, MultiPartParser)
    permission_classes = (IsBusiness, StorageAPIBasePermission)
    swagger_schema = None
    storage_type = None

    @swagger_auto_schema(auto_schema=None)
    def get(self, request, *args, **kwargs):
        form_layout_file = os.path.join(
            os.path.dirname(inspect.getfile(self.__class__)), "form_layout.yml"
        )
        if not os.path.exists(form_layout_file):
            raise NotFound(f'"form_layout.yml" is not found for {self.__class__.__name__}')

        form_layout = read_yaml(form_layout_file)
        return Response(form_layout[self.storage_type])


class ImportStorageValidateAPI(StorageValidateAPI):
    serializer_class = ImportStorageSerializer


class ExportStorageValidateAPI(StorageValidateAPI):
    serializer_class = ExportStorageSerializer


class ImportStorageFormLayoutAPI(StorageFormLayoutAPI):
    storage_type = "ImportStorage"


class ExportStorageFormLayoutAPI(StorageFormLayoutAPI):
    storage_type = "ExportStorage"
