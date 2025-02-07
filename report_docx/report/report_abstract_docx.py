# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging
from io import BytesIO
from odoo import models
from docx import Document

_logger = logging.getLogger(__name__)


class ReportDocxAbstract(models.AbstractModel):
    _name = "report.report_docx.abstract"
    _description = "Abstract DOCX Report"

    def _get_objs_for_report(self, docids, data):
        """
        Returns objects for DOCX report. Similar logic as XLSX.
        :param docids: list of integers, typically provided by qwebactionmanager for regular Models.
        :param data: dictionary of data, if present typically provided by qwebactionmanager for TransientModels.
        :return: recordset of active model for ids.
        """
        if docids:
            ids = docids
        elif data and "context" in data:
            ids = data["context"].get("active_ids", [])
        else:
            ids = self.env.context.get("active_ids", [])
        return self.env[self.env.context.get("active_model")].browse(ids)

    def create_docx_report(self, docids, data):
        """
        This function generates a DOCX report.
        """
        objs = self._get_objs_for_report(docids, data)
        file_data = BytesIO()
        doc = Document()
        
        # Call custom report function
        self.generate_docx_report(doc, data, objs)

        # Save document to memory
        doc.save(file_data)
        file_data.seek(0)
        return file_data.read(), "docx"

    def generate_docx_report(self, doc, data, objs):
        """
        This method must be overridden in the inherited model.
        Example:
        - Adding table with data
        - Adding headers and footers
        """
        raise NotImplementedError("You must implement 'generate_docx_report' in your subclass.")
