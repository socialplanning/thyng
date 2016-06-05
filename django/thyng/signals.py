from django.db.models import signals

from .models import Project, ProjectMember


def update_featurelets(sender, instance, **kwargs):
    project = instance.project
    featurelets = project.projectfeaturelet_set.all()
    for featurelet in featurelets:
        group = 'project_admin' if instance.role == Project.ADMIN_ROLE else 'project_member'
        resp = requests.get("http://localhost:8002/" + reverse(
            'featurelet', args=[project.slug, featurelet.slug, 'thyng_api']),
                            data={'username': instance.user.username, 'group': group})
        print resp
signals.post_save.connect(update_featurelets, sender=ProjectMember)
