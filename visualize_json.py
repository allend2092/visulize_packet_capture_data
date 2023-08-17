import networkx as nx
import matplotlib.pyplot as plt
import json

# Specify the path to your JSON file
filename = "172-16-100-54-whats-app-video-call-sara.json"

# Load the data from the JSON file
with open(filename, 'r') as file:
    data = json.load(file)

# Now the 'data' variable contains the data from the JSON file
print(data)  # This will print the loaded data for verification

# Create a directed graph
G = nx.DiGraph()

# Add nodes and edges based on the flows
for flow in data["flows"]:
    src_ip = flow["source_ip"]
    dst_ip = flow["destination_ip"]
    bytes_transferred = flow["bytes_transferred"]

    # Add nodes
    G.add_node(src_ip)
    G.add_node(dst_ip)

    # Add or update edge
    if G.has_edge(src_ip, dst_ip):
        G[src_ip][dst_ip]["weight"] += bytes_transferred
    else:
        G.add_edge(src_ip, dst_ip, weight=bytes_transferred)

# Draw the graph
pos = nx.spring_layout(G)
edges = G.edges(data=True)
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, width=1)
edge_labels = {(u, v): f"{d['weight']} bytes" for u, v, d in edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

# Display the plot
plt.title("Network Flows Visualization")
plt.show()
