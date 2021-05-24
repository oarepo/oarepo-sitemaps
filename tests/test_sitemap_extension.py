import json

from flask_sitemap import Sitemap
from invenio_pidstore.models import PersistentIdentifier
from oarepo_records_draft import current_drafts

from sample.config import SAMPLE_DRAFT_PID_TYPE
from sample.record import SampleDraftRecord
from sample.search import SampleRecordsSearch


def test_sitemap_extension(app, client, db, community):

    assert isinstance(app.extensions['sitemap'], Sitemap)

    url = "https://localhost:5000/sitemap.xml"
    response = client.get(url)
    print(response.data)

    assert response.status_code == 200

    app.config['SITEMAP_MAX_URL_COUNT'] = 1
    for pid in range(1, 100):
        client.post('/cesnet/records/draft/',
                    data=json.dumps({"title": "title", "_primary_community": "cesnet", "state": "published"}),
                    content_type='application/json')
        record_pid = PersistentIdentifier.query.filter_by(pid_type=SAMPLE_DRAFT_PID_TYPE, pid_value=pid).one()
        record = SampleDraftRecord.get_record(id_=record_pid.object_uuid)
        current_drafts.publish(record=record, record_pid=record_pid, require_valid=False)

    url = "https://localhost:5000/sitemap.xml"
    response = client.get(url)
    print(response.data)
    assert response.status_code == 200
    for x in SampleRecordsSearch(index="sample-sample-v1.0.0").source(includes=['id', '_primary_community']):
        print(x)

    assert 'http://localhost:5000/sitemap1.xml' in str(response.data)
    assert 'http://localhost:5000/sitemap10.xml' in str(response.data)
    assert 'http://localhost:5000/sitemap11.xml' not in str(response.data)