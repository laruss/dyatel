import pytest
from selenium.webdriver.common.by import By

from dyatel.dyatel_sel.elements.mobile_element import MobileElement
from dyatel.dyatel_sel.elements.web_element import WebElement
from dyatel.dyatel_sel.pages.mobile_page import MobilePage
from dyatel.dyatel_sel.pages.web_page import WebPage
from dyatel.dyatel_sel.sel_utils import selenium_locator_types
from dyatel.exceptions import InvalidSelectorException
from dyatel.mixins.internal_utils import all_tags


tags = {'header h4', *all_tags}


@pytest.mark.parametrize('locator', ('.element', '[id *= element]', 'div#some_id'))
@pytest.mark.parametrize('base_class', (MobileElement, WebElement))
def test_base_class_auto_css_locator(locator, base_class):
    assert base_class(locator, '', '', '', False).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('locator', tags)
def test_base_class_auto_tag_name_locator(locator):
    assert WebElement(locator, '', '', '', False).locator_type == By.TAG_NAME


@pytest.mark.parametrize('locator', tags)
def test_base_class_auto_tag_name_locator_mobile(locator):
    assert MobileElement(locator, '', '', '', False).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('locator', ('//a', '/b', '//*[@contains(@class, "name") and .="name"]'))
@pytest.mark.parametrize('base_class', (MobileElement, WebElement))
def test_base_class_auto_xpath_locator(locator, base_class):
    assert base_class(locator, '', '', '', False).locator_type == By.XPATH


@pytest.mark.parametrize('locator', ('some-id', 'example__of--id'))
def test_base_class_auto_id_locator_web(locator):
    assert WebElement(locator, '', '', '', False).locator_type == By.ID


@pytest.mark.parametrize('locator', ('some-id', 'example__of--id', 'com.android.chrome:id/bottom_container'))
def test_base_class_auto_id_locator_mobile(locator):
    assert MobileElement(locator, '', '', '', False).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('base_class', (MobileElement, WebElement))
def test_specify_css_locator_type(base_class):
    assert base_class('[href="/loaddelay"]', By.CSS_SELECTOR, '', '', False).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('locator', tags)
def test_specify_class_name_locator_type_mobile(locator):
    assert WebElement(locator, By.CLASS_NAME, '', '', False).locator_type == By.CLASS_NAME


@pytest.mark.parametrize('locator', tags)
def test_specify_class_name_locator_type_web(locator):
    assert MobileElement(locator, By.CLASS_NAME, '', '', False).locator_type == By.CSS_SELECTOR


@pytest.mark.parametrize('base_class', (MobileElement, WebElement))
def test_name_missed(base_class):
    locator = '.sample .locator'
    assert base_class(locator, '', '', '', False).name == locator


@pytest.mark.parametrize('base_class', (MobileElement, WebElement))
def test_name_specified(base_class):
    locator, name = '.sample .locator', 'sample name'
    assert base_class(locator, '', name, '', False).name == name


@pytest.mark.parametrize('base_class', (MobileElement, WebElement))
@pytest.mark.parametrize('locator_type', selenium_locator_types)
def test_locator_type_given_instead_of_locator_element(base_class, locator_type):
    try:
        base_class(locator_type, '', '', '', False)
    except InvalidSelectorException:
        pass
    else:
        raise Exception('Unexpected behavior')


@pytest.mark.parametrize('base_class', (MobilePage, WebPage))
@pytest.mark.parametrize('locator_type', selenium_locator_types)
def test_locator_type_given_instead_of_locator_page(base_class, locator_type):
    try:
        base_class(locator=locator_type, locator_type='', name='')
    except InvalidSelectorException:
        pass
    else:
        raise Exception('Unexpected behavior')
