# Copyright (C) 2017 Creu Blanca
# Copyright 2021 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnuorg/licenses/agpl.html).

import json
import logging

from werkzeug.urls import url_decode

from odoo.http import (
    content_disposition,
    request,
    route,
    serialize_exception as _serialize_exception,
)
from odoo.tools import html_escape
from odoo.tools.safe_eval import safe_eval, time

from odoo.addons.web.controllers import main as report

_logger = logging.getLogger(__name__)


class ReportController(report.ReportController):
    @route()
    def report_routes(self, reportname, docids=None, converter=None, **data):
        """ Тайлангийн төрөл "docx" байвал Word файлыг үүсгэж татаж авах механизмыг ажиллуулна """
        if converter == "docx":
            report = request.env["ir.actions.report"]._get_report_from_name(reportname)
            context = dict(request.env.context)
            if docids:
                docids = [int(i) for i in docids.split(",")]
            if data.get("options"):
                data.update(json.loads(data.pop("options")))
            if data.get("context"):
                data["context"] = json.loads(data["context"])
                context.update(data["context"])

            # Тайлан үүсгэх
            docx = report.with_context(**context)._render_docx(docids, data=data)[0]
            docx_http_headers = [
                ("Content-Type", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
                ("Content-Length", str(len(docx))),
            ]
            return request.make_response(docx, headers=docx_http_headers)

        return super(ReportController, self).report_routes(
            reportname, docids, converter, **data
        )

    @route()
    def report_download(self, data, context=None):
        """ Тайлан татах үед "docx" төрөл дээр ажиллах механизмыг нэмнэ """
        requestcontent = json.loads(data)
        url, report_type = requestcontent[0], requestcontent[1]

        if report_type == "docx":
            reportname = url
            try:
                reportname = url.split("/report/docx/")[1].split("?")[0]
                docids = None
                if "/" in reportname:
                    reportname, docids = reportname.split("/")
                if docids:
                    # Generic report:
                    response = self.report_routes(
                        reportname, docids=docids, converter="docx", context=context
                    )
                else:
                    # Particular report:
                    data = dict(url_decode(url.split("?")[1]).items())
                    if "context" in data:
                        context, data_context = json.loads(context or "{}"), json.loads(
                            data.pop("context")
                        )
                        context = json.dumps({**context, **data_context})
                    response = self.report_routes(
                        reportname, converter="docx", context=context, **data
                    )

                report = request.env["ir.actions.report"]._get_report_from_name(
                    reportname
                )
                filename = "%s.%s" % (report.name, "docx")

                if docids:
                    ids = [int(x) for x in docids.split(",")]
                    obj = request.env[report.model].browse(ids)
                    if report.print_report_name and not len(obj) > 1:
                        report_name = safe_eval(
                            report.print_report_name, {"object": obj, "time": time}
                        )
                        filename = "%s.%s" % (report_name, "docx")

                if not response.headers.get("Content-Disposition"):
                    response.headers.add(
                        "Content-Disposition", content_disposition(filename)
                    )
                return response

            except Exception as e:
                _logger.exception("Error while generating report %s", reportname)
                se = _serialize_exception(e)
                error = {"code": 200, "message": "Odoo Server Error", "data": se}
                return request.make_response(html_escape(json.dumps(error)))

        return super(ReportController, self).report_download(data, context)
