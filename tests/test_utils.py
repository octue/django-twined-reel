from django.test import TestCase
from django_twined.models import ServiceRevision
from django_twined.utils.versions import select_latest_service_revision_by_semantic_version


class TestSelectLatestServiceRevisionBySemanticVersion(TestCase):
    def test_service_revisions_with_non_semantic_version_tags_ignored(self):
        """Test that service revisions with tags that aren't semantic versions are ignored."""
        namespace = "my-org"
        name = "my-service"

        ServiceRevision.objects.create(namespace=namespace, name=name, tag="hello")
        ServiceRevision.objects.create(namespace=namespace, name=name, tag="0.1.0")
        ServiceRevision.objects.create(namespace=namespace, name=name, tag="2.1.0")
        latest_revision = ServiceRevision.objects.create(namespace=namespace, name=name, tag="11.1.0")

        self.assertEqual(
            select_latest_service_revision_by_semantic_version(namespace=namespace, name=name),
            latest_revision,
        )

    def test_versions_ordered_naturally(self):
        """Test that service revisions can be ordered correctly by semantic version (i.e. naturally)."""
        namespace = "my-org"
        name = "my-service"

        ServiceRevision.objects.create(namespace=namespace, name=name, tag="0.1.0")
        ServiceRevision.objects.create(namespace=namespace, name=name, tag="2.1.0")
        latest_revision = ServiceRevision.objects.create(namespace=namespace, name=name, tag="11.1.0")

        self.assertEqual(
            select_latest_service_revision_by_semantic_version(namespace=namespace, name=name),
            latest_revision,
        )

    def test_non_candidate_version_considered_newer_than_candidate_versions(self):
        """Test that service revisions with a candidate part in their version tag are considered older than a service
        revision with the same semantic version but no candidate part (i.e. that `2.1.0` is newer than `2.1.0.beta-1`).
        """
        namespace = "my-org"
        name = "my-service"

        ServiceRevision.objects.create(namespace=namespace, name=name, tag="2.1.0.beta-2")
        ServiceRevision.objects.create(namespace=namespace, name=name, tag="2.1.0.beta-1")
        latest_revision = ServiceRevision.objects.create(namespace=namespace, name=name, tag="2.1.0")

        self.assertEqual(
            select_latest_service_revision_by_semantic_version(namespace=namespace, name=name),
            latest_revision,
        )

    def test_candidate_versions_ordered_alphabetically(self):
        """Test that service revisions with the same semantic version apart from the candidate part are ordered by their
        candidate parts alphabetically.
        """
        namespace = "my-org"
        name = "my-service"

        latest_revision = ServiceRevision.objects.create(namespace=namespace, name=name, tag="2.1.0.beta-3")
        ServiceRevision.objects.create(namespace=namespace, name=name, tag="2.1.0.beta-2")
        ServiceRevision.objects.create(namespace=namespace, name=name, tag="2.1.0.beta-1")

        self.assertEqual(
            select_latest_service_revision_by_semantic_version(namespace=namespace, name=name),
            latest_revision,
        )