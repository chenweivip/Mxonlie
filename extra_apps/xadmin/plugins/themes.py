#coding:utf-8
from __future__ import print_function
import httplib2
import requests
from django.template import loader
from django.core.cache import cache
from django.utils import six
from django.utils.translation import ugettext as _
from xadmin.sites import site
from xadmin.models import UserSettings
from xadmin.views import BaseAdminPlugin, BaseAdminView
from xadmin.util import static, json
import six
if six.PY2:
    import urllib
else:
    import urllib.parse

THEME_CACHE_KEY = 'xadmin_themes'


class ThemePlugin(BaseAdminPlugin):

    enable_themes = False
    # {'name': 'Blank Theme', 'description': '...', 'css': 'http://...', 'thumbnail': '...'}
    user_themes = None
    use_bootswatch = False
    default_theme = static('xadmin/css/themes/bootstrap-xadmin.css')
    bootstrap2_theme = static('xadmin/css/themes/bootstrap-theme.css')

    def init_request(self, *args, **kwargs):
        return self.enable_themes

    def _get_theme(self):
        if self.user:
            try:
                return UserSettings.objects.get(user=self.user, key="site-theme").value
            except Exception:
                pass
        if '_theme' in self.request.COOKIES:
            if six.PY2:
                func = urllib.unquote
            else:
                func = urllib.parse.unquote
            return func(self.request.COOKIES['_theme'])
        return self.default_theme

    def get_context(self, context):
        context['site_theme'] = self._get_theme()
        return context

    # Media
    def get_media(self, media):
        return media + self.vendor('jquery-ui-effect.js', 'xadmin.plugin.themes.js')

    # Block Views
    def block_top_navmenu(self, context, nodes):

        themes = [
            {'name': _(u"Default"), 'description': _(u"Default bootstrap theme"), 'css': self.default_theme},
            {'name': _(u"Bootstrap2"), 'description': _(u"Bootstrap 2.x theme"), 'css': self.bootstrap2_theme},
            ]
        select_css = context.get('site_theme', self.default_theme)

        if self.user_themes:
            themes.extend(self.user_themes)


        if self.use_bootswatch:

            ex_themes = cache.get(THEME_CACHE_KEY)
            if ex_themes:

                themes.extend(json.loads(ex_themes))
            else:
                ex_themes = []
                try:
                    # h = httplib2.Http()
                    # resp, content = h.request("https://bootswatch.com/api/3.json", 'GET', '',
                    #     headers={"Accept": "application/json", "User-Agent": self.request.META['HTTP_USER_AGENT']})
                    # if six.PY3:
                    #
                    #     content = content.decode()
                    # watch_themes = json.loads(content)['themes']
                    themes_dict = {'version': "3.3.6",
                            'themes': [
                                {
                                    'name': "Cerulean",
                                    'description': "A calm blue sky",
                                    'thumbnail': "https://bootswatch.com/cerulean/thumbnail.png",
                                    'preview': "https://bootswatch.com/cerulean/",
                                    'css': "https://bootswatch.com/cerulean/bootstrap.css",
                                    'cssMin': "https://bootswatch.com/cerulean/bootstrap.min.css",
                                    'cssCdn': "https://maxcdn.bootstrapcdn.com/bootswatch/latest/cerulean/bootstrap.min.css",
                                    'less': "https://bootswatch.com/cerulean/bootswatch.less",
                                    'lessVariables': "https://bootswatch.com/cerulean/variables.less",
                                    'scss': "https://bootswatch.com/cerulean/_bootswatch.scss",
                                    'scssVariables': "https://bootswatch.com/cerulean/_variables.scss"
                                },
                            {
                                'name': "Cosmo",
                                'description': "An ode to Metro",
                                'thumbnail': "https://bootswatch.com/cosmo/thumbnail.png",
                                'preview': "https://bootswatch.com/cosmo/",
                                'css': "https://bootswatch.com/cosmo/bootstrap.css",
                                'cssMin': "https://bootswatch.com/cosmo/bootstrap.min.css",
                                'cssCdn': "https://maxcdn.bootstrapcdn.com/bootswatch/latest/cosmo/bootstrap.min.css",
                                'less': "https://bootswatch.com/cosmo/bootswatch.less",
                                'lessVariables': "https://bootswatch.com/cosmo/variables.less",
                                'scss': "https://bootswatch.com/cosmo/_bootswatch.scss",
                                'scssVariables': "https://bootswatch.com/cosmo/_variables.scss"
                            },
                            {
                                'name': "Cyborg",
                                'description': "Jet black and electric blue",
                                'thumbnail': "https://bootswatch.com/cyborg/thumbnail.png",
                                'preview': "https://bootswatch.com/cyborg/",
                                'css': "https://bootswatch.com/cyborg/bootstrap.css",
                                'cssMin': "https://bootswatch.com/cyborg/bootstrap.min.css",
                                'cssCdn': "https://maxcdn.bootstrapcdn.com/bootswatch/latest/cyborg/bootstrap.min.css",
                                'less': "https://bootswatch.com/cyborg/bootswatch.less",
                                'lessVariables': "https://bootswatch.com/cyborg/variables.less",
                                'scss': "https://bootswatch.com/cyborg/_bootswatch.scss",
                                'scssVariables': "https://bootswatch.com/cyborg/_variables.scss"
                            },
                            {
                                'name': "Darkly",
                                'description': "Flatly in night mode",
                                'thumbnail': "https://bootswatch.com/darkly/thumbnail.png",
                                'preview': "https://bootswatch.com/darkly/",
                                'css': "https://bootswatch.com/darkly/bootstrap.css",
                                'cssMin': "https://bootswatch.com/darkly/bootstrap.min.css",
                                'cssCdn': "https://maxcdn.bootstrapcdn.com/bootswatch/latest/darkly/bootstrap.min.css",
                                'less': "https://bootswatch.com/darkly/bootswatch.less",
                                'lessVariables': "https://bootswatch.com/darkly/variables.less",
                                'scss': "https://bootswatch.com/darkly/_bootswatch.scss",
                                'scssVariables': "https://bootswatch.com/darkly/_variables.scss"
                            },
                            {
                                'name': "Flatly",
                                'description': "Flat and modern",
                                'thumbnail': "https://bootswatch.com/flatly/thumbnail.png",
                                'preview': "https://bootswatch.com/flatly/",
                                'css': "https://bootswatch.com/flatly/bootstrap.css",
                                'cssMin': "https://bootswatch.com/flatly/bootstrap.min.css",
                                'cssCdn': "https://maxcdn.bootstrapcdn.com/bootswatch/latest/flatly/bootstrap.min.css",
                                'less': "https://bootswatch.com/flatly/bootswatch.less",
                                'lessVariables': "https://bootswatch.com/flatly/variables.less",
                                'scss': "https://bootswatch.com/flatly/_bootswatch.scss",
                                'scssVariables': "https://bootswatch.com/flatly/_variables.scss"
                            },
                            {
                                'name': "Journal",
                                'description': "Crisp like a new sheet of paper",
                                'thumbnail': "https://bootswatch.com/journal/thumbnail.png",
                                'preview': "https://bootswatch.com/journal/",
                                'css': "https://bootswatch.com/journal/bootstrap.css",
                                'cssMin': "https://bootswatch.com/journal/bootstrap.min.css",
                                'cssCdn': "https://maxcdn.bootstrapcdn.com/bootswatch/latest/journal/bootstrap.min.css",
                                'less': "https://bootswatch.com/journal/bootswatch.less",
                                'lessVariables': "https://bootswatch.com/journal/variables.less",
                                'scss': "https://bootswatch.com/journal/_bootswatch.scss",
                                'scssVariables': "https://bootswatch.com/journal/_variables.scss"
                            },
                            {
                                'name': "Lumen",
                                'description': "Light and shadow",
                                'thumbnail': "https://bootswatch.com/lumen/thumbnail.png",
                                'preview': "https://bootswatch.com/lumen/",
                                'css': "https://bootswatch.com/lumen/bootstrap.css",
                                'cssMin': "https://bootswatch.com/lumen/bootstrap.min.css",
                                'cssCdn': "https://maxcdn.bootstrapcdn.com/bootswatch/latest/lumen/bootstrap.min.css",
                                'less': "https://bootswatch.com/lumen/bootswatch.less",
                                'lessVariables': "https://bootswatch.com/lumen/variables.less",
                                'scss': "https://bootswatch.com/lumen/_bootswatch.scss",
                                'scssVariables': "https://bootswatch.com/lumen/_variables.scss"
                            },
                            {
                                'name': "Paper",
                                'description': "Material is the metaphor",
                                'thumbnail': "https://bootswatch.com/paper/thumbnail.png",
                                'preview': "https://bootswatch.com/paper/",
                                'css': "https://bootswatch.com/paper/bootstrap.css",
                                'cssMin': "https://bootswatch.com/paper/bootstrap.min.css",
                                'cssCdn': "https://maxcdn.bootstrapcdn.com/bootswatch/latest/paper/bootstrap.min.css",
                                'less': "https://bootswatch.com/paper/bootswatch.less",
                                'lessVariables': "https://bootswatch.com/paper/variables.less",
                                'scss': "https://bootswatch.com/paper/_bootswatch.scss",
                                'scssVariables': "https://bootswatch.com/paper/_variables.scss"
                            },
                            {
                                'name': "Readable",
                                'description': "Optimized for legibility",
                                'thumbnail': "https://bootswatch.com/readable/thumbnail.png",
                                'preview': "https://bootswatch.com/readable/",
                                'css': "https://bootswatch.com/readable/bootstrap.css",
                                'cssMin': "https://bootswatch.com/readable/bootstrap.min.css",
                                'cssCdn': "https://maxcdn.bootstrapcdn.com/bootswatch/latest/readable/bootstrap.min.css",
                                'less': "https://bootswatch.com/readable/bootswatch.less",
                                'lessVariables': "https://bootswatch.com/readable/variables.less",
                                'scss': "https://bootswatch.com/readable/_bootswatch.scss",
                                'scssVariables': "https://bootswatch.com/readable/_variables.scss"
                            },
                            {
                                'name': "Sandstone",
                                'description': "A touch of warmth",
                                'thumbnail': "https://bootswatch.com/sandstone/thumbnail.png",
                                'preview': "https://bootswatch.com/sandstone/",
                                'css': "https://bootswatch.com/sandstone/bootstrap.css",
                                'cssMin': "https://bootswatch.com/sandstone/bootstrap.min.css",
                                'cssCdn': "https://maxcdn.bootstrapcdn.com/bootswatch/latest/sandstone/bootstrap.min.css",
                                'less': "https://bootswatch.com/sandstone/bootswatch.less",
                                'lessVariables': "https://bootswatch.com/sandstone/variables.less",
                                'scss': "https://bootswatch.com/sandstone/_bootswatch.scss",
                                'scssVariables': "https://bootswatch.com/sandstone/_variables.scss"
                            },
                            {
                                'name': "Simplex",
                                'description': "Mini and minimalist",
                                'thumbnail': "https://bootswatch.com/simplex/thumbnail.png",
                                'preview': "https://bootswatch.com/simplex/",
                                'css': "https://bootswatch.com/simplex/bootstrap.css",
                                'cssMin': "https://bootswatch.com/simplex/bootstrap.min.css",
                                'cssCdn': "https://maxcdn.bootstrapcdn.com/bootswatch/latest/simplex/bootstrap.min.css",
                                'less': "https://bootswatch.com/simplex/bootswatch.less",
                                'lessVariables': "https://bootswatch.com/simplex/variables.less",
                                'scss': "https://bootswatch.com/simplex/_bootswatch.scss",
                                'scssVariables': "https://bootswatch.com/simplex/_variables.scss"
                            },
                            {
                                'name': "Slate",
                                'description': "Shades of gunmetal gray",
                                'thumbnail': "https://bootswatch.com/slate/thumbnail.png",
                                'preview': "https://bootswatch.com/slate/",
                                'css': "https://bootswatch.com/slate/bootstrap.css",
                                'cssMin': "https://bootswatch.com/slate/bootstrap.min.css",
                                'cssCdn': "https://maxcdn.bootstrapcdn.com/bootswatch/latest/slate/bootstrap.min.css",
                                'less': "https://bootswatch.com/slate/bootswatch.less",
                                'lessVariables': "https://bootswatch.com/slate/variables.less",
                                'scss': "https://bootswatch.com/slate/_bootswatch.scss",
                                'scssVariables': "https://bootswatch.com/slate/_variables.scss"
                            },
                            {
                                'name': "Solar",
                                'description': "A spin on Solarized",
                                'thumbnail': "https://bootswatch.com/solar/thumbnail.png",
                                'preview': "https://bootswatch.com/solar/",
                                'css': "https://bootswatch.com/solar/bootstrap.css",
                                'cssMin': "https://bootswatch.com/solar/bootstrap.min.css",
                                'cssCdn': "https://maxcdn.bootstrapcdn.com/bootswatch/latest/solar/bootstrap.min.css",
                                'less': "https://bootswatch.com/solar/bootswatch.less",
                                'lessVariables': "https://bootswatch.com/solar/variables.less",
                                'scss': "https://bootswatch.com/solar/_bootswatch.scss",
                                'scssVariables': "https://bootswatch.com/solar/_variables.scss"
                            },
                            {
                                'name': "Spacelab",
                                'description': "Silvery and sleek",
                                'thumbnail': "https://bootswatch.com/spacelab/thumbnail.png",
                                'preview': "https://bootswatch.com/spacelab/",
                                'css': "https://bootswatch.com/spacelab/bootstrap.css",
                                'cssMin': "https://bootswatch.com/spacelab/bootstrap.min.css",
                                'cssCdn': "https://maxcdn.bootstrapcdn.com/bootswatch/latest/spacelab/bootstrap.min.css",
                                'less': "https://bootswatch.com/spacelab/bootswatch.less",
                                'lessVariables': "https://bootswatch.com/spacelab/variables.less",
                                'scss': "https://bootswatch.com/spacelab/_bootswatch.scss",
                                'scssVariables': "https://bootswatch.com/spacelab/_variables.scss"
                            },
                            {
                                'name': "Superhero",
                                'description': "The brave and the blue",
                                'thumbnail': "https://bootswatch.com/superhero/thumbnail.png",
                                'preview': "https://bootswatch.com/superhero/",
                                'css': "https://bootswatch.com/superhero/bootstrap.css",
                                'cssMin': "https://bootswatch.com/superhero/bootstrap.min.css",
                                'cssCdn': "https://maxcdn.bootstrapcdn.com/bootswatch/latest/superhero/bootstrap.min.css",
                                'less': "https://bootswatch.com/superhero/bootswatch.less",
                                'lessVariables': "https://bootswatch.com/superhero/variables.less",
                                'scss': "https://bootswatch.com/superhero/_bootswatch.scss",
                                'scssVariables': "https://bootswatch.com/superhero/_variables.scss"
                            },
                            {
                                'name': "United",
                                'description': "Ubuntu orange and unique font",
                                'thumbnail': "https://bootswatch.com/united/thumbnail.png",
                                'preview': "https://bootswatch.com/united/",
                                'css': "https://bootswatch.com/united/bootstrap.css",
                                'cssMin': "https://bootswatch.com/united/bootstrap.min.css",
                                'cssCdn': "https://maxcdn.bootstrapcdn.com/bootswatch/latest/united/bootstrap.min.css",
                                'less': "https://bootswatch.com/united/bootswatch.less",
                                'lessVariables': "https://bootswatch.com/united/variables.less",
                                'scss': "https://bootswatch.com/united/_bootswatch.scss",
                                'scssVariables': "https://bootswatch.com/united/_variables.scss"
                            },
                            {
                                'name': "Yeti",
                                'description': "A friendly foundation",
                                'thumbnail': "https://bootswatch.com/yeti/thumbnail.png",
                                'preview': "https://bootswatch.com/yeti/",
                                'css': "https://bootswatch.com/yeti/bootstrap.css",
                                'cssMin': "https://bootswatch.com/yeti/bootstrap.min.css",
                                'cssCdn': "https://maxcdn.bootstrapcdn.com/bootswatch/latest/yeti/bootstrap.min.css",
                                'less': "https://bootswatch.com/yeti/bootswatch.less",
                                'lessVariables': "https://bootswatch.com/yeti/variables.less",
                                'scss': "https://bootswatch.com/yeti/_bootswatch.scss",
                                'scssVariables': "https://bootswatch.com/yeti/_variables.scss"
                            }
                        ]
                    }
                    watch_themes = themes_dict['themes']


                    ex_themes.extend([
                        {'name': t['name'], 'description': t['description'],
                            'css': t['cssMin'], 'thumbnail': t['thumbnail']}
                        for t in watch_themes])
                except Exception as e:
                    print(e)

                cache.set(THEME_CACHE_KEY, json.dumps(ex_themes), 24 * 3600)
                themes.extend(ex_themes)

        nodes.append(loader.render_to_string('xadmin/blocks/comm.top.theme.html', {'themes': themes, 'select_css': select_css}))


site.register_plugin(ThemePlugin, BaseAdminView)
