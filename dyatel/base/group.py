from __future__ import annotations

import copy
from typing import Any, Union

from dyatel.base.driver_wrapper import DriverWrapper
from dyatel.base.element import Element
from dyatel.mixins.driver_mixin import get_driver_wrapper_from_object
from dyatel.mixins.internal_utils import get_child_elements_with_names
from dyatel.mixins.previous_object_mixin import PreviousObjectDriver


class AfterInitMeta(type):
    """ Call a custom function right after __init__ of original class """

    def __call__(cls, *args, **kwargs):
        """
        Wrapper for calling a custom function right after __init__ of original class

        :param args: original class args
        :param kwargs: original class kwargs
        :return: class object
        """
        obj = type.__call__(cls, *args, **kwargs)
        obj.customise_children()
        return obj


class Group(Element, metaclass=AfterInitMeta):
    """ Group of elements. Should be defined as class """

    def __init__(self, locator: str = '', locator_type: str = '', name: str = '',
                 parent: Any = None, wait: bool = None, driver_wrapper: Union[DriverWrapper, Any] = None, **kwargs):
        """
        Initializing of group based on current driver

        :param locator: anchor locator of group. Can be defined without locator_type
        :param locator_type: Selenium only: specific locator type
        :param name: name of group (will be attached to logs)
        :param parent: parent of element. Can be Group or Page objects
        :param wait: include wait/checking of element in wait_page_loaded/is_page_opened methods of Page
        :param driver_wrapper: set custom driver for group and group elements
        :param kwargs:
          - desktop: str = locator that will be used for desktop platform
          - mobile: str = locator that will be used for all mobile platforms
          - ios: str = locator that will be used for ios platform
          - android: str = locator that will be used for android platform
        """
        self.locator = locator
        self.locator_type = locator_type
        self.name = name
        self.parent = parent
        self.wait = wait
        self._init_locals = locals()

        super().__init__(locator=self.locator, locator_type=self.locator_type, name=self.name, parent=self.parent,
                         wait=self.wait)
        # it's necessary to leave it after init
        if driver_wrapper:
            self._driver_instance = get_driver_wrapper_from_object(self, driver_wrapper)
            self.set_driver(self._driver_instance)
        elif self.driver_wrapper:
            PreviousObjectDriver().set_driver_from_previous_object_for_page_or_group(self, 6)

    def __repr__(self):
        return super().__repr__()

    def set_driver(self, driver_wrapper) -> Group:
        """
        Set driver instance for group and elements

        :param driver_wrapper: driver wrapper object ~ Driver/WebDriver/MobileDriver/CoreDriver/PlayDriver
        :return: self
        """
        if not driver_wrapper:
            return self

        self._set_driver(driver_wrapper, Element)
        return self

    def customise_children(self):
        """
        Set parent and custom driver for Group class variables, if their instance is Element class
        Will be called automatically after __init__ by metaclass `AfterInitMeta`
        """
        for name, value in get_child_elements_with_names(self, Element).items():
            setattr(self, name, copy.copy(value))
            value = getattr(self, name)
            if value.parent is None:
                value.parent = self
            else:
                setattr(value, 'parent', copy.copy(value.parent))
