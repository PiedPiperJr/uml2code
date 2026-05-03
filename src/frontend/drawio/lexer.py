import base64
import zlib

import xmltodict

from helpers.utils import lowercase_keys


class DrawIOLexer:
    """Tokenizes a draw.io XML file into one list of cell dicts per page."""

    def tokenize(self, xml_source: str) -> list[list[dict]]:
        data = xmltodict.parse(xml_source)
        data = lowercase_keys(data)

        diagrams = data["mxfile"]["diagram"]
        if isinstance(diagrams, dict):
            diagrams = [diagrams]

        return [cells for d in diagrams if (cells := self._page_cells(d))]

    # ── Per-page extraction ───────────────────────────────────────────────────

    def _page_cells(self, diagram: dict) -> list[dict]:
        model = self._get_model(diagram)
        if model is None:
            return []
        root = model.get("root", {})
        return self._collect_cells(root)

    def _get_model(self, diagram: dict) -> dict | None:
        if "mxgraphmodel" in diagram:
            return diagram["mxgraphmodel"]
        # Compressed diagram: content is Base64(deflate(mxGraphModel XML))
        content = diagram.get("#text", "").strip()
        if not content:
            return None
        try:
            xml = _decompress(content)
            return lowercase_keys(xmltodict.parse(xml)).get("mxgraphmodel")
        except Exception:
            return None

    def _collect_cells(self, root: dict) -> list[dict]:
        cells: list[dict] = []

        # Plain mxCell elements
        raw = root.get("mxcell", [])
        if isinstance(raw, dict):
            raw = [raw]
        cells.extend(raw)

        # UserObject / object wrappers (same semantics, two names)
        for key in ("userobject", "object"):
            raw = root.get(key, [])
            if isinstance(raw, dict):
                raw = [raw]
            for wrapper in raw:
                cell = _normalize_wrapper(wrapper)
                if cell:
                    cells.append(cell)

        return cells


# ── Module-level helpers ──────────────────────────────────────────────────────

def _decompress(text: str) -> str:
    """Base64-decode → raw-deflate-decompress → URL-decode a compressed diagram payload."""
    from urllib.parse import unquote
    raw = zlib.decompress(base64.b64decode(text), -15).decode("utf-8")
    return unquote(raw)


def _normalize_wrapper(wrapper: dict) -> dict | None:
    """Flatten a UserObject/object wrapper into a plain cell dict.

    The wrapper carries id + label; the nested mxCell carries style/vertex/parent.
    """
    inner = wrapper.get("mxcell", {})
    if not inner:
        return None
    cell = dict(inner)
    cell["@id"]    = wrapper.get("@id",    inner.get("@id", ""))
    cell["@value"] = wrapper.get("@label", wrapper.get("@value", ""))
    return cell
