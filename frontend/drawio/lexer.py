import xmltodict
from helpers.utils import lowercase_keys


class DrawIOLexer:
    """Tokenizes a draw.io XML file into a flat list of raw cell dicts."""

    def tokenize(self, xml_source: str) -> list[dict]:
        data = xmltodict.parse(xml_source)
        data = lowercase_keys(data)

        diagram = data["mxfile"]["diagram"]
        if isinstance(diagram, dict):
            cells = diagram["mxgraphmodel"]["root"]["mxcell"]
        elif isinstance(diagram, list):
            cells = diagram[0]["mxgraphmodel"]["root"]["mxcell"]
        else:
            raise ValueError("No diagram found in the XML source")

        if isinstance(cells, dict):
            cells = [cells]

        return cells
