import pytest

from dyatel.base.checkbox import Checkbox
from dyatel.base.element import Element
from dyatel.base.group import Group
from dyatel.exceptions import UnsuitableArgumentsException
from dyatel.mixins.internal_utils import get_platform_locator


class ExtendedClass(Group):
    def __init__(self, locator='group1', name='group1'):
        super().__init__(locator=f'{locator} updated', name=name)


class SomeGroup(Group):
    def __init__(self):
        super().__init__('default_group', mobile='mobile_group')

    link_to_class = ExtendedClass('some locator', name='nested element')  # all elements initialised two times

    multiple_checkbox_partial = Checkbox(desktop='desktop_checkbox', mobile='mobile_checkbox', name='multiple checkbox all')
    multiple_element_partial = Element(desktop='desktop_locator', mobile='mobile_locator', name='multiple element all')
    multiple_element_all = Element(
        desktop='desktop_locator',
        ios='ios_locator',
        android='android_locator',
        name='multiple element all'
    )

    multiple_element_broken_ios = Element(ios='ios_locator', mobile='mobile_locator',
                                          name='multiple element broken ios')

    multiple_element_broken_android = Element(android='android_locator', mobile='mobile_locator',
                                              name='multiple element broken android')

    multiple_element_broken_all = Element(android='android_locator', ios='ios_locator', mobile='mobile_locator',
                                          name='multiple element broken all')


@pytest.mark.parametrize(
    'driver',
    ('mocked_selenium_driver', 'mocked_ios_driver', 'mocked_play_driver'),
    ids=['selenium', 'appium', 'playwright']
)
def test_link_to_class_locator(driver):
    assert SomeGroup().link_to_class.locator == 'some locator updated'


def test_multiple_locator_ios(mocked_ios_driver):
    assert 'ios_locator' in get_platform_locator(SomeGroup().multiple_element_all)
    assert 'mobile_group' in get_platform_locator(SomeGroup())


def test_multiple_locator_android(mocked_android_driver):
    assert 'android_locator' in get_platform_locator(SomeGroup().multiple_element_all)
    assert 'mobile_group' in get_platform_locator(SomeGroup())


def test_multiple_locator_selenium(mocked_selenium_driver):
    assert 'desktop_locator' in get_platform_locator(SomeGroup().multiple_element_all)
    assert 'default_group' in get_platform_locator(SomeGroup())


def test_multiple_locator_playwright(mocked_play_driver):
    assert 'desktop_locator' in get_platform_locator(SomeGroup().multiple_element_all)
    assert 'default_group' in get_platform_locator(SomeGroup())


@pytest.mark.parametrize(
    'driver',
    ('mocked_ios_driver', 'mocked_android_driver'),
    ids=['ios', 'android']
)
def test_multiple_locator_mobile(driver, request):
    request.getfixturevalue(driver)
    assert 'mobile_locator' in get_platform_locator(SomeGroup().multiple_element_partial)


@pytest.mark.parametrize(
    'driver',
    ('mocked_ios_driver', 'mocked_android_driver'),
    ids=['ios', 'android']
)
def test_multiple_locator_negative_all(driver, request):
    request.getfixturevalue(driver)
    try:
        get_platform_locator(SomeGroup().multiple_element_broken_all)
    except UnsuitableArgumentsException:
        pass
    else:
        raise AssertionError('Unexpected result')


def test_multiple_locator_negative_ios(mocked_ios_driver):
    try:
        get_platform_locator(SomeGroup().multiple_element_broken_ios)
    except UnsuitableArgumentsException:
        pass
    else:
        raise AssertionError('Unexpected result')


def test_multiple_locator_negative_android(mocked_android_driver):
    try:
        get_platform_locator(SomeGroup().multiple_element_broken_android)
    except UnsuitableArgumentsException:
        pass
    else:
        raise AssertionError('Unexpected result')
