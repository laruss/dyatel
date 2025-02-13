from __future__ import annotations

import time
from io import BytesIO
from typing import Union, List, Any

from PIL import Image
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumWebDriver
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
from appium.webdriver.webelement import WebElement as AppiumWebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import (
    StaleElementReferenceException as SeleniumStaleElementReferenceException,
    InvalidArgumentException as SeleniumInvalidArgumentException,
    InvalidSelectorException as SeleniumInvalidSelectorException,
    NoSuchElementException as SeleniumNoSuchElementException,
    ElementNotInteractableException as SeleniumElementNotInteractableException,
    ElementClickInterceptedException as SeleniumElementClickInterceptedException,
)

from dyatel.dyatel_sel.sel_utils import ActionChains
from dyatel.js_scripts import get_element_size_js, get_element_position_on_screen_js
from dyatel.keyboard_keys import KeyboardKeys
from dyatel.mixins.log_mixin import LogMixin
from dyatel.shared_utils import cut_log_data
from dyatel.mixins.element_mixin import ElementMixin
from dyatel.mixins.driver_mixin import DriverMixin
from dyatel.exceptions import (
    TimeoutException,
    InvalidSelectorException,
    DriverWrapperException,
    NoSuchElementException,
    ElementNotInteractableException,
)
from dyatel.mixins.internal_utils import (
    WAIT_EL,
    get_child_elements,
    initialize_objects_with_args,
    get_platform_locator,
)


