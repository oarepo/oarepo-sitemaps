from marshmallow import INCLUDE, Schema, fields, validate
from oarepo_communities.marshmallow import OARepoCommunitiesMixin
from oarepo_invenio_model.marshmallow import InvenioRecordMetadataSchemaV1Mixin


class SampleSchemaV1(InvenioRecordMetadataSchemaV1Mixin,
                              OARepoCommunitiesMixin,):
    title = fields.String( required=True)
    state = fields.String( required=True)
    class Meta:
        unknown = INCLUDE