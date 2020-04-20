# tool-integrations

This repository provides small software solutions for providing linkage and integrations between various
 tools (i.e.: software). As an example, a bridge between two tools where the request from does not quite
 match the API of the other.

### Content

- [ansible-tower-bridges/github-webhook](ansible-tower-bridges/github-webhook) provides a bridge interfa
ce between GitHub webhooks and Ansible Tower API job launch requests.
- [argo-cd-bridges/gitlab](argo-cd-bridges/gitlab) provides a bridge interface between GitLab and Application resources in an Argo CD instance
- [quay/imagestream-sync](quay/imagestream-sync) synchronizes ImageStreams referencing images from Quay using Quay notification based webhooks
- [alertmanager-notifier-gateway/alertmanager-line-gateway](alertmanager-notifier-gateway/alertmanager-line-gateway) provide a processing gateway for alertmanager alert to Line messenger.