class CoreElement(ElementMixin, DriverMixin, LogMixin):

    def __init__(self, locator: str, locator_type: str, name: str, parent: Any, wait: bool):
        """
        Initializing of core element with appium/selenium driver
        Contain same methods/data for both WebElement and MobileElement classes

        :param locator: anchor locator of page. Can be defined without locator_type
        :param locator_type: specific locator type
        :param name: name of element (will be attached to logs)
        :param parent: parent of element. Can be Web/MobileElement, Web/MobilePage or Group objects
        """
        self._element: Union[SeleniumWebElement, None] = None
        self.__element: Union[SeleniumWebElement, None] = None

        self.locator = locator
        self.locator_type = locator_type
        self.name = name if name else self.locator
        self.parent: Any = parent
        self.wait = wait

        self.child_elements: List[CoreElement] = get_child_elements(self, CoreElement)
        initialize_objects_with_args(self.child_elements)  # required for Group

    # Element

    @property
    def element(self) -> SeleniumWebElement:
        """
        Get selenium WebElement object

        :return: Locator
        """
        return self._get_element(wait=True)

    @element.setter
    def element(self, selenium_element: SeleniumWebElement):
        """
        Current class element setter. Try to avoid usage of this function

        :param: selenium_element: selenium WebElement object, that will be set for current class
        """
        self._element = selenium_element

    # Element interaction

    def click(self) -> CoreElement:
        """
        Click to current element

        :return: self
        """
        self.log(f'Click into "{self.name}"')

        self.element = self._get_element()
        exception_msg = f'Element "{self.name}" not interactable {self.get_element_logging_data()}'

        try:
            self.wait_clickable(silent=True).element.click()
        except SeleniumElementNotInteractableException:
            raise ElementNotInteractableException(exception_msg) from None
        except SeleniumElementClickInterceptedException as exc:
            raise ElementNotInteractableException(f'{exception_msg}. Original error: {exc.msg}') from None
        finally:
            self.element = None

        return self

    def type_text(self, text: Union[str, KeyboardKeys], silent: bool = False) -> CoreElement:
        """
        Type text to current element

        :param: text: text to be typed
        :param: silent: erase log
        :return: self
        """
        text = str(text)

        if not silent:
            self.log(f'Type text {cut_log_data(text)} into "{self.name}"')

        self.element.send_keys(text)
        return self

    def type_slowly(self, text: str, sleep_gap: float = 0.05, silent: bool = False) -> CoreElement:
        """
        Type text to current element slowly

        :param: text: text to be slowly typed
        :param: sleep_gap: sleep gap before each key press
        :param: silent: erase log
        :return: self
        """
        text = str(text)

        if not silent:
            self.log(f'Type text "{cut_log_data(text)}" into "{self.name}"')

        element = self.element
        for letter in str(text):
            element.send_keys(letter)
            time.sleep(sleep_gap)
        return self

    def clear_text(self, silent: bool = False) -> CoreElement:
        """
        Clear text from current element

        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Clear text in "{self.name}"')

        self.element.clear()
        return self

    # Element waits

    def wait_element(self, timeout: int = WAIT_EL, silent: bool = False) -> CoreElement:
        """
        Wait for current element available in page

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait until presence of "{self.name}"')

        is_displayed = False
        start_time = time.time()
        while time.time() - start_time < timeout and not is_displayed:
            is_displayed = self.is_displayed(silent=True)

        if not is_displayed:
            base_exception_msg = f'Element "{self.name}" not visible after {timeout} seconds'
            raise TimeoutException(f'{base_exception_msg} {self.get_element_logging_data()}') from None

        return self

    def wait_element_hidden(self, timeout: int = WAIT_EL, silent: bool = False) -> CoreElement:
        """
        Wait until element hidden

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait hidden of "{self.name}"')

        is_hidden = False
        start_time = time.time()
        while time.time() - start_time < timeout and not is_hidden:
            is_hidden = self.is_hidden(silent=True)

        if not is_hidden:
            msg = f'"{self.name}" still visible after {timeout} seconds. {self.get_element_logging_data()}'
            raise TimeoutException(msg) from None

        return self

    def wait_clickable(self, timeout: int = WAIT_EL, silent: bool = False) -> CoreElement:
        """
        Wait until element clickable

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait until "{self.name}" become clickable')

        element = self.element
        is_clickable = False
        start_time = time.time()
        while time.time() - start_time < timeout and not is_clickable:
            is_clickable = element.is_enabled()

        if not is_clickable:
            msg = f'"{self.name}" not clickable after {timeout} seconds. {self.get_element_logging_data()}'
            raise TimeoutException(msg) from None

        return self

    def wait_availability(self, timeout: int = WAIT_EL, silent: bool = False) -> CoreElement:
        """
        Wait for current element available in DOM

        :param: timeout: time to stop waiting
        :param: silent: erase log
        :return: self
        """
        if not silent:
            self.log(f'Wait until "{self.name}" will be available in DOM')

        is_available = False
        start_time = time.time()
        while time.time() - start_time < timeout and not is_available:
            is_available = self.is_available()

        if not is_available:
            msg = f'"{self.name}" not available in DOM after {timeout} seconds. {self.get_element_logging_data()}'
            raise TimeoutException(msg) from None

        return self

    # Element state

    def scroll_into_view(self, block: str = 'center', behavior: str = 'instant',
                         sleep: Union[int, float] = 0) -> CoreElement:
        """
        Scroll element into view by js script

        :param: block: start - element on the top; end - element at the bottom
        :param: behavior: scroll type: smooth or instant
        :param: sleep: delay after scroll
        :return: self
        """
        self.log(f'Scroll element "{self.name}" into view')

        self.driver.execute_script(
            'arguments[0].scrollIntoView({{block: "{}", behavior: "{}"}});'.format(block, behavior), self.element
        )

        if sleep:
            time.sleep(sleep)

        return self

    def get_screenshot(self, filename: str) -> Image:
        """
        Taking element screenshot and saving with given path/filename

        :param filename: path/filename
        :return: image binary
        """
        self.log(f'Get screenshot of "{self.name}"')
        image_binary = self.screenshot_base
        image_binary.save(filename)
        return image_binary

    @property
    def screenshot_base(self) -> Image:
        """
        Get driver width scaled screenshot binary of element without saving

        :return: screenshot binary
        """
        element = self.element
        return self._scaled_screenshot(element.screenshot_as_png, element.size['width'])

    @property
    def text(self) -> str:
        """
        Get current element text

        :return: element text
        """
        return self.element.text

    @property
    def inner_text(self) -> str:
        """
        Get current element inner text

        :return: element inner text
        """
        return self.get_attribute('textContent', silent=True) or self.get_attribute('innerText', silent=True)

    @property
    def value(self) -> str:
        """
        Get value from current element

        :return: element value
        """
        return self.get_attribute('value', silent=True)

    def is_available(self) -> bool:
        """
        Check current element availability in DOM

        :return: True if present in DOM
        """
        elements = self._find_elements(self._get_base(wait=False))
        is_available = bool(len(elements))

        if is_available:
            self.__element = elements[0]

        return is_available

    def is_displayed(self, silent: bool = False) -> bool:
        """
        Check visibility of element

        :param: silent: erase log
        :return: True if element visible
        """
        if not silent:
            self.log(f'Check displaying of "{self.name}"')

        try:
            self.__element = self._get_element(wait=False)
            return self.__element.is_displayed()
        except (NoSuchElementException, DriverWrapperException, SeleniumStaleElementReferenceException):
            return False

    def is_hidden(self, silent: bool = False) -> bool:
        """
        Check invisibility of current element

        :param: silent: erase log
        :return: True if element hidden
        """
        if not silent:
            self.log(f'Check invisibility of "{self.name}"')

        return not self.is_displayed(silent=True)

    def get_attribute(self, attribute: str, silent: bool = False) -> str:
        """
        Get custom attribute from current element

        :param: attribute: custom attribute: value, innerText, textContent etc.
        :param: silent: erase log
        :return: custom attribute value
        """
        if not silent:
            self.log(f'Get "{attribute}" from "{self.name}"')

        return self.element.get_attribute(attribute)

    def get_elements_texts(self, silent: bool = False) -> List[str]:
        """
        Get all texts from all matching elements

        :param: silent: erase log
        :return: list of texts
        """
        if not silent:
            self.log(f'Get all texts from "{self.name}"')

        self.wait_element(silent=True)
        return list(element_item.text for element_item in getattr(self, 'all_elements'))

    def get_elements_count(self, silent: bool = False) -> int:
        """
        Get elements count

        :param: silent: erase log
        :return: elements count
        """
        if not silent:
            self.log(f'Get elements count of "{self.name}"')

        return len(getattr(self, 'all_elements'))

    def get_rect(self) -> dict:
        """
        A dictionary with the size and location of the element.

        :return: dict ~ {'y': 0, 'x': 0, 'width': 0, 'height': 0}
        """
        element = self.element
        size = self.driver.execute_script(get_element_size_js, element)
        location = self.driver.execute_script(get_element_position_on_screen_js, element)
        sorted_items: list = sorted({**size, **location}.items(), reverse=True)
        return dict(sorted_items)

    # Mixin

    def _get_wait(self, timeout: int = WAIT_EL) -> WebDriverWait:
        """
        Get wait with depends on parent element if available

        :return: driver
        """
        return WebDriverWait(self.driver, timeout)

    @property
    def _action_chains(self) -> ActionChains:
        """
        Get action chains with depends on parent element if available

        :return: ActionChains
        """
        return ActionChains(self.driver)

    def _scaled_screenshot(self, screenshot_binary: bin, width: int) -> Image:
        """
        Get scaled screenshot to fit driver window / element size

        :param screenshot_binary: original screenshot binary
        :param width: driver or element width
        :return: scaled image binary
        """
        img_binary = Image.open(BytesIO(screenshot_binary))
        scale = img_binary.size[0] / width

        if scale != 1:
            new_image_size = (int(img_binary.size[0] / scale), int(img_binary.size[1] / scale))
            img_binary = img_binary.resize(new_image_size, Image.Resampling.LANCZOS)

        return img_binary

    def _get_element(self, wait: bool = True) -> SeleniumWebElement:
        """
        Get selenium element from driver or parent element

        :param wait: wait for element or element parent before grab
        :return: SeleniumWebElement
        """
        element = self._element

        if not element:
            base = getattr(self.parent, '_element', None)

            if not base:
                base = self._get_base(wait=wait)

            try:
                element = self._find_element(base)
            except NoSuchElementException:
                element = None

            if not element and wait:
                try:
                    element = self.wait_element(silent=True).__element
                except TimeoutException:
                    element = None

        if not element:
            msg = f'Cant find element "{self.name}". {self.get_element_logging_data()}'
            raise NoSuchElementException(msg) from None

        return element

    def _get_base(self, wait: bool = True) -> Union[SeleniumWebDriver, SeleniumWebElement]:
        """
        Get driver with depends on parent element if available

        :return: driver
        """
        base = self.driver

        if not base:
            raise DriverWrapperException("Can't find driver") from None

        if self.driver_wrapper.mobile:
            if self.driver_wrapper.is_native_context:
                return base

        if self.parent:
            self.log(f'Get element "{self.name}" from parent element "{self.parent.name}"', level='debug')

            try:

                if isinstance(self.parent, CoreElement):
                    base = self.parent._get_element(wait=wait)
                else:
                    get_element_func = getattr(self.parent.anchor, '_get_element')
                    base = get_element_func(wait=wait)

            except NoSuchElementException:
                message = f'Cant find parent element "{self.parent.name}". {self.get_element_logging_data(self.parent)}'
                raise NoSuchElementException(message) from None

        return base

    def _find_element(self, base: Any) -> SeleniumWebElement:
        """
        Find selenium/appium element

        :param base: parent element/driver object
        :return: SeleniumWebElement or AppiumWebElement
        """
        try:
            return base.find_element(self.locator_type, get_platform_locator(self))
        except (SeleniumInvalidArgumentException, SeleniumInvalidSelectorException) as exc:
            self._raise_invalid_selector_exception(exc)
        except SeleniumNoSuchElementException as exc:
            raise NoSuchElementException(exc.msg) from None

    def _find_elements(self, base: Any) -> List[Union[SeleniumWebElement, AppiumWebElement]]:
        """
        Find all selenium/appium elements

        :param base: parent element/driver object
        :return: list of SeleniumWebElement or AppiumWebElement
        """
        try:
            return base.find_elements(self.locator_type, get_platform_locator(self))
        except (SeleniumInvalidArgumentException, InvalidSelectorException) as exc:
            self._raise_invalid_selector_exception(exc)

    def _raise_invalid_selector_exception(self, exc: Any) -> None:
        """
        Raises InvalidSelectorException if specific keywords in exception message

        :param exc: original exc object
        :return: None
        """
        if 'invalid locator' in exc.msg or 'is not a valid' in exc.msg:
            msg = f'Selector for "{self.name}" is invalid. {self.get_element_logging_data(self)}'
            raise InvalidSelectorException(msg) from None
        else:
            raise exc from None
