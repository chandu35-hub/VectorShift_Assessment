from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# allow local frontend dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

@app.post('/pipelines/parse')
async def parse_pipeline(request: Request):
    payload = await request.json()
    nodes = payload.get('nodes', [])
    edges = payload.get('edges', [])

    node_ids = {n['id'] for n in nodes}

    # build adjacency from source -> target
    graph = {nid: [] for nid in node_ids}
    indegree = {nid: 0 for nid in node_ids}
    for e in edges:
        s = e.get('source')
        t = e.get('target')
        if s in node_ids and t in node_ids:
            graph[s].append(t)
            indegree[t] = indegree.get(t, 0) + 1

    # Kahn's algorithm for topological sort
    queue = [n for n, d in indegree.items() if d == 0]
    topo = []
    while queue:
        n = queue.pop(0)
        topo.append(n)
        for nb in graph.get(n, []):
            indegree[nb] -= 1
            if indegree[nb] == 0:
                queue.append(nb)

    is_dag = len(topo) == len(node_ids)

    return {
        'num_nodes': len(nodes),
        'num_edges': len(edges),
        'is_dag': is_dag,
        'topological_order': topo if is_dag else [],
    }

