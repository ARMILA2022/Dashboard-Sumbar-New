
import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

# =========================================================
# KONFIGURASI
# =========================================================

st.set_page_config(
    page_title="Dashboard Klasterisasi Sumatera Barat",
    page_icon="🗺️",
    layout="wide"
)

# =========================================================
# CSS / TEMA WARNA
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #F5F7FA;
}

.main-title {
    background-color: #12355B;
    padding: 25px;
    border-radius: 15px;
    color: white;
    margin-bottom: 25px;
}

.main-title h1 {
    color: white;
    margin-bottom: 5px;
}

.main-title p {
    color: #E8F1F8;
    font-size: 16px;
}

.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    border-left: 5px solid #1D4E89;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.08);
}

.section-title {
    color: #12355B;
    font-weight: 700;
    margin-top: 20px;
}

.info-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# BACA DATA
# =========================================================

df_dashboard = pd.read_excel(
    "data_dashboard.xlsx"
)

df_centroid = pd.read_excel(
    "centroid_cluster.xlsx"
)

df_model = pd.read_excel(
    "informasi_model.xlsx"
)

gdf = gpd.read_file(
    "hasil_cluster_peta.geojson"
)


# =========================================================
# INFORMASI MODEL
# =========================================================

k_optimal = int(
    df_model.loc[
        df_model["Parameter"] == "K Optimal",
        "Nilai"
    ].iloc[0]
)

dbi_final = float(
    df_model.loc[
        df_model["Parameter"] == "DBI Final",
        "Nilai"
    ].iloc[0]
)

jumlah_wilayah = int(
    df_model.loc[
        df_model["Parameter"] == "Jumlah Kabupaten/Kota",
        "Nilai"
    ].iloc[0]
)

jumlah_indikator = int(
    df_model.loc[
        df_model["Parameter"] == "Jumlah Indikator",
        "Nilai"
    ].iloc[0]
)


# =========================================================
# JUDUL
# =========================================================

