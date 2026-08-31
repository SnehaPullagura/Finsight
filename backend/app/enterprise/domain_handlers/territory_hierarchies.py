from typing import Any, Dict, List, Optional

class TerritoryNode:
    def __init__(self, node_id: str, name: str, level: str, parent_id: Optional[str] = None):
        self.node_id = node_id
        self.name = name
        self.level = level # Global, Theater, Region, Area, Territory
        self.parent_id = parent_id
        self.children = []
        self.assigned_quota = 0.0

class EnterpriseTerritoryHierarchy:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node: TerritoryNode):
        self.nodes[node.node_id] = node
        if node.parent_id and node.parent_id in self.nodes:
            self.nodes[node.parent_id].children.append(node)

    def calculate_rollup_quota(self, node_id: str) -> float:
        if node_id not in self.nodes:
            return 0.0
        node = self.nodes[node_id]
        if not node.children:
            return node.assigned_quota
        return node.assigned_quota + sum(self.calculate_rollup_quota(c.node_id) for c in node.children)
