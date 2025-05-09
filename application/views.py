from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import User, Task, Label
from rest_framework.permissions import IsAuthenticated, AllowAny
from .utils import generate_token

# Create your views here.

class RootView(APIView):
    def get(self, request):
        try:
            return Response({
                "status_code": 200,
                "message": "API Running Successfully!",
            }, status=status.HTTP_200_OK
        )
        except Exception as error:
            return Response({
                    "status_code": 200,
                    "message": "Something went wrong!",
                    "error": error
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class RegisterView(APIView):
    def post(self, request):
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')

            if not all([email, username, password]):
                return Response({
                    'status_code': 400,
                    'message': 'Please enter all fields.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if User.objects.filter(email=email).exists():
                return Response({
                    'status_code': 400,
                    'message': 'Email is already taken.',
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User(
                    username=username,
                    email=email,
                )

                user.set_password(request.data['password'])
                user.save()

                return Response({
                    "status_code": 201,
                    "message": "User Created Successfully!",
                    "data":{
                        "username": username,
                        "email": email
                    }
                }, status=status.HTTP_201_CREATED)
            except Exception as error:
                return Response({
                    "status_code": 200,
                    "message": "Something went wrong while creating user!",
                    "error": error
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as error:
            return Response({
                    "status_code": 500,
                    "message": "Something went wrong!",
                    "error": error
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({
                'status_code': 400,
                'message': 'Enter both email and password.'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({
                'status_code': 404,
                'message': 'Email Not Registered.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if not user.check_password(password):
            return Response({
                'status_code': 401,
                'message': 'Invaild Password.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        try:
            tokens = generate_token(user)
        except Exception as error:
            return Response({
                'status_code': 500,
                'message': f'Something Went Wrong.',
                'error': error
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'status_code': 200,
            'message': 'Login successful.',
            'refresh': tokens['refresh'],
            'access': tokens['access'],
        }, status=status.HTTP_200_OK)

class AddLabelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            name = request.data.get('name')

            if not name:
                return Response({
                    'status_code': 400,
                    'message': 'Please enter Label name.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if Label.objects.filter(name=name).exists():
                return Response({
                    'status_code': 400,
                    'message': 'Label already Exists.',
                }, status=status.HTTP_400_BAD_REQUEST)
            
            label = Label.objects.create(
                owner=request.user,
                name=name,
            )

            return Response({
                'status_code': 201,
                'message': 'Label added successfully.',
                'data': {
                    'id': label.id, # type: ignore
                    'name': label.name,
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({
                'status_code': 500,
                'message': f'Something Went Wrong.',
                'error': error
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetAllLabelsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        labels = Label.objects.filter(owner=request.user)
        labels_data = []

        for label in labels:
            labels_data.append({
                'id': label.id, # type: ignore
                'name': label.name,
                'owner': label.owner.username,
            })

        return Response({
            'status_code': 200,
            'data': labels_data
        }, status=status.HTTP_200_OK)

class DeleteLabelView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            label = Label.objects.get(id=pk, owner=request.user)

            if Task.objects.filter(labels=label).exists():
                return Response({
                    'status_code': 400,
                    'message': 'Label is already assigned to one or more tasks.'
                }, status=status.HTTP_400_BAD_REQUEST)

            label.delete()

            return Response({
                'status_code': 200,
                'message': 'Label deleted successfully.'
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'status_code': 404,
                'message': 'Label not found.'
            }, status=status.HTTP_404_NOT_FOUND)

class EditLabelView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            label = Label.objects.get(id=pk, owner=request.user)
        except:
            return Response({
                'status_code': 404,
                'message': 'Label not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        new_label_name = request.data.get('name')
        
        if not new_label_name:
            return Response({
                'status_code': 400,
                'message': 'Label name is required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        label.name = new_label_name
        label.save()

        return Response({
            'status_code': 200,
            'message': 'Label updated successfully.',
            'data': {
                'id': label.id, # type: ignore
                'name': label.name
            }
        }, status=status.HTTP_200_OK)

class AddTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            title = request.data.get('title')
            description = request.data.get('description')
            labels = request.data.get('labels')

            if not all([title, description, labels]):
                return Response({
                    'status_code': 400,
                    'message': 'Please enter all required fields.'
                }, status=status.HTTP_400_BAD_REQUEST)

            correct_labels = []
            wrong_labels = []

            for label_name in labels:
                try:
                    label = Label.objects.get(name=label_name)
                    # label = Label.objects.get(name=label_name, owner=request.user)
                    correct_labels.append(label)
                except: wrong_labels.append(label_name)

            if wrong_labels:
                return Response({
                    'status_code': 400,
                    'message': "The following labels do not exist.",
                    'error': wrong_labels
                }, status=status.HTTP_400_BAD_REQUEST)

            task = Task.objects.create(
                title=title,
                description=description,
                owner=request.user
            )
            task.labels.set(correct_labels)

            return Response({
                'status_code': 201,
                'message': 'Task added successfully.',
                'data': {
                    'id': task.id, # type: ignore
                    'title': task.title,
                    'description': task.description,
                    'labels': labels
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as error:
            return Response({
                'status_code': 500,
                'message': 'Something Went Wrong.',
                'error': str(error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetAllTasksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(owner=request.user)
        task_data = []

        for task in tasks:
            task_data.append({
                'id': task.id, # type: ignore
                'title': task.title,
                'description': task.description,
                'labels': [label.name for label in task.labels.all()]
            })

        return Response({
            'status_code': 200,
            'data': task_data
        }, status=status.HTTP_200_OK)

class EditTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            task = Task.objects.get(id=pk, owner=request.user)
        except:
            return Response({
                'status_code': 404,
                'message': 'Task not found.'
            }, status=status.HTTP_404_NOT_FOUND)

        title = request.data.get('title')
        description = request.data.get('description')
        labels = request.data.get('labels')

        if not all([title, description, labels]):
            return Response({
                'status_code': 400,
                'message': 'Please enter all fields.'
            }, status=status.HTTP_400_BAD_REQUEST)

        correct_labels = []
        wrong_labels = []

        for label_name in labels:
            try:
                label = Label.objects.get(name=label_name)
                # label = Label.objects.get(name=label_name, owner=request.user)
                correct_labels.append(label)
            except: wrong_labels.append(label_name)

        if wrong_labels:
            return Response({
                'status_code': 400,
                'message': "The following labels do not exist.",
                'error': wrong_labels
            }, status=status.HTTP_400_BAD_REQUEST)

        task.title = title
        task.description = description
        task.save()
        task.labels.set(correct_labels)

        return Response({
            'status_code': 200,
            'message': 'Task updated successfully.',
            'data': {
                'id': task.id, # type: ignore
                'title': task.title,
                'description': task.description,
                'labels': labels
            }
        }, status=status.HTTP_200_OK)

class DeleteTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            task = Task.objects.get(id=pk, owner=request.user)
            task.delete()

            return Response({
                'status_code': 200,
                'message': 'Task deleted successfully.'
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'status_code': 404,
                'message': 'Task not found.'
            }, status=status.HTTP_404_NOT_FOUND)
