import numpy as np
import plotly.graph_objects as go
import networkx as nx
from user_types import user_types


def get_layout(G, seed, dim=2):
    """Generates layout for either 2D or 3D layout."""
    if dim == 3:
        return nx.spring_layout(G, seed=seed, dim=3)
    else:
        return nx.spring_layout(G, seed=seed)


def generate_node_attributes(G, pos, dim=2):
    """Generate node attributes based on dimension (2D or 3D)."""
    node_x, node_y, node_z, node_text, node_color = [], [], [], [], []

    for node in G.nodes():
        x, y = pos[node][:2]  # First two coordinates for 2D/3D
        node_x.append(x)
        node_y.append(y)
        if dim == 3:
            z = pos[node][2]
            node_z.append(z)
        
        node_data = G.nodes[node]
        node_color.append(node_data["color"])
        node_text.append(
              f"User ID: {node}<br>User Type: {node_data['user_type']}<br>"
              f"Follower Count: {node_data['follower_count']}<br>"
              f"Following Count: {node_data['following_count']}<br>"
          )
    
    return node_x, node_y, node_z, node_text, node_color


def generate_edge_trace(pos, edges, color, width, name, dim=2, ):
    """Generate edge traces for either 2D or 3D plot."""
    edge_x, edge_y, edge_z = [], [], []
    for edge in edges:
        x0, y0 = pos[edge[0]][:2]
        x1, y1 = pos[edge[1]][:2]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
        
        if dim == 3:
            z0 = pos[edge[0]][2]
            z1 = pos[edge[1]][2]
            edge_z += [z0, z1, None]

    if dim == 3:
        return go.Scatter3d(x=edge_x, y=edge_y, z=edge_z, mode='lines', name=name, line=dict(color=color, width=width), hoverinfo='none')
    else:
        return go.Scatter(x=edge_x, y=edge_y, mode='lines', name=name, line=dict(color=color, width=width), hoverinfo='none')



def generate_node_trace(node_x, node_y, node_z, node_color, node_text, dim=2):
    """Generate node trace for either 2D or 3D plot."""
    if dim == 3:
        return go.Scatter3d(
            x=node_x, y=node_y, z=node_z,
            mode='markers',
            marker=dict(showscale=False, color=node_color, size=10, line=dict(width=1, color='black')),
            text=node_text,
            hoverinfo='text',
            name='User types'
        )
    else:
        return go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            marker=dict(showscale=False, color=node_color, size=10, line=dict(width=1, color='black')),
            text=node_text,
            hoverinfo='text',
            name='User types'
        )



def generate_legend_traces(user_types):
    """Generate legend traces for user types."""
    legend_traces = []
    for user_type, attributes in user_types.items():
        color = attributes["color"]
        legend_traces.append(go.Scatter(
            x=[None], y=[None],
            mode='markers',
            marker=dict(size=10, color=color),
            legendgroup=user_type,
            showlegend=True,
            name=user_type
        ))
    return legend_traces


def plot_X_network(G, seed, dim=2):
    pos = get_layout(G, seed, dim=dim)
    node_x, node_y, node_z, node_text, node_color = generate_node_attributes(G, pos, dim=dim)
    node_trace = generate_node_trace(node_x, node_y, node_z, node_color, node_text, dim=dim)

    mutual_edges, one_way_edges = [], []
    for u, v in G.edges():
        if G.has_edge(v, u):
            mutual_edges.append((u, v))
        else:
            one_way_edges.append((u, v))

    one_way_edge_trace = generate_edge_trace(pos, one_way_edges, 'gray', 1, 'One-way follow', dim=dim)
    mutual_edge_trace = generate_edge_trace(pos, mutual_edges, 'purple', 1.5, 'Mutual follow', dim=dim)

    user_type_legend = user_types.copy()
    user_type_legend['Agent'] = {'color': 'black'}
    legend_traces = generate_legend_traces(user_type_legend)

    layout = go.Layout(
        title="X Network Visualization (3D)" if dim == 3 else "X Network Visualization (2D)",
        showlegend=True,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        autosize=True, 
        height=800, 
        width=None,
        scene=dict(
            xaxis=dict(showbackground=False, showticklabels=False),
            yaxis=dict(showbackground=False, showticklabels=False),
            zaxis=dict(showbackground=False, showticklabels=False) if dim == 3 else None
        ) if dim == 3 else None,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False) if dim == 2 else None,
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False) if dim == 2 else None
    )

    fig = go.Figure(data=[one_way_edge_trace, mutual_edge_trace, node_trace] + legend_traces, layout=layout)
    fig.show()





