from invenio_search import RecordsSearch
from oarepo_communities.search import CommunitySearch


class SampleRecordsSearch(CommunitySearch):
    """Article collection search."""

    LIST_SOURCE_FIELDS = [
        'id', 'oarepo:validity.valid', 'oarepo:draft',
        'title', 'creator', 'created'
        '_primary_community', '_communities', 'modified'
        '$schema'
    ]
