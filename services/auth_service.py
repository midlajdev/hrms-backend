from rest_framework_simplejwt.tokens import RefreshToken

def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    refresh["role"] = user.role

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    
    }

def logout_user(refresh_token):
    token = RefreshToken(refresh_token)
    token.blacklist()
