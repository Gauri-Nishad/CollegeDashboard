from college_project_api.models import User

def role_name_processor(request):
    # Check if the user is logged in and session contains role information
    if request.session.get('role'):
        try:
            role_id = request.session.get('role')
            user = User.objects.select_related('role').get(id=role_id)
            return {"role_name": user.role.name}
        except User.DoesNotExist:
            return {"role_name": None}
    return {"role_name": None}
