from django.urls import path
import application.views as view

urlpatterns = [
    path('health-check/', view.RootView.as_view(), name='health_check'),
    path('register/', view.RegisterView.as_view(), name='register'),
    path('login/', view.LoginView.as_view(), name='login'),
    
    path('add-task/', view.AddTaskView.as_view(), name='add_task'),
    path('tasks/', view.GetAllTasksView.as_view(), name='get_all_tasks'),
    path('edit-task/<int:pk>/edit/', view.EditTaskView.as_view(), name='edit_task'),
    path('delete-task/<int:pk>/delete/', view.DeleteTaskView.as_view(), name='delete_task'),
    
    path('add-label/', view.AddLabelView.as_view(), name='add_label'),
    path('labels/', view.GetAllLabelsView.as_view(), name='get_all_labels'),
    path('edit-label/<int:pk>/edit/', view.EditLabelView.as_view(), name='edit_label'),
    path('delete-label/<int:pk>/delete/', view.DeleteLabelView.as_view(), name='delete_label'),
]
