# PyCPS 1.0.1

* Columns that are not parsable as numeric are now returned as strings. Previously, if any columns failed to parse as numeric an exception was raised. (https://github.com/matt-saenz/PyCPS/pull/3)

# PyCPS 1.0.0

* `get_asec()` and `get_basic()` no longer set an upper limit on supported years.

# PyCPS 0.2.0

* `get_asec()` now supports CPS ASEC microdata for 1992 to 2013.
* `get_basic()` now supports basic monthly CPS microdata for 2023.

# PyCPS 0.1.0

* Initial release.
