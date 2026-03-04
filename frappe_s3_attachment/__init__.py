# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__version__ = '0.0.4'

try:
    import frappe.utils.pdf as _frappe_pdf

    _original_inline_private_images = _frappe_pdf.inline_private_images

    def _inline_with_s3(html):
        from frappe_s3_attachment.controller import inline_s3_images
        html = inline_s3_images(html)
        return _original_inline_private_images(html)

    _frappe_pdf.inline_private_images = _inline_with_s3
except Exception:
    pass
