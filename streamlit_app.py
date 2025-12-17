import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import re
from sympy import symbols, diff, latex, solve, lambdify, integrate, Eq
from sympy.parsing.sympy_parser import parse_expr
import warnings
warnings.filterwarnings('ignore')

# Konfigurasi halaman
st.set_page_config(
    page_title="Math Function & Optimization WebApp",
    page_icon="📊",
    layout="wide"
)

# ===============================
# MULTI-LANGUAGE SUPPORT
# ===============================
texts = {
    'id': {
        'title': 'Math Function & Optimization WebApp',
        'nav_home': '🏠 Anggota Kelompok',
        'nav_function': '📈 Fungsi & Turunan',
        'nav_optimization': '⚡ Pemecah Optimisasi',
        'nav_story_problems': '📚 Soal Cerita Optimisasi',
        'language': 'Pilih Bahasa:',
        
        # Home page
        'group_members': '👥 Anggota Kelompok',
        'about_project': '📋 Tentang Proyek',
        'project_description': '''
        Aplikasi web ini dibuat untuk memenuhi tugas proyek Matematika Lanjutan dengan fitur:
        1. **Visualisasi fungsi matematika** dengan grafik interaktif
        2. **Kalkulator turunan** dengan penjelasan langkah demi langkah
        3. **Pemecah masalah optimisasi** untuk soal cerita
        4. **Antarmuka yang user-friendly** dengan tampilan LaTeX
        ''',
        
        # Function page
        'function_title': '📊 Visualisasi Fungsi & Turunan',
        'input_function': 'Masukkan Fungsi Matematika',
        'function_example': 'Contoh: sin(x), exp(x), x**2 + 3*x - 5, log(x)',
        'x_range': 'Rentang x:',
        'derivative_process': '🎯 Proses Turunan',
        'derivative_steps': 'Langkah-langkah Turunan:',
        'first_derivative': 'Turunan pertama:',
        'second_derivative': 'Turunan kedua:',
        'function_info': '📈 Informasi Fungsi',
        'derivative_info': '📉 Informasi Turunan',
        'domain': 'Domain:',
        'local_min': 'Nilai minimum lokal:',
        'local_max': 'Nilai maksimum lokal:',
        'critical_points': 'Titik kritis:',
        
        # Optimization page
        'optimization_title': '⚡ Pemecah Masalah Optimisasi',
        'input_type': 'Pilih jenis input:',
        'example_problems': 'Gunakan contoh soal',
        'manual_input': 'Masukkan soal optimisasi manual',
        'optimization_description': 'Masukkan Soal Optimisasi:',
        'function_config': 'Konfigurasi Fungsi:',
        'objective_function': 'Fungsi yang akan dioptimalkan (f(x)):',
        'constraint': 'Kendala (jika ada):',
        'optimization_steps': '🔍 Proses Penyelesaian',
        'step1': 'Langkah 1: Turunan Pertama',
        'step2': 'Langkah 2: Titik Kritis',
        'step3': 'Langkah 3: Uji Turunan Kedua',
        'step4': 'Langkah 4: Nilai Optimum',
        'conclusion': '✅ Kesimpulan',
        'maximum_value': 'Nilai maksimum:',
        'minimum_value': 'Nilai minimum:',
        'interpretation': '📝 Interpretasi untuk Soal:',
        
        # Story problems page
        'story_title': '📚 Soal Cerita Optimisasi',
        'select_category': 'Pilih Kategori Soal:',
        'problem_statement': '📄 Pernyataan Masalah:',
        'problem_formulation': '🧮 Formulasi Matematika:',
        'solution_steps': '📝 Langkah-langkah Penyelesaian:',
        'final_answer': '✅ Jawaban Akhir:',
        'units': 'satuan',
        
        # Categories
        'area': 'Luas',
        'perimeter': 'Keliling',
        'volume': 'Volume',
        'profit': 'Keuntungan',
        
        # Area problems
        'area_problem1': 'Luas Maksimum Persegi Panjang',
        'area_description1': 'Seorang petani memiliki 100 meter pagar untuk membuat kandang persegi panjang. Tentukan dimensi yang memberikan luas maksimum.',
        'area_formulation1': 'Misal panjang = x, lebar = y. Keliling = 2x + 2y = 100 → y = 50 - x. Luas A = x*y = x*(50-x)',
        'area_solution1': '1. A(x) = 50x - x²\n2. A\'(x) = 50 - 2x\n3. Set A\'(x) = 0 → 50 - 2x = 0 → x = 25\n4. A\'\'(x) = -2 < 0 (maksimum)\n5. y = 50 - 25 = 25\nLuas maksimum saat persegi menjadi bujur sangkar dengan sisi 25 m.',
        
        'area_problem2': 'Luas Maksimum dengan Sisi Sungai',
        'area_description2': 'Seorang petani memiliki 200 meter pagar untuk membatasi area persegi panjang di samping sungai (tidak perlu pagar di sisi sungai). Tentukan dimensi yang memberikan luas maksimum.',
        'area_formulation2': 'Misal panjang sejajar sungai = x, lebar = y. Total pagar = x + 2y = 200 → y = 100 - x/2. Luas A = x*y = x*(100 - x/2)',
        
        # Volume problems
        'volume_problem1': 'Volume Maksimum Kotak Tanpa Tutup',
        'volume_description1': 'Dari selembar karton berukuran 20 cm × 30 cm, dipotong persegi di setiap sudut dan dilipat untuk membuat kotak tanpa tutup. Tentukan ukuran potongan untuk volume maksimum.',
        'volume_formulation1': 'Misal panjang potongan = x. Panjang kotak = 30-2x, lebar = 20-2x, tinggi = x. Volume V = x*(30-2x)*(20-2x)',
        
        'volume_problem2': 'Volume Maksimum Silinder dalam Kerucut',
        'volume_description2': 'Sebuah silinder ditempatkan dalam kerucut dengan tinggi 10 cm dan jari-jari alas 5 cm. Tentukan dimensi silinder dengan volume maksimum.',
        'volume_formulation2': 'Misal jari-jari silinder = r, tinggi = h. Dari kesebangunan: (5-r)/5 = h/10 → h = 10 - 2r. Volume V = πr²h = πr²(10-2r)',
        
        # Profit problems
        'profit_problem1': 'Keuntungan Maksimum Penjualan Tiket',
        'profit_description1': 'Sebuah bioskop dapat menampung 800 penonton. Dengan harga tiket Rp 50.000, semua tiket terjual. Setiap penurunan harga Rp 5.000 menambah 50 penonton. Tentukan harga tiket untuk keuntungan maksimum.',
        'profit_formulation1': 'Misal penurunan harga sebanyak x kali. Harga = 50000 - 5000x, penonton = 800 + 50x. Keuntungan P = (50000-5000x)*(800+50x)',
        
        'profit_problem2': 'Keuntungan Maksimum Produksi',
        'profit_description2': 'Sebuah perusahaan memproduksi x unit barang dengan biaya C(x) = 1000 + 20x + 0.1x² dan harga jual p(x) = 100 - 0.2x. Tentukan jumlah produksi untuk keuntungan maksimum.',
        'profit_formulation2': 'Keuntungan P(x) = pendapatan - biaya = x*(100-0.2x) - (1000+20x+0.1x²)',
        
        # Footer
        'footer': 'Mathematical Function & Optimization WebApp | Dibuat dengan Streamlit, SymPy, dan Matplotlib | © 2024 Kelompok: Ahmad Rizki Aryadi, Christina Malinda Derankian, Ari Muamar'
    },
    
    'en': {
        'title': 'Math Function & Optimization WebApp',
        'nav_home': '🏠 Group Members',
        'nav_function': '📈 Function & Derivative',
        'nav_optimization': '⚡ Optimization Solver',
        'nav_story_problems': '📚 Story Optimization Problems',
        'language': 'Select Language:',
        
        # Home page
        'group_members': '👥 Group Members',
        'about_project': '📋 About Project',
        'project_description': '''
        This web application is created to fulfill Advanced Mathematics project with features:
        1. **Mathematical function visualization** with interactive graphs
        2. **Derivative calculator** with step-by-step explanations
        3. **Optimization problem solver** for story problems
        4. **User-friendly interface** with LaTeX display
        ''',
        
        # Function page
        'function_title': '📊 Function & Derivative Visualization',
        'input_function': 'Enter Mathematical Function',
        'function_example': 'Example: sin(x), exp(x), x**2 + 3*x - 5, log(x)',
        'x_range': 'x range:',
        'derivative_process': '🎯 Derivative Process',
        'derivative_steps': 'Derivative Steps:',
        'first_derivative': 'First derivative:',
        'second_derivative': 'Second derivative:',
        'function_info': '📈 Function Information',
        'derivative_info': '📉 Derivative Information',
        'domain': 'Domain:',
        'local_min': 'Local minimum value:',
        'local_max': 'Local maximum value:',
        'critical_points': 'Critical points:',
        
        # Optimization page
        'optimization_title': '⚡ Optimization Problem Solver',
        'input_type': 'Select input type:',
        'example_problems': 'Use example problems',
        'manual_input': 'Enter optimization problem manually',
        'optimization_description': 'Enter Optimization Problem:',
        'function_config': 'Function Configuration:',
        'objective_function': 'Function to optimize (f(x)):',
        'constraint': 'Constraint (if any):',
        'optimization_steps': '🔍 Solution Process',
        'step1': 'Step 1: First Derivative',
        'step2': 'Step 2: Critical Points',
        'step3': 'Step 3: Second Derivative Test',
        'step4': 'Step 4: Optimum Value',
        'conclusion': '✅ Conclusion',
        'maximum_value': 'Maximum value:',
        'minimum_value': 'Minimum value:',
        'interpretation': '📝 Interpretation for Problem:',
        
        # Story problems page
        'story_title': '📚 Optimization Story Problems',
        'select_category': 'Select Problem Category:',
        'problem_statement': '📄 Problem Statement:',
        'problem_formulation': '🧮 Mathematical Formulation:',
        'solution_steps': '📝 Solution Steps:',
        'final_answer': '✅ Final Answer:',
        'units': 'units',
        
        # Categories
        'area': 'Area',
        'perimeter': 'Perimeter',
        'volume': 'Volume',
        'profit': 'Profit',
        
        # Area problems
        'area_problem1': 'Maximum Area of Rectangle',
        'area_description1': 'A farmer has 100 meters of fence to make a rectangular enclosure. Determine dimensions that give maximum area.',
        'area_formulation1': 'Let length = x, width = y. Perimeter = 2x + 2y = 100 → y = 50 - x. Area A = x*y = x*(50-x)',
        'area_solution1': '1. A(x) = 50x - x²\n2. A\'(x) = 50 - 2x\n3. Set A\'(x) = 0 → 50 - 2x = 0 → x = 25\n4. A\'\'(x) = -2 < 0 (maximum)\n5. y = 50 - 25 = 25\nMaximum area when rectangle becomes square with side 25 m.',
        
        'area_problem2': 'Maximum Area with River Side',
        'area_description2': 'A farmer has 200 meters of fence to enclose a rectangular area next to a river (no fence needed on river side). Determine dimensions for maximum area.',
        'area_formulation2': 'Let length parallel to river = x, width = y. Total fence = x + 2y = 200 → y = 100 - x/2. Area A = x*y = x*(100 - x/2)',
        
        # Volume problems
        'volume_problem1': 'Maximum Volume of Open Box',
        'volume_description1': 'From a 20 cm × 30 cm cardboard, squares are cut from each corner and folded to make an open box. Determine cut size for maximum volume.',
        'volume_formulation1': 'Let cut length = x. Box length = 30-2x, width = 20-2x, height = x. Volume V = x*(30-2x)*(20-2x)',
        
        'volume_problem2': 'Maximum Cylinder in Cone',
        'volume_description2': 'A cylinder is placed inside a cone with height 10 cm and base radius 5 cm. Find cylinder dimensions for maximum volume.',
        'volume_formulation2': 'Let cylinder radius = r, height = h. From similarity: (5-r)/5 = h/10 → h = 10 - 2r. Volume V = πr²h = πr²(10-2r)',
        
        # Profit problems
        'profit_problem1': 'Maximum Ticket Sales Profit',
        'profit_description1': 'A cinema can hold 800 audience. At ticket price Rp 50,000, all tickets sold. Every Rp 5,000 price decrease adds 50 audience. Determine ticket price for maximum profit.',
        'profit_formulation1': 'Let price decrease count = x. Price = 50000 - 5000x, audience = 800 + 50x. Profit P = (50000-5000x)*(800+50x)',
        
        'profit_problem2': 'Maximum Production Profit',
        'profit_description2': 'A company produces x units with cost C(x) = 1000 + 20x + 0.1x² and selling price p(x) = 100 - 0.2x. Determine production quantity for maximum profit.',
        'profit_formulation2': 'Profit P(x) = revenue - cost = x*(100-0.2x) - (1000+20x+0.1x²)',
        
        # Footer
        'footer': 'Mathematical Function & Optimization WebApp | Built with Streamlit, SymPy, and Matplotlib | © 2025 Group: Ahmad Rizki Aryadi, Christina Malinda Derankian, Ari Muamar'
    }
}

