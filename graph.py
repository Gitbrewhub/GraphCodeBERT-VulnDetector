import networkx as nx
import plotly.graph_objects as go
import re

# ---------- FULL INTERACTIVE GRAPH ----------
def show_graph(code):
    G = nx.DiGraph()
    lines = code.strip().split("\n")
    prev = None

    for i, line in enumerate(lines):
        line = line.strip()
        if not line or "#include" in line:
            continue

        stmt = f"S{i+1}"
        G.add_node(stmt, type="stmt")

        if prev:
            G.add_edge(prev, stmt)
        prev = stmt

        variables = re.findall(r'\b[a-zA-Z_]\w*\b', line)

        for var in variables:
            if var in ["int", "char", "return"]:
                continue
            v = f"V:{var}"
            G.add_node(v, type="var")
            G.add_edge(v, stmt)

        funcs = re.findall(r'(\w+)\s*\(', line)

        for f in funcs:
            fn = f"F:{f}"
            G.add_node(fn, type="func")
            G.add_edge(stmt, fn)

            if f in ["strcpy", "gets", "scanf"]:
                G.nodes[fn]["danger"] = True
                G.nodes[stmt]["danger"] = True

    pos = nx.spring_layout(G, seed=42)

    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode='lines',
                            line=dict(width=1, color='gray'),
                            hoverinfo='none')

    node_x, node_y, colors, texts = [], [], [], []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        data = G.nodes[node]

        if data.get("danger"):
            colors.append("red")
        elif data["type"] == "stmt":
            colors.append("skyblue")
        elif data["type"] == "var":
            colors.append("lightgreen")
        else:
            colors.append("violet")

        texts.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=texts,
        textposition="top center",
        marker=dict(color=colors, size=20)
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(title="Interactive Dependency Graph", showlegend=False)

    return fig


# ---------- FOCUS GRAPH ----------
def show_vulnerability_graph(code):
    G = nx.DiGraph()
    lines = code.strip().split("\n")
    danger_funcs = ["strcpy", "gets", "scanf"]

    for i, line in enumerate(lines):
        for f in danger_funcs:
            if f in line:
                stmt = f"S{i+1}"
                func = f"F:{f}"

                G.add_node(stmt, color="red")
                G.add_node(func, color="red")
                G.add_edge(stmt, func)

    pos = nx.spring_layout(G, seed=42)

    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(x=edge_x, y=edge_y, mode='lines')

    node_x, node_y = [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=list(G.nodes),
        marker=dict(color="red", size=22)
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(title="🔥 Vulnerability Focus Graph")

    return fig