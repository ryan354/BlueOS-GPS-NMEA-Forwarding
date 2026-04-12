import json
from pathlib import Path
from networkx.readwrite import json_graph
import networkx as nx
from graphify.export import to_obsidian, to_canvas
from graphify.cluster import score_all

data = json.loads(Path('graphify-out/graph.json').read_text())
G = json_graph.node_link_graph(data, edges='links')

communities = {}
for node_id, ndata in G.nodes(data=True):
    cid = ndata.get('community', 0)
    if cid not in communities:
        communities[cid] = []
    communities[cid].append(node_id)

labels = {
    0: "API Models & Forwarding Config",
    1: "Architecture Documentation",
    2: "Protocol Handlers (UDP/TCP)",
    3: "NMEA Sentence Generation",
    4: "MAVLink Reader & Polling",
    5: "FastAPI Routes & Endpoints",
    6: "Config Persistence",
    7: "NMEA Standard Reference",
    8: "Pydantic Config Models",
    9: "Project Identity",
    10: "Graphify Detection",
    11: "Web Dashboard",
    12: "Poll Rate Config"
}

cohesion = score_all(G, communities)

obsidian_dir = 'graphify-out/obsidian'

n = to_obsidian(G, communities, obsidian_dir, community_labels=labels or None, cohesion=cohesion)
print(f'Obsidian vault: {n} notes in {obsidian_dir}/')

to_canvas(G, communities, f'{obsidian_dir}/graph.canvas', community_labels=labels or None)
print(f'Canvas: {obsidian_dir}/graph.canvas')
print()
print(f'Open {obsidian_dir}/ as a vault in Obsidian.')
print('  Graph view   - nodes colored by community')
print('  graph.canvas - structured layout with communities as groups')
