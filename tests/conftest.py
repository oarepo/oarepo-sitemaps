
# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""
import os
import shutil
import sys

import pytest
from flask import Flask, make_response
from flask_login import LoginManager, login_user
from flask_principal import Principal
from flask_security.datastore import Datastore
from helpers import set_identity
from invenio_access import InvenioAccess
from invenio_access.permissions import Permission
from invenio_accounts import InvenioAccounts
from invenio_accounts.models import User
from invenio_base.signals import app_loaded
from invenio_db import InvenioDB
from invenio_db import db as _db
from invenio_indexer import InvenioIndexer
from invenio_jsonschemas import InvenioJSONSchemas
from invenio_pidstore import InvenioPIDStore
from invenio_records import InvenioRecords
from invenio_records_rest import InvenioRecordsREST
from invenio_records_rest.utils import allow_all
from invenio_records_rest.views import create_blueprint_from_app
from invenio_rest import InvenioREST
from invenio_search import InvenioSearch
from invenio_search.cli import destroy, init
from oarepo_actions.ext import Actions
from oarepo_communities import OARepoCommunities
from oarepo_communities.api import OARepoCommunity
from oarepo_communities.converters import CommunityPIDConverter
from oarepo_communities.handlers import CommunityHandler
from oarepo_mapping_includes.ext import OARepoMappingIncludesExt
from oarepo_records_draft.ext import RecordsDraft, RecordsDraftState
from oarepo_validate.ext import OARepoValidate
from sqlalchemy_utils import create_database, database_exists

from oarepo_sitemaps.ext import OARepoSitemap
from sample.ext import SampleExt
from tests.helpers import LiteEntryPoint


@pytest.fixture(scope="module")
def base_app():
    """Flask applicat-ion fixture."""
    instance_path = os.path.join(sys.prefix, 'var', 'tests-instance')

    # empty the instance path
    if os.path.exists(instance_path):
        shutil.rmtree(instance_path)
    os.makedirs(instance_path)

    os.environ['INVENIO_INSTANCE_PATH'] = instance_path

    app_ = Flask('invenio-model-testapp', instance_path=instance_path)
    app_.config.update(
        TESTING=True,
        JSON_AS_ASCII=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'SQLALCHEMY_DATABASE_URI',
            'sqlite:///:memory:'),
        SERVER_NAME='localhost:5000',
        SECURITY_PASSWORD_SALT='TEST_SECURITY_PASSWORD_SALT',
        SECRET_KEY='TEST_SECRET_KEY',
        INVENIO_INSTANCE_PATH=instance_path,
        SEARCH_INDEX_PREFIX='',
        JSONSCHEMAS_HOST='localhost:5000',
        SEARCH_ELASTIC_HOSTS=os.environ.get('SEARCH_ELASTIC_HOSTS', None),
        PIDSTORE_RECID_FIELD='id',
        SUPPORTED_LANGUAGES = ["cs", "en", "it"],
        OAREPO_COMMUNITIES_COMMUNITIES_FIELD = "cesnet",
        OAREPO_COMMUNITIES_ENDPOINTS=['recid', 'drecid'],
        OAREPO_FSM_ENABLED_REST_ENDPOINTS=['recid','drecid'],
        FILES_REST_PERMISSION_FACTORY=allow_all,
        ELASTICSEARCH_DEFAULT_LANGUAGE_TEMPLATE={
            "type": "text",
            "fields": {
                "keywords": {
                    "type": "keyword"
                }
            }
        }
    )
    Datastore(app_)
    InvenioDB(app_)
    InvenioIndexer(app_)
    InvenioSearch(app_)
    RecordsDraft(app_)
    OARepoCommunities(app_)
    OARepoSitemap(app_)
    return app_


@pytest.yield_fixture()
def app(base_app, es_clear):
    """Flask application fixture."""

    base_app._internal_jsonschemas = InvenioJSONSchemas(base_app)

    InvenioREST(base_app)
    InvenioRecordsREST(base_app)
    InvenioRecords(base_app)
    InvenioPIDStore(base_app)
    OARepoMappingIncludesExt(base_app)
    OARepoValidate(base_app)
    Actions(base_app)
    OARepoCommunities(base_app)
    InvenioAccounts(base_app)
    base_app.url_map.converters['commpid'] = CommunityPIDConverter

    SampleExt(base_app)
    LoginManager(base_app)
    Permission(base_app)
    InvenioAccess(base_app)
    Principal(base_app)
    InvenioSearch(base_app)
    login_manager = LoginManager()
    login_manager.init_app(base_app)
    login_manager.login_view = 'login'
    # es_trace_logger = logging.getLogger('elasticsearch.trace')
    # es_trace_logger.setLevel(logging.DEBUG)
    # handler = logging.StreamHandler()
    # es_trace_logger.addHandler(handler)


    base_app.register_blueprint(create_blueprint_from_app(base_app))

    @login_manager.user_loader
    def basic_user_loader(user_id):
        user_obj = User.query.get(int(user_id))
        return user_obj

    @base_app.route('/test/login/<int:id>', methods=['GET', 'POST'])
    def test_login(id):
        print("test: logging user with id", id)
        response = make_response()
        user = User.query.get(id)
        login_user(user)
        set_identity(user)
        return response

    app_loaded.send(None, app=base_app)

    with base_app.app_context():
        yield base_app
def extra_entrypoints(app, group=None, name=None):
    data = {
        'oarepo_enrollments.enrollments': [
            LiteEntryPoint('communities', CommunityHandler),
        ],
    }

    names = data.keys() if name is None else [name]
    for key in names:
        for entry_point in data[key]:
            yield entry_point


@pytest.fixture
def community(db, app):
    """Community fixture."""
    comid = 'cesnet'
    community = OARepoCommunity.create(
        {'description': 'Community description'},
        title='Title',
        id_=comid)
    db.session.commit()
    yield comid, community

@pytest.yield_fixture()
def client(app):
    """Get tests client."""
    with app.test_client() as client:
        yield client


@pytest.fixture
def db(app):
    """Create database for the tests."""
    with app.app_context():
        if not database_exists(str(_db.engine.url)) and \
                app.config['SQLALCHEMY_DATABASE_URI'] != 'sqlite://':
            create_database(_db.engine.url)
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture()
def prepare_es(app, db):
    runner = app.test_cli_runner()
    result = runner.invoke(destroy, ['--yes-i-know', '--force'])
    if result.exit_code:
        print(result.output, file=sys.stderr)
    assert result.exit_code == 0
    result = runner.invoke(init)
    if result.exit_code:
        print(result.output, file=sys.stderr)
    assert result.exit_code == 0


