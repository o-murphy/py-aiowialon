from importlib import metadata

try:
    __version__ = metadata.version("py_aiowialon")
except metadata.PackageNotFoundError:
    __version__ = "undefined version"

__all__ = ("__version__",)