# CSS untuk styling
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
    .member-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .step-box {
        background-color: #EFF6FF;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #60A5FA;
    }
    .latex-box {
        background-color: #F1F5F9;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-size: 1.2rem;
    }
    .problem-card {
        background-color: #F0F9FF;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #10B981;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ===============================
# INITIALIZE SESSION STATE
# ===============================
if 'language' not in st.session_state:
    st.session_state.language = 'id'

# ===============================
# SIDEBAR NAVIGATION
# ===============================
st.sidebar.title("🔢 " + texts[st.session_state.language]['title'])
language = st.sidebar.radio(
    texts[st.session_state.language]['language'], 
    ["🇮🇩 Indonesia", "🇺🇸 English"],
    index=0 if st.session_state.language == 'id' else 1
)

# Update language based on selection
if language == "🇮🇩 Indonesia":
    st.session_state.language = 'id'
else:
    st.session_state.language = 'en'

# Get current language texts
t = texts[st.session_state.language]

# Navigation
page = st.sidebar.radio("Navigate to:", 
                        [t['nav_home'], t['nav_function'], t['nav_optimization'], t['nav_story_problems']])

# ===============================
# HELPER FUNCTIONS
# ===============================
def solve_story_problem(problem_type, problem_num):
    """Solve specific story problems"""
    x = symbols('x')
    
    if problem_type == 'area':
        if problem_num == 1:
            # Maximum area of rectangle with 100m fence
            A = x*(50-x)  # Area function
            A_prime = diff(A, x)
            critical_points = solve(A_prime, x)
            A_double_prime = diff(A, x, 2)
            
            solution = {
                'function': A,
                'derivative': A_prime,
                'critical_points': critical_points,
                'second_derivative': A_double_prime,
                'max_point': (25, 25),
                'max_value': 625,
                'units': 'meters'
            }
            return solution
            
        elif problem_num == 2:
            # Maximum area with river side
            A = x*(100 - x/2)
            A_prime = diff(A, x)
            critical_points = solve(A_prime, x)
            A_double_prime = diff(A, x, 2)
            
            solution = {
                'function': A,
                'derivative': A_prime,
                'critical_points': critical_points,
                'second_derivative': A_double_prime,
                'max_point': (100, 50),
                'max_value': 5000,
                'units': 'meters'
            }
            return solution
    
    elif problem_type == 'volume':
        if problem_num == 1:
            # Maximum volume of open box
            V = x*(30-2*x)*(20-2*x)
            V_prime = diff(V, x)
            critical_points = solve(V_prime, x)
            # Filter valid solutions (0 < x < 10)
            valid_points = [cp for cp in critical_points if 0 < float(cp) < 10]
            
            solution = {
                'function': V,
                'derivative': V_prime,
                'critical_points': valid_points,
                'max_point': (3.924,),
                'max_value': 1056.3,
                'units': 'cm'
            }
            return solution
            
        elif problem_num == 2:
            # Maximum cylinder in cone
            V = sp.pi * x**2 * (10 - 2*x)
            V_prime = diff(V, x)
            critical_points = solve(V_prime, x)
            # Filter valid solutions (0 < x < 5)
            valid_points = [cp for cp in critical_points if 0 < float(cp) < 5]
            
            solution = {
                'function': V,
                'derivative': V_prime,
                'critical_points': valid_points,
                'max_point': (3.333,),
                'max_value': 155.5,
                'units': 'cm'
            }
            return solution
    
    elif problem_type == 'profit':
        if problem_num == 1:
            # Maximum ticket profit
            P = (50000 - 5000*x)*(800 + 50*x)
            P_prime = diff(P, x)
            critical_points = solve(P_prime, x)
            P_double_prime = diff(P, x, 2)
            
            solution = {
                'function': P,
                'derivative': P_prime,
                'critical_points': critical_points,
                'second_derivative': P_double_prime,
                'max_point': (4,),
                'max_value': 3240000,
                'units': 'rupiah'
            }
            return solution
            
        elif problem_num == 2:
            # Maximum production profit
            P = x*(100 - 0.2*x) - (1000 + 20*x + 0.1*x**2)
            P_prime = diff(P, x)
            critical_points = solve(P_prime, x)
            P_double_prime = diff(P, x, 2)
            
            solution = {
                'function': P,
                'derivative': P_prime,
                'critical_points': critical_points,
                'second_derivative': P_double_prime,
                'max_point': (133.33,),
                'max_value': 4333.33,
                'units': 'units'
            }
            return solution
    
    return None

# ===============================
# PAGE 1: HOME / GROUP MEMBERS
# ===============================
if page == t['nav_home']:
    st.markdown(f'<h1 class="main-header">{t["group_members"]}</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="member-card">', unsafe_allow_html=True)
        st.markdown("### Ahmad Rizki Aryadi")
        st.markdown("**NIM:** 004202205038")
        st.markdown("**Role:** Python Coding")
        st.markdown("**Contributions:**")
        st.markdown("- Web interface design")
        st.markdown("- Optimization solver")
        st.markdown("- Web testing")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="member-card">', unsafe_allow_html=True)
        st.markdown("### Christina Malinda Derankian")
        st.markdown("**NIM:** 004202205023")
        st.markdown("**Role:** Content Creator")
        st.markdown("**Contributions:**")
        st.markdown("- Story problem creation")
        st.markdown("- Web testing")
        st.markdown("- Documentation")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="member-card">', unsafe_allow_html=True)
        st.markdown("### Ari Muamar")
        st.markdown("**NIM:** 004202205045")
        st.markdown("**Role:** Report & Presentation")
        st.markdown("**Contributions:**")
        st.markdown("- Presentation creation")
        st.markdown("- Web testing")
        st.markdown("- Project documentation")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### {t['about_project']}")
    st.markdown(t['project_description'])
    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# PAGE 2: FUNCTION & DERIVATIVE
# ===============================
elif page == t['nav_function']:
    st.markdown(f'<h1 class="main-header">{t["function_title"]}</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### {t['input_function']}")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        func_input = st.text_input(
            f"Function f(x) (use x as variable):",
            value="x**3 - 3*x**2 + 2*x + 5",
            help=t['function_example']
        )
    
    with col2:
        x_range = st.slider(f"{t['x_range']}", -10.0, 10.0, (-5.0, 5.0))
    
    if func_input:
        try:
            x = symbols('x')
            f_expr = parse_expr(func_input, transformations='all')
            
            st.markdown('<div class="latex-box">', unsafe_allow_html=True)
            st.markdown("### Entered Function:")
            st.latex(f"f(x) = {latex(f_expr)}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown(f'<div class="sub-header">{t["derivative_process"]}</div>', unsafe_allow_html=True)
            
            st.markdown(f"### {t['derivative_steps']}")
            
            if f_expr.is_Add:
                terms = f_expr.as_ordered_terms()
                st.markdown('<div class="step-box">', unsafe_allow_html=True)
                st.markdown("**Step 1:** Apply sum rule: $(u + v)' = u' + v'$")
                st.markdown(f"$f(x) = {latex(f_expr)}$")
                st.markdown(f"$f'(x) = \\frac{{d}}{{dx}}({latex(terms[0])}) + \\frac{{d}}{{dx}}({latex(terms[1])})$")
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown('<div class="step-box">', unsafe_allow_html=True)
            st.markdown("**Step 2:** Differentiate each term:")
            
            if f_expr.is_Add:
                derivative_terms = []
                for term in f_expr.as_ordered_terms():
                    term_deriv = diff(term, x)
                    st.markdown(f"$\\frac{{d}}{{dx}}({latex(term)}) = {latex(term_deriv)}$")
                    derivative_terms.append(term_deriv)
                f_prime_expr = sum(derivative_terms)
            else:
                f_prime_expr = diff(f_expr, x)
                st.markdown(f"$\\frac{{d}}{{dx}}({latex(f_expr)}) = {latex(f_prime_expr)}$")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown('<div class="step-box">', unsafe_allow_html=True)
            st.markdown(f"**Step 3:** {t['first_derivative']}")
            st.latex(f"f'(x) = {latex(f_prime_expr)}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            if st.checkbox(f"Show {t['second_derivative'].lower()} (f''(x))"):
                f_double_prime = diff(f_expr, x, 2)
                st.markdown('<div class="step-box">', unsafe_allow_html=True)
                st.markdown(f"**{t['second_derivative']}:**")
                st.latex(f"f''(x) = {latex(f_double_prime)}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown(f'<div class="sub-header">📊 {t["function_info"].split(" ")[-1]}</div>', unsafe_allow_html=True)
            
            x_vals = np.linspace(x_range[0], x_range[1], 400)
            f_lambdified = lambdify(x, f_expr, 'numpy')
            f_prime_lambdified = lambdify(x, f_prime_expr, 'numpy')
            
            try:
                y_vals = f_lambdified(x_vals)
                y_prime_vals = f_prime_lambdified(x_vals)
                
                fig, ax = plt.subplots(2, 1, figsize=(10, 8))
                
                ax[0].plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {func_input}')
                ax[0].set_xlabel('x')
                ax[0].set_ylabel('f(x)')
                ax[0].set_title('Function Graph')
                ax[0].grid(True, alpha=0.3)
                ax[0].legend()
                
                ax[1].plot(x_vals, y_prime_vals, 'r-', linewidth=2, label=f"f'(x)")
                ax[1].set_xlabel('x')
                ax[1].set_ylabel("f'(x)")
                ax[1].set_title('First Derivative Graph')
                ax[1].grid(True, alpha=0.3)
                ax[1].legend()
                
                plt.tight_layout()
                st.pyplot(fig)
                
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.markdown(f"### {t['function_info']}")
                    st.write(f"**{t['domain']}** x ∈ [{x_range[0]}, {x_range[1]}]")
                    st.write(f"**{t['local_min']}** {np.min(y_vals):.4f}")
                    st.write(f"**{t['local_max']}** {np.max(y_vals):.4f}")
                
                with col_info2:
                    st.markdown(f"### {t['derivative_info']}")
                    critical_points = solve(f_prime_expr, x)
                    if critical_points:
                        st.write(f"**{t['critical_points']}**")
                        for point in critical_points:
                            st.write(f"x = {latex(point)}")
                
            except Exception as e:
                st.error(f"Visualization error: {str(e)}")
        
        except Exception as e:
            st.error(f"Function parsing error: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# PAGE 3: OPTIMIZATION SOLVER
# ===============================
elif page == t['nav_optimization']:
    st.markdown(f'<h1 class="main-header">{t["optimization_title"]}</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"### {t['input_type']}")
    option = st.radio("", [t['example_problems'], t['manual_input']])
    
    example_problems_dict = {
        t['area_problem1']: t['area_description1'],
        t['area_problem2']: t['area_description2'],
        t['volume_problem1']: t['volume_description1'],
        t['volume_problem2']: t['volume_description2'],
        t['profit_problem1']: t['profit_description1'],
        t['profit_problem2']: t['profit_description2']
    }
    
    if option == t['example_problems']:
        selected_problem = st.selectbox(f"{t['select_category']}:", list(example_problems_dict.keys()))
        problem_text = example_problems_dict[selected_problem]
        st.text_area(f"{t['problem_statement']}:", value=problem_text, height=100)
        
        if selected_problem == t['area_problem1']:
            func_input = "x*(50-x)"
            constraint = "0 < x < 50"
        elif selected_problem == t['area_problem2']:
            func_input = "x*(100 - x/2)"
            constraint = "0 < x < 200"
        elif selected_problem == t['volume_problem1']:
            func_input = "x*(30-2*x)*(20-2*x)"
            constraint = "0 < x < 10"
        elif selected_problem == t['volume_problem2']:
            func_input = "pi*x**2*(10-2*x)"
            constraint = "0 < x < 5"
        elif selected_problem == t['profit_problem1']:
            func_input = "(50000-5000*x)*(800+50*x)"
            constraint = "x >= 0"
        elif selected_problem == t['profit_problem2']:
            func_input = "x*(100-0.2*x) - (1000+20*x+0.1*x**2)"
            constraint = "x >= 0"
    
    else:
        st.markdown(f"### {t['optimization_description']}")
        problem_text = st.text_area(
            f"{t['problem_description']}:",
            height=100,
            placeholder=t['area_description1']
        )
        
        st.markdown(f"### {t['function_config']}")
        col1, col2 = st.columns(2)
        with col1:
            func_input = st.text_input(
                f"{t['objective_function']}:",
                value="x*(50-x)",
                help="Function to maximize or minimize"
            )
        with col2:
            constraint = st.text_input(
                f"{t['constraint']}:",
                value="0 < x < 50",
                help="Example: x > 0, 0 ≤ x ≤ 10"
            )
    
    if func_input:
        st.markdown(f'<div class="sub-header">{t["optimization_steps"]}</div>', unsafe_allow_html=True)
        
        try:
            x = symbols('x')
            f_expr = parse_expr(func_input, transformations='all')
            
            st.markdown('<div class="latex-box">', unsafe_allow_html=True)
            st.markdown("**Optimization function:**")
            st.latex(f"f(x) = {latex(f_expr)}")
            if constraint:
                st.markdown(f"**Constraint:** {constraint}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown('<div class="step-box">', unsafe_allow_html=True)
            st.markdown(f"### {t['step1']}")
            f_prime = diff(f_expr, x)
            st.markdown("Find first derivative:")
            st.latex(f"f'(x) = \\frac{{d}}{{dx}}({latex(f_expr)}) = {latex(f_prime)}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown('<div class="step-box">', unsafe_allow_html=True)
            st.markdown(f"### {t['step2']}")
            st.markdown("Set first derivative to zero:")
            st.latex(f"{latex(f_prime)} = 0")
            
            solutions = solve(f_prime, x)
            if solutions:
                st.markdown("**Solutions:**")
                for i, sol in enumerate(solutions, 1):
                    st.latex(f"x_{{{i}}} = {latex(sol)} ≈ {float(sol):.4f}")
                critical_points = solutions
            else:
                st.warning("No critical points found")
                critical_points = []
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown('<div class="step-box">', unsafe_allow_html=True)
            st.markdown(f"### {t['step3']}")
            if critical_points:
                f_double_prime = diff(f_expr, x, 2)
                st.markdown("Find second derivative:")
                st.latex(f"f''(x) = {latex(f_double_prime)}")
                
                st.markdown("Evaluate at critical points:")
                for sol in critical_points:
                    try:
                        second_deriv_val = f_double_prime.subs(x, sol)
                        st.latex(f"f''({latex(sol)}) = {latex(second_deriv_val)} ≈ {float(second_deriv_val):.4f}")
                        
                        if second_deriv_val > 0:
                            st.success(f"x = {latex(sol)} is **local minimum** (f'' > 0)")
                        elif second_deriv_val < 0:
                            st.success(f"x = {latex(sol)} is **local maximum** (f'' < 0)")
                        else:
                            st.warning("Second derivative test inconclusive")
                    except:
                        pass
            else:
                st.info("No critical points to test")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown('<div class="step-box">', unsafe_allow_html=True)
            st.markdown(f"### {t['step4']}")
            if critical_points:
                for sol in critical_points:
                    try:
                        func_val = f_expr.subs(x, sol)
                        st.latex(f"f({latex(sol)}) = {latex(func_val)} ≈ {float(func_val):.4f}")
                    except:
                        pass
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown(f'<div class="sub-header">📊 Solution Visualization</div>', unsafe_allow_html=True)
            
            x_min, x_max = -5, 5
            if critical_points:
                x_vals = [float(sol) for sol in critical_points if sol.is_real]
                if x_vals:
                    x_min = min(x_vals) - 2
                    x_max = max(x_vals) + 2
            
            x_plot = np.linspace(x_min, x_max, 400)
            f_lambdified = lambdify(x, f_expr, 'numpy')
            f_prime_lambdified = lambdify(x, f_prime, 'numpy')
            
            try:
                y_vals = f_lambdified(x_plot)
                y_prime_vals = f_prime_lambdified(x_plot)
                
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
                
                ax1.plot(x_plot, y_vals, 'b-', linewidth=2, label='f(x)')
                ax1.set_xlabel('x')
                ax1.set_ylabel('f(x)')
                ax1.set_title('Optimization Function')
                ax1.grid(True, alpha=0.3)
                ax1.legend()
                
                if critical_points:
                    for sol in critical_points:
                        try:
                            if sol.is_real:
                                sol_float = float(sol)
                                func_val = f_lambdified(sol_float)
                                ax1.plot(sol_float, func_val, 'ro', markersize=8)
                        except:
                            pass
                
                ax2.plot(x_plot, y_prime_vals, 'r-', linewidth=2, label="f'(x)")
                ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)
                ax2.set_xlabel('x')
                ax2.set_ylabel("f'(x)")
                ax2.set_title('First Derivative')
                ax2.grid(True, alpha=0.3)
                ax2.legend()
                
                if critical_points:
                    for sol in critical_points:
                        try:
                            if sol.is_real:
                                ax2.plot(float(sol), 0, 'ro', markersize=8)
                        except:
                            pass
                
                plt.tight_layout()
                st.pyplot(fig)
                
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(f"### {t['conclusion']}")
                
                if critical_points:
                    max_val = -np.inf
                    min_val = np.inf
                    max_point = None
                    min_point = None
                    
                    for sol in critical_points:
                        if sol.is_real:
                            try:
                                val = float(f_expr.subs(x, sol))
                                if val > max_val:
                                    max_val = val
                                    max_point = float(sol)
                                if val < min_val:
                                    min_val = val
                                    min_point = float(sol)
                            except:
                                pass
                    
                    if max_point is not None:
                        st.success(f"**{t['maximum_value']}** f({max_point:.4f}) = {max_val:.4f}")
                    if min_point is not None:
                        st.success(f"**{t['minimum_value']}** f({min_point:.4f}) = {min_val:.4f}")
                
                if 'problem_text' in locals() and problem_text:
                    st.markdown(f"### {t['interpretation']}")
                    st.info(problem_text)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Visualization error: {str(e)}")
        
        except Exception as e:
            st.error(f"Optimization processing error: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# PAGE 4: STORY OPTIMIZATION PROBLEMS
# ===============================
elif page == t['nav_story_problems']:
    st.markdown(f'<h1 class="main-header">{t["story_title"]}</h1>', unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    category = st.selectbox(
        f"{t['select_category']}:",
        [t['area'], t['volume'], t['profit']]
    )
    
    if category == t['area']:
        st.markdown('<div class="problem-card">', unsafe_allow_html=True)
        st.markdown(f"### 1. {t['area_problem1']}")
        st.markdown(f"**{t['problem_statement']}**")
        st.write(t['area_description1'])
        
        st.markdown(f"**{t['problem_formulation']}**")
        st.write(t['area_formulation1'])
        
        if st.button(f"Solve Problem 1 ({t['area']})"):
            solution = solve_story_problem('area', 1)
            if solution:
                st.markdown(f"**{t['solution_steps']}**")
                st.write(t['area_solution1'])
                
                st.markdown(f"**{t['final_answer']}**")
                st.success(f"Maximum area = {solution['max_value']} square {t['units']}")
                st.success(f"Dimensions: length = {solution['max_point'][0]} {t['units']}, width = {solution['max_point'][1]} {t['units']}")
                
                st.latex(f"A(x) = {latex(solution['function'])}")
                st.latex(f"A'(x) = {latex(solution['derivative'])}")
                st.latex(f"A''(x) = {latex(solution['second_derivative'])}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="problem-card">', unsafe_allow_html=True)
        st.markdown(f"### 2. {t['area_problem2']}")
        st.markdown(f"**{t['problem_statement']}**")
        st.write(t['area_description2'])
        
        st.markdown(f"**{t['problem_formulation']}**")
        st.write(t['area_formulation2'])
        
        if st.button(f"Solve Problem 2 ({t['area']})"):
            solution = solve_story_problem('area', 2)
            if solution:
                st.markdown(f"**{t['solution_steps']}**")
                st.write("1. A(x) = 100x - x²/2")
                st.write("2. A'(x) = 100 - x")
                st.write("3. Set A'(x) = 0 → x = 100")
                st.write("4. A''(x) = -1 < 0 (maximum)")
                st.write("5. y = 100 - 100/2 = 50")
                
                st.markdown(f"**{t['final_answer']}**")
                st.success(f"Maximum area = {solution['max_value']} square {t['units']}")
                st.success(f"Dimensions: length parallel to river = {solution['max_point'][0]} {t['units']}, width = {solution['max_point'][1]} {t['units']}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif category == t['volume']:
        st.markdown('<div class="problem-card">', unsafe_allow_html=True)
        st.markdown(f"### 1. {t['volume_problem1']}")
        st.markdown(f"**{t['problem_statement']}**")
        st.write(t['volume_description1'])
        
        st.markdown(f"**{t['problem_formulation']}**")
        st.write(t['volume_formulation1'])
        
        if st.button(f"Solve Problem 1 ({t['volume']})"):
            solution = solve_story_problem('volume', 1)
            if solution:
                st.markdown(f"**{t['solution_steps']}**")
                st.write("1. V(x) = x(30-2x)(20-2x) = 4x³ - 100x² + 600x")
                st.write("2. V'(x) = 12x² - 200x + 600")
                st.write("3. Solve V'(x) = 0 → x ≈ 3.924 or x ≈ 12.743")
                st.write("4. x ≈ 12.743 invalid (too large), so x ≈ 3.924")
                st.write("5. V''(3.924) < 0 (maximum)")
                
                st.markdown(f"**{t['final_answer']}**")
                st.success(f"Maximum volume ≈ {solution['max_value']} cubic {t['units']}")
                st.success(f"Cut size = {solution['max_point'][0]:.3f} {t['units']}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="problem-card">', unsafe_allow_html=True)
        st.markdown(f"### 2. {t['volume_problem2']}")
        st.markdown(f"**{t['problem_statement']}**")
        st.write(t['volume_description2'])
        
        st.markdown(f"**{t['problem_formulation']}**")
        st.write(t['volume_formulation2'])
        
        if st.button(f"Solve Problem 2 ({t['volume']})"):
            solution = solve_story_problem('volume', 2)
            if solution:
                st.markdown(f"**{t['solution_steps']}**")
                st.write("1. V(r) = πr²(10-2r) = 10πr² - 2πr³")
                st.write("2. V'(r) = 20πr - 6πr²")
                st.write("3. Set V'(r) = 0 → r(20 - 6r) = 0 → r = 0 or r = 10/3")
                st.write("4. r = 0 invalid, so r = 10/3 ≈ 3.333")
                st.write("5. V''(10/3) < 0 (maximum)")
                st.write("6. h = 10 - 2*(10/3) = 10/3 ≈ 3.333")
                
                st.markdown(f"**{t['final_answer']}**")
                st.success(f"Maximum volume ≈ {solution['max_value']:.1f}π cubic {t['units']} ≈ {solution['max_value']:.1f} cubic {t['units']}")
                st.success(f"Cylinder radius = {solution['max_point'][0]:.3f} {t['units']}, height = {solution['max_point'][0]:.3f} {t['units']}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif category == t['profit']:
        st.markdown('<div class="problem-card">', unsafe_allow_html=True)
        st.markdown(f"### 1. {t['profit_problem1']}")
        st.markdown(f"**{t['problem_statement']}**")
        st.write(t['profit_description1'])
        
        st.markdown(f"**{t['problem_formulation']}**")
        st.write(t['profit_formulation1'])
        
        if st.button(f"Solve Problem 1 ({t['profit']})"):
            solution = solve_story_problem('profit', 1)
            if solution:
                st.markdown(f"**{t['solution_steps']}**")
                st.write("1. P(x) = (50000-5000x)(800+50x) = -250000x² + 2000000x + 40000000")
                st.write("2. P'(x) = -500000x + 2000000")
                st.write("3. Set P'(x) = 0 → x = 4")
                st.write("4. P''(x) = -500000 < 0 (maximum)")
                st.write("5. Price = 50000 - 5000*4 = 30000")
                st.write("6. Audience = 800 + 50*4 = 1000")
                
                st.markdown(f"**{t['final_answer']}**")
                st.success(f"Maximum profit = Rp {solution['max_value']:,}")
                st.success(f"Ticket price = Rp 30,000, Audience = 1000 people")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="problem-card">', unsafe_allow_html=True)
        st.markdown(f"### 2. {t['profit_problem2']}")
        st.markdown(f"**{t['problem_statement']}**")
        st.write(t['profit_description2'])
        
        st.markdown(f"**{t['problem_formulation']}**")
        st.write(t['profit_formulation2'])
        
        if st.button(f"Solve Problem 2 ({t['profit']})"):
            solution = solve_story_problem('profit', 2)
            if solution:
                st.markdown(f"**{t['solution_steps']}**")
                st.write("1. P(x) = -0.3x² + 80x - 1000")
                st.write("2. P'(x) = -0.6x + 80")
                st.write("3. Set P'(x) = 0 → x = 80/0.6 = 400/3 ≈ 133.33")
                st.write("4. P''(x) = -0.6 < 0 (maximum)")
                
                st.markdown(f"**{t['final_answer']}**")
                st.success(f"Maximum profit = {solution['max_value']:.2f} {t['units']}")
                st.success(f"Production quantity = {solution['max_point'][0]:.2f} {t['units']}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# FOOTER
# ===============================
st.markdown("---")
st.markdown(
    f"""
    <div style="text-align: center; color: #666; padding: 20px;">
        <p>{t['footer']}</p>
    </div>
    """,
    unsafe_allow_html=True
)


