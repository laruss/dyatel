# Dyatel Changelog

---
## v1.3.4
*Release date: in development*
---

## v1.3.5
*Release date: 2022-01-17*

### Fixed
- Error logs fixes

## v1.3.3
*Release date: 2022-01-12*

### Changed
- `element.assert_screenshot` elements removal rework

## v1.3.2
*Release date: 2022-12-08*

### Added
- mobile `element.hide_keyboard` method added
- `fill_background` arg in `element.assert_screenshot`

### Changed
- ios safaridriver support removed
- reruns disabling for visual tests without references

### Fixed
- Pillow warning fixes
- other fixes and improvements


## v1.3.1
*Release date: 2022-12-02*

### Added
- `element.wait_element_hidden_without_error` method
- `element.assert_screenshot` hard reference generation support
- `element.assert_screenshot` soft reference generation fix
- `element.hover` silent argument

### Changed
- Reworked wait argument for `element`: False - wait element hidden; True - wait element visible
- `page.is_page_opened` without url support
- selenium - tags (locator type) updated

### Fixed
- DifferentDriverWrapper and elements initialization fixes


## v1.3.0
*Release date: 2022-10-18*

### Added 
- `driver_wrapper.get_inner_window_size` method
- `driver_wrapper.switch_to_frame` method for selenium based driver
- `driver_wrapper.switch_to_parent_frame` method for selenium based driver
- `driver_wrapper.switch_to_default_content` method for selenium based driver
- `driver_wrapper.delete_cookie` method for selenium/appium based driver
- `element.is_visible` method 
- `element.is_fully_visible` method
- `element.__repr__`, `checkbox.__repr__`, `group.__repr__`, `page.__repr__` 
- `scroll_into_view` before `element.click_into_center/hover/etc.` if element isn't visible
- `name_suffix` arg for `element.assert_screenshot` 
- Auto implemented `driver` in hidden object (function/property etc.) for `element/checkbox/group/page`
- Auto implemented `parent` in hidden object (function/property etc.) for `element/checkbox`
- Platform specific locator by object kwargs: ios/android/mobile/desktop

### Changed
- `element.get_rect` for selenium desktop
- All visual comparisons staff moved to `VisualComparison` class 
- Logging

### Fixed
- `get_object_kwargs` function
- `initialize_objects_with_args` function
- `element.assert_screenshot` driver name for remote
- Click by location after scroll

---
## v1.2.8
*Release date: 2022-09-20*

### Added 
- `driver_wrapper.is_native_context` property on mobile
- `driver_wrapper.is_web_context` property on mobile
- `driver_wrapper.visual_reference_generation` that disable AssertionError exception in `element.assert_screenshot`
- `ElementNotInteractableException` handler in `element.click`

### Changed
- `element.get_rect` output value sorting
- `PlayDriver`/`CoreDriver` class variables moved to `DriverWrapper`
- `os.environ['visual']` changed to `driver_wrapper.visual_regression_path`
- `element.wait_element` exception message
- Mobile: Finding elements in native context now skips parent

### Fixed
- `autolog` params
- `driver_wrapper.switch_to_tab` with default params

---
## v1.2.6/7
*Release date: 2022-09-15*

### Fixed
- screenshot name generation

---
## v1.2.5
*Release date: 2022-09-13*

### Added
- `element.click_into_center` method
- `driver_wrapper.click_by_coordinates` method

### Fixed
- `calculate_coordinate_to_click` calculation
- Shared object of groups become unique for each class

---
## v1.2.4
*Release date: 2022-09-08*

### Added
- `assert_screenshot()` elements removal

---
## v1.2.3
*Release date: 2022-09-02*

### Fixed
- `element.is_displayed()` exception handler

---
## v1.2.1/2
*Release date: 2022-08-31*

### Fixed
- Annotations

---
## v1.2.0
*Release date: 2022-08-31*

### Added
- [Allure Screen Diff Plugin](https://github.com/allure-framework/allure2/blob/master/plugins/screen-diff-plugin/README.md) support
- Driver specific logs 
- Custom exceptions
- Screenshot name generation in `assert_screenshot`
- `KeyboardKeys` class
- `element.send_keyboard_action` method

### Changed
- `get_text` property become `text`
- `get_value` property become `value`
- `get_screenshot_base` property become `screenshot_base`
- `get_inner_text` property become `inner_text`
- `by_attr` arg of `Checkbox` removed
- `calculate_coordinate_to_click` now calculate coordinates from element location

### Fixed
- Reduced count of `find_element` execution
- Page `driver_wrapper` getter exception

---
## v1.1.1
*Release date: 2022-08-10*

### Added
- iOS SafariDriver basic support 
- Different second driver support (for mobile/desktop safari)
- Tabs manipulating methods for desktop in `CoreDriver/PlayDriver`
- Context manipulating methods for mobile in `MobileDriver`
- [pytest-rerunfailures](https://pypi.org/project/pytest-rerunfailures/#pytest-rerunfailures) support
- Type annotations for most of code
- Auto `locator_type` support for `com.android` locator 
- `element.hover` support on mobiles
- `element.hover_outside` method, that moves pointer outside from current position
- `page.swipe(_up/_down)` methods for mobile  
- Default cookie path/domain in `driver_wrapper.set_cookie` method

### Changed
- `Driver` becomes `DriverWrapper` for more readability
- Mixins classes renamed and moved to `dyatel.mixins` folder
- Selenium `core_element.wait_element` now using `is_displayed`
- Selenium exception stacktrace reduced in most cases

### Fixed
- Custom `driver_wrapper`/`driver` for child elements
- Selenium `KeyError` of `driver_wrapper.set_cookie` without `domain` 
- Driver creation with function scope of pytest

---

## v1.1.0
*Release date: 2022-07-23*

### Added
- `Checkbox` class for Playwright and Selenium 
- `set_text` method in `Element` class
- `wait_elements_count` method in `Element` class
- `wait_element_text` method in `Element` class
- `wait_element_value` method in `Element` class
- `driver_wrapper` arg for `Group` and `Page`

### Changed
- Page/Group `set_driver` workflow
- `CorePage` and `PlayPage` methods moved to `Page` 

---

## v1.0.5
*Release date: 2022-07-10*

### Added
- `_first_element` property in `PlayElement`

### Changed
- `element` property replaced with `_first_element` for elements interactions
- `parent` nesting of `Element` changed from one level to endless
- `PlayElement` / `CoreElement` initialization

### Fixed
- `all_elements` execution time/nesting

---

## v1.0.4
*Release date: 2022-07-07*

### Added
- `set_driver` function for page object
- Multiple drivers support

### Changed
- Drivers initialization
- `driver`, `driver_wrapper` become property methods