st.markdown("""
<div class="main-title">

<h1>🗺️ Dashboard Klasterisasi Sosial Ekonomi</h1>

<p>
Kabupaten/Kota di Provinsi Sumatera Barat
</p>

<p>
Analisis menggunakan algoritma K-Means berdasarkan
9 indikator sosial ekonomi periode 2021–2025.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# RINGKASAN MODEL
# =========================================================

st.markdown(
    '<h2 class="section-title">📌 Ringkasan Hasil Klasterisasi</h2>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🏘️ Kabupaten/Kota",
        jumlah_wilayah
    )

with col2:
    st.metric(
        "🔵 K Optimal",
        k_optimal
    )

with col3:
    st.metric(
        "📊 DBI Final",
        f"{dbi_final:.4f}"
    )

with col4:
    st.metric(
        "📋 Indikator",
        jumlah_indikator
    )


st.info(
    f"Model K-Means menghasilkan {k_optimal} cluster "
    f"dengan nilai Davies-Bouldin Index (DBI) sebesar "
    f"{dbi_final:.4f}. "
    "Nilai DBI yang lebih rendah menunjukkan kualitas "
    "pemisahan cluster yang lebih baik."
)


st.divider()


# =========================================================
# PILIH WILAYAH
# =========================================================

st.markdown(
    '<h2 class="section-title">🔎 Eksplorasi Kabupaten/Kota</h2>',
    unsafe_allow_html=True
)

pilihan_wilayah = st.selectbox(
    "Pilih Kabupaten/Kota:",
    sorted(
        df_dashboard[
            "Kabupaten/Kota"
        ].unique()
    )
)


# Data wilayah terpilih

data_wilayah = df_dashboard[
    df_dashboard[
        "Kabupaten/Kota"
    ] == pilihan_wilayah
].iloc[0]


cluster_wilayah = int(
    data_wilayah["Cluster"]
)


# =========================================================
# PROFIL WILAYAH
# =========================================================

st.markdown(
    f'<h2 class="section-title">📍 Profil {pilihan_wilayah}</h2>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Kabupaten/Kota",
        pilihan_wilayah
    )

with col2:

    st.metric(
        "Cluster",
        f"Cluster {cluster_wilayah}"
    )


# =========================================================
# 9 INDIKATOR
# =========================================================

st.markdown(
    '<h2 class="section-title">📊 Nilai 9 Indikator Sosial Ekonomi</h2>',
    unsafe_allow_html=True
)

indikator_tampil = pd.DataFrame({

    "Indikator": [

        "Tingkat Kemiskinan (%)",

        "PDRB per Kapita (Ribu Rp)",

        "TPT (%)",

        "Gini Ratio",

        "Umur Harapan Hidup (Tahun)",

        "Harapan Lama Sekolah (Tahun)",

        "Rata-rata Lama Sekolah (Tahun)",

        "Pengeluaran Per Kapita (Ribu Rp)",

        "Laju Pertumbuhan Ekonomi (%)"

    ],

    "Nilai": [

        data_wilayah[
            "Tingkat_Kemiskinan (%)"
        ],

        data_wilayah[
            "PDRB_per_Kapita (Ribu Rp)"
        ],

        data_wilayah[
            "TPT (%)"
        ],

        data_wilayah[
            "Gini_Ratio"
        ],

        data_wilayah[
            "Umur Harapan Hidup(Tahun)"
        ],

        data_wilayah[
            "Harapan Lama Sekolah(Tahun)"
        ],

        data_wilayah[
            "Rata-rata Lama Sekolah(Tahun)"
        ],

        data_wilayah[
            "Pengeluaran Per Kapita(Ribu Rupiah/Orang/Tahun)"
        ],

        data_wilayah[
            "Laju Pertumbuhan Ekonomi"
        ]

    ]

})

indikator_tampil["Nilai"] = (
    indikator_tampil["Nilai"]
    .round(2)
)

st.dataframe(
    indikator_tampil,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# GRAFIK INDIKATOR
# =========================================================

st.markdown(
    f'<h2 class="section-title">📈 Grafik Indikator {pilihan_wilayah}</h2>',
    unsafe_allow_html=True
)

fig_indikator = px.bar(
    indikator_tampil,
    x="Nilai",
    y="Indikator",
    orientation="h",
    text="Nilai",
    title=f"Profil Indikator Sosial Ekonomi {pilihan_wilayah}"
)

fig_indikator.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig_indikator.update_layout(
    height=550
)

st.plotly_chart(
    fig_indikator,
    use_container_width=True
)


st.divider()


# =========================================================
# KARAKTERISTIK CLUSTER
# =========================================================

st.markdown(
    f'<h2 class="section-title">📌 Karakteristik Cluster {cluster_wilayah}</h2>',
    unsafe_allow_html=True
)

centroid_selected = df_centroid[
    df_centroid["Cluster"]
    == cluster_wilayah
]

if len(centroid_selected) > 0:

    centroid_data = centroid_selected.drop(
        columns=["Cluster"]
    )

    centroid_display = (
        centroid_data
        .T
        .reset_index()
    )

    centroid_display.columns = [
        "Indikator",
        "Nilai Normalisasi"
    ]

    centroid_display[
        "Nilai Normalisasi"
    ] = (
        centroid_display[
            "Nilai Normalisasi"
        ]
        .round(4)
    )

    st.dataframe(
        centroid_display,
        use_container_width=True,
        hide_index=True
    )

    # Grafik centroid

    fig_centroid = px.bar(
        centroid_display,
        x="Indikator",
        y="Nilai Normalisasi",
        title=f"Profil Centroid Cluster {cluster_wilayah}"
    )

    fig_centroid.update_layout(
        xaxis_tickangle=-45,
        height=500
    )

    st.plotly_chart(
        fig_centroid,
        use_container_width=True
    )


st.divider()


# =========================================================
# PETA
# =========================================================

st.markdown(
    '<h2 class="section-title">🗺️ Peta Klasterisasi Kabupaten/Kota</h2>',
    unsafe_allow_html=True
)

gdf["Cluster"] = (
    gdf["Cluster"]
    .astype(str)
)


warna_cluster = {

    "1": "#2E86AB",

    "2": "#F6C85F",

    "3": "#6A994E"

}


fig_map = px.choropleth_mapbox(

    gdf,

    geojson=gdf.__geo_interface__,

    locations=gdf.index,

    color="Cluster",

    hover_name="kab_kota",

    color_discrete_map=warna_cluster,

    mapbox_style="open-street-map",

    center={
        "lat": -0.95,
        "lon": 100.35
    },

    zoom=6.5,

    opacity=0.7

)


fig_map.update_layout(

    height=650,

    margin={
        "r": 0,
        "t": 0,
        "l": 0,
        "b": 0
    }

)


st.plotly_chart(
    fig_map,
    use_container_width=True
)


st.divider()


# =========================================================
# DISTRIBUSI CLUSTER
# =========================================================

st.markdown(
    '<h2 class="section-title">📊 Distribusi Kabupaten/Kota Setiap Cluster</h2>',
    unsafe_allow_html=True
)

jumlah_cluster_df = (

    df_dashboard[
        "Cluster"
    ]

    .value_counts()

    .sort_index()

    .reset_index()

)

jumlah_cluster_df.columns = [

    "Cluster",

    "Jumlah Kabupaten/Kota"

]


fig_bar = px.bar(

    jumlah_cluster_df,

    x="Cluster",

    y="Jumlah Kabupaten/Kota",

    text="Jumlah Kabupaten/Kota",

    title="Jumlah Kabupaten/Kota pada Setiap Cluster",

    color="Cluster",

    color_discrete_map={
        1: "#2E86AB",
        2: "#F6C85F",
        3: "#6A994E"
    }

)


st.plotly_chart(

    fig_bar,

    use_container_width=True

)


# =========================================================
# DAFTAR ANGGOTA CLUSTER
# =========================================================

st.markdown(
    '<h2 class="section-title">📋 Daftar Kabupaten/Kota Berdasarkan Cluster</h2>',
    unsafe_allow_html=True
)

pilihan_cluster = st.selectbox(

    "Pilih Cluster:",

    sorted(
        df_dashboard[
            "Cluster"
        ].unique()
    )

)


df_filter = df_dashboard[

    df_dashboard[
        "Cluster"
    ] == pilihan_cluster

]


st.dataframe(

    df_filter[
        [
            "Kabupaten/Kota",

            "Cluster"

        ]
    ],

    use_container_width=True,

    hide_index=True

)


# =========================================================
# DOWNLOAD
# =========================================================

st.markdown(
    '<h2 class="section-title">📥 Unduh Data Hasil Klasterisasi</h2>',
    unsafe_allow_html=True
)

csv_download = df_dashboard.to_csv(
    index=False
)


st.download_button(

    label="📥 Download Hasil Klasterisasi",

    data=csv_download,

    file_name="hasil_cluster_dashboard.csv",

    mime="text/csv"

)
