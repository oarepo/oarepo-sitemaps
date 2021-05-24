from flask_sitemap import Sitemap
from oarepo_communities.converters import CommunityPIDValue
from oarepo_records_draft import current_drafts


def sitemap_ext(app=None):
    sitemap = Sitemap(app)
    app.config['SITEMAP_MAX_URL_COUNT'] = 10000

    @sitemap.register_generator
    def record():
        for x in current_drafts.managed_records.records:
            search_class = x.published.resolve('search_class')
            index = x.published.rest['search_index']
            rest_name = x.published.rest_name

            for url in search_class(index=index).source(includes=['id', '_primary_community', 'modified']):
                id = url.id
                community = url._primary_community

                modified = url.modified

                entrypoint = 'invenio_records_rest.' + rest_name + '_item'

                yield entrypoint, {'pid_value': CommunityPIDValue(id,community) }, modified, 'weakly', 1


class OARepoSitemap(object):
    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""

        app.extensions['testinvenio-oarepo_actions'] = self
        sitemap_ext(app=app)