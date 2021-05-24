import datetime

from flask import url_for
from invenio_records.api import Record
from oarepo_actions.decorators import action
from oarepo_communities.converters import CommunityPIDValue
from oarepo_communities.proxies import current_oarepo_communities
from oarepo_communities.record import CommunityRecordMixin
from oarepo_fsm.mixins import FSMMixin
from oarepo_records_draft.record import DraftRecordMixin
from oarepo_validate import MarshmallowValidatedRecordMixin, SchemaKeepingRecordMixin

from .constants import SAMPLE_ALLOWED_SCHEMAS, SAMPLE_PREFERRED_SCHEMA
from .marshmallow import SampleSchemaV1


class SampleRecord(SchemaKeepingRecordMixin,
                   MarshmallowValidatedRecordMixin,
                   CommunityRecordMixin,FSMMixin,
                   Record):
    ALLOWED_SCHEMAS = SAMPLE_ALLOWED_SCHEMAS
    PREFERRED_SCHEMA = SAMPLE_PREFERRED_SCHEMA
    MARSHMALLOW_SCHEMA = SampleSchemaV1
    index_name = 'sample'

    @property
    def canonical_url(self):
        return url_for(f'invenio_records_rest.recid_item',
                       pid_value=CommunityPIDValue(
                           self['id'],
                           current_oarepo_communities.get_primary_community_field(self)
                       ), _external=True)

class SampleDraftRecord(DraftRecordMixin, SampleRecord):
    @property
    def canonical_url(self):
        return url_for(f'invenio_records_rest.drecid_item',
                       pid_value=CommunityPIDValue(
                           self['id'],
                           current_oarepo_communities.get_primary_community_field(self)
                       ), _external=True)

    def validate(self, *args, **kwargs):
        if 'created' not in self:
            self['created'] = datetime.date.today().strftime('%Y-%m-%d')

        self['modified'] = datetime.date.today().strftime('%Y-%m-%d')
        return super().validate(*args, **kwargs)