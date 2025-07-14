def user_is_role(user, role):
    """devuelve True si el usuario es el rol que se le pasa por parametro"""
    for rol in user.role:
        if rol.name == role:
            return True
    return False
