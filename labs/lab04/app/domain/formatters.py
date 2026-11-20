from abc import ABC, abstractmethod
import json
import re
from xml.etree.ElementTree import Element, SubElement, tostring

from app.support.types import event_dict


XML_UNSUPPORTED_CHAR = re.compile(r"[^\t\n\r\x20-\uD7FF\uE000-\uFFFD\U00010000-\U0010FFFF]")


class AuditFormatter(ABC):
    @abstractmethod
    def format(self, event):
        raise NotImplementedError


class TextAuditFormatter(AuditFormatter):
    def format(self, event):
        return f'{event.event_id}|{event.event_type}|{event.entity_id}'


class JsonAuditFormatter(AuditFormatter):
    def format(self, event):
        return json.dumps(event_dict(event), ensure_ascii=False)


class XmlAuditFormatter(AuditFormatter):
    def format(self, event):
        fields = event_dict(event)
        details = fields.pop("details")
        root = Element("event")
        for name, value in fields.items():
            SubElement(root, name).text = value

        details_element = SubElement(root, "details")
        for key, value in details.items():
            if XML_UNSUPPORTED_CHAR.search(key) or XML_UNSUPPORTED_CHAR.search(value):
                # XML 1.0 cannot represent some characters, even as references.
                detail = SubElement(details_element, "detail", encoding="json")
                detail.text = json.dumps([key, value])
            else:
                SubElement(details_element, "detail", key=key).text = value

        return tostring(root, encoding="unicode").replace("\r", "&#13;")
