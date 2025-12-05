import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import re
from sympy import symbols, diff, latex, solve, lambdify, integrate
from sympy.parsing.sympy_parser import parse_expr
import warnings
warnings.filterwarnings('ignore')

# Konfigurasi halaman
st.set_page_config(
    page_title="Math Function & Optimization WebApp",
    page_icon="📊",
    layout="wide"
)

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
</style>
""", unsafe_allow_html=True)

# Sidebar untuk navigasi
st.sidebar.title("🔢 Navigasi Aplikasi")
page = st.sidebar.radio("Pilih Halaman:", 
                         ["🏠 Anggota Kelompok", "📈 Fungsi & Turunan", "⚡ Pemecah Optimisasi"])

# Halaman 1: Anggota Kelompok
if page == "🏠 Anggota Kelompok":
    st.markdown('<h1 class="main-header">👥 Anggota Kelompok</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="member-card">', unsafe_allow_html=True)
        st.markdown("### Ahmad Rizki Aryadi")
        st.markdown("**NIM:** 004202205038")
        st.markdown("**Peran:** Membuat cooding python")
        st.markdown("**Kontribusi:**")
        st.markdown("- Mendesign tampilan web")
        st.markdown("- Optimisasi solver")
        st.markdown("- testing web ")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="member-card">', unsafe_allow_html=True)
        st.markdown("### Christina Malinda Derankian")
        st.markdown("**NIM:** 004202205023")
        st.markdown("**Peran:** isi materi web")
        st.markdown("**Kontribusi:**")
        st.markdown("- Membuat soal cerita ")
        st.markdown("- testing web ")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="member-card">', unsafe_allow_html=True)
        st.markdown("### Ari Muamar")
        st.markdown("**NIM:** 1122334455")
        st.markdown("**Peran:** Membuat report")
        st.markdown("**Kontribusi:**")
        st.markdown("- Membuat ppt")
        st.markdown("- testing web ")
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 📋 Tentang Proyek")
    st.markdown("""
    Aplikasi web ini dibuat untuk memenuhi tugas proyek Matematika Lanjutan dengan fitur:
    1. **Visualisasi fungsi matematika** dengan grafik interaktif
    2. **Kalkulator turunan** dengan penjelasan langkah demi langkah
    3. **Pemecah masalah optimisasi** untuk soal cerita
    4. **Antarmuka yang user-friendly** dengan tampilan LaTeX
    """)
    st.markdown("</div>", unsafe_allow_html=True)

# Halaman 2: Fungsi & Turunan
elif page == "📈 Fungsi & Turunan":
    st.markdown('<h1 class="main-header">📊 Visualisasi Fungsi & Turunan</h1>', unsafe_allow_html=True)
    
    # Input fungsi
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Masukkan Fungsi Matematika")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        func_input = st.text_input(
            "Fungsi f(x) (gunakan x sebagai variabel):",
            value="x**3 - 3*x**2 + 2*x + 5",
            help="Contoh: sin(x), exp(x), x**2 + 3*x - 5, log(x)"
        )
    
    with col2:
        x_range = st.slider("Rentang x:", -10.0, 10.0, (-5.0, 5.0))
    
    # Validasi input
    if func_input:
        try:
            x = symbols('x')
            # Parse fungsi
            f_expr = parse_expr(func_input, transformations='all')
            
            # Tampilkan fungsi dalam LaTeX
            st.markdown('<div class="latex-box">', unsafe_allow_html=True)
            st.markdown("### Fungsi yang dimasukkan:")
            st.latex(f"f(x) = {latex(f_expr)}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Hitung turunan
            st.markdown('<div class="sub-header">🎯 Proses Turunan</div>', unsafe_allow_html=True)
            
            # Langkah-langkah turunan
            st.markdown("### Langkah-langkah Turunan:")
            
            # Cek jika fungsi merupakan penjumlahan/pengurangan
            if f_expr.is_Add:
                terms = f_expr.as_ordered_terms()
                st.markdown('<div class="step-box">', unsafe_allow_html=True)
                st.markdown("**Langkah 1:** Terapkan aturan penjumlahan: $(u + v)' = u' + v'$")
                st.markdown(f"$f(x) = {latex(f_expr)}$")
                st.markdown(f"$f'(x) = \\frac{{d}}{{dx}}({latex(terms[0])}) + \\frac{{d}}{{dx}}({latex(terms[1])})$")
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Turunan dari masing-masing suku
            st.markdown('<div class="step-box">', unsafe_allow_html=True)
            st.markdown("**Langkah 2:** Turunkan setiap suku:")
            
            # Pecah menjadi suku-suku individu
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
            
            # Tampilkan hasil akhir
            st.markdown('<div class="step-box">', unsafe_allow_html=True)
            st.markdown("**Langkah 3:** Hasil turunan pertama:")
            st.latex(f"f'(x) = {latex(f_prime_expr)}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Hitung turunan kedua jika diminta
            if st.checkbox("Tampilkan turunan kedua (f''(x))"):
                f_double_prime = diff(f_expr, x, 2)
                st.markdown('<div class="step-box">', unsafe_allow_html=True)
                st.markdown("**Turunan kedua:**")
                st.latex(f"f''(x) = {latex(f_double_prime)}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Visualisasi
            st.markdown('<div class="sub-header">📊 Visualisasi Grafik</div>', unsafe_allow_html=True)
            
            # Buat data untuk plotting
            x_vals = np.linspace(x_range[0], x_range[1], 400)
            f_lambdified = lambdify(x, f_expr, 'numpy')
            f_prime_lambdified = lambdify(x, f_prime_expr, 'numpy')
            
            try:
                y_vals = f_lambdified(x_vals)
                y_prime_vals = f_prime_lambdified(x_vals)
                
                # Plot
                fig, ax = plt.subplots(2, 1, figsize=(10, 8))
                
                # Plot fungsi asli
                ax[0].plot(x_vals, y_vals, 'b-', linewidth=2, label=f'f(x) = {func_input}')
                ax[0].set_xlabel('x')
                ax[0].set_ylabel('f(x)')
                ax[0].set_title('Grafik Fungsi Asli')
                ax[0].grid(True, alpha=0.3)
                ax[0].legend()
                
                # Plot turunan
                ax[1].plot(x_vals, y_prime_vals, 'r-', linewidth=2, label=f"f'(x)")
                ax[1].set_xlabel('x')
                ax[1].set_ylabel("f'(x)")
                ax[1].set_title('Grafik Turunan Pertama')
                ax[1].grid(True, alpha=0.3)
                ax[1].legend()
                
                plt.tight_layout()
                st.pyplot(fig)
                
                # Info tambahan
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.markdown("### 📈 Informasi Fungsi")
                    st.write(f"**Domain:** x ∈ [{x_range[0]}, {x_range[1]}]")
                    st.write(f"**Nilai minimum lokal:** {np.min(y_vals):.4f}")
                    st.write(f"**Nilai maksimum lokal:** {np.max(y_vals):.4f}")
                
                with col_info2:
                    st.markdown("### 📉 Informasi Turunan")
                    # Cari titik kritis
                    critical_points = solve(f_prime_expr, x)
                    if critical_points:
                        st.write("**Titik kritis:**")
                        for point in critical_points:
                            st.write(f"x = {latex(point)}")
                    
            except Exception as e:
                st.error(f"Error dalam visualisasi: {str(e)}")
        
        except Exception as e:
            st.error(f"Error dalam parsing fungsi: {str(e)}")
            st.info("Pastikan fungsi menggunakan sintaks Python yang valid. Contoh: 'x**2 + sin(x)'")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Halaman 3: Optimisasi
elif page == "⚡ Pemecah Optimisasi":
    st.markdown('<h1 class="main-header">⚡ Pemecah Masalah Optimisasi</h1>', unsafe_allow_html=True)
    
    # Pilihan: contoh atau input manual
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Pilih jenis input:")
    option = st.radio("", ["Gunakan contoh soal", "Masukkan soal optimisasi manual"])
    
    if option == "Gunakan contoh soal":
        example_problems = {
            "Kotak tanpa tutup": "Seorang pengrajin ingin membuat kotak tanpa tutup dari selembar karton berukuran 12 inci x 20 inci dengan memotong persegi identik dari setiap sudut dan melipat sisi-sisinya ke atas. Tentukan ukuran potongan yang menghasilkan volume maksimum.",
            "Jarak minimum": "Tentukan titik pada kurva y = x² yang terdekat dengan titik (0, 3).",
            "Luas maksimum": "Seorang petani memiliki 200 meter pagar untuk membatasi area persegi panjang di samping sungai (tidak perlu pagar di sisi sungai). Tentukan dimensi yang memberikan luas maksimum."
        }
        
        selected_problem = st.selectbox("Pilih contoh soal:", list(example_problems.keys()))
        problem_text = example_problems[selected_problem]
        st.text_area("Soal:", value=problem_text, height=100)
        
        # Predefined solutions
        if selected_problem == "Kotak tanpa tutup":
            func_input = "x*(12-2*x)*(20-2*x)"  # Volume
            constraint = "0 < x < 6"  # x adalah panjang potongan
            
        elif selected_problem == "Jarak minimum":
            func_input = "sqrt(x**2 + (x**2 - 3)**2)"  # Jarak kuadrat
            constraint = "x ∈ ℝ"
            
        elif selected_problem == "Luas maksimum":
            func_input = "x*(200-2*x)"  # Luas
            constraint = "0 < x < 100"
    
    else:  # Input manual
        st.markdown("### Masukkan Soal Optimisasi:")
        problem_text = st.text_area(
            "Deskripsi masalah:",
            height=100,
            placeholder="Contoh: Tentukan dua bilangan yang jumlahnya 20 dan hasil kalinya maksimum."
        )
        
        st.markdown("### Konfigurasi Fungsi:")
        col1, col2 = st.columns(2)
        with col1:
            func_input = st.text_input(
                "Fungsi yang akan dioptimalkan (f(x)):",
                value="x*(20-x)",
                help="Fungsi yang ingin dimaksimalkan atau diminimalkan"
            )
        
        with col2:
            constraint = st.text_input(
                "Kendala (jika ada):",
                value="0 < x < 20",
                help="Contoh: x > 0, 0 ≤ x ≤ 10"
            )
    
    # Proses optimisasi
    if func_input:
        st.markdown('<div class="sub-header">🔍 Proses Penyelesaian</div>', unsafe_allow_html=True)
        
        try:
            x = symbols('x')
            f_expr = parse_expr(func_input, transformations='all')
            
            # Tampilkan fungsi
            st.markdown('<div class="latex-box">', unsafe_allow_html=True)
            st.markdown("**Fungsi yang dioptimalkan:**")
            st.latex(f"f(x) = {latex(f_expr)}")
            if constraint:
                st.markdown(f"**Dengan kendala:** {constraint}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Langkah 1: Cari turunan pertama
            st.markdown('<div class="step-box">', unsafe_allow_html=True)
            st.markdown("### Langkah 1: Turunan Pertama")
            f_prime = diff(f_expr, x)
            st.markdown("Cari turunan pertama fungsi:")
            st.latex(f"f'(x) = \\frac{{d}}{{dx}}({latex(f_expr)}) = {latex(f_prime)}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Langkah 2: Cari titik kritis
            st.markdown('<div class="step-box">', unsafe_allow_html=True)
            st.markdown("### Langkah 2: Titik Kritis")
            st.markdown("Atur turunan pertama sama dengan nol untuk mencari titik kritis:")
            st.latex(f"{latex(f_prime)} = 0")
            
            # Selesaikan untuk x
            solutions = solve(f_prime, x)
            if solutions:
                st.markdown("**Solusi:**")
                for i, sol in enumerate(solutions, 1):
                    st.latex(f"x_{{{i}}} = {latex(sol)} ≈ {float(sol):.4f}")
                critical_points = solutions
            else:
                st.warning("Tidak ditemukan titik kritis (mungkin perlu memeriksa batas domain)")
                critical_points = []
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Langkah 3: Uji turunan kedua
            st.markdown('<div class="step-box">', unsafe_allow_html=True)
            st.markdown("### Langkah 3: Uji Turunan Kedua")
            if critical_points:
                f_double_prime = diff(f_expr, x, 2)
                st.markdown("Cari turunan kedua:")
                st.latex(f"f''(x) = {latex(f_double_prime)}")
                
                st.markdown("Evaluasi pada titik kritis:")
                for sol in critical_points:
                    try:
                        second_deriv_val = f_double_prime.subs(x, sol)
                        st.latex(f"f''({latex(sol)}) = {latex(second_deriv_val)} ≈ {float(second_deriv_val):.4f}")
                        
                        if second_deriv_val > 0:
                            st.success(f"x = {latex(sol)} adalah **minimum lokal** (f'' > 0)")
                        elif second_deriv_val < 0:
                            st.success(f"x = {latex(sol)} adalah **maksimum lokal** (f'' < 0)")
                        else:
                            st.warning("Uji turunan kedua tidak konklusif")
                    except:
                        pass
            else:
                st.info("Tidak ada titik kritis untuk diuji")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Langkah 4: Evaluasi fungsi
            st.markdown('<div class="step-box">', unsafe_allow_html=True)
            st.markdown("### Langkah 4: Nilai Optimum")
            
            # Evaluasi fungsi pada titik kritis
            if critical_points:
                for sol in critical_points:
                    try:
                        func_val = f_expr.subs(x, sol)
                        st.latex(f"f({latex(sol)}) = {latex(func_val)} ≈ {float(func_val):.4f}")
                    except:
                        pass
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Visualisasi
            st.markdown('<div class="sub-header">📊 Visualisasi Solusi</div>', unsafe_allow_html=True)
            
            # Tentukan rentang x untuk plotting
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
                
                # Plot fungsi
                ax1.plot(x_plot, y_vals, 'b-', linewidth=2, label='f(x)')
                ax1.set_xlabel('x')
                ax1.set_ylabel('f(x)')
                ax1.set_title('Fungsi yang Dioptimalkan')
                ax1.grid(True, alpha=0.3)
                ax1.legend()
                
                # Tandai titik kritis
                if critical_points:
                    for sol in critical_points:
                        try:
                            if sol.is_real:
                                sol_float = float(sol)
                                func_val = f_lambdified(sol_float)
                                ax1.plot(sol_float, func_val, 'ro', markersize=8, 
                                        label=f'x = {sol_float:.2f}')
                        except:
                            pass
                
                # Plot turunan
                ax2.plot(x_plot, y_prime_vals, 'r-', linewidth=2, label="f'(x)")
                ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)
                ax2.set_xlabel('x')
                ax2.set_ylabel("f'(x)")
                ax2.set_title('Turunan Pertama')
                ax2.grid(True, alpha=0.3)
                ax2.legend()
                
                # Tandai titik nol turunan
                if critical_points:
                    for sol in critical_points:
                        try:
                            if sol.is_real:
                                ax2.plot(float(sol), 0, 'ro', markersize=8)
                        except:
                            pass
                
                plt.tight_layout()
                st.pyplot(fig)
                
                # Kesimpulan
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### ✅ Kesimpulan")
                
                if critical_points:
                    # Cari maksimum dan minimum
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
                        st.success(f"**Nilai maksimum:** f({max_point:.4f}) = {max_val:.4f}")
                    if min_point is not None:
                        st.success(f"**Nilai minimum:** f({min_point:.4f}) = {min_val:.4f}")
                
                # Interpretasi untuk soal cerita
                if 'problem_text' in locals() and problem_text:
                    st.markdown("### 📝 Interpretasi untuk Soal:")
                    st.info(problem_text)
                    
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error dalam visualisasi: {str(e)}")
        
        except Exception as e:
            st.error(f"Error dalam memproses optimisasi: {str(e)}")
            st.info("Pastikan fungsi menggunakan sintaks yang valid. Contoh: x*(20-x) untuk x(20-x)")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: #666; padding: 20px;">
        <p><strong>Mathematical Function & Optimization WebApp</strong> | Dibuat dengan Streamlit, SymPy, dan Matplotlib</p>
        <p>© 2024 Kelompok: Ahmad Rizki Aryadi, Christina Malinda Derankian, Ari Muamar</p>
    </div>
    """,
    unsafe_allow_html=True
)