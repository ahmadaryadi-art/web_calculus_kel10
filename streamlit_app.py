import streamlit as st
import numpy as np
#import sympy as sp
import plotly.graph_objects as go
import plotly.express as px
from sympy import symbols, diff, latex, solve, lambdify
from sympy.parsing.sympy_parser import parse_expr

# CSS untuk styling
st.set_page_config(page_title="Math Function & Optimization WebApp", page_icon="📊", layout="wide")

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #3B82F6;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    .card {
        background-color: #F8FAFC;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🔢 Navigation")
page = st.sidebar.radio("Select Page:", 
                         ["🏠 Team Members", "📈 Function & Derivatives", "⚡ Optimization Solver"])

# Page 1: Team Members
if page == "🏠 Team Members":
    st.markdown('<h1 class="main-header">👥 Team Members</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Ahmad Rizki Aryadi")
        st.markdown("**NIM:** 1234567890")
        st.markdown("**Role:** Project Manager & Backend Developer")
        st.markdown("**Contribution:**")
        st.markdown("- Differential algorithms implementation")
        st.markdown("- SymPy integration for calculus")
        st.markdown("- Optimization solver")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Christina Malinda Derankian")
        st.markdown("**NIM:** 0987654321")
        st.markdown("**Role:** UI/UX Designer & Frontend Developer")
        st.markdown("**Contribution:**")
        st.markdown("- Application interface design")
        st.markdown("- 2D & 3D graph visualization")
        st.markdown("- CSS styling")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### Ari Muamar")
        st.markdown("**NIM:** 1122334455")
        st.markdown("**Role:** Data Analyst & Testing")
        st.markdown("**Contribution:**")
        st.markdown("- Mathematical function testing")
        st.markdown("- Optimization result validation")
        st.markdown("- Code documentation")
        st.markdown("</div>", unsafe_allow_html=True)

# Page 2: Function & Derivatives
elif page == "📈 Function & Derivatives":
    st.markdown('<h1 class="main-header">📊 Function Visualization & Derivatives</h1>', unsafe_allow_html=True)
    
    # Function input
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Enter Mathematical Function")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        func_input = st.text_input(
            "Function f(x) (use x as variable):",
            value="x**3 - 3*x**2 + 2*x + 5",
            help="Examples: sin(x), exp(x), x**2 + 3*x - 5, log(x)"
        )
    with col2:
        x_range = st.slider("x range:", -10.0, 10.0, (-5.0, 5.0))
    
    if func_input:
        try:
            x = symbols('x')
            f_expr = parse_expr(func_input, transformations='all')
            
            # Display function in LaTeX
            st.markdown("### Function:")
            st.latex(f"f(x) = {latex(f_expr)}")
            
            # Calculate derivative
            st.markdown("### Derivative Calculation:")
            f_prime = diff(f_expr, x)
            st.latex(f"f'(x) = {latex(f_prime)}")
            
            # Visualization with Plotly
            st.markdown("### Graph Visualization:")
            
            # Generate data
            x_vals = np.linspace(x_range[0], x_range[1], 400)
            f_lambdified = lambdify(x, f_expr, 'numpy')
            f_prime_lambdified = lambdify(x, f_prime, 'numpy')
            
            try:
                y_vals = f_lambdified(x_vals)
                y_prime_vals = f_prime_lambdified(x_vals)
                
                # Create Plotly figure
                fig = go.Figure()
                
                # Add original function
                fig.add_trace(go.Scatter(
                    x=x_vals, 
                    y=y_vals,
                    mode='lines',
                    name=f'f(x) = {func_input}',
                    line=dict(color='blue', width=3)
                ))
                
                # Add derivative
                fig.add_trace(go.Scatter(
                    x=x_vals, 
                    y=y_prime_vals,
                    mode='lines',
                    name="f'(x)",
                    line=dict(color='red', width=2, dash='dash')
                ))
                
                # Update layout
                fig.update_layout(
                    title="Function and Its Derivative",
                    xaxis_title="x",
                    yaxis_title="y",
                    hovermode='x unified',
                    template='plotly_white'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Function information
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.markdown("#### Function Info:")
                    st.write(f"**Domain:** x ∈ [{x_range[0]}, {x_range[1]}]")
                    st.write(f"**Min value:** {np.min(y_vals):.4f}")
                    st.write(f"**Max value:** {np.max(y_vals):.4f}")
                
                with col_info2:
                    st.markdown("#### Derivative Info:")
                    critical_points = solve(f_prime, x)
                    if critical_points:
                        st.write("**Critical points:**")
                        for point in critical_points:
                            st.write(f"x = {latex(point)}")
                
            except Exception as e:
                st.error(f"Error in visualization: {str(e)}")
        
        except Exception as e:
            st.error(f"Error parsing function: {str(e)}")
            st.info("Please use valid Python syntax. Example: 'x**2 + sin(x)'")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Page 3: Optimization Solver
elif page == "⚡ Optimization Solver":
    st.markdown('<h1 class="main-header">⚡ Optimization Problem Solver</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Enter Optimization Problem")
    
    # Example problems
    example_problems = {
        "Box without lid": "A craftsman wants to make a box without a lid from a 12x20 inch cardboard by cutting identical squares from each corner. Find the cut size that maximizes volume.",
        "Minimize distance": "Find the point on curve y = x² closest to point (0, 3).",
        "Maximize area": "A farmer has 200 meters of fence for a rectangular area next to a river (no fence on river side). Find dimensions that maximize area."
    }
    
    selected_problem = st.selectbox("Choose example:", list(example_problems.keys()))
    problem_text = example_problems[selected_problem]
    st.write(f"**Problem:** {problem_text}")
    
    # Predefined functions for examples
    if selected_problem == "Box without lid":
        func_input = "x*(12-2*x)*(20-2*x)"
    elif selected_problem == "Minimize distance":
        func_input = "(x**2 + (x**2 - 3)**2)"  # Square of distance
    else:
        func_input = "x*(200-2*x)"
    
    st.text_input("Function to optimize (f(x)):", value=func_input, key="opt_func")
    
    if func_input:
        try:
            x = symbols('x')
            f_expr = parse_expr(func_input, transformations='all')
            
            st.markdown("### Solution Steps:")
            
            # Step 1: First derivative
            st.markdown("#### Step 1: First Derivative")
            f_prime = diff(f_expr, x)
            st.latex(f"f'(x) = {latex(f_prime)}")
            
            # Step 2: Critical points
            st.markdown("#### Step 2: Critical Points")
            solutions = solve(f_prime, x)
            if solutions:
                st.write("Setting f'(x) = 0:")
                for sol in solutions:
                    if sol.is_real:
                        st.latex(f"x = {latex(sol)} ≈ {float(sol):.4f}")
            
            # Step 3: Second derivative test
            st.markdown("#### Step 3: Second Derivative Test")
            if solutions:
                f_double_prime = diff(f_expr, x, 2)
                st.latex(f"f''(x) = {latex(f_double_prime)}")
                
                for sol in solutions:
                    if sol.is_real:
                        second_deriv_val = f_double_prime.subs(x, sol)
                        st.latex(f"f''({latex(sol)}) = {latex(second_deriv_val)} ≈ {float(second_deriv_val):.4f}")
                        
                        if second_deriv_val > 0:
                            st.success(f"x = {latex(sol)} is a **local minimum**")
                        elif second_deriv_val < 0:
                            st.success(f"x = {latex(sol)} is a **local maximum**")
            
            # Step 4: Optimal value
            st.markdown("#### Step 4: Optimal Value")
            if solutions:
                for sol in solutions:
                    if sol.is_real:
                        func_val = f_expr.subs(x, sol)
                        st.latex(f"f({latex(sol)}) = {latex(func_val)} ≈ {float(func_val):.4f}")
            
            # Visualization
            st.markdown("### Visualization")
            x_min, x_max = -5, 5
            if solutions:
                x_vals = [float(sol) for sol in solutions if sol.is_real]
                if x_vals:
                    x_min = min(x_vals) - 2
                    x_max = max(x_vals) + 2
            
            x_plot = np.linspace(x_min, x_max, 400)
            f_lambdified = lambdify(x, f_expr, 'numpy')
            
            try:
                y_vals = f_lambdified(x_plot)
                
                # Create interactive plot
                fig = px.line(x=x_plot, y=y_vals, 
                             labels={'x': 'x', 'y': 'f(x)'},
                             title=f"Function: f(x) = {func_input}")
                
                # Add critical points
                if solutions:
                    for sol in solutions:
                        if sol.is_real:
                            sol_val = float(sol)
                            func_val = float(f_expr.subs(x, sol))
                            fig.add_trace(go.Scatter(
                                x=[sol_val],
                                y=[func_val],
                                mode='markers',
                                marker=dict(size=15, color='red'),
                                name=f'Critical point x={sol_val:.2f}'
                            ))
                
                fig.update_layout(template='plotly_white')
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"Visualization error: {str(e)}")
        
        except Exception as e:
            st.error(f"Error solving optimization: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("**Mathematical Function & Optimization WebApp** | Created with Streamlit and SymPy")

