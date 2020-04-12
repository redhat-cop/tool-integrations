# Plugins receive a parameter of type gitlab.v4.objects.Project
# More info about this type: https://python-gitlab.readthedocs.io/en/stable/gl_objects/projects.html#reference
# Plugins should return a boolean indicating whether or not the GitLab project should be processed


def plugin(project) -> bool:
    print(f"This is running on {project.id} from inside of a plugin!")
    # print(project.files.get('engagements.json', "master").decode())
    return True
