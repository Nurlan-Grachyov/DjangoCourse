def is_in_group(request):
    if request.user.is_authenticated:
        return {"is_in_group": request.user.groups.filter(name="managers").exists()}
    return {"is_in_group": False}
