import streamlit as st
from random_tree import RANDOMTREE
from solve_lin_prog import SOlVELINPROG

############### utils ###############
def write_constr_to_session_state(slp):
    A = slp.A()
    n = slp.n
    l = slp.l
    constr1 = f"{A[0]}"
    constr2 = f"{A[1:n+1]}"
    constr3 = f"{A[n+1:n*n+n+1]}"
    constr4 = f"{A[n*n+n+1: 2*n*l+n*n+n+1]}"
    st.session_state["constr1"] = constr1
    st.session_state["constr2"] = constr2
    st.session_state["constr3"] = constr3
    st.session_state["constr4"] = constr4


def get_matrices(height, max_noc, max_dist, colors): 

    rt = RANDOMTREE(height = height, max_noc = max_noc, max_dist = max_dist, colors = colors)
    fv = rt.get_fairness_vectors()
    slp = SOlVELINPROG(random_tree = rt, k = 2, alpha = fv["alpha"], beta = fv["beta"])
    write_constr_to_session_state(slp)
    



############### Main Page ###############
st.header("Visualize Linear Program")
### Introduction
st.subheader("Introduction")
st.text("""In what follows we will try to visualize the vectors and matrices
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

### The linear program in matrix notation
st.header("The linear program in matrix notation")
st.subheader("The A matrix")
st.text("In our case the vectors for the different constraints look like this: ")

# Constraint 1
st.text("Constraint 1: ")
st.latex(r'''
    \sum_{i\in V} y_i \leq k, \\
    ''')
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







############### Sidebar Page ###############
with st.sidebar:

    header = st.header("Adjust Random tree parameters")

    tree_height = st.slider("height", min_value=1, max_value=10, value=3)
    max_noc = st.slider("max number of children", min_value=1, max_value=5, value=2)
    max_dist = st.slider("max distance between nodes", min_value=1, max_value=10, value=1)
    colors = st.slider("number of colors", min_value=2, max_value=10, value=2)

    kwargs = {"height": tree_height, "max_noc": max_noc, "max_dist": max_dist, "colors": colors}

    generate_button = st.button("generate random tree", on_click = get_matrices, kwargs = kwargs)