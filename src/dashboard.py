import streamlit as st
import matplotlib.pyplot as plt
from random_tree import RANDOMTREE
from solve_lin_prog import SOlVELINPROG

############### utils ###############
def write_constr_to_session_state(slp):
    A = slp.A()
    b = slp.b()
    c = slp.c()
    n = slp.n
    l = slp.l
    constr1 = f"{A[0]}"
    constr2 = f"{A[1:n+1]}"
    constr3 = f"{A[n+1:n*n+n+1]}"
    constr4 = f"{A[n*n+n+1: 2*n*l+n*n+n+1]}"
    b_vec = f"{b}"
    c_vec = f"{c}"
    st.session_state["constr1"] = constr1
    st.session_state["constr2"] = constr2
    st.session_state["constr3"] = constr3
    st.session_state["constr4"] = constr4
    st.session_state["b_vec"] = b_vec
    st.session_state["c_vec"] = c_vec


def draw_items(height, max_noc, max_dist, colors): 

    # setup RANDOMTREE and SOLVELINPROG object
    rt = RANDOMTREE(height = height, max_noc = max_noc, max_dist = max_dist, colors = colors)
    fv = rt.get_fairness_vectors()
    slp = SOlVELINPROG(random_tree = rt, k = 2, alpha = fv["alpha"], beta = fv["beta"])
    
    # For matrizes
    write_constr_to_session_state(slp)
    
    # For picture of tree
    fig = rt.draw_tree()
    st.session_state["random_tree"] = fig



############### Main Page ###############
tab1, tab2, tab3 = st.tabs(["Intro", "Tree", "LP"])

#### Tab 1 ####
with tab1: 

    ### Introduction
    st.subheader("Introduction")
    st.text(r"""In what follows we will try to visualize the vectors and matrices
involved in a Linear Programm that is a first step in order to solve the 
fair clustering problem on a tree. The linear program has the following form:  
            """)
    st.latex(r'''
        \textbf{LP1} := \min \sum_{i,j \in V} d(i,j) \cdot x_{ji}, \\
        ''')
    st.latex(r'''
        \sum_{i\in V} y_i \leq k, \\
        ''')
    st.latex(r'''
        \sum_{i\in V} x_{ji} \geq 1 \qquad \forall j\in V, \\
        ''')
    st.latex(r'''
        x_{ji} \leq y_i \qquad \forall i,j \in V, \\
        ''')
    st.latex(r'''
        \alpha_c \sum_{j \in V} x_{ji} \leq \sum_{j\in V_c} 
            x_{ji} \leq \beta_c \sum_{j \in V} 
            x_{ji} \qquad \forall i\in V, c\in C,
        ''')

#### Tab2 ####
with tab2: 

    ### The Random Tree
    if "random_tree" in st.session_state:
        st.pyplot(st.session_state["random_tree"])

#### Tab 3 ####
with tab3: 
    
    ### The linear program in matrix notation
    st.header("The linear program in matrix notation")
    st.text("Let ")
    st.latex(r"""n := \text{number of nodes}""")
    st.latex(r"""l := \text{number of colors}.""")
    st.text("We would like to write our linear program in the following form:")
    st.latex(r"""
        \textbf{LP} := \min c^{T} z, 
    """)
    st.latex(r"""
        Az \leq b,
    """)
    st.text("""where,""")
    st.latex(r""" c \in \mathbb{R}^{n*(n+1) \times 1}, \quad 
                A \in \mathbb{R}^{1+n*(1+n+2*l) \times n*(n+1)}, \quad
                b \in \mathbb{R}^{n*(n+1) \times 1}
            """)
    st.text("and")
    st.latex(r"""
        z := (y_1, ... ,y_n, x_{00}, ... , x_{0n}, ... , x_{n0}, ... , x_{nn})
    """)

    ## The A matrix
    st.subheader("The A matrix")
    st.text("In our case the vectors for the different constraints look like this: ")

    # Constraint 1
    st.text("Constraint 1: ")
    st.latex(r'''
        \sum_{i\in V} y_i \leq k, \\
        ''')
    st.latex(r"""
    """)
    st.text("Vector 1: ")
    with st.container():
        if "constr1" in st.session_state:  
            st.text(st.session_state["constr1"])

    # Constraint 2
    st.text("Constraint 2: ")
    st.latex(r"""
        \sum_{i\in V} x_{ji} \geq 1 \qquad \forall j\in V, \\
    """)
    st.text("Vector 2: ")
    with st.container(): 
        if "constr2" in st.session_state: 
            st.text(st.session_state["constr2"])

    # Constraint 3
    st.text("Constraint 3: ")
    st.latex(r"""
        x_{ji} \leq y_i \qquad \forall i,j \in V, \\
    """)
    st.text("Vector 3: ")
    with st.container(): 
        if "constr3" in st.session_state: 
            st.text(st.session_state["constr3"])

    # Constraint 4
    st.text("Constraint 4: ")
    st.latex(r"""
        \alpha_c \sum_{j \in V} x_{ji} \leq \sum_{j\in V_c} 
            x_{ji} \leq \beta_c \sum_{j \in V} 
            x_{ji} \qquad \forall i\in V, c\in C,
    """)
    st.text("Vector 4: ")
    with st.container(): 
        if "constr4" in st.session_state: 
            st.text(st.session_state["constr4"])

    ## The b vector 
    st.subheader("The b vector")
    st.text("The b vector in our case looks like this: ")
    with st.container(): 
        if "b_vec" in st.session_state: 
            st.text(st.session_state["b_vec"])

    ## The c vector
    st.subheader("The c vector")
    st.text("The c vector in our case looks like this: ")
    with st.container(): 
        if "c_vec" in st.session_state: 
            st.text(st.session_state["c_vec"])




############### Sidebar Page ###############
with st.sidebar:

    header = st.header("Adjust Random tree parameters")

    tree_height = st.slider("height", min_value=1, max_value=10, value=3)
    max_noc = st.slider("max number of children", min_value=1, max_value=5, value=2)
    max_dist = st.slider("max distance between nodes", min_value=1, max_value=10, value=1)
    colors = st.slider("number of colors", min_value=2, max_value=10, value=2)

    kwargs = {"height": tree_height, "max_noc": max_noc, "max_dist": max_dist, "colors": colors}

    generate_button = st.button("generate random tree", on_click = draw_items, kwargs = kwargs)