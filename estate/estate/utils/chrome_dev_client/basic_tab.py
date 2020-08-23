"""
    Implement a abcstract class of `Chrome.Tab`

    Support callback method of chrome events

"""
from abc import ABCMeta
from abc import abstractmethod


class ChromeBasicTab(metaclass=ABCMeta):
    """Abstract class for Chrome Tab"""
    def __init__(self, tab):
        """Constructor

            @param tab: instance of Browser.Tab
            @type tab: object
        """
        # Data of response
        self._frame_id = None
        self._html_content = None
        # Handler
        self._tab = tab
        # Register Call back method
        self._tab.Network.requestWillBeSent = self._on_request_will_be_sent
        self._tab.Network.responseReceived = self._on_response_received
        self._tab.Page.frameStartedLoading = self._on_frame_started_loading
        self._tab.Page.frameStoppedLoading = self._on_frame_stopped_loading

    def _on_frame_started_loading(self, frameId):
        """Callback method for frame loading"""
        if not self._frame_id:
            self._frame_id = frameId

    @abstractmethod
    def _on_frame_stopped_loading(self, frameId):
        """Callback method  after frame loaded"""
        ...

    @abstractmethod
    def _on_request_will_be_sent(self, **kwargs):
        """Callback method before request"""
        ...

    @abstractmethod
    def _on_response_received(self, **kwargs):
        """Callback method after response received"""
        ...

    def _get_html_response(self):
        """Return html string"""
        self._tab.Page.stopLoading()

        root_dom = self._tab.DOM.getDocument()
        result = self._tab.DOM.getOuterHTML(
            nodeId=root_dom.get('root')['nodeId']
        )
        self._html_content = result['outerHTML']

        return self._html_content

    def _clear_context(self):
        """Reset data"""
        self._frame_id = None
        self._html_content = None

    def _goto_uri(self, uri, timeout=None, inject_js=None):
        """Request a url"""
        self._clear_context()

        self._tab.start()
        self._tab.Network.enable()
        self._tab.Page.enable()

        self.inject_javascript(inject_js)
        self._tab.Page.navigate(url=uri)

        if timeout:
            self._tab.wait(timeout)

    def inject_javascript(self, js_code):
        """Inject javascript code into chrome (best before windows.onload())"""
        if js_code:
            self._tab.Page.addScriptToEvaluateOnNewDocument(
                source=js_code
            )

    def wait_response(self, timeout):
        """Waiting for response"""
        if self._tab:
            self._tab.wait(timeout)
