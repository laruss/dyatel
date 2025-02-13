from dyatel.dyatel_sel.core.core_page import CorePage


class WebPage(CorePage):

    def __init__(self, locator: str, locator_type: str, name: str):
        """
        Initializing of web page with selenium driver

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of page (will be attached to logs)
        """
        super().__init__(locator=locator, locator_type=locator_type, name=name)
