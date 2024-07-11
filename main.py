import streamlit as st
import pandas as pd
import numpy as np
import math

# Inisialisasi data1 dan data2 dengan menggunakan state
if 'data1' not in st.session_state:
    st.session_state.data1 = [
        60, 90, 90, 120, 90, 60, 90, 120, 90, 30, 60, 60, 90, 120, 30, 60, 60, 90, 30, 90, 60, 90, 90, 60, 30, 90, 60, 90, 
        120, 90, 30, 90, 90, 60, 30, 90, 60, 90, 90, 90, 60, 60, 90, 90, 60, 60, 120, 90, 90, 90, 60, 60, 90, 90, 60, 90, 
        120, 90, 120, 90, 90, 120, 90, 90, 90, 90, 120, 90, 90, 60, 90, 120, 120, 90, 90, 60, 60, 30, 60, 30, 120, 90, 120, 
        90, 90, 90, 60, 90, 60, 120, 90, 90, 120, 90, 60, 90, 120, 90, 30, 120
    ]

if 'data2' not in st.session_state:
    st.session_state.data2 = [
        75, 75, 75, 70, 90, 85, 70, 80, 70, 75, 75, 75, 70, 80, 85, 85, 70, 75, 70, 75, 75, 70, 75, 65, 75, 85, 75, 75, 
        75, 75, 75, 70, 70, 65, 85, 85, 75, 75, 75, 75, 75, 80, 85, 75, 75, 65, 75, 75, 75, 75, 65, 80, 85, 80, 75, 90, 60, 
        75, 75, 85, 75, 80, 80, 80, 85, 75, 80, 65, 75, 85, 80, 65, 80, 80, 75, 75, 80, 75, 75, 85, 60, 65, 70, 75, 75, 70, 
        80, 75, 75, 75, 60, 75, 70, 75, 75, 70, 80, 75, 75, 75
    ]

# Fungsi untuk menghitung distribusi frekuensi dan statistik
def calculate_frequency(data):
    freq_table = pd.Series(data).value_counts().sort_index().reset_index()
    freq_table.columns = ['Waktu', 'Frequency']

    mean = np.mean(data)
    variance = np.var(data)
    std_dev = np.std(data)

    return freq_table, mean, variance, std_dev

# Fungsi untuk menambah data ke data1 dan data2
def add_data(data_key, new_data):
    new_data_list = new_data.split(',')
    new_data_list = [int(val.strip()) for val in new_data_list]  # Convert to integers
    st.session_state[data_key].extend(new_data_list)

# Fungsi untuk menghasilkan tabel Linear Congruential Generator (LCG)
def generate_lcg_table(seed, a, c, m, n, data_mean, data_std_dev):
    if n < 100:
        st.warning("The value of n must be 100 or greater.")
        return None
    
    lcg_data = []
    ui_values = []
    ui_plus_1_values = []
    ln_ui_values = []
    sqrt_values = []
    sin_values = []
    z_values = []
    x_values = []
    used_values = set()
    phi = math.pi
    x = seed
    for _ in range(n + 1):
        x = (a * x + c) % m
        if x in used_values:
            st.warning(f"Duplicate value detected: {x}. Adjusting parameters to avoid duplicates.")
            a += 1  # Adjust parameter to avoid duplicates
            x = (a * x + c) % m  # Recalculate x
        lcg_data.append(x)
        ui = x / m
        ui_plus_1 = ((a * x + c) % m) / m if _ < n else np.nan  # Calculate Ui+1
        ui_values.append(ui)
        ui_plus_1_values.append(ui_plus_1)
        ln_ui = np.log(ui)
        ln_ui_values.append(ln_ui)
        sqrt_value = np.sqrt(-2 * ln_ui) if ln_ui != 0 else np.nan
        sqrt_values.append(sqrt_value)
        sin_value = np.sin(2 * phi * ui_plus_1)
        sin_values.append(sin_value)
        z_value = sqrt_value * sin_value
        z_values.append(z_value)
        x_value = data_mean + data_std_dev * z_value
        x_values.append(x_value)
        used_values.add(x)
    
    # Buat DataFrame untuk tabel LCG
    lcg_table = pd.DataFrame({
        'Index': range(1, n + 2),  # <- Adjusting index range
        'LCG Value': lcg_data,
        'Ui': ui_values,
        'Ui+1': ui_plus_1_values,
        '(-2lnUi)^1/2': sqrt_values,
        'Sin(2PHIUi+1)': sin_values,
        'z': z_values,
        'x': x_values
    })
    
    # Hapus baris dengan nilai NaN di kolom x
    lcg_table = lcg_table.dropna(subset=['x'])
    
    # Bulatkan nilai kolom x
    lcg_table['x'] = lcg_table['x'].round(0).astype(int)
    
    return lcg_table

