import logging

logger = logging.getLogger(__name__)

from .xml_obj import Symbol, DataType, SubItem
from .xml_collector import TmcFile

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
