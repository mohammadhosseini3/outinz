from django.shortcuts import redirect

def unauthenticate_user(view_function):
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_function(request,*args,**kwargs)
    return wrapper

def allowed_users(allowed_roles=[]):
    def decorator(view_function):
        def wrapper(request,*args,**kwargs):
            
            if request.user.groups.exists:
                x = request.user.groups.all()[0]

            if str(x) in allowed_roles:
                return view_function(request,*args,**kwargs)
                
            else:
                return redirect("/")
        return wrapper
    return decorator