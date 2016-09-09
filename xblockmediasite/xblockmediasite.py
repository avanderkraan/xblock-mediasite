'''
@author: aamvanderkraan
This XBlock gives the ability to access a sonicfoundry mediasite
through API's. A configuration file holds information about which
mediasite server is accessed.
Originally, this program was developed for the TU Delft where the
mediasite is called Collegerama. Collegerama contains a lot of
recorded lectures, presentations and live events.
With this XBlock a teacher or course maker can select a part of a
recording to use in an edX online course.
'''
import pkg_resources
from django.template import Context, Template
from dateutil.parser import parse
from xblock.core import XBlock
from xblock.fields import Scope, String
from xblock.fragment import Fragment
import mediasite_settings
from mediasite.client import Client


class XBlockMediasite(XBlock):
    '''
    XBlockMediasite gives course-makers a tool to select a mediasite video
    to show to a student. The TU Delft mediasite is called Collegerama.
    Selecting a start time and an end time results in showing a part
    of a mediasite video.
    '''
    signin_message = ''

    # Scope: content
    mediasite_url = String(default='http://collegerama-vs-accept.tudelft.net',
                           scope=Scope.content,
                           help='Your presentation fragment')

    presentation_name = String(default='',
                               scope=Scope.content,
                               help='A student friendly presentation name')

    presentation_description = String(default='',
                                      scope=Scope.content,
                                      help='A student friendly description '
                                      'for this presentation')

    course_code = String(default='',
                         scope=Scope.content,
                         help='Course code, known to course makers')

    # Scope: settings
    time_start = String(default='00:00:00',
                        scope=Scope.settings,
                        help='Start of presentation (HH:MM:SS)')

    time_end = String(default='00:00:00',
                      scope=Scope.settings,
                      help='End of presentation (HH:MM:SS)')

    # extracted values, calculated from the user interface input
    # and used in the output url
    x_presentation = String(default='', scope=Scope.settings)
    x_play_from = String(default='', scope=Scope.settings)
    x_duration = String(default='', scope=Scope.settings)

    # variables that are used within this class but are not preserved because
    # they are read from a settings file each time this class is called.
    _server_root = 'http://collegerama-vs-accept.tudelft.net/Mediasite7'
    _maximum_items = '50'
    _date_format = '%Y-%M-%D'
    # default display_name
    _display_name = 'Mediasite'
    try:
        _server_root = mediasite_settings.server_root
    except:
        pass
    try:
        _maximum_items = str(mediasite_settings.maximum_items)
    except:
        pass
    try:
        _date_format = str(mediasite_settings.date_format)
    except:
        pass
    try:
        _display_name = str(mediasite_settings.display_name)
    except:
        pass
    display_name = String(display_name='',
                          default='%s' % _display_name,
                          scope=Scope.settings,
                          help='This name appears in the horizontal '
                          'navigation at the top of the page')

    # other class related variables, used for creating html
    presentation_cells = ''
    selected_presentation_title = ''

    def_presentation = 'Select a presentation'

    client = Client()

    def resource_string(self, path):
        '''
        Handy helper for getting resources from our kit.
        '''
        data = pkg_resources.resource_string(__name__,  # @UndefinedVariable
                                             path)
        # error caused by pythonpath settings at project properties
        return data.decode("utf8")

    def render_template(self, template_path, context={}):
        '''
        Evaluate a template by resource path, applying the provided context
        '''
        template_str = self.resource_string(template_path)
        return Template(template_str).render(Context(context))

    def student_view(self, context=None):
        '''
        The primary view of the MediasiteXBlock, shown to students
        when viewing courses.
        Context display name comes from mediasite_settings.py
        '''
        context = {'display_name': self.display_name}
        _client = Client()
        _credential_check = str(_client._get_home('Home'))
        _template = "static/html/errorxblock.html"
        if _credential_check.find('failed') == -1:
            _server_info = self.client.get_server_info()
            if _server_info and 'SiteName' in _server_info:
                _template = "static/html/studentxblock.html"
        html = self.render_template(_template, context)
        frag = Fragment(html.format(self=self))
        return frag

    def studio_view(self, context=None):
        '''
        The primary view of the MediasiteXBlock, shown to tutors or
        course makers when creating/editing courses.
        Context display name comes from mediasite_settings.py
        The key 'SiteName' should exist in the get_server_info() response.
        '''
        context = {'display_name': self.display_name}
        _client = Client()
        _credential_check = str(_client._get_home('Home'))
        _template = "static/html/errorxblock.html"
        if _credential_check.find('failed') == -1:
            _server_info = self.client.get_server_info()
            if _server_info and 'SiteName' in _server_info:
                self.signin_message = 'Connection with the mediasite server' \
                    ' is working correctly'
                _template = "static/html/studioxblock.html"
            else:
                self.signin_message = 'A connection with the mediasite' \
                    ' server could not be established at this moment'
        html = self.render_template(_template, context)
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/xblockmediasite.css"))
        frag.add_css(self.resource_string
                     ("static/css/jquery.datetimeentry.css"))
        frag.add_javascript(self.resource_string
                            ("static/js/src/jquery.plugin.js"))
        frag.add_javascript(self.resource_string
                            ("static/js/src/jquery.datetimeentry.js"))
        frag.add_javascript(self.resource_string
                            ("static/js/src/xblockmediasite.js"))
        frag.initialize_js('MediasiteXBlock')
        return frag

    @XBlock.json_handler
    def set_mediasite_url(self, data, suffix=''):
        '''
        @param data: a dict, contains check and a selected presentation
        @return: a dict with a composed mediasite url
        '''
        assert data['check'] == 'mediasite_url'
        if 'presentation' in data:
            self.x_presentation = data['presentation']
        if self.x_presentation != self.def_presentation:
            self.mediasite_url = self._set_mediasite_url()
        else:
            self.mediasite_url = self._server_root

        return {'mediasite_preview_action_link': self.mediasite_url}

    @XBlock.json_handler
    def set_presentation_name(self, data, suffix=''):
        '''
        Sets the presentation name
        @param data: a dict, contains check and a presentation name
        @return: a dict with a presentation name
        '''
        assert data['check'] == 'presentation_name'
        self.presentation_name = data['presentation_name']
        self.display_name = self.presentation_name
        return {'presentation_name': self.presentation_name}

    @XBlock.json_handler
    def set_presentation_description(self, data, suffix=''):
        '''
        Sets the presentation description
        @param data: a dict, contains check and a presentation description
        @return: a dict with a presentation description
        '''
        assert data['check'] == 'presentation_description'
        self.presentation_description = data['presentation_description']
        return {'presentation_description': self.presentation_description}

    @XBlock.json_handler
    def get_course_code(self, data, suffix=''):
        '''
        Search for courses with the given course code
        Returns at most a maximum number of items,
            see mediasite_settings.py items,
            and a warning if there are more items
        Sorting is done server-side, so in the event of more than the maximum
            number of item the sorting remains intact
        With select=card more record-items are returned than with the default
            setting
        With select=full more record-items are returned than with the default
            setting and with select=card
        @param data: a dict, contains the course code
        @return: a dict with a filtered list of presentations
        '''
        assert data['check'] == 'course_code'
        _presentation_cells = ''
        _orderby = ''
        _ordertype = ''
        _warning = ''
        # for the table generation
        _tablerow = '<tr id="%s" class="%s">'
        _tablerow += '<td class="date">%s</td><td class="title">%s</td></tr>'
        _table_cell_id = 'select-presentation-id'

        # default
        _ordertype_value = ''
        _orderby_value = 'Title asc, CreationDate desc'
        _title_ordertype_value = 'asc'
        _creation_date_ordertype_value = 'desc'

        if 'ordertype' in data:
            _ordertype_value = data['ordertype']

        if 'orderby' in data:
            orderby_data_value = data['orderby']
            if orderby_data_value.startswith('creation-date'):
                _creation_date_ordertype_value = \
                    _ordertype_value or _creation_date_ordertype_value
                _orderby_value = 'CreationDate %s, Title %s' % \
                    (_creation_date_ordertype_value, _title_ordertype_value)
            if orderby_data_value.startswith('title'):
                _title_ordertype_value = \
                    _ordertype_value or _title_ordertype_value
                _orderby_value = 'Title %s, CreationDate %s' % \
                    (_title_ordertype_value, _creation_date_ordertype_value)
            _orderby = '%s%s' % ('&$orderby=', _orderby_value)

        if 'course_code' in data:
            my_course_code = data['course_code']
            my_filter_criterium = "startswith(Title, '%s')" % my_course_code
            my_filter = '%s%s%s' % (my_filter_criterium, _orderby,
                                    '&$skip=0&$top=%s&$select=card'
                                    % self._maximum_items)
            result = self.client.get_resource('Presentations',
                                              query_options="$filter=%s"
                                              % my_filter)
            try:
                number_of_items = result.get('odata.count')
                if int(number_of_items) > int(self._maximum_items):
                    _warning = 'Too many items. Only showing %s from a total' \
                                ' of %s items' % (self._maximum_items,
                                                  number_of_items)
                for value in result['value']:
                    my_title = value['Title']
                    my_creation_date = value['CreationDate']
                    try:
                        _datetime_creation_date = parse(my_creation_date)
                        _format = '{:%s}' % self._date_format
                        my_creation_date = \
                            _format.format(_datetime_creation_date)
                    except:
                        pass
                    _presentation_cells += _tablerow % (value['Id'],
                                                        _table_cell_id,
                                                        my_creation_date,
                                                        my_title)

            except:
                pass
        if _presentation_cells == '':
            _warning = 'No result found, please rephrase your search'
        self.presentation_cells = _presentation_cells
        self.course_code = my_course_code
        return {'presentation_cells': self.presentation_cells,
                'course_code': self.course_code,
                'warning': _warning}

    @XBlock.json_handler
    def duration(self, data, suffix=''):
        '''
        Sets the duration of a presentation and composes a fresh mediasite url
        @param data: a dict, contains check, a start-time and an end-time
        @return: a default presentation selection
        '''
        assert data['check'] == 'duration'
        self.time_start = data['start-time'] or '00:00:00'
        self.time_end = data['end-time'] or '00:00:00'

        _time_start = self.time_start.split(':')
        _time_end = self.time_end.split(':')
        _play_from = int(_time_start[0]) * 3600000 + int(_time_start[1]) * \
            60000 + int(_time_start[2]) * 1000  # milliseconds
        _play_until = int(_time_end[0]) * 3600000 + int(_time_end[1]) * \
            60000 + int(_time_end[2]) * 1000  # milliseconds
        if _play_from > 0:
            self.x_play_from = str(_play_from)
        else:
            self.x_play_from = ''
        _duration = _play_until - _play_from  # milliseconds
        if _duration > 0:
            self.x_duration = str(_duration)
        else:
            self.x_duration = ''
        self.mediasite_url = self._set_mediasite_url()
        return {'def_presentation': self.def_presentation}

    def _set_mediasite_url(self):
        '''
        An internal method that composes a mediasite url using 'self' variables
        @return: a fresh mediasite url
        '''
        if self.x_presentation:
            _presentation = '%s' % self.x_presentation
        else:
            _presentation = ''
        if self.x_play_from:
            _play_from = '&playFrom=%s' % self.x_play_from
        else:
            _play_from = ''
        if self.x_duration:
            _duration = '&duration=%s' % self.x_duration
        else:
            _duration = ''
        _auto_start = '&autoStart=%s' % 'false'
        mediasite_link = '%s/Play/%s?%s%s%s' % (self._server_root,
                                                _presentation,
                                                _play_from,
                                                _duration,
                                                _auto_start)
        mediasite_link = mediasite_link.replace('?&', '?')
        return mediasite_link

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        '''
        Saves the entered scope based data
        @param data: a dict, contains check
        @return: a dict with a result of this action
        '''
        assert data['check'] == 'save'
        return {
            'result': 'success',
        }

    @XBlock.json_handler
    def studio_cancel(self, data, suffix=''):
        '''
        Clears and saves the scope based data
        @param data: a dict, contains check
        @return: a dict with a result of this action
        '''
        assert data['check'] == 'cancel'
        self.presentation_name = ''
        self.presentation_description = ''
        self.presentation_cells = ''
        self.course_code = ''
        self.mediasite_url = self._server_root
        self.x_duration = ''
        self.x_play_from = ''
        self.x_presentation = ''
        self.time_start = '00:00:00'
        self.time_end = '00:00:00'
        return {
            'result': 'cancelled',
        }

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("MediasiteXBlock",
             """<vertical_demo>
                <MediasiteXBlock/>
                </vertical_demo>
             """),
        ]

    """
    @XBlock.json_handler
    def set_presentation_period_filter(self, data, suffix=''):
        '''
        Filters a list of presentations according to the selected period
        @param data: a dict, contains check and a selected period
        @return: a dict with a filtered list of presentations
        '''
        assert data['check'] == 'period_filter'
        if self.client.is_authenticated():
            if 'period' in data:
                self.start_date = self.valid_periods[data['period']]
            self.presentation_options = \
                self._get_presentation_options(start_date = self.start_date)
            return {'presentation_options': self.presentation_options}
    """
