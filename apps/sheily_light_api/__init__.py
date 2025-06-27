"""SHEILY-light API package initializer.

Adds convenience alias so that internal modules can be imported via
`from sheily_modules.xxx import ...` regardless of whether the caller
is inside the `sheily_light_api` package or at project root.
"""

import importlib
import sys

# Register alias only if not already present
_pkg_name = __name__  # "sheily_light_api"
_modules_pkg_name = f"{_pkg_name}.sheily_modules"
_routers_pkg_name = f"{_pkg_name}.sheily_routers"

import types

# Provide legacy alias 'apps.sheily_light_api' expected by some modules
if "apps" not in sys.modules:
    sys.modules["apps"] = types.ModuleType("apps")
# alias packages under apps
sys.modules["apps"].sheily_light_api = sys.modules[_pkg_name]
sys.modules["apps.sheily_light_api"] = sys.modules[_pkg_name]

if "sheily_modules" not in sys.modules:
    sys.modules["sheily_modules"] = importlib.import_module(_modules_pkg_name)

# expose routers alias likewise
if "sheily_routers" not in sys.modules:
    sys.modules["sheily_routers"] = importlib.import_module(_routers_pkg_name)
    sys.modules["sheily_modules"] = importlib.import_module(_modules_pkg_name)
