def all_user_serializer(all_user):
    result = []
    total = len(all_user)
    for user in all_user:
        result.append(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email_id": user.email_id
            }
        )
    return {"Total user": total, "all user detail": result}


def user_serializer(user):
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email_id": user.email_id
    }