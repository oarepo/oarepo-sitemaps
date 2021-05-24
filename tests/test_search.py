import json

from invenio_indexer.api import RecordIndexer
from invenio_pidstore.models import PersistentIdentifier
from oarepo_records_draft import current_drafts

from sample.config import SAMPLE_DRAFT_PID_TYPE
from sample.record import SampleDraftRecord


def test_search_records(app, db, client, community):

    assert len(current_drafts.managed_records) == 1

    response = client.post('/cesnet/records/draft/',
                           data=json.dumps({"title": "necooo", "_primary_community": "cesnet", "state": "published"}),
                           content_type='application/json')
    assert response.status_code == 201
    print(response.data)

    response = client.post('/cesnet/records/draft/',
                           data=json.dumps({"title": "xyyyyyyyyyyyyy", "_primary_community": "cesnet", "state": "published"}),
                           content_type='application/json')
    assert response.status_code == 201

    response = client.get('/cesnet/records/draft/1', content_type='application/json')
    assert response.status_code == 200

    response = client.get('/cesnet/records/draft/2', content_type='application/json')
    assert response.status_code == 200

    record_pid = PersistentIdentifier.query. \
        filter_by(pid_type=SAMPLE_DRAFT_PID_TYPE, pid_value='1').one()
    record = SampleDraftRecord.get_record(id_=record_pid.object_uuid)
    current_drafts.publish(record=record, record_pid=record_pid, require_valid=False)

    record_pid = PersistentIdentifier.query. \
        filter_by(pid_type=SAMPLE_DRAFT_PID_TYPE, pid_value='2').one()
    record = SampleDraftRecord.get_record(id_=record_pid.object_uuid)
    current_drafts.publish(record=record, record_pid=record_pid, require_valid=False)

    indexer = RecordIndexer()
    indexer.client.indices.refresh()

    response = client.get('/cesnet/records/1', content_type='application/json')
    assert response.status_code == 200

    response = client.get('/cesnet/records/2', content_type='application/json')
    assert response.status_code == 200

    search_class = ''
    for x in current_drafts.managed_records.records:
        search_class = x.published.resolve('search_class')

    ids = []
    primary_keys = []

    for x in search_class(index="sample-sample-v1.0.0").source(includes=['id', '_primary_community']):
        ids.append(x.id)
        primary_keys.append(x._primary_community)

    assert ids == ['1', '2']
    assert primary_keys == ['cesnet', 'cesnet']

    url = "https://localhost:5000/sitemap.xml"
    response = client.get(url)
    print(response.data)
    assert response.status_code == 200
    assert 'http://localhost:5000/cesnet/records/1' in str(response.data)
    assert 'http://localhost:5000/cesnet/records/2' in str(response.data)
    assert 'http://localhost:5000/records/1' not in str(response.data)


