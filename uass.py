import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd  # Ditambahkan untuk merapikan representasi matriks
import matplotlib

# Memaksa matplotlib menggunakan backend Agg agar tidak memicu warning thread di Streamlit
matplotlib.use('Agg')

# ==========================================
# 1. INITIALIZATION & STATE MANAGEMENT
# ==========================================
if 'nodes' not in st.session_state:
    # Node awal (Denpasar & sekitarnya)
    st.session_state.nodes = ["Gudang Pusat", "Toko Gianyar", "Kurir Denpasar", "Drop Point Badung"]

if 'graph_list' not in st.session_state:
    # Representasi 1: Adjacency List (Weighted & Undirected Graph)
    st.session_state.graph_list = {
        "Gudang Pusat": [("Toko Gianyar", 25), ("Kurir Denpasar", 10)],
        "Toko Gianyar": [("Gudang Pusat", 25), ("Drop Point Badung", 30)],
        "Kurir Denpasar": [("Gudang Pusat", 10), ("Drop Point Badung", 15)],
        "Drop Point Badung": [("Toko Gianyar", 30), ("Kurir Denpasar", 15)]
    }

# ==========================================
# 2. HELPER FUNCTIONS (REPRESENTATION CONVERSION)
# ==========================================
def get_adjacency_matrix():
    """Mengubah Adjacency List menjadi Adjacency Matrix (Representasi 2)"""
    nodes = st.session_state.nodes
    n = len(nodes)
    # Inisialisasi matriks dengan nilai tak hingga (inf)
    matrix = [[float('inf')] * n for _ in range(n)]
    
    # Jarak ke diri sendiri adalah 0
    for i in range(n):
        matrix[i][i] = 0
        
    # Isi bobot berdasarkan adjacency list
    for u_idx, node_u in enumerate(nodes):
        if node_u in st.session_state.graph_list:
            for node_v, weight in st.session_state.graph_list[node_u]:
                if node_v in nodes:
                    v_idx = nodes.index(node_v)
                    matrix[u_idx][v_idx] = weight
    return matrix

# ==========================================
# 3. ALGORITMA DIJKSTRA (ANALYSIS & LOG PROCESS)
# ==========================================
def dijkstra_shortest_path(start_node, target_node):
    """Menghitung rute terpendek sekaligus merekam log proses perhitungan"""
    nodes = st.session_state.nodes
    matrix = get_adjacency_matrix()
    n = len(nodes)
    
    start_idx = nodes.index(start_node)
    target_idx = nodes.index(target_node)
    
    distances = [float('inf')] * n
    distances[start_idx] = 0
    visited = [False] * n
    parent = [-1] * n
    
    log_proses = []
    log_proses.append(f"<b>[Inisialisasi]</b> Memulai pencarian dari <b>{start_node}</b>.")
    
    for _ in range(n):
        # Cari node dengan jarak minimum yang belum dikunjungi
        min_dist = float('inf')
        u = -1
        for i in range(n):
            if not visited[i] and distances[i] < min_dist:
                min_dist = distances[i]
                u = i
                
        if u == -1 or u == target_idx:
            break
            
        visited[u] = True
        log_proses.append(f"<br><b>[Eksplorasi]</b> Mengunjungi Node: <b>{nodes[u]}</b> (Jarak saat ini: {distances[u]} km)")
        
        # Update jarak tetangga (Relaksasi Sisi)
        for v in range(n):
            weight = matrix[u][v]
            if weight > 0 and weight != float('inf') and not visited[v]:
                new_dist = distances[u] + weight
                if new_dist < distances[v]:
                    log_proses.append(f"&nbsp;&nbsp;&nbsp;&nbsp;→ Memeriksa rute ke <i>{nodes[v]}</i>: {distances[u]} + {weight} = {new_dist} km. (Lebih cepat! Update jarak)")
                    distances[v] = new_dist
                    parent[v] = u
                else:
                    log_proses.append(f"&nbsp;&nbsp;&nbsp;&nbsp;→ Memeriksa rute ke <i>{nodes[v]}</i>: {distances[u]} + {weight} = {new_dist} km. (Lebih lambat dari {distances[v]} km, abaikan)")
                    
    # Konstruksi Jalur Akhir
    path = []
    curr = target_idx
    if distances[curr] != float('inf'):
        while curr != -1:
            path.insert(0, nodes[curr])
            curr = parent[curr]
            
    return distances[target_idx], path, log_proses

# ==========================================
# 4. STREAMLIT INTERACTIVE INTERFACE
# ==========================================
st.set_page_config(page_title="DSS Logistik Graph", layout="wide")
st.title("🚚 Decision Support System Jalur Logistik UMKM")
st.caption("Aplikasi optimasi rute pengiriman barang berbasis struktur data Graph & Algoritma Dijkstra")

# Pembagian Layout Menjadi 2 Kolom (Kiri: Manajemen Data, Kanan: Hasil DSS)
col1, col2 = st.columns([1, 1.2])

with col1:
    st.header("🛠️ Manajemen Struktur Data Graph")
    
    # --- FITUR 1: INPUT DATA NODE ---
    with st.expander("📍 Tambah Lokasi Baru (Node)", expanded=False):
        new_node = st.text_input("Nama Lokasi (Misal: Toko C, Rumah Budi):", key="input_node")
        if st.button("Tambah Lokasi"):
            if new_node and new_node not in st.session_state.nodes:
                st.session_state.nodes.append(new_node)
                st.session_state.graph_list[new_node] = []
                st.success(f"Lokasi '{new_node}' berhasil ditambahkan!")
                st.rerun()
            elif new_node in st.session_state.nodes:
                st.warning("Lokasi sudah terdaftar.")

    # --- FITUR 1: INPUT DATA EDGE ---
    with st.expander("🛣️ Tambah Rute Jalan Baru (Edge + Weight)", expanded=False):
        if len(st.session_state.nodes) >= 2:
            node_a = st.selectbox("Lokasi Asal:", st.session_state.nodes, key="edge_a")
            node_b = st.selectbox("Lokasi Tujuan:", st.session_state.nodes, key="edge_b")
            weight = st.number_input("Jarak / Bobot (Km):", min_value=1, max_value=500, value=10)
            
            if st.button("Hubungkan Rute"):
                if node_a != node_b:
                    # Input ke Adjacency List (Undirected: A ke B dan B ke A)
                    st.session_state.graph_list[node_a] = [item for item in st.session_state.graph_list[node_a] if item[0] != node_b]
                    st.session_state.graph_list[node_b] = [item for item in st.session_state.graph_list[node_b] if item[0] != node_a]
                    
                    st.session_state.graph_list[node_a].append((node_b, weight))
                    st.session_state.graph_list[node_b].append((node_a, weight))
                    st.success(f"Rute {node_a} ↔️ {node_b} ({weight} km) berhasil disimpan!")
                    st.rerun()
                else:
                    st.error("Lokasi asal dan tujuan tidak boleh sama.")
        else:
            st.info("Tambahkan minimal 2 lokasi terlebih dahulu untuk membuat rute.")

    # Tampilkan representasi data ke dosen
    st.subheader("📊 Representasi di Memori")
    display_mode = st.radio("Lihat Struktur Data:", ["Adjacency List", "Adjacency Matrix"])
    
    if display_mode == "Adjacency List":
        st.json(st.session_state.graph_list)
    else:
        matrix_data = get_adjacency_matrix()
        st.write("Matriks 2D (Nilai 'inf' berarti tidak terhubung langsung):")
        
        # PERBAIKAN: Menggunakan Pandas DataFrame agar kolom tabel sejajar sempurna dengan nama lokasi
        df_matrix = pd.DataFrame(
            matrix_data, 
            columns=st.session_state.nodes, 
            index=st.session_state.nodes
        )
        st.dataframe(df_matrix, use_container_width=True)

with col2:
    st.header("🤖 Proses Analisis & Rekomendasi Keputusan")
    
    if len(st.session_state.nodes) >= 2:
        col_start, col_target = st.columns(2)
        with col_start:
            start_point = st.selectbox("📍 Titik Awal Pengiriman (Gudang):", st.session_state.nodes, index=0)
        with col_target:
            target_point = st.selectbox("🏁 Alamat Tujuan Konsumen:", st.session_state.nodes, index=min(1, len(st.session_state.nodes)-1))
            
        # --- FITUR 3: PROSES ANALISIS KEPUTUSAN ---
        if st.button("🚀 Analisis & Hitung Rute Terbaik", type="primary", use_container_width=True):
            
            total_cost, shortest_path, logs = dijkstra_shortest_path(start_point, target_point)
            
            if total_cost == float('inf') or not shortest_path:
                st.error(f"❌ Tidak ditemukan jalur yang menghubungkan {start_point} ke {target_point}. Silakan tambahkan rute pembantu terlebih dahulu.")
            else:
                # --- FITUR 4: MENAMPILKAN HASIL REKOMENDASI ---
                st.markdown("---")
                st.subheader("💡 Rekomendasi Keputusan Akhir")
                
                rute_text = " ➡️ ".join([f"**{p}**" for p in shortest_path])
                st.success(f"**RUTE TERBAIK:** {rute_text}")
                
                # Menghitung estimasi keputusan bisnis tambahan (Optimasi)
                st.metric(label="Total Jarak Pengiriman", value=f"{total_cost} Km")
                st.info(f"ℹ️ **Saran Operasional:** Kurir direkomendasikan melewati rute di atas untuk mengoptimalkan efisiensi bahan bakar.")
                
                # --- FITUR 2: VISUALISASI GRAPH ---
                st.subheader("🖼️ Visualisasi Model Jaringan Jarak")
                
                G = nx.Graph()
                for node in st.session_state.nodes:
                    G.add_node(node)
                for u in st.session_state.graph_list:
                    for v, w in st.session_state.graph_list[u]:
                        G.add_edge(u, v, weight=w)
                        
                fig, ax = plt.subplots(figsize=(8, 5))
                pos = nx.spring_layout(G, seed=42)
                
                # Mewarnai jalur terpendek dengan warna merah tebal
                path_edges = list(zip(shortest_path, shortest_path[1:]))
                edge_colors = []
                edge_widths = []
                for u, v in G.edges():
                    if (u, v) in path_edges or (v, u) in path_edges:
                        edge_colors.append('#ff4b4b')
                        edge_widths.append(4.0)
                    else:
                        edge_colors.append('#cccccc')
                        edge_widths.append(1.5)
                
                nx.draw_networkx_nodes(G, pos, node_color='#1f77b4', node_size=800, ax=ax)
                nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths, ax=ax)
                nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold", font_family="sans-serif", ax=ax)
                
                edge_labels = nx.get_edge_attributes(G, 'weight')
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9, ax=ax)
                
                plt.axis('off')
                st.pyplot(fig)
                
                # --- FITUR 5: MENAMPILKAN PROSES PERHITUNGAN ---
                st.subheader("🕵️ Langkah & Proses Perhitungan (Log Dijkstra)")
                with st.expander("Lihat bagaimana AI/Algoritma mengambil keputusan", expanded=True):
                    for line in logs:
                        st.markdown(line, unsafe_allow_html=True)
    else:
        st.info("Aplikasi membutuhkan minimal 2 lokasi untuk mensimulasikan sistem keputusan.")