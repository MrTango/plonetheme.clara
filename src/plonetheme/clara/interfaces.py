"""Module where all interfaces, events and exceptions live."""

from plone.pageletlayout.interfaces import IPlonePageletlayoutLayer


class IPlonethemeClaraLayer(IPlonePageletlayoutLayer):
    """Marker interface that defines a browser layer.

    Extends the pagelet-layout layer so Clara's chrome-pagelet overrides
    (same provider name, this layer) are unambiguously more specific than
    the base registrations.
    """
