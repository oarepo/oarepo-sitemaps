#from invenio_indexer.api import RecordIndexer
# from .indexer import RefreshingRecordIndexer
from functools import partial

from invenio_indexer.api import RecordIndexer
from invenio_records_rest.utils import allow_all
from links import sample_links_factory
from oarepo_communities.links import community_record_links_factory
from oarepo_communities.search import community_search_factory

from .search import SampleRecordsSearch

SAMPLE_RECORD_CLASS = 'sample.record.SampleRecord'
RECORD_PID = 'pid(recid,record_class="sample.record:SampleRecord")'
RECORD_DRAFT_PID = 'pid(recid,record_class="sample.record:SampleRecord")'
RECORD_PID_TYPE = 'recid'
SAMPLE_DRAFT_PID_TYPE = 'drecid'
SAMPLE_DRAFT_RECORD_CLASS = 'sample.record.SampleDraftRecord'
RECORDS_DRAFT_ENDPOINTS = {
    'recid': dict(
        draft='drecid',
        pid_type='recid',
        pid_minter='recid',
        pid_fetcher='recid',
        default_endpoint_prefix=True,
        search_class=SampleRecordsSearch,
        indexer_class=RecordIndexer,
        search_index="sample-sample-v1.0.0" ,
        search_type=None,
        record_serializers={
            'application/json': 'oarepo_validate:json_response',
        },
        search_serializers={
            'application/json': 'oarepo_validate:json_search',
        },
        record_loaders={
            'application/json': 'oarepo_validate:json_loader',
            'application/json-patch+json': 'oarepo_validate:json_loader'
        },
        record_class='sample.record:SampleRecord',
        list_route='/<community_id>/records/published/',
        item_route=f'/<commpid({RECORD_PID_TYPE},model="records",record_class="{SAMPLE_RECORD_CLASS}"):pid_value>',
        default_media_type='application/json',
        max_result_window=10000,
        error_handlers=dict(),
        publish_permission_factory_imp=allow_all,
        read_permission_factory_imp=allow_all,
        unpublish_permission_factory_imp=allow_all,
        edit_permission_factory_imp=allow_all,
        search_factory_imp=community_search_factory,
        links_factory_imp=partial(community_record_links_factory, original_links_factory=sample_links_factory),
    )
    ,
    'drecid': dict(
        create_permission_factory_imp=allow_all,
        delete_permission_factory_imp=allow_all,
        update_permission_factory_imp=allow_all,
        read_permission_factory_imp=allow_all,
        search_index="draft-sample-sample-v1.0.0",
        record_class='sample.record:SampleDraftRecord',
        list_route= '/<community_id>/records/draft/',
        item_route=f'/<commpid({SAMPLE_DRAFT_PID_TYPE},model="records/draft",record_class="{SAMPLE_DRAFT_RECORD_CLASS}"):pid_value>',
        files=dict(
            put_file_factory=allow_all,
            get_file_factory=allow_all,
            delete_file_factory=allow_all,
        ),
        links_factory_imp=partial(community_record_links_factory, original_links_factory=sample_links_factory),
    )
}