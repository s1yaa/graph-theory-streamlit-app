import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import io
import sys
import contextlib
import math
import itertools
import random
import copy
import base64

student_name = "Siya Kolwalkar"
student_roll = "24B-CO-065"
student_sem = "4"

st.set_page_config(
    page_title="Graph Theory Lab",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700&display=swap');
    
    [data-testid="stHeader"], 
    [data-testid="stDecoration"],
    [data-testid="collapsedControl"],
    header,
    footer,
    #MainMenu {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }
    
    .stApp {
        background-color: #FFFFFF;
        color: #212121;
        font-family: 'Inter', sans-serif;
    }
    
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #F4F9F4 !important;
        border-right: 1px solid #E1EBE1;
        padding-top: 1.5rem;
    }
    
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] h3 {
        color: #1B5E20 !important;
        font-weight: 500 !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
        margin-top: 0;
        margin-bottom: 1rem;
    }
    
    section[data-testid="stSidebar"] button {
        display: none !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        border-bottom: 2px solid #E8F5E9;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #F5F5F5;
        border-radius: 6px 6px 0px 0px;
        border: 1px solid #E0E0E0;
        color: #616161;
        padding: 8px 20px;
        font-weight: 600;
        font-size: 15px;
        font-family: 'Inter', sans-serif;
        transition: all 0.2s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #E8F5E9;
        color: #2E7D32;
        border-color: #A5D6A7;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2E7D32 !important;
        color: #FFFFFF !important;
        border: 1px solid #2E7D32 !important;
        box-shadow: 0 4px 6px rgba(46, 125, 50, 0.15);
    }
    
    div.stButton > button {
        background-color: #2E7D32 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 24px !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
        box-shadow: 0 4px 10px rgba(46, 125, 50, 0.2) !important;
        transition: all 0.3s ease !important;
        cursor: pointer;
    }
    
    div.stButton > button:hover {
        background-color: #1B5E20 !important;
        box-shadow: 0 6px 14px rgba(27, 94, 32, 0.3) !important;
        transform: translateY(-1px);
    }
    
    .console-box {
        background-color: #0B130E;
        color: #A9DFBF;
        font-family: 'Courier New', Courier, monospace;
        padding: 18px;
        border-radius: 8px;
        border-left: 6px solid #2E7D32;
        margin-top: 15px;
        margin-bottom: 15px;
        white-space: pre-wrap;
        font-size: 14px;
        line-height: 1.5;
        max-height: 400px;
        overflow-y: auto;
        box-shadow: inset 0 0 15px rgba(0,0,0,0.6);
    }
    
    .console-header {
        font-family: 'Outfit', sans-serif;
        color: #2E7D32;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 5px;
        font-size: 15px;
    }
    
    .theory-box {
        background-color: #F9FDF9;
        border: 1px solid #C8E6C9;
        border-left: 5px solid #2E7D32;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 20px;
    }

    .date-box {
        background-color: #E8F5E9;
        border: 1px solid #A5D6A7;
        border-left: 5px solid #388E3C;
        padding: 10px 16px;
        border-radius: 8px;
        margin-bottom: 14px;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        color: #1B5E20;
        font-weight: 600;
    }
    
    .conclusion-box {
        background-color: #E8F5E9;
        border: 1px solid #C8E6C9;
        border-left: 5px solid #1B5E20;
        padding: 16px;
        border-radius: 8px;
        margin-top: 10px;
        margin-bottom: 20px;
        font-family: 'Inter', sans-serif;
        font-size: 15px;
        color: #1B5E20;
        line-height: 1.6;
    }
    
    .academic-footer {
        width: 100%;
        background-color: #F4F9F4;
        color: #1B5E20;
        text-align: center;
        padding: 18px 10px;
        border-top: 2px solid #A5D6A7;
        margin-top: 50px;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        border-radius: 8px;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.02);
    }
</style>
""", unsafe_allow_html=True)

def load_source_code_file(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return f"# [File '{filename}' not found in workspace directory]"
    except Exception as e:
        return f"# [Error loading file '{filename}': {str(e)}]"

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception:
        return ""

@contextlib.contextmanager
def capture_stdout():
    old_out = sys.stdout
    new_out = io.StringIO()
    sys.stdout = new_out
    try:
        yield new_out
    finally:
        sys.stdout = old_out

logo_base64 = get_base64_image("Goa_College_of_Engineering_logo.png")

st.sidebar.markdown("""
<h3 style="color: #1B5E20; font-family: 'Outfit', sans-serif; font-size: 21px; font-weight: 700; border-bottom: 2px solid #A5D6A7; padding-bottom: 8px; margin-bottom: 12px;">
    🔬 Experiment Hub
</h3>
""", unsafe_allow_html=True)

expt_choices = [
    "Experiment 1: Basic Graphs",
    "Experiment 2: Graph Isomorphism",
    "Experiment 3: Subgraphs",
    "Experiment 4: Degree Sequence",
    "Experiment 5: Line Graph",
    "Experiment 6: Kruskal Minimum Spanning Tree",
    "Experiment 7: Dijkstra's Shortest Path Algorithm",
    "Experiment 8: Closed Walks, Trails and Paths",
    "Experiment 9: Eulerian Circuits",
    "Experiment 10: Hamiltonian Circuits",
    "Experiment 11: Greedy Vertex Coloring"
]

selected_expt_label = st.sidebar.radio(
    "Select Graph Theory Experiment:",
    options=expt_choices,
    index=0
)

expt_num = int(selected_expt_label.split(" ")[1].split(":")[0])

header_logo_html = ""
if logo_base64:
    header_logo_html = f'<img src="data:image/png;base64,{logo_base64}" width="65" height="65" style="border-radius: 8px; background-color: white; padding: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);">'
else:
    header_logo_html = """<svg width="55" height="55" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="20" cy="50" r="10" fill="#1B5E20" />
        <circle cx="50" cy="20" r="10" fill="#2E7D32" />
        <circle cx="50" cy="80" r="10" fill="#2E7D32" />
        <circle cx="80" cy="50" r="10" fill="#1B5E20" />
        <line x1="20" y1="50" x2="50" y2="20" stroke="#4CAF50" stroke-width="4" />
        <line x1="20" y1="50" x2="50" y2="80" stroke="#4CAF50" stroke-width="4" />
        <line x1="50" y1="20" x2="80" y2="50" stroke="#4CAF50" stroke-width="4" />
        <line x1="50" y1="80" x2="80" y2="50" stroke="#4CAF50" stroke-width="4" />
        <line x1="50" y1="20" x2="50" y2="80" stroke="#81C784" stroke-width="2.5" stroke-dasharray="6" />
        <circle cx="50" cy="50" r="12" fill="#4CAF50" fill-opacity="0.25" />
    </svg>"""

st.markdown(f"""
<div class="academic-header" style="display: flex; align-items: center; gap: 20px; border-bottom: 3px solid #2E7D32; padding-bottom: 15px; margin-bottom: 25px;">
    {header_logo_html}
    <div>
        <h1 style="margin: 0; color: #1B5E20; font-family: 'Outfit', sans-serif; font-size: 30px; font-weight: 700; letter-spacing: -0.5px;">CMP-226 Graph Theory and Combinatorics Lab</h1>
    </div>
</div>
""", unsafe_allow_html=True)

experiments_metadata = {
    1: {
        "title": "Basic Graphs ",
        "date": "3 February 2026",
        "filenames": ["graph.py", "graph2.py"],
        "aim": "To implement basic graphs such as null graph, complete graph, cycle graph, path graph, complete bipartite graph and wheel graph.",
        "theory": """
        Graphs are fundamental mathematical structures used to model pairwise relations between objects. A graph $G = (V, E)$ consists of a set of vertices $V$ and a set of edges $E$. 
        In this experiment, we explore six fundamental simple graph families:
        
        1. **Null Graph ($N_n$):** A graph containing $n$ isolated vertices and zero edges ($E = \\emptyset$).
        2. **Complete Graph ($K_n$):** A simple graph with $n$ vertices where a unique edge connects every pair of distinct vertices. It contains exactly $\\frac{n(n-1)}{2}$ edges.
        3. **Path Graph ($P_n$):** A graph of order $n$ whose vertices can be listed in the order $v_1, v_2, \\dots, v_n$ such that the edges are $(v_i, v_{i+1})$ for $1 \\le i < n$.
        4. **Complete Bipartite Graph ($K_{m,n}$):** A bipartite graph where the vertex set is partitioned into two disjoint subsets $V_1$ (size $m$) and $V_2$ (size $n$) such that every vertex in $V_1$ is connected by a unique edge to every vertex in $V_2$, and no edges exist within $V_1$ or $V_2$.
        5. **Cycle Graph ($C_n$):** A closed path graph with $n$ vertices ($n \\ge 3$) where the vertices form a single closed loop.
        6. **Wheel Graph ($W_n$):** Formed by connecting a single universal hub vertex to all vertices of a cycle graph $C_{n-1}$ of order $n-1$.
        """,
        "conclusion": "Basic graphs such as null graph, complete graph, cycle graph, path graph, complete bipartite graph, and wheel graph were successfully implemented and visualized using Python and NetworkX without using built-in graph generation functions."
    },
    2: {
        "title": "Graph Isomorphism ",
        "date": "10 February 2026",
        "filenames": ["isomorphism.py", "isomorphism2.py"],
        "aim": "To implement graph isomorphism verification in order to compare structural equivalence between two graphs.",
        "theory": """
        ### What is Isomorphism?
        
        **General Definition:**
        In general, two graphs $G$ and $H$ are said to be **isomorphic** (written $G \\cong H$, or sometimes $G = H$) if there are bijections $\\theta: V(G) \\to V(H)$ and $\\phi: E(G) \\to E(H)$ such that $\\psi_G(e) = uv$ if and only if $\\psi_H(\\phi(e)) = \\theta(u)\\theta(v)$; such a pair $(\\theta, \\phi)$ of mappings is called an isomorphism between $G$ and $H$.
        

        **Simple Graph Case:**
        For simple graphs (without multiple edges or self-loops), this simplifies nicely: Two simple graphs $G_1 = (V_1, E_1)$ and $G_2 = (V_2, E_2)$ are **isomorphic** (denoted $G_1 \\cong G_2$) if there exists a bijective function (one-to-one and onto mapping) $f: V_1 \\to V_2$ such that:
        $$(u, v) \\in E_1 \\iff (f(u), f(v)) \\in E_2 \\quad \\forall u,v \\in V_1$$
        This bijection $f$ preserves both adjacency and non-adjacency. If such a mapping exists, the graphs are structurally identical, differing only in vertex labels or layout.

        
        ### How Can We Check if Two Graphs are Isomorphic?
        
        To determine if two graphs are isomorphic, we check **Graph Invariants**—structural properties that must remain unchanged under isomorphism. If any of these necessary conditions fail, the graphs are definitely **NOT** isomorphic:
        
        1. **Number of Vertices ($|V_1| = |V_2|$):** Both graphs must have the exact same number of nodes.
        2. **Number of Edges ($|E_1| = |E_2|$):** Both graphs must have the exact same number of edges.
        3. **Degree Sequence:** The sorted list of vertex degrees must be identical (e.g., if one graph has three vertices of degree 3, the other must as well).
        4. **Cycle Structure:** Both graphs must contain the same number of cycles of specific lengths (e.g., number of triangles, 4-cycles, etc.).
        
        """,
        "conclusion": "Graph isomorphism verification for comparing structural equivalence between two graphs was successfully implemented."
    },
    3: {
        "title": "Subgraphs ",
        "date": "17 February 2026",
        "filenames": ["subgraph.py", "subgraph2.py"],
        "aim": "To implement and generate different types of subgraphs such as spanning subgraph, vertex-induced subgraph, and edge-induced subgraph from a given graph.",
        "theory": """
        ### Definition of a Subgraph
        
        A graph $H$ is a **subgraph** of $G$ (written $H \\subseteq G$) if:
        1. $V(H) \\subseteq V(G)$ (the vertex set of $H$ is a subset of $G$'s vertex set).
        2. $E(H) \\subseteq E(G)$ (the edge set of $H$ is a subset of $G$'s edge set).
        3. The incidence function $\\psi_H$ is the restriction of $\\psi_G$ to $E(H)$.
        
        * **Proper Subgraph:** When $H \\subseteq G$ but $H \\neq G$, we write $H \\subset G$ and call $H$ a **proper subgraph** of $G$.
        * **Supergraph:** If $H$ is a subgraph of $G$, then $G$ is a **supergraph** of $H$.
        * **Spanning Subgraph:** A subgraph (or spanning supergraph) $H$ of $G$ is a subgraph with $V(H) = V(G)$ (it contains all vertices of $G$).

        
        ### Underlying Simple Graph
        By deleting from $G$ all loops and, for every pair of adjacent vertices, all but one link/edge joining them, we obtain a simple spanning subgraph of $G$, called the **underlying simple graph** of $G$.

        
        ### Induced Subgraphs
        
        #### 1. Vertex-Induced Subgraph ($G[V']$)
        Suppose that $V'$ is a nonempty subset of $V$. The subgraph of $G$ whose vertex set is $V'$ and whose edge set consists of all edges of $G$ that have both endpoints in $V'$ is called the **subgraph of $G$ induced by $V'$** and is denoted by $G[V']$.
        
        * **Vertex Deletion ($G - V'$):** The induced subgraph $G[V \\setminus V']$ is denoted by $G - V'$; it is the subgraph obtained from $G$ by deleting the vertices in $V'$ together with their incident edges. 
        * For a single vertex $v$, we write $G - v$ instead of $G - \\{v\\}$.
        
        #### 2. Edge-Induced Subgraph ($G[E']$)
        Suppose that $E'$ is a nonempty subset of $E$. The subgraph of $G$ whose vertex set is the set of ends of edges in $E'$ and whose edge set is $E'$ is called the **subgraph of $G$ induced by $E'$** and is denoted by $G[E']$.
        
        * **Edge Deletion ($G - E'$):** The spanning subgraph of $G$ with edge set $E \\setminus E'$ is written as $G - E'$; it is the subgraph obtained from $G$ by deleting the edges in $E'$. 
        * For a single edge $e$, we write $G - e$ instead of $G - \\{e\\}$.
        * **Edge Addition ($G + E'$):** The graph obtained from $G$ by adding a set of edges $E'$ is denoted by $G + E'$. For a single edge $e$, we write $G + e$ instead of $G + \\{e\\}$.
        """,
        "conclusion": "Generation and visualization of spanning, induced, and edge-induced subgraphs from a given graph was successfully implemented."
    },
    4: {
        "title": "Degree Sequence ",
        "date": "23 February 2026",
        "filenames": ["degreesequence.py", "degreesequence2.py"],
        "aim": "To determine and construct a graph corresponding to a given degree sequence and verify whether the sequence is graphical.",
        "theory": """
        ### What is the Degree of a Vertex?
        The **degree** of a vertex $v$, denoted by $d(v)$ or $deg(v)$, is the number of edges incident to $v$ in a graph $G$.
        * In general graphs, a loop incident on a vertex contributes $2$ to its degree.
        * **Handshaking Lemma:** The sum of degrees of all vertices in any graph is equal to twice the number of edges:
          $$\\sum_{v \\in V} d(v) = 2|E|$$
          An immediate consequence of this lemma is that any graph must have an **even number of vertices of odd degree**.

        
        ### What is a Degree Sequence?
        A **degree sequence** of a graph is a list of the degrees of its vertices, typically written in non-increasing (descending) order:
        $$S = (d_1, d_2, \\dots, d_n) \\quad \\text{where } d_1 \\ge d_2 \\ge \\dots \\ge d_n$$

        
        ### What is "Graphical"?
        A sequence of non-negative integers $S = (d_1, d_2, \\dots, d_n)$ is called **graphical** (or **realizable**) if there exists a **simple** undirected graph $G$ (containing no loops or multiple/parallel edges) whose vertex degrees are exactly the terms of the sequence.

        
        ### The Havel-Hakimi Theorem
        The **Havel-Hakimi Theorem** (1955, 1962) provides a necessary and sufficient recursive method to determine whether a given degree sequence is graphical.
        
        **Theorem:**
        Let $S = (d_1, d_2, \\dots, d_n)$ be a finite sequence of non-negative integers sorted in non-increasing order ($d_1 \\ge d_2 \\ge \\dots \\ge d_n$) with $d_1 > 0$. The sequence $S$ is graphical if and only if the reduced sequence:
        $$S' = (d_2 - 1, d_3 - 1, \\dots, d_{d_1 + 1} - 1, d_{d_1+2}, \\dots, d_n)$$
        is also graphical, after sorting it in non-increasing order.

        
        ### Step-by-Step Havel-Hakimi Algorithm
        
        1. **Sort:** Arrange the sequence in non-increasing (descending) order.
        2. **Check Base Cases:**
           * If the sequence consists entirely of $0$s, it is **graphical** (corresponds to an empty/null graph). Stop.
           * If any element in the sequence is negative, or if the first element $d_1$ exceeds the number of remaining elements (meaning $d_1 \\ge n$), the sequence is **NOT graphical**. Stop.
        3. **Reduce:**
           * Remove the first element $d_1$.
           * Subtract $1$ from each of the next $d_1$ elements in the sequence.
        4. **Repeat:** Repeat the process starting from Step 1.
        
        """,
        "conclusion": "Construction of a graph corresponding to a given degree sequence using the Havel–Hakimi method was successfully implemented."
    },
    5: {
        "title": "Line Graph ",
        "date": "10 March 2026",
        "filenames": ["linegraph.py", "linegraph2.py"],
        "aim": "Convert the original graph into its line graph, where each edge of the original graph becomes a vertex in the new graph, and adjacency is defined by shared endpoints in the original graph.",
        "theory": """
        The **Line Graph** $L(G)$ of an undirected graph $G$ represents the adjacencies between the edges of $G$. In other words, $L(G)$ shifts the focus from vertices to edges.
        
        **Definition:**
        Given a graph $G = (V, E)$, its line graph $L(G)$ is a graph such that:
        1. Each vertex of $L(G)$ represents an edge of $G$.
        2. Two vertices in $L(G)$ are connected by an edge if and only if their corresponding edges in $G$ share a common endpoint (are adjacent in $G$).
        
        **Properties:**
        * If $G$ is a cycle graph $C_n$, then $L(G) \\cong C_n$.
        * If $G$ is a star graph $K_{1,k}$, then its line graph $L(G)$ is a complete graph $K_k$.
        * The number of vertices in $L(G)$ is equal to $|E(G)|$.
        * The number of edges in $L(G)$ is given by $\\sum_{v \\in V} \\frac{deg(v)(deg(v)-1)}{2}$.
        """,
        "conclusion": "Construction of a line graph from a given graph using adjacency matrix, both with and without NetworkX functions, was successfully implemented."
    },
    6: {
        "title": "Kruskal Minimum Spanning Tree ",
        "date": "24 March 2026",
        "filenames": ["MST.py", "MST2.py"],
        "aim": "To implement Kruskal’s Algorithm to generate the minimum spanning tree, ensuring all vertices are connected with minimum possible total edge weight and without cycles.",
        "theory": """
        ### Spanning Tree & Minimum Spanning Tree (MST)
        A **Spanning Tree** of a connected graph $G$ is a spanning subgraph that is a tree (connected and containing no cycles). 
        For a weighted graph, the **Minimum Spanning Tree (MST)** is a spanning tree whose total sum of edge weights is minimized:
        $$w(T) = \\sum_{e \\in E(T)} w(e) \\quad \\text{is minimized}$$

        
        ### Kruskal's Algorithm 
        The formal mathematical statement of Kruskal's algorithm is defined as follows:
        
        1. **Step 1:** Choose a link $e_1$ such that $w(e_1)$ is as small as possible.
        2. **Step 2:** If edges $e_1, e_2, \\dots, e_i$ have been chosen, then choose an edge $e_{i+1}$ from $E \\setminus \\{e_1, e_2, \\dots, e_i\\}$ in such a way that:
           * **(i)** the subgraph $G[\\{e_1, e_2, \\dots, e_{i+1}\\}]$ is acyclic (contains no cycles);
           * **(ii)** $w(e_{i+1})$ is as small as possible subject to condition **(i)**.
        3. **Step 3:** Stop when Step 2 cannot be implemented further.
        
        """,
        "conclusion": "Kruskal’s Algorithm to generate the minimum spanning tree, ensuring all vertices are connected with minimum possible total edge weight and without cycles was successfully implemented."
    },
    7: {
        "title": "Dijkstra's Shortest Path Algorithm ",
        "date": "31 March 2026",
        "filenames": ["spa.py", "spa2.py"],
        "aim": "To implement Shortest Path Algorithm in order to compute the shortest path between two vertices in a weighted graph.",
        "theory": """
        ### What is a Weighted Graph?
        A **weighted graph** is a graph in which a real number (called a **weight**) is assigned to each edge. Formally, a weighted graph is a pair $(G, w)$, where:
        * $G = (V, E)$ is a graph.
        * $w: E \\to \\mathbb{R}$ is a weight function that maps each edge $e \\in E$ to a real number $w(e)$ (representing physical distance, cost, time, or capacity).
        
        The weight of a path $P$, denoted by $w(P)$, is the sum of the weights of the edges belonging to $P$:
        $$w(P) = \\sum_{e \\in E(P)} w(e)$$
        The **shortest path** between two vertices $u$ and $v$ is a path $P$ connecting them such that $w(P)$ is minimized.

        
        ### Dijkstra's Algorithm
        Dijkstra's Algorithm is a greedy algorithm used to find the shortest paths from a single source vertex $u_0$ to all other vertices in a weighted graph with non-negative edge weights.
        
        #### Algorithmic Steps:
        1. **Step 1:** Set $l(u_0) = 0$, $l(u) = \\infty$ for all $u \\neq u_0$, $S_0 = \\{u_0\\}$, and $i = 0$. *(Here, $l(v)$ represents the tentative distance label of vertex $v$, and $S_i$ is the set of vertices with finalized shortest paths).*
        2. **Step 2:** For each $v \\notin S_i$, replace $l(v)$ by:
           $$\\min\\{l(v), l(u_i) + w(u_i, v)\\}$$
           Compute $\\min_{v \\notin S_i} \\{l(v)\\}$ and let $u_{i+1}$ denote a vertex for which this minimum is attained. Set:
           $$S_{i+1} = S_i \\cup \\{u_{i+1}\\}$$
        3. **Step 3:** If $i = \\nu - 1$ (where $\\nu = |V|$ is the total number of vertices), **stop**. If $i < \\nu - 1$, replace $i$ by $i + 1$ and go to **Step 2**.
        """,
        "conclusion": "Shortest Path Algorithm in order to compute the shortest path between two vertices in a weighted graph was successfully implemented."
    },
    8: {
        "title": "Closed Walks, Trails and Paths",
        "date": "7 April 2026",
        "filenames": ["walks.py", "walks2.py"],
        "aim": "To implement generation of closed walks, trails and paths in a connected graph.",
        "theory": """
        ### Walks in Graphs
        A **walk** in a graph $G$ is a finite non-null sequence:
        $$W = v_0 e_1 v_1 e_2 v_2 \\dots e_k v_k$$
        whose terms are alternately vertices and edges, such that for $1 \\le i \\le k$, the endpoints of edge $e_i$ are $v_{i-1}$ and $v_i$.
        
        * We say that $W$ is a **walk from $v_0$ to $v_k$**, or a **$(v_0, v_k)$-walk**.
        * The vertices $v_0$ and $v_k$ are called the **origin** and **terminus** of $W$, respectively.
        * The vertices $v_1, v_2, \\dots, v_{k-1}$ are called its **internal vertices**.
        * The integer $k$ is the **length** of $W$.

        
        ### Classification of Walks
        
        * **Walk:** Alternating sequence of vertices and edges. Vertices and edges can be repeated.
        * **Closed Walk:** A walk is **closed** if it has positive length ($k > 0$) and its origin and terminus are identical ($v_0 = v_k$).
        * **Trail:** A walk $W$ in which all the edges $e_1, e_2, \\dots, e_k$ are **distinct** (no edge is repeated). The length of $W$ is just the number of edges, denoted by $e(W)$.
        * **Path:** A trail in which the vertices $v_0, v_1, \\dots, v_k$ are also **distinct** (no vertex, and consequently no edge, is repeated). We also use the word 'path' to denote the graph or subgraph whose vertices and edges are the terms of the path.
        """,
        "conclusion": "Generation of closed walks, trails and paths in a connected graph was successfully implemented."
    },
    9: {
        "title": "Eulerian Circuits ",
        "date": "28 April 2026",
        "filenames": ["eularian.py", "eularian2.py"],
        "aim": "To implement an algorithm that checks for the existence of an eularian circuit and constructs a circuit that traverses every edge of the graph exactly once.",
        "theory": """
        ### Eulerian Trail and Eulerian Circuit
        
        * **Eulerian Trail:** An Eulerian trail (or Eulerian path) in a graph $G$ is a trail that visits **every edge** of $G$ exactly once.
        * **Eulerian Circuit:** An Eulerian circuit (or Eulerian cycle) in $G$ is a **closed walk** that is a trail and visits **every edge** of $G$ exactly once (starts and ends at the same vertex, traversing each edge precisely once).
        * A graph $G$ is called **Eulerian** if it contains an Eulerian circuit.

        
        ### Euler's Theorem
        
        * **Theorem 1 (Eulerian Circuit):** A connected undirected graph $G$ has an Eulerian circuit if and only if **every vertex in $G$ has an even degree**.
        * **Theorem 2 (Eulerian Trail):** A connected undirected graph $G$ has an Eulerian trail (but not an Eulerian circuit) if and only if it has **exactly two vertices of odd degree**. Furthermore, the trail must start at one of these odd-degree vertices and end at the other.

        
        ### Fleury's Algorithm
        Fleury's Algorithm is a classical method to construct an Eulerian circuit (or trail) by systematically traversing the edges of a graph without getting stuck in isolated components.
        
        #### Algorithmic Steps:
        1. **Step 1:** Choose an arbitrary vertex $v_0$, and set $W_0 = v_0$.
        2. **Step 2:** Suppose that the trail $W_i = v_0 e_1 v_1 \\dots e_i v_i$ has been chosen. Then choose an edge $e_{i+1}$ from $E \\setminus \\{e_1, e_2, \\dots, e_i\\}$ in such a way that:
           * **(i)** $e_{i+1}$ is incident with $v_i$;
           * **(ii)** unless there is no alternative, $e_{i+1}$ is **not a cut-edge (bridge)** of the remaining subgraph $G_i = G \\setminus \\{e_1, e_2, \\dots, e_i\\}$.
        3. **Step 3:** Stop when Step 2 can no longer be implemented.
        """,
        "conclusion": "An algorithm that checks for the existence of an eularian circuit and constructs a circuit that traverses every edge of the graph exactly once was successfully implemented."
    },
    10: {
        "title": "Hamiltonian Circuits ",
        "date": "5 May 2026",
        "filenames": ["hamiltonian.py"],
        "aim": "To implement a method that determines whether a graph contains a hamiltonian circuit, that is a cycle that visits every vertex exactly once except the starting vertex.",
        "theory": """
        A **Hamiltonian Path** is a path that visits every vertex in the graph exactly once.
        A **Hamiltonian Circuit (Cycle)** is a closed loop that visits every vertex in the graph exactly once and returns to the starting vertex.
        
        **Backtracking Algorithm:**
        To identify all Hamiltonian circuits, we use a recursive depth-first search:
        1. Start at a designated vertex $v_0$.
        2. Recursively add adjacent vertices to a path list if they have not been visited yet.
        3. If the path list contains all $|V|$ vertices, check if there is an edge connecting the last vertex back to the start vertex $v_0$.
           * If yes, a Hamiltonian circuit is found! We record it.
        4. Backtrack: remove the last added vertex and try other neighbors.
        """,
        "conclusion": "A method that determines whether a graph contains a hamiltonian circuit, that is a cycle that visits every vertex exactly once except the starting vertex was successfully implemented."
    },
    11: {
        "title": "Greedy Vertex Coloring ",
        "date": "12 May 2026",
        "filenames": ["vertexcoloring.py", "vertexcoloring2.py"],
        "aim": "To implement Greedy graph coloring algorithm that assigns colors to the vertices such that no two adjacent vertices share the same color with minimal chromatic number",
        "theory": """
        **Vertex Coloring:**
        A vertex coloring of a graph $G = (V,E)$ is an assignment of colors to the vertices such that no two adjacent vertices share the same color. 
        The **Chromatic Number** $\\chi(G)$ is the minimum number of colors needed to color $G$.
        
        **Greedy Vertex Coloring Algorithm:**
        A simple, heuristic algorithm:
        1. Order the vertices (e.g., alphabetically or by degree).
        2. Color the first vertex with the first color.
        3. For each subsequent vertex, assign it the lowest-indexed color that has not been assigned to any of its already-colored neighbors.
        
        **Sudoku as a Graph Coloring Problem:**
        A $4 \\times 4$ Sudoku puzzle can be mathematically modeled as a graph coloring problem:
        * **Vertices:** 16 vertices, representing the cells of the $4 \\times 4$ grid.
        * **Colors:** 4 colors, representing the digits 1, 2, 3, and 4.
        * **Edges:** We add an edge between two cells if they belong to the same row, same column, or same $2 \\times 2$ subgrid block. Adjacent cells cannot have the same digit (color).
        * **Pre-colored vertices:** The cells with pre-filled numbers in the Sudoku grid.
        """,
        "conclusion": "Greedy graph coloring algorithm that assigns colors to the vertices such that no two adjacent vertices share the same color with minimal chromatic number was successfully implemented."
    }
}

expt_data = experiments_metadata[expt_num]

st.markdown(f"## Experiment {expt_num}: {expt_data['title'].strip()}")

selected_file = st.selectbox(
    "📁 Select Laboratory File to View & Run:",
    options=expt_data["filenames"],
    key=f"selector_expt_{expt_num}"
)

active_key = "standard"
manual_files = ["graph2.py", "isomorphism.py", "subgraph2.py", "degreesequence2.py", "linegraph2.py", "MST2.py", "spa2.py", "walks2.py", "eularian2.py", "vertexcoloring2.py"]
if selected_file in manual_files:
    active_key = "manual"


tab1, tab2, tab3 = st.tabs([
    "📑 Aim & Theory", 
    "💻 Source Code", 
    "🚀 Run Experiment"
])

with tab1:
    st.markdown(
        f"<div class='date-box'> &nbsp; Date of Experiment: &nbsp; <span style='font-size:15px;'>{expt_data['date']}</span></div>",
        unsafe_allow_html=True
    )
    st.markdown("### Aim")
    st.markdown(f"<div class='theory-box'>{expt_data['aim']}</div>", unsafe_allow_html=True)
    
    st.markdown("### Theory")
    st.markdown(expt_data['theory'])
    
    st.markdown("### Conclusion")
    st.markdown(f"<div class='conclusion-box'>{expt_data['conclusion']}</div>", unsafe_allow_html=True)

with tab2:
    st.markdown(f"### Source Code: `{selected_file}`")
    st.info(f"Currently displaying the exact workspace source code of `{selected_file}`.")
    
    code_content = load_source_code_file(selected_file)
    st.code(code_content, language="python")

with tab3:
    st.markdown(f"###  Run `{selected_file}`")
    st.write("Configure parameters below and click 'Run Experiment' to execute this file and inspect visual & printed output.")

    inputs = {}
    
    if expt_num == 4:
        st.markdown("#### 📝 Havel-Hakimi User Input")
        degree_seq_str = st.text_input(
            "Enter Degree Sequence (integers separated by space):",
            value="3 3 3 3",
            key="expt4_degree_input"
        )
        inputs["degree_sequence"] = degree_seq_str
        st.caption("Example graphical sequences: `3 3 3 3`, `2 2 2 2`, `3 2 3 2`. Non-graphical: `3 3 3 2`, `4 1 1 1`.")
        
    elif expt_num == 5:
        st.markdown("#### 📝 Graph Adjacency Matrix User Input")
        n_vertices = st.number_input(
            "Enter Number of Vertices (N):",
            min_value=2,
            max_value=6,
            value=4,
            key="expt5_n_input"
        )
        inputs["n"] = n_vertices
        
        default_matrix = "0 1 1 0\n1 0 1 0\n1 1 0 1\n0 0 1 0"
        if n_vertices == 3:
            default_matrix = "0 1 1\n1 0 1\n1 1 0"
        elif n_vertices == 5:
            default_matrix = "0 1 0 0 1\n1 0 1 0 0\n0 1 0 1 0\n0 0 1 0 1\n1 0 0 1 0"
            
        adj_input = st.text_area(
            f"Enter {n_vertices}x{n_vertices} Adjacency Matrix (one row per line, elements separated by space):",
            value=default_matrix,
            height=130,
            key="expt5_matrix_input"
        )
        inputs["adjacency_matrix"] = adj_input
        st.caption("Note: Enter a symmetric 0-1 matrix with 0s on the diagonal for a simple graph.")
        
    elif expt_num == 7:
        st.markdown("#### 📝 Dijkstra Target Configuration")
        source_choice = st.selectbox(
            "Select Single-Source Starting Node:",
            options=["1", "2", "3", "4", "5", "6", "7", "8"],
            index=0,
            key="expt7_source_input"
        )
        inputs["source"] = source_choice
        
    elif expt_num == 8:
        st.markdown("#### 📝 Walks Starting Vertex")
        walks_start = st.selectbox(
            "Select Walk Start Node:",
            options=["1", "2", "3", "4", "5", "6"],
            index=0,
            key="expt8_start_input"
        )
        inputs["start_node"] = walks_start
        st.button("🎲 Re-roll Random Path/Trail/Walk Paths", key="re_roll_walks")
        
    run_btn = st.button("🚀 Run Experiment", key=f"run_action_{selected_file}")
    
    if run_btn:
        st.markdown("<div class='console-header'>📺 Terminal Console Output:</div>", unsafe_allow_html=True)
        
        plt.close('all')
        
        try:
            with capture_stdout() as captured:
                
                if expt_num == 1:
                    fig = plt.figure(figsize=(14, 8))
                    
                    if active_key == "standard":
                        print(f"Running Basic Graphs via Standard networkx generator script: {selected_file}")
                        N5 = nx.empty_graph(5)
                        pos_N5 = nx.circular_layout(N5)
                        plt.subplot(2, 3, 1)
                        nx.draw(N5, pos_N5, with_labels=True, node_color="lightblue", node_size=800)
                        plt.title("N5 (Null Graph)")
                        print("Constructed circular-layout Null Graph N5.")
                        
                        K6 = nx.complete_graph(6)
                        pos_K6 = nx.circular_layout(K6)
                        plt.subplot(2, 3, 2)
                        nx.draw(K6, pos_K6, with_labels=True, node_color="orange", node_size=800)
                        plt.title("K6 (Complete Graph)")
                        print("Constructed circular-layout Complete Graph K6.")
                        
                        P5 = nx.path_graph(5)
                        pos_P5 = {i: (i, 0) for i in range(5)}
                        plt.subplot(2, 3, 3)
                        nx.draw(P5, pos_P5, with_labels=True, node_color="red", node_size=800)
                        plt.title("P5 (Path Graph)")
                        print("Constructed linear-layout Path Graph P5.")
                        
                        K34 = nx.complete_bipartite_graph(3, 4)
                        pos_K34 = {}
                        for i in range(3): pos_K34[i] = (0, i)
                        for i in range(3, 7): pos_K34[i] = (1, i-3)
                        plt.subplot(2, 3, 4)
                        nx.draw(K34, pos_K34, with_labels=True, node_color=["skyblue"]*3 + ["lightgreen"]*4, node_size=800)
                        plt.title("K3,4 (Complete Bipartite Graph)")
                        print("Constructed partitioned Complete Bipartite Graph K3,4.")
                        
                        C8 = nx.cycle_graph(8)
                        pos_C8 = nx.circular_layout(C8)
                        plt.subplot(2, 3, 5)
                        nx.draw(C8, pos_C8, with_labels=True, node_color="violet", node_size=800)
                        plt.title("C8 (Cycle Graph)")
                        print("Constructed circular-layout Cycle Graph C8.")
                        
                        W6 = nx.wheel_graph(6)
                        pos_W6 = nx.circular_layout(W6)
                        pos_W6[0] = (0, 0)
                        plt.subplot(2, 3, 6)
                        nx.draw(W6, pos_W6, with_labels=True, node_color="yellow", node_size=800)
                        plt.title("W6 (Wheel Graph)")
                        print("Constructed Wheel Graph W6 with central hub 0.")
                        
                    else:
                        print(f"Running Basic Graphs via Manual script: {selected_file}")
                        G1 = nx.Graph()
                        G1.add_nodes_from(range(5))
                        pos1 = {i: (i, 0) for i in range(5)}
                        plt.subplot(2, 3, 1)
                        nx.draw(G1, pos1, with_labels=True, node_color="lightblue", node_size=800)
                        plt.title("N5 (Null Graph)")
                        print("Constructed N5 manually (only vertices added).")
                        
                        G2 = nx.Graph()
                        nodes = range(6)
                        G2.add_nodes_from(nodes)
                        for i in nodes:
                            for j in nodes:
                                if i < j: G2.add_edge(i, j)
                        pos2 = nx.circular_layout(G2)
                        plt.subplot(2, 3, 2)
                        nx.draw(G2, pos2, with_labels=True, node_color="orange", node_size=800)
                        plt.title("K6 (Complete Graph)")
                        print("Constructed K6 manually (all-pairs loops).")
                        
                        G3 = nx.Graph()
                        G3.add_edges_from([(0,1),(1,2),(2,3),(3,4)])
                        pos3 = {i: (i, 0) for i in range(5)}
                        plt.subplot(2, 3, 3)
                        nx.draw(G3, pos3, with_labels=True, node_color="red", node_size=800)
                        plt.title("P5 (Path Graph)")
                        print("Constructed P5 manually (sequential link array).")
                        
                        G4 = nx.Graph()
                        left, right = [0,1,2], [3,4,5,6]
                        for u in left:
                            for v in right: G4.add_edge(u, v)
                        pos4 = {}
                        for i in range(3): pos4[i] = (0, i)
                        for i in range(4): pos4[i+3] = (1, i)
                        plt.subplot(2, 3, 4)
                        nx.draw(G4, pos4, with_labels=True, node_color=["skyblue"]*3 + ["lightgreen"]*4, node_size=800)
                        plt.title("K3,4 (Complete Bipartite Graph)")
                        print("Constructed K3,4 manually (bipartite cross-edges loop).")
                        
                        G5 = nx.Graph()
                        G5.add_edges_from([(i, (i+1)%8) for i in range(8)])
                        pos5 = nx.circular_layout(G5)
                        plt.subplot(2, 3, 5)
                        nx.draw(G5, pos5, with_labels=True, node_color="violet", node_size=800)
                        plt.title("C8 (Cycle Graph)")
                        print("Constructed C8 manually (modular circular connections).")
                        
                        G6 = nx.Graph()
                        edges_w6 = [(i, i+1) for i in range(1,5)] + [(5,1)] + [(0, i) for i in range(1,6)]
                        G6.add_edges_from(edges_w6)
                        pos6 = nx.circular_layout(G6)
                        pos6[0] = (0,0)
                        plt.subplot(2, 3, 6)
                        nx.draw(G6, pos6, with_labels=True, node_color="yellow", node_size=800)
                        plt.title("W6 (Wheel Graph)")
                        print("Constructed W6 manually (cycle edges + hub spokes).")
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    print("\nAll basic graph drawings mapped and rendered.")

                elif expt_num == 2:
                    def get_cycles_info(G):
                        edges = list(G.edges())
                        nodes = list(G.nodes())
                        cycles = []
                        def dfs(path, start):
                            curr = path[-1]
                            for u, v in edges:
                                nbr = None
                                if u == curr: nbr = v
                                elif v == curr: nbr = u
                                if nbr is None: continue
                                if nbr == start and len(path) > 2:
                                    cycles.append(tuple(sorted(path)))
                                elif nbr not in path:
                                    dfs(path + [nbr], start)
                        for node in nodes:
                            dfs([node], node)
                        unique = []
                        seen = set()
                        for c in cycles:
                            if c not in seen:
                                seen.add(c)
                                unique.append(c)
                        return unique, [len(c) for c in unique], len(unique)

                    def graph_info(G):
                        n = G.number_of_nodes()
                        e = G.number_of_edges()
                        deg = sorted([d for _, d in G.degree()])
                        if active_key == "standard":
                            cycles = list(nx.cycle_basis(G))
                            clengths = [len(c) for c in cycles]
                            ccount = len(cycles)
                        else:
                            _, clengths, ccount = get_cycles_info(G)
                        return n, e, deg, ccount, clengths

                    def isomorphic_manual(G1, G2):
                        if G1.number_of_nodes() != G2.number_of_nodes(): return False, None
                        if G1.number_of_edges() != G2.number_of_edges(): return False, None
                        if sorted([d for _, d in G1.degree()]) != sorted([d for _, d in G2.degree()]): return False, None
                        
                        _, lengths1, count1 = get_cycles_info(G1)
                        _, lengths2, count2 = get_cycles_info(G2)
                        if count1 != count2 or sorted(lengths1) != sorted(lengths2):
                            return False, None
                        
                        n1 = list(G1.nodes())
                        n2 = list(G2.nodes())
                        for perm in itertools.permutations(n2):
                            match = True
                            for i in range(len(n1)):
                                for j in range(len(n1)):
                                    if G1.has_edge(n1[i], n1[j]) != G2.has_edge(perm[i], perm[j]):
                                        match = False
                                        break
                                if not match: break
                            if match:
                                bijection = {n1[i]: perm[i] for i in range(len(n1))}
                                return True, bijection
                        return False, None

                    def isomorphic_standard(G1, G2):
                        GM = nx.isomorphism.GraphMatcher(G1, G2)
                        if GM.is_isomorphic():
                            return True, GM.mapping
                        return False, None

                    print(f"Running Heptagon Pairs Isomorphism: {selected_file}")
                    G1 = nx.Graph()
                    G1.add_edges_from([(1,2),(1,3),(1,6),(1,7),(2,3),(2,4),(2,7),(3,4),(3,5),(4,5),(4,6),(5,6),(5,7),(6,7)])
                    G2 = nx.Graph()
                    G2.add_edges_from([(1,2),(1,3),(1,6),(1,7),(2,3),(2,4),(2,5),(3,4),(3,7),(4,5),(4,6),(5,6),(5,7),(6,7)])
                    
                    graphs = [G1, G2]
                    titles = ["Graph 1 (G1)", "Graph 2 (G2)"]
                    
                    for i, G in enumerate(graphs):
                        n, e, deg, ccount, clengths = graph_info(G)
                        print(f"{titles[i]} Invariants:")
                        print("  Nodes count:", n)
                        print("  Edges count:", e)
                        print("  Degree sequence:", deg)
                        print("  Cycle basis count:", ccount)
                        print("  Cycle lengths:", clengths)
                        print("-" * 35)
                        
                    if selected_file == "isomorphism2.py":
                        iso, bijection = isomorphic_standard(G1, G2)
                    else:
                        iso, bijection = isomorphic_manual(G1, G2)
                        
                    print("G1 and G2 isomorphic:", iso)
                    if iso: print("  Bijection bijection mapping:", bijection)
                    
                    def heptagon_layout(nodes):
                        n = len(nodes)
                        pos = {}
                        for i, node in enumerate(sorted(nodes)):
                            angle = 2 * math.pi * i / n
                            pos[node] = (math.cos(angle), math.sin(angle))
                        return pos
                        
                    pos1 = heptagon_layout(G1.nodes())
                    pos2 = heptagon_layout(G2.nodes())
                    
                    fig = plt.figure(figsize=(12, 6))
                    plt.subplot(1, 2, 1)
                    nx.draw(G1, pos=pos1, with_labels=True, node_color="#C8E6C9", node_size=800, edge_color="#2E7D32")
                    plt.title("Graph 1")
                    
                    plt.subplot(1, 2, 2)
                    nx.draw(G2, pos=pos2, with_labels=True, node_color="#C8E6C9", node_size=800, edge_color="#2E7D32")
                    plt.title("Graph 2")
                    plt.tight_layout()
                    st.pyplot(fig)

                elif expt_num == 3:
                    print(f"Running Subgraphs Generation script: {selected_file}")
                    G = nx.Graph()
                    edges = [(1,2), (1, 4), (1, 3), (2, 3), (2, 6), (2, 5), (3, 4), (4, 5), (5, 6)]
                    G.add_edges_from(edges)
                    
                    pos = {1: (0, 3), 2: (3, 3), 3: (-0.5, 1.5), 4: (4, 1.5), 5: (0.5, 0), 6: (2.5, 0)}
                    nodes_subset = [1, 2, 5, 6]
                    edge_subset = [(1,2), (1,3), (2,5), (5,6)]
                    
                    if selected_file == "subgraph.py":
                        print("Using built-in NetworkX subgraph and edge_subgraph structures...")
                        G_induced = G.subgraph(nodes_subset)
                        G_spanning = G.copy()
                        subgraph = nx.minimum_spanning_tree(G_spanning)
                        G_edge_induced = G.edge_subgraph(edge_subset)
                    else:
                        print("Using manual nested loops to verify nodes and filter subsets...")
                        G_induced = nx.Graph()
                        for u, v in edges:
                            if u in nodes_subset and v in nodes_subset: G_induced.add_edge(u, v)
                        
                        spanning_edges = [(1,2), (1,3), (2,5), (5,6), (4,5)]
                        subgraph = nx.Graph()
                        subgraph.add_edges_from(spanning_edges)
                        
                        G_edge_induced = nx.Graph()
                        G_edge_induced.add_edges_from(edge_subset)
                        
                    print(f"Original Graph: Nodes = {G.number_of_nodes()}, Edges = {G.number_of_edges()}")
                    print(f"Spanning Subgraph: Nodes = {subgraph.number_of_nodes()}, Edges = {subgraph.number_of_edges()}")
                    print(f"Induced Subgraph (on nodes {nodes_subset}): Nodes = {G_induced.number_of_nodes()}, Edges = {G_induced.number_of_edges()}")
                    print(f"Edge-Induced Subgraph (on edges {edge_subset}): Nodes = {G_edge_induced.number_of_nodes()}, Edges = {G_edge_induced.number_of_edges()}")
                    
                    x_vals = [p[0] for p in pos.values()]
                    y_vals = [p[1] for p in pos.values()]
                    x_min, x_max = min(x_vals)-1, max(x_vals)+1
                    y_min, y_max = min(y_vals)-1, max(y_vals)+1
                    
                    fig = plt.figure(figsize=(12, 8))
                    plt.subplot(2, 2, 1)
                    nx.draw(G, pos, with_labels=True, node_color="yellow", node_size=700)
                    plt.title("Original Graph")
                    plt.xlim(x_min, x_max); plt.ylim(y_min, y_max)
                    
                    plt.subplot(2, 2, 2)
                    nx.draw(subgraph, pos, with_labels=True, node_color="lightgreen", node_size=700)
                    plt.title("Spanning Subgraph")
                    plt.xlim(x_min, x_max); plt.ylim(y_min, y_max)
                    
                    plt.subplot(2, 2, 3)
                    nx.draw(G_induced, pos, with_labels=True, node_color="lightblue", node_size=700)
                    plt.title("Induced Subgraph")
                    plt.xlim(x_min, x_max); plt.ylim(y_min, y_max)
                    
                    plt.subplot(2, 2, 4)
                    nx.draw(G_edge_induced, pos, with_labels=True, node_color="orange", node_size=700)
                    plt.title("Edge Induced Subgraph")
                    plt.xlim(x_min, x_max); plt.ylim(y_min, y_max)
                    plt.tight_layout()
                    st.pyplot(fig)

                elif expt_num == 4:
                    deg_seq_str = inputs["degree_sequence"]
                    print(f"Running Degree Sequence verification script: {selected_file}")
                    
                    try:
                        degree_sequence = list(map(int, deg_seq_str.strip().split()))
                        print(f"Parsing User-Defined Sequence: {degree_sequence}")
                    except ValueError:
                        print("Invalid Input! Could not parse sequence integers. Resetting to default [3, 3, 3, 3]")
                        degree_sequence = [3, 3, 3, 3]
                        
                    if selected_file == "degreesequence.py":
                        print("Verifying via networkx built-in graphical Havel-Hakimi...")
                        if nx.is_graphical(degree_sequence):
                            print("\nThe degree sequence is graphical.")
                            G = nx.havel_hakimi_graph(degree_sequence)
                            print("Degrees in constructed graph:")
                            print(dict(G.degree()))
                            
                            fig = plt.figure(figsize=(8, 6))
                            pos = nx.spring_layout(G)
                            nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800, font_size=12)
                            plt.title("Graph from Given Degree Sequence (Built-in)")
                            st.pyplot(fig)
                        else:
                            print("\nThe degree sequence is NOT graphical.")
                            st.error("The degree sequence is NOT graphical.")
                            
                    else:
                        print("Verifying via manual step-by-step sorting & reduction algorithm...")
                        def havel_hakimi_graph(degree_sequence):
                            n = len(degree_sequence)
                            G = nx.Graph()
                            G.add_nodes_from(range(n))
                            degree_list = [(degree_sequence[i], i) for i in range(n)]
                            
                            while True:
                                degree_list.sort(reverse=True)
                                if degree_list[0][0] == 0: return G
                                
                                d, node = degree_list[0]
                                degree_list.pop(0)
                                if d > len(degree_list): return None
                                
                                for i in range(d):
                                    deg, neighbor = degree_list[i]
                                    G.add_edge(node, neighbor)
                                    degree_list[i] = (deg - 1, neighbor)
                                    if deg - 1 < 0: return None
                                    
                        if sum(degree_sequence) % 2 != 0:
                            print("Not Graphical (Sum of degrees must be even)")
                            st.error("Not Graphical (Sum of degrees must be even)")
                        else:
                            G = havel_hakimi_graph(degree_sequence)
                            if G is None:
                                print("The degree sequence is NOT graphical.")
                                st.error("The degree sequence is NOT graphical.")
                            else:
                                print("The degree sequence is graphical.")
                                print("Degrees in constructed graph:")
                                print(dict(G.degree()))
                                
                                fig = plt.figure(figsize=(8, 6))
                                pos = nx.spring_layout(G)
                                nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=800)
                                plt.title("Graph from Given Degree Sequence (Manual)")
                                st.pyplot(fig)

                elif expt_num == 5:
                    n = inputs["n"]
                    matrix_text = inputs["adjacency_matrix"]
                    
                    print(f"Running Line Graph conversion script: {selected_file}")
                    print(f"Reading user-defined Adjacency Matrix (size {n}x{n}):")
                    
                    adj_matrix = []
                    try:
                        lines = [line.strip() for line in matrix_text.strip().split("\n") if line.strip()]
                        if len(lines) < n:
                            raise ValueError(f"Rows count ({len(lines)}) is less than N ({n}).")
                        for i in range(n):
                            row = list(map(int, lines[i].split()))
                            if len(row) < n:
                                raise ValueError(f"Row {i} has only {len(row)} elements instead of N={n}")
                            adj_matrix.append(row[:n])
                        
                        for r in adj_matrix: print(" ", r)
                    except Exception as e:
                        print(f"Parsing error: {e}. Falling back to default C4 Cycle Graph adjacency matrix.")
                        st.warning(f"Adjacency Matrix parse error: {e}. Loaded default star/cycle matrix instead.")
                        adj_matrix = [[0 if i == j else (1 if abs(i-j) == 1 or (i==0 and j==n-1) or (i==n-1 and j==0) else 0) for j in range(n)] for i in range(n)]
                        for r in adj_matrix: print(" ", r)
                        
                    G = nx.Graph()
                    edges = []
                    for i in range(n):
                        for j in range(i, n):
                            if adj_matrix[i][j] == 1:
                                G.add_edge(i, j)
                                edges.append((i, j))
                                
                    print("\nEdges of Original Graph:")
                    for edge in edges: print(" ", edge)
                    
                    if selected_file == "linegraph.py":
                        print("Constructing line graph using networkx.line_graph...")
                        L = nx.line_graph(G)
                    else:
                        print("Constructing line graph L(G) manually by checking shared endpoints...")
                        L = nx.Graph()
                        for edge in edges: L.add_node(edge)
                        for i in range(len(edges)):
                            for j in range(i + 1, len(edges)):
                                e1 = edges[i]
                                e2 = edges[j]
                                if (e1[0] in e2) or (e1[1] in e2): L.add_edge(e1, e2)
                                
                    fig = plt.figure(figsize=(10, 5))
                    plt.subplot(1, 2, 1)
                    nx.draw(G, with_labels=True, node_color='lightblue', edge_color='#0288D1', node_size=600)
                    plt.title("Original Graph")
                    
                    plt.subplot(1, 2, 2)
                    nx.draw(L, with_labels=True, node_color='lightgreen', edge_color='#2E7D32', node_size=600)
                    plt.title("Line Graph")
                    plt.tight_layout()
                    st.pyplot(fig)

                elif expt_num == 6:
                    print(f"Running Minimum Spanning Tree script: {selected_file}")
                    G = nx.Graph()
                    edges = [
                        ('a','b',4), ('a','h',8), ('b','h',11), ('b','c',8),
                        ('c','d',7), ('c','f',4), ('c','i',2), ('d','e',9),
                        ('d','f',14), ('e','f',10), ('f','g',2), ('g','h',1),
                        ('g','i',6), ('h','i',7)
                    ]
                    G.add_weighted_edges_from(edges)
                    
                    pos = {
                        'a': (0, 4.5), 'b': (2, 6), 'c': (4, 6), 'd': (6, 6),
                        'e': (8, 4.5), 'f': (6, 3), 'g': (4, 3), 'h': (2, 3), 'i': (3, 4.5)
                    }
                    
                    if selected_file == "MST.py":
                        print("Calculating MST using Kruskal via NetworkX MST built-in...")
                        mst = nx.minimum_spanning_tree(G, algorithm='kruskal')
                        total_cost = sum(d['weight'] for _, _, d in mst.edges(data=True))
                        print(f"Calculated MST. Total cost = {total_cost}")
                        
                        fig = plt.figure(figsize=(12, 5))
                        plt.subplot(1, 2, 1)
                        nx.draw(G, pos, with_labels=True, node_size=400, node_color='#FFE082')
                        labels = nx.get_edge_attributes(G, 'weight')
                        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
                        plt.title("Original Weighted Graph")
                        
                        plt.subplot(1, 2, 2)
                        nx.draw(mst, pos, with_labels=True, node_size=400, node_color='#C8E6C9')
                        labels = nx.get_edge_attributes(mst, 'weight')
                        nx.draw_networkx_edge_labels(mst, pos, edge_labels=labels)
                        plt.title(f"Minimum Spanning Tree (Cost = {total_cost})")
                        plt.tight_layout()
                        st.pyplot(fig)
                        
                    else:
                        print("Executing step-by-step manual Kruskal's merging forest algorithm...")
                        sorted_edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])
                        mst = nx.Graph()
                        mst.add_nodes_from(G.nodes())
                        steps = []
                        costs = []
                        cost = 0
                        
                        for u, v, data in sorted_edges:
                            components = list(nx.connected_components(mst))
                            same_component = False
                            for comp in components:
                                if u in comp and v in comp:
                                    same_component = True
                                    break
                            if not same_component:
                                mst.add_edge(u, v, weight=data['weight'])
                                cost += data['weight']
                                steps.append(mst.copy())
                                costs.append(cost)
                                print(f"Selected Edge ({u}, {v}) of weight {data['weight']}. Cumulative Forest Cost: {cost}")
                                
                        total_plots = len(steps) + 1
                        cols = 3
                        rows = math.ceil(total_plots / cols)
                        
                        fig = plt.figure(figsize=(15, 4.5 * rows))
                        plt.subplot(rows, cols, 1)
                        nx.draw(G, pos, with_labels=True, node_size=400, node_color='#FFE082')
                        labels = nx.get_edge_attributes(G, 'weight')
                        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
                        plt.title("Original Graph")
                        
                        for i in range(len(steps)):
                            plt.subplot(rows, cols, i + 2)
                            nx.draw(steps[i], pos, with_labels=True, node_size=400, node_color='#C8E6C9')
                            labels = nx.get_edge_attributes(steps[i], 'weight')
                            nx.draw_networkx_edge_labels(steps[i], pos, edge_labels=labels)
                            plt.title(f"Step {i+1} | Cost = {costs[i]}")
                            
                        plt.tight_layout()
                        st.pyplot(fig)
                        print(f"\nMST built. Final total cost = {cost}")

                elif expt_num == 7:
                    source = inputs["source"]
                    print(f"Running Dijkstra Single-Source Shortest Path script: {selected_file}")
                    
                    G = nx.Graph()
                    edges = [
                        ('1', '2', 6), ('1', '3', 7), ('2', '3', 8), ('2', '4', 9),
                        ('2', '6', 14), ('3', '4', 5), ('3', '5', 4), ('4', '5', 6),
                        ('4', '6', 10), ('5', '7', 7), ('6', '7', 11), ('6', '8', 8),
                        ('7', '8', 6)
                    ]
                    G.add_weighted_edges_from(edges)
                    
                    pos = {
                        '1': (-1, 0), '3': (-0.5, -1), '2': (-0.5, 1), '4': (0, 0),
                        '5': (0, -2), '6': (0.5, 1), '7': (0.5, -1), '8': (1, 0)
                    }
                    
                    if selected_file == "spa.py":
                        print("Invoking built-in single source Dijkstra path generators...")
                        dist = nx.single_source_dijkstra_path_length(G, source)
                        paths = nx.single_source_dijkstra_path(G, source)
                        
                        nodes_sorted = sorted(G.nodes(), key=int)
                        table_data = []
                        for nd in nodes_sorted:
                            table_data.append([
                                f"{source} -> {nd}",
                                " -> ".join(paths[nd]),
                                dist[nd]
                            ])
                            print(f"Path to node '{nd}': {' -> '.join(paths[nd])} (Cost: {dist[nd]})")
                            
                        fig = plt.figure(figsize=(12, 5))
                        plt.subplot(1, 2, 1)
                        nx.draw(G, pos, with_labels=True, node_size=500, node_color='#FFE082')
                        labels = nx.get_edge_attributes(G, 'weight')
                        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
                        plt.title("Weighted Network")
                        
                        plt.subplot(1, 2, 2)
                        plt.axis('off')
                        table = plt.table(
                            cellText=table_data,
                            colLabels=["Connection", "Shortest Path Sequence", "Path Cost"],
                            loc='center'
                        )
                        table.auto_set_font_size(False)
                        table.set_fontsize(11)
                        table.scale(1, 2)
                        plt.title(f"Shortest Paths (Dijkstra - Source {source})")
                        
                        plt.tight_layout()
                        st.pyplot(fig)
                        
                    else:
                        print("Running step-by-step manual Dijkstra relaxation...")
                        def dijkstra_steps(G, source):
                            dist = {node: float('inf') for node in G.nodes()}
                            dist[source] = 0
                            visited = set()
                            parent = {node: None for node in G.nodes()}
                            steps = []
                            while len(visited) < len(G.nodes()):
                                current = min((nd for nd in G.nodes() if nd not in visited), key=lambda x: dist[x])
                                visited.add(current)
                                steps.append((current, visited.copy(), dist.copy(), parent.copy()))
                                for neighbor in G.neighbors(current):
                                    weight = G[current][neighbor]['weight']
                                    if neighbor not in visited:
                                        new_dist = dist[current] + weight
                                        if new_dist < dist[neighbor]:
                                            dist[neighbor] = new_dist
                                            parent[neighbor] = current
                            return steps
                            
                        steps = dijkstra_steps(G, source)
                        n_steps = len(steps)
                        cols = 3
                        rows = math.ceil(n_steps / cols)
                        
                        fig, axes = plt.subplots(rows, cols, figsize=(15, 4.8 * rows))
                        axes = axes.flatten()
                        built_tree_edges = []
                        
                        for i, (current, visited, dist, parent) in enumerate(steps):
                            ax = axes[i]
                            node_colors = []
                            for node in G.nodes():
                                if node == source: node_colors.append('#3F51B5')
                                elif node == current: node_colors.append('#FF9800')
                                else: node_colors.append('#E0E0E0')
                                
                            nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=500, ax=ax)
                            
                            for u, v, data in G.edges(data=True):
                                x1, y1 = pos[u]
                                x2, y2 = pos[v]
                                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                                dx, dy = x2 - x1, y2 - y1
                                length = (dx**2 + dy**2) ** 0.5
                                if length != 0:
                                    offset_x = -dy / length * 0.08
                                    offset_y = dx / length * 0.08
                                else:
                                    offset_x = offset_y = 0
                                ax.text(mx + offset_x, my + offset_y, str(data['weight']), fontsize=9)
                                
                            if parent[current] is not None:
                                new_edge = (parent[current], current)
                                built_tree_edges.append(new_edge)
                                nx.draw_networkx_edges(G, pos, edgelist=[new_edge], width=4, edge_color='#F57C00', ax=ax)
                            nx.draw_networkx_edges(G, pos, edgelist=built_tree_edges, width=2, edge_color='#388E3C', ax=ax)
                            
                            for node in visited:
                                x, y = pos[node]
                                ax.text(x + 0.08, y + 0.08, f"d={dist[node]}", fontsize=9, color='#1565C0', weight='bold')
                                
                            ax.set_title(f"Step {i+1}: Selected {current}")
                            ax.axis('off')
                            print(f"Step {i+1}: Relaxed around node '{current}'. Tentative distances: {dict(dist)}")
                            
                        for j in range(i + 1, len(axes)):
                            axes[j].axis('off')
                            
                        plt.tight_layout()
                        st.pyplot(fig)

                elif expt_num == 8:
                    start_node = inputs["start_node"]
                    print(f"Running Walks, Trails, & Paths script: {selected_file}")
                    
                    G = nx.Graph()
                    edges = [
                        ('1','2'), ('1','5'), ('1','6'), ('2','4'), ('2','6'),
                        ('3','4'), ('3','6'), ('4','5'), ('4','6'), ('5','6')
                    ]
                    G.add_edges_from(edges)
                    adj = {}
                    for u, v in edges:
                        adj.setdefault(u, []).append(v)
                        adj.setdefault(v, []).append(u)
                        
                    pos = {
                        '1': (0, 1), '2': (0.5, 0), '3': (0.5, -1), '4': (0, -2),
                        '5': (-0.5, -1), '6': (-0.5, 0)
                    }
                    edge_labels = {
                        ('1','2'): 'e1', ('1','5'): 'e2', ('1','6'): 'e3', ('2','4'): 'e4',
                        ('2','6'): 'e5', ('3','4'): 'e6', ('3','6'): 'e7', ('4','5'): 'e8',
                        ('4','6'): 'e9', ('5','6'): 'e10'
                    }
                    def get_label(u, v):
                        return edge_labels.get((u, v)) or edge_labels.get((v, u))

                    if selected_file == "walks.py":
                        print("Tracing topological elements via standard deterministic algorithms...")
                        all_paths = list(nx.all_simple_paths(G, source=start_node, target='6'))
                        path = all_paths[0] if all_paths else [start_node]
                        path_edges = list(zip(path, path[1:]))
                        G_path = nx.Graph(); G_path.add_edges_from(path_edges)
                        path_labels = {(u,v): get_label(u,v) for u,v in path_edges}
                        
                        trail_edges = list(nx.dfs_edges(G, source=start_node))
                        trail_nodes = [trail_edges[0][0]] + [v for u, v in trail_edges]
                        G_trail = nx.Graph(); G_trail.add_edges_from(trail_edges)
                        trail_labels = {(u,v): get_label(u,v) for u,v in trail_edges}
                        
                        cycles = nx.cycle_basis(G)
                        cycle = cycles[0] if cycles else [start_node]
                        closed_walk = cycle + [cycle[0]]
                        cycle_edges = list(zip(closed_walk, closed_walk[1:]))
                        G_cycle = nx.Graph(); G_cycle.add_edges_from(cycle_edges)
                        cycle_labels = {(u,v): get_label(u,v) for u,v in cycle_edges}
                        
                    else:
                        print("Tracing randomized walker routes based on adjacent selections...")
                        def random_path(start, max_len=5):
                            path = [start]
                            visited = {start}
                            while len(path) < max_len:
                                curr = path[-1]
                                neighbors = [nd for nd in adj[curr] if nd not in visited]
                                if not neighbors: break
                                nxt = random.choice(neighbors)
                                path.append(nxt)
                                visited.add(nxt)
                            return path
                            
                        def random_trail(start, max_len=7):
                            trail = [start]
                            used_edges = set()
                            while len(trail) < max_len:
                                curr = trail[-1]
                                neighbors = adj[curr]
                                valid = []
                                for nd in neighbors:
                                    e = tuple(sorted((curr, nd)))
                                    if e not in used_edges: valid.append(nd)
                                if not valid: break
                                nxt = random.choice(valid)
                                trail.append(nxt)
                                used_edges.add(tuple(sorted((curr, nxt))))
                            return trail
                            
                        def random_closed_walk(start, steps=6):
                            walk = [start]
                            for _ in range(steps):
                                curr = walk[-1]
                                nxt = random.choice(adj[curr])
                                walk.append(nxt)
                            if walk[-1] != start: walk.append(start)
                            return walk
                            
                        path = random_path(start_node)
                        trail_nodes = random_trail(start_node)
                        closed_walk = random_closed_walk(start_node)
                        
                        path_edges = list(zip(path, path[1:]))
                        trail_edges = list(zip(trail_nodes, trail_nodes[1:]))
                        cycle_edges = list(zip(closed_walk, closed_walk[1:]))
                        
                        G_path = nx.Graph(); G_path.add_edges_from(path_edges)
                        G_trail = nx.Graph(); G_trail.add_edges_from(trail_edges)
                        G_cycle = nx.Graph(); G_cycle.add_edges_from(cycle_edges)
                        
                        path_labels = {(u,v): get_label(u,v) for u,v in path_edges}
                        trail_labels = {(u,v): get_label(u,v) for u,v in trail_edges}
                        cycle_labels = {(u,v): get_label(u,v) for u,v in cycle_edges}
                        
                    print(f"Path sequence generated: {path}")
                    print(f"Trail sequence generated: {trail_nodes}")
                    print(f"Closed Walk sequence generated: {closed_walk}")
                    
                    fig = plt.figure(figsize=(20, 5))
                    plt.subplot(1, 4, 1)
                    nx.draw(G, pos, with_labels=True, node_size=500, node_color='#CFD8DC')
                    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
                    plt.title("Original Graph")
                    
                    plt.subplot(1, 4, 2)
                    nx.draw(G_path, pos, with_labels=True, node_size=500, node_color='#B3E5FC', edge_color='#0288D1')
                    nx.draw_networkx_edge_labels(G_path, pos, edge_labels=path_labels)
                    plt.title(f"Simple Path\n{path}")
                    
                    plt.subplot(1, 4, 3)
                    nx.draw(G_trail, pos, with_labels=True, node_size=500, node_color='#C8E6C9', edge_color='#2E7D32')
                    nx.draw_networkx_edge_labels(G_trail, pos, edge_labels=trail_labels)
                    plt.title(f"Trail (Unique Edges)\n{trail_nodes}")
                    
                    plt.subplot(1, 4, 4)
                    nx.draw(G_cycle, pos, with_labels=True, node_size=500, node_color='#FFE082', edge_color='#F57C00')
                    nx.draw_networkx_edge_labels(G_cycle, pos, edge_labels=cycle_labels)
                    plt.title(f"Closed Walk\n{closed_walk}")
                    plt.tight_layout()
                    st.pyplot(fig)

                elif expt_num == 9:
                    print(f"Running Eulerian Circuit identifier script: {selected_file}")
                    G = nx.Graph()
                    edges = [
                        ('1','2'), ('1','4'), ('2','3'), ('2','5'), ('2','6'),
                        ('3','4'), ('4','5'), ('4','6')
                    ]
                    G.add_edges_from(edges)
                    
                    pos = {
                        '1': (0, 1), '2': (0.5, 0), '3': (0.5, -1), '4': (0, -2),
                        '5': (-0.5, -1), '6': (-0.5, 0)
                    }
                    edge_labels = {
                        ('1','2'): 'e1', ('1','4'): 'e2', ('2','3'): 'e3', ('2','5'): 'e4',
                        ('2','6'): 'e5', ('3','4'): 'e6', ('4','5'): 'e7', ('4','6'): 'e8'
                    }
                    
                    if selected_file == "eularian.py":
                        print("Verifying if graph is Eulerian using NetworkX standard rules...")
                        if nx.is_eulerian(G):
                            print("Graph is Eulerian")
                            circuit = list(nx.eulerian_circuit(G))
                            path = [circuit[0][0]] + [v for u, v in circuit]
                            print("Eulerian Circuit Found:", path)
                            
                            steps = []
                            tempG = copy.deepcopy(G)
                            steps.append(tempG.copy())
                            for u, v in circuit:
                                tempG.remove_edge(u, v)
                                steps.append(tempG.copy())
                                
                            total = len(steps)
                            cols = 3
                            rows = math.ceil(total / cols)
                            
                            fig = plt.figure(figsize=(15, 5 * rows))
                            for i, graph_step in enumerate(steps):
                                plt.subplot(rows, cols, i + 1)
                                nx.draw(graph_step, pos, with_labels=True, node_size=500, node_color='#C8E6C9')
                                
                                current_labels = {}
                                for e in graph_step.edges():
                                    if e in edge_labels: current_labels[e] = edge_labels[e]
                                    elif (e[1], e[0]) in edge_labels: current_labels[e] = edge_labels[(e[1], e[0])]
                                    
                                nx.draw_networkx_edge_labels(graph_step, pos, edge_labels=current_labels)
                                if i == 0:
                                    plt.title("Original Graph")
                                else:
                                    removed = circuit[i-1]
                                    plt.title(f"Remove {removed}\nRemaining Edges: {graph_step.number_of_edges()}")
                                    print(f"Step {i}: Removed traversed edge {removed}. Remaining Edges count: {graph_step.number_of_edges()}")
                                    
                            plt.tight_layout()
                            st.pyplot(fig)
                        else:
                            print("Graph is NOT Eulerian.")
                            st.error("Graph is NOT Eulerian.")
                            
                    else:
                        print("Tracing Eulerian circuit manually using Fleury's algorithm...")
                        def build_adj(edges):
                            adj = {}
                            for u, v in edges:
                                adj.setdefault(u, []).append(v)
                                adj.setdefault(v, []).append(u)
                            return adj
                            
                        def is_eulerian(adj):
                            for node in adj:
                                if len(adj[node]) % 2 != 0: return False
                            return True
                            
                        def dfs_count(adj, start, visited):
                            visited.add(start)
                            count = 1
                            for nbr in adj[start]:
                                if nbr not in visited: count += dfs_count(adj, nbr, visited)
                            return count
                            
                        def is_valid_edge(adj, u, v):
                            if len(adj[u]) == 1: return True
                            visited = set()
                            count1 = dfs_count(adj, u, visited)
                            adj[u].remove(v)
                            adj[v].remove(u)
                            visited = set()
                            count2 = dfs_count(adj, u, visited)
                            adj[u].append(v)
                            adj[v].append(u)
                            return count1 == count2
                            
                        def fleury(edges):
                            adj = build_adj(edges)
                            if not is_eulerian(adj): return None
                            start = list(adj.keys())[0]
                            path = [start]
                            while adj[start]:
                                for v in adj[start]:
                                    if is_valid_edge(adj, start, v):
                                        path.append(v)
                                        adj[start].remove(v)
                                        adj[v].remove(start)
                                        start = v
                                        break
                            return path
                            
                        circuit = fleury(edges)
                        
                        fig = plt.figure(figsize=(10, 5))
                        plt.subplot(1, 2, 1)
                        nx.draw(G, pos, with_labels=True, node_size=500, node_color='#FFE082')
                        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
                        plt.title("Original Graph")
                        
                        plt.subplot(1, 2, 2)
                        if circuit:
                            print("Eulerian Circuit:", circuit)
                            circuit_edges = list(zip(circuit, circuit[1:]))
                            G_euler = nx.Graph(); G_euler.add_edges_from(circuit_edges)
                            nx.draw(G_euler, pos, with_labels=True, node_size=500, node_color='#C8E6C9', edge_color='#2E7D32', width=3)
                            plt.title(f"Eulerian Circuit\n{circuit}")
                        else:
                            print("Graph is NOT Eulerian!")
                            plt.text(0.3, 0.5, "No Eulerian Circuit", fontsize=12)
                            plt.title("Result")
                            
                        plt.tight_layout()
                        st.pyplot(fig)

                elif expt_num == 10:
                    print(f"Running Hamiltonian Circuit recursive backtrack script: {selected_file}")
                    G = nx.Graph()
                    edges = [
                        ('1','2'), ('1','4'), ('2','3'), ('2','5'), ('2','6'),
                        ('3','4'), ('3','5'), ('3','6'), ('4','5'), ('4','6')
                    ]
                    G.add_edges_from(edges)
                    
                    pos = {
                        '1': (0, 1), '2': (0.5, 0), '3': (0.5, -1), '4': (0, -2),
                        '5': (-0.5, -1), '6': (-0.5, 0)
                    }
                    
                    adj = {}
                    for u, v in edges:
                        adj.setdefault(u, []).append(v)
                        adj.setdefault(v, []).append(u)
                        
                    nodes = list(adj.keys())
                    n = len(nodes)
                    all_circuits = []
                    
                    def hamiltonian(path):
                        if len(path) == n:
                            if path[-1] in adj[path[0]]:
                                circuit = path + [path[0]]
                                if circuit[::-1] not in all_circuits:
                                    all_circuits.append(circuit)
                            return
                        current = path[-1]
                        for neighbor in adj[current]:
                            if neighbor not in path:
                                hamiltonian(path + [neighbor])
                                
                    start = nodes[0]
                    hamiltonian([start])
                    
                    print("Hamiltonian Circuits found:")
                    for idx, c in enumerate(all_circuits, 1):
                        print(f"  {idx}: {c}")
                        
                    total = len(all_circuits) + 1
                    cols = 3
                    rows = math.ceil(total / cols)
                    
                    fig = plt.figure(figsize=(15, 4.5 * rows))
                    plt.subplot(rows, cols, 1)
                    nx.draw(G, pos, with_labels=True, node_size=500, node_color='#CFD8DC')
                    plt.title("Original Graph")
                    
                    for i, circuit in enumerate(all_circuits):
                        plt.subplot(rows, cols, i + 2)
                        H = nx.Graph()
                        circuit_edges = list(zip(circuit, circuit[1:]))
                        H.add_edges_from(circuit_edges)
                        
                        nx.draw(H, pos, with_labels=True, node_size=500, node_color='#FFE082', edge_color='#E65100', width=3.5)
                        plt.title(f"Circuit {i+1}\n{circuit}")
                        
                    plt.tight_layout()
                    st.pyplot(fig)

                elif expt_num == 11:
                    print(f"Running Graph Colouring and Sudoku script: {selected_file}")
                    
                    VG = nx.Graph()
                    edges = [
                        ('1','2'), ('1','3'), ('2','4'), ('2','3'), ('3','4'), ('3','5'),
                        ('4','5'), ('4','6'), ('4','7'), ('4','8'), ('4','9'),
                        ('5','6'), ('5','9'), ('7','8')
                    ]
                    VG.add_edges_from(edges)
                    
                    pos = {
                        '1': (0, 1), '2': (-0.5, 0), '3': (-0.5, -1), '4': (0.5, 0),
                        '5': (0.5, -1), '6': (0, -1.5), '7': (1, -1.5), '8': (1.5, 0), '9': (1.5, -1)
                    }
                    
                    color_names = ['red', 'lightblue', 'lightgreen', 'yellow']
                    color_hex = ['#FF8A80', '#80D8FF', '#B9F6CA', '#FFE57F']
                    
                    if selected_file == "vertexcoloring.py":
                        print("Coloring original graph using networkx.coloring.greedy_color...")
                        def my_strategy(G, colors): return iter(sorted(G.nodes()))
                        vertex_colors = nx.coloring.greedy_color(VG, strategy=my_strategy)
                    else:
                        print("Coloring original graph manually using custom greedy check loops...")
                        def manual_greedy_coloring(G):
                            coloring = {}
                            nodes = sorted(G.nodes())
                            for node in nodes:
                                used_colors = set()
                                for neighbor in G.neighbors(node):
                                    if neighbor in coloring: used_colors.add(coloring[neighbor])
                                color = 0
                                while color in used_colors: color += 1
                                coloring[node] = color
                            return coloring
                        vertex_colors = manual_greedy_coloring(VG)
                        
                    vg_node_colors = []
                    for node in VG.nodes():
                        vg_node_colors.append(color_hex[vertex_colors[node]])
                        print(f"  Vertex {node} ---> {color_names[vertex_colors[node]].upper()}")
                        
                    print("\nChromatic Number =", max(vertex_colors.values()) + 1)
                    
                    print("\nSolved Sudoku (using Graph Coloring representation):")
                    sudoku = [
                        [2, 0, 0, 0],
                        [0, 0, 2, 0],
                        [0, 3, 0, 0],
                        [0, 0, 0, 1]
                    ]
                    
                    SG = nx.Graph()
                    for i in range(1, 17): SG.add_node(i)
                    cell_to_vertex = {}
                    k = 1
                    for r in range(4):
                        for c in range(4):
                            cell_to_vertex[(r, c)] = k
                            k += 1
                            
                    row_straight, row_curved = [], []
                    col_straight, col_curved = [], []
                    block_edges = []
                    
                    for r1 in range(4):
                        for c1 in range(4):
                            for r2 in range(4):
                                for c2 in range(4):
                                    if (r1, c1) < (r2, c2):
                                        u = cell_to_vertex[(r1, c1)]
                                        v = cell_to_vertex[(r2, c2)]
                                        if r1 == r2:
                                            if abs(c1 - c2) == 1: row_straight.append((u, v))
                                            else: row_curved.append((u, v))
                                        elif c1 == c2:
                                            if abs(r1 - r2) == 1: col_straight.append((u, v))
                                            else: col_curved.append((u, v))
                                        elif (r1//2 == r2//2) and (c1//2 == c2//2):
                                            block_edges.append((u, v))
                                            
                    SG.add_edges_from(row_straight + row_curved + col_straight + col_curved + block_edges)
                    
                    sudoku_colors = {}
                    for r in range(4):
                        for c in range(4):
                            if sudoku[r][c] != 0:
                                vertex = cell_to_vertex[(r, c)]
                                sudoku_colors[vertex] = sudoku[r][c] - 1
                                
                    def is_safe(node, color):
                        for nbr in SG.neighbors(node):
                            if nbr in sudoku_colors:
                                if sudoku_colors[nbr] == color: return False
                        return True
                        
                    nodes_list = []
                    for r in range(4):
                        for c in range(4): nodes_list.append(cell_to_vertex[(r, c)])
                        
                    preferred_order = [3, 2, 0, 1]
                    def solve(index=0):
                        if index == len(nodes_list): return True
                        node = nodes_list[index]
                        if node in sudoku_colors: return solve(index + 1)
                        for color in preferred_order:
                            if is_safe(node, color):
                                sudoku_colors[node] = color
                                if solve(index + 1): return True
                                del sudoku_colors[node]
                        return False
                        
                    solve()
                    solution = [[0] * 4 for _ in range(4)]
                    for (r, c), vertex in cell_to_vertex.items():
                        solution[r][c] = sudoku_colors[vertex] + 1
                        
                    for row in solution: print(" ", row)
                    
                    sudoku_pos = {}
                    k = 1
                    spacing = 3
                    for r in range(4):
                        for c in range(4):
                            sudoku_pos[k] = (c * spacing, -r * spacing)
                            k += 1
                            
                    sg_node_colors = []
                    for node in SG.nodes():
                        sg_node_colors.append(color_hex[sudoku_colors[node]])
                        
                    solved_labels = {}
                    for (r, c), vertex in cell_to_vertex.items():
                        solved_labels[vertex] = str(solution[r][c])
                        
                    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
                    
                    axes[0].set_title("Greedy Vertex Coloring", fontsize=14, weight='bold')
                    nx.draw(VG, pos, ax=axes[0], with_labels=True, node_color=vg_node_colors, node_size=700, width=2, edge_color='#424242')
                    axes[0].axis('off')
                    
                    axes[1].set_title("Solved Sudoku Graph (16 Cells)", fontsize=14, weight='bold')
                    nx.draw_networkx_edges(SG, sudoku_pos, ax=axes[1], edgelist=row_straight, edge_color='#757575', width=1.5)
                    nx.draw_networkx_edges(SG, sudoku_pos, ax=axes[1], edgelist=col_straight, edge_color='#757575', width=1.5)
                    nx.draw_networkx_edges(SG, sudoku_pos, ax=axes[1], edgelist=block_edges, edge_color='#757575', width=1.5)
                    
                    SG_directed = nx.DiGraph(SG)
                    for u, v in row_curved:
                        nx.draw_networkx_edges(SG_directed, sudoku_pos, ax=axes[1], edgelist=[(u, v)], edge_color='#9E9E9E', width=1, connectionstyle="arc3,rad=0.4", arrows=True, arrowstyle='-')
                    for u, v in col_curved:
                        nx.draw_networkx_edges(SG_directed, sudoku_pos, ax=axes[1], edgelist=[(u, v)], edge_color='#9E9E9E', width=1, connectionstyle="arc3,rad=-0.4", arrows=True, arrowstyle='-')
                        
                    nx.draw_networkx_nodes(SG, sudoku_pos, ax=axes[1], node_color=sg_node_colors, node_size=900, edgecolors='#424242')
                    nx.draw_networkx_labels(SG, sudoku_pos, labels=solved_labels, ax=axes[1], font_size=15, font_weight='bold')
                    axes[1].axis('off')
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                
            st.markdown(f"<div class='console-box'>{captured.getvalue()}</div>", unsafe_allow_html=True)
            st.success("Experiment run completed successfully!")
            
        except Exception as e:
            st.error(f"Error executing script logic: {str(e)}")

st.markdown(f"""
<div class="academic-footer">
    <div style="display: flex; justify-content: center; gap: 20px; font-weight: 500; font-size: 13.5px; color: #2E7D32;">
        <span><strong>Name:</strong> {student_name}</span>
        <span>&bull;</span>
        <span><strong>Roll No:</strong> {student_roll}</span>
        <span>&bull;</span>
        <span><strong>Semester:</strong> {student_sem}</span>
    </div>
</div>
""", unsafe_allow_html=True)