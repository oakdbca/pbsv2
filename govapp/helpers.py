def is_member_of(user, group_name):
    # Todo: Consider caching the groups
    return user.is_superuser or user.groups.filter(name=group_name).exists()


def is_internal(user):
    return user.is_superuser or user.is_staff
