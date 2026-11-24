"""Official Python SDK for the Hypersender WhatsApp API, SMS API, and OTP API."""

__version__ = "1.0.1"

from ._base import HypersenderError
from ._client import Hypersender

__all__ = ["Hypersender", "HypersenderError", "__version__"]