# Fungsi untuk membuat tabel simulasi
def create_simulation_table(lcg_table1, lcg_table2):
    # Ambil kolom A dari Ui LCG1
    kolom_A = lcg_table1['Ui'].values.tolist()
    
    # Ambil kolom B dari Ui LCG2
    kolom_B = lcg_table2['Ui'].values.tolist()
    
    # Ambil kolom C dari kolom x LCG1
    kolom_C = lcg_table1['x'].values.tolist()
    
    # Ambil kolom D dari kolom x LCG2
    kolom_E = lcg_table2['x'].values.tolist()
    
    # Tambahkan kolom F yang konstan 5
    kolom_F = [5] * len(kolom_A)
    
    # Hitung nilai kumulatif untuk kolom C
    kolom_D = np.cumsum(kolom_C).tolist()
    
    # Tambahkan kolom G yang nilai hasil dari kolom D + E
    kolom_G = [d + e for d, e in zip(kolom_E, kolom_D)]
    
    # Tambahkan kolom H sesuai aturan yang diberikan
    kolom_H = []
    for g_minus_1, e in zip([0] + kolom_G[:-1], kolom_D):
        if g_minus_1 > e:
            kolom_H.append(g_minus_1 - e)
        else:
            kolom_H.append(0)
    
    # Tambahkan kolom I sesuai aturan yang diberikan
    kolom_I = []
    for e, g_minus_1 in zip(kolom_D, [0] + kolom_G[:-1]):
        if e > g_minus_1:
            kolom_I.append(e - g_minus_1)
        else:
            kolom_I.append(0)
    
    # Buat DataFrame untuk tabel simulasi
    simulation_table = pd.DataFrame({
        'A': kolom_A,
        'B': kolom_B,
        'C': kolom_C,
        'D': kolom_D,
        'E': kolom_E,
        'F': kolom_F,
        'G': kolom_G,
        'H': kolom_H,
        'I': kolom_I
    })
    
    return simulation_table

# Streamlit app
st.title("Streamlit App for LCG Simulation")

# Input baru untuk data1
st.sidebar.title("Tambah Data Waktu Antar Kedatangan Telepon Pemesanan")
new_data1 = st.sidebar.text_input("Enter new data for Data1 (comma separated values):")
if st.sidebar.button("Add to Data1"):
    if new_data1:
        add_data('data1', new_data1)

# Input baru untuk data2
st.sidebar.title("Tambah Data Waktu Penerimaan Telepon Pemesanan")
new_data2 = st.sidebar.text_input("Enter new data for Data2 (comma separated values):")
if st.sidebar.button("Add to Data2"):
    if new_data2:
        add_data('data2', new_data2)

# Tampilkan data1 dan data2 dalam bentuk teks
st.write("### Waktu Antar Kedatangan Telepon Pemesanan")
st.write("", ', '.join(map(str, st.session_state.data1)))
st.write("### Waktu Penerimaan Telepon Pemesanan")
st.write("", ', '.join(map(str, st.session_state.data2)))

# Hitung distribusi frekuensi dan statistik untuk Data1
freq_table1, mean1, var1, std_dev1 = calculate_frequency(st.session_state.data1)

