import frappe
from frappe.core.doctype.file.file import File


class S3File(File):
    def get_content(self, *args, **kwargs):
        """Fetch file content from S3 when the file is stored there,
        bypassing get_full_path() which can't resolve S3 API URLs."""
        if self._is_on_s3():
            if self.is_folder:
                frappe.throw(frappe._("Cannot get file contents of a Folder"))

            from frappe_s3_attachment.controller import S3Operations
            try:
                s3 = S3Operations()
                response = s3.read_file_from_s3(self.content_hash)
                self._content = response["Body"].read()
                return self._content
            except Exception:
                frappe.throw(
                    frappe._("Could not fetch file {0} from S3").format(self.file_name)
                )

        return super().get_content(*args, **kwargs)

    def _is_on_s3(self):
        return (
            self.content_hash
            and self.file_url
            and self.file_url.startswith(
                "/api/method/frappe_s3_attachment.controller.generate_file"
            )
        )
