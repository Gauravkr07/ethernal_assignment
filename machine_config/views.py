from rest_framework import viewsets, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics

from machine_config.models import Machine, MachineData
from machine_config.serializer import MachineSerializer, MachineDataSerializer, UserRegistrationSerializer
from machine_config.permission import IsManager, IsSupervisor, IsOperator

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return [permissions.AllowAny()]
        elif self.request.user.groups.filter(name='Supervisor').exists():
            return [IsSupervisor()]
        elif self.request.user.groups.filter(name='Operator').exists():
            return [IsOperator()]
        return [permissions.IsAuthenticated()]

    def partial_update(self, request, *args, **kwargs):
        try:
            response = super().partial_update(request, *args, **kwargs)
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MachineDataViewSet(viewsets.ModelViewSet):
    queryset = MachineData.objects.all()
    serializer_class = MachineDataSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return [permissions.AllowAny()]
        elif self.request.user.groups.filter(name='Supervisor').exists():
            return [IsSupervisor()]
        elif self.request.user.groups.filter(name='Operator').exists():
            return [IsOperator()]
        return [permissions.IsAuthenticated()]

    def partial_update(self, request, *args, **kwargs):
        try:
            response = super().partial_update(request, *args, **kwargs)
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MachineDetailView(generics.RetrieveAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([IsManager | IsSupervisor | IsOperator])
def machine_list(request):
    machines = Machine.objects.all()
    serializer = MachineSerializer(machines, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsManager])
def create_machine(request):
    serializer = MachineSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsManager])
def create_machine_data(request):
    serializer = MachineDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