# Tampilkan tabel distribusi frekuensi dan statistik untuk Data1
st.write("### Tabel Frekuensi Waktu Antar Kedatangan Telepon Pemesanan")
st.write("Mean:", round(mean1, 2))
st.write("Variance:", round(var1, 2))
st.write("Standard Deviation:", round(std_dev1, 2))
st.dataframe(freq_table1, hide_index=True)

# Hitung distribusi frekuensi dan statistik untuk Data2
freq_table2, mean2, var2, std_dev2 = calculate_frequency(st.session_state.data2)

# Tampilkan tabel distribusi frekuensi dan statistik untuk Data2
st.write("### Tabel Frekuensi Waktu Penerimaan Telepon Pemesanan")
st.write("Mean:", round(mean2, 2))
st.write("Variance:", round(var2, 2))
st.write("Standard Deviation:", round(std_dev2, 2))
st.dataframe(freq_table2, hide_index=True)

# Plot histogram based on frequency distribution for Data1
st.write("### Histogram Waktu Antar Kedatangan Telepon Pemesanan")
st.bar_chart(freq_table1.set_index('Waktu')['Frequency'])

# Plot histogram based on frequency distribution for Data2
st.write("### Histogram Waktu Penerimaan Telepon Pemesanan")
st.bar_chart(freq_table2.set_index('Waktu')['Frequency'])

# Tampilkan tabel LCG dan simulasi
st.sidebar.title("Linear Congruential Generator (LCG) Parameters")
n = st.sidebar.number_input("Number of values (n) for LCG Table 1", min_value=100, step=1, value=100)
col1, col2 = st.sidebar.columns(2)

with col1:
    seed1 = st.number_input("Z0 for LCG Table 1", min_value=0, step=1, value=10122035)
    a1 = st.number_input("Multiplier (a) for LCG Table 1", min_value=0, step=1, value=21)
    c1 = st.number_input("Increment (c) for LCG Table 1", min_value=0, step=1, value=31)
    m1 = st.number_input("Modulus (m) for LCG Table 1", min_value=1, step=1, value=500)

with col2:
    seed2 = st.number_input("Z0 for LCG Table 2", min_value=0, step=1, value=10122001)
    a2 = st.number_input("Multiplier (a) for LCG Table 2", min_value=0, step=1, value=31)
    c2 = st.number_input("Increment (c) for LCG Table 2", min_value=0, step=1, value=51)
    m2 = st.number_input("Modulus (m) for LCG Table 2", min_value=1, step=1, value=1000)

# Generate LCG tables
lcg_table1 = generate_lcg_table(seed1, a1, c1, m1, n, mean1, std_dev1)
lcg_table2 = generate_lcg_table(seed2, a2, c2, m2, n, mean2, std_dev2)

# Tampilkan tabel LCG
if lcg_table1 is not None:
    st.write("### LCG Table 1")
    st.dataframe(lcg_table1, hide_index=True)

if lcg_table2 is not None:
    st.write("### LCG Table 2")
    st.dataframe(lcg_table2, hide_index=True)

# Buat dan tampilkan tabel simulasi
simulation_table = create_simulation_table(lcg_table1, lcg_table2)
if not simulation_table.empty:
    st.write("### Simulation Table")
    st.dataframe(simulation_table, hide_index=True)
    st.write("## Keterangan : ")
    st.write("A = Waktu Kedatangan Telepon Pemesanan")
    st.write("B = Waktu Penerimaan Telepon Pemesanan")
    st.write("C = Waktu Kedatangan Telepon Pemesanan (Detik)")
    st.write("D = Kumulatif Kedatangan Telepon Pemesanan (Detik)")
    st.write("E = Lama Penerimaan Telepon Pemesanan")
    st.write("F = Jumlah Pemesanan Air Mineral (Galon)")
    st.write("G = Selesai Waktu Pelayanan")
    st.write("H = Waktu Pelanggan Menunggu Pelayanan")
    st.write("I = Waktu Customer Service Menganggur")
