from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, exceptions
from rest_framework.response import Response
from projects.permissions import IsRecieverApplicationAcceptReject, IsTeamleadApplicationAcceptReject, IsTeamleadApplicationSend, IsTeamleadOrReadOnly
from projects.serializers import *
from projects.models import Project


class ProjectAPICreateView(generics.CreateAPIView):
    serializer_class = ProjectWriteSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ProjectWriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            instance = Project.objects.get(pk=serializer.data['id'])
            instance.members.add(instance.teamlead.pk)
            instance.save()

            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)


class ProjectAPIListView(generics.ListAPIView):
    serializer_class = ProjectReadListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(approved=True)
    

class ProjectAPIMyListView(generics.ListAPIView):
    serializer_class = ProjectReadDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(members__in=self.request.user.pk)
    

class ProjectAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectWriteSerializer
    permission_classes = [IsAuthenticated, IsTeamleadOrReadOnly]

    def get(self, request, *args, **kwargs):
        if self.kwargs['pk']:
            project = Project.objects.get(pk=self.kwargs['pk'])
            serializer = ProjectReadDetailSerializer(project)
                
            return Response(serializer.data)
    
        return Response([], status=status.HTTP_404_NOT_FOUND)


class VacancyAPICreateView(generics.CreateAPIView):
    serializer_class = VacancyWriteSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = VacancyWriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            project = Project.objects.get(pk=self.kwargs['pk'])

            if self.request.user.pk == project.teamlead.pk:
                project.vacancies.add(serializer.data['id'])
                project.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            else:
                return Response('У вас недостаточно прав!', status=status.HTTP_403_FORBIDDEN)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BranchAPIListView(generics.ListAPIView):
    serializer_class = BranchSerializer
    permission_classes = [IsAuthenticated]
    

class IncomingApplicationAPICreateView(generics.CreateAPIView):
    serializer_class = IncomingApplicationWriteSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = IncomingApplicationWriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            project = Project.objects.get(pk=serializer.data['project'])
            project.incoming_applications.add(serializer.data['id'])
            project.save()

            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)
    

class IncomingApplicationAPIListView(generics.ListAPIView):
    serializer_class = IncomingApplicationReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return IncomingApplication.objects.filter(project__teamlead=self.request.user.pk)
    

class IncomingApplicationAPIAcceptView(generics.DestroyAPIView):
    queryset = IncomingApplication.objects.all()
    serializer_class = IncomingApplicationWriteSerializer
    permission_classes = [IsAuthenticated, IsTeamleadApplicationAcceptReject]

    def destroy(self, request, *args, **kwargs):
        try:
            obj = self.get_object()

            if not Project.objects.filter(pk=obj.project.pk, members__user=obj.user_from):
                vacancy = obj.vacancy
                vacancy.open = False
                vacancy.save()

                member = Member.objects.create(user=obj.user_from, vacancy=vacancy)

                project = obj.project
                project.members.add(member.pk)
                project.vacancies.remove(member.vacancy.pk)
                project.save()

            self.perform_destroy(obj)

        except Http404:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)
    

class IncomingApplicationAPIRejectView(generics.DestroyAPIView):
    queryset = IncomingApplication.objects.all()
    serializer_class = IncomingApplicationWriteSerializer
    permission_classes = [IsAuthenticated, IsTeamleadApplicationAcceptReject]
    

class OutgoingApplicationAPICreateView(generics.CreateAPIView):
    serializer_class = OutgoingApplicationWriteSerializer
    permission_classes = [IsAuthenticated, IsTeamleadApplicationSend]

    def post(self, request, *args, **kwargs):
        serializer = OutgoingApplicationWriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            project = Project.objects.get(pk=serializer.data['project'])
            project.outgoing_applications.add(serializer.data['id'])
            project.save()

            return Response(serializer.data, status=201)
        
        return Response(serializer.errors, status=400)
    

class OutgoingApplicationAPIListView(generics.ListAPIView):
    serializer_class = OutgoingApplicationReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OutgoingApplication.objects.filter(user_to=self.request.user.pk)
    

class OutgoingApplicationAPIAcceptView(generics.DestroyAPIView):
    queryset = OutgoingApplication.objects.all()
    serializer_class = OutgoingApplicationWriteSerializer
    permission_classes = [IsAuthenticated, IsRecieverApplicationAcceptReject]

    def destroy(self, request, *args, **kwargs):
        try:
            obj = self.get_object()

            if not Project.objects.filter(pk=obj.project.pk, members__user=obj.user_to):
                vacancy = obj.vacancy
                vacancy.open = False
                vacancy.save()

                member = Member.objects.create(user=obj.user_to, vacancy=vacancy)

                project = obj.project
                project.members.add(member.pk)
                project.vacancies.remove(member.vacancy.pk)
                project.save()

            self.perform_destroy(obj)

        except Http404:
            pass

        return Response(status=status.HTTP_204_NO_CONTENT)
    

class OutgoingApplicationAPIRejectView(generics.DestroyAPIView):
    queryset = OutgoingApplication.objects.all()
    serializer_class = OutgoingApplicationWriteSerializer
    permission_classes = [IsAuthenticated, IsRecieverApplicationAcceptReject]
    

