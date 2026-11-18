import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="Florería Sarai - Logística",
    page_icon="🌸",
    layout="wide"
)

# --- CARGA DE ARCHIVOS JSON ---
CONFIG_FILE = "fournisseur.json"
ORDERS_FILE = "pedidos.json"

def load_json(file_path, default_data):
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default_data
    return default_data

default_config = {
    "proveedores": {
        "Florícola Andina": {"lead_time_dias": 2, "vida_util_tienda": 3},
        "Importaciones Flora": {"lead_time_dias": 4, "vida_util_tienda": 2},
        "Cultivos del Sur": {"lead_time_dias": 1, "vida_util_tienda": 4}
    },
    "catalogo_flores": {
        "Rosas": "Florícola Andina",
        "Lirios": "Importaciones Flora",
        "Margaritas": "Cultivos del Sur",
        "Girasoles": "Florícola Andina",
        "Tulipanes": "Importaciones Flora",
        "Claveles": "Cultivos del Sur"
    },
    "bouquets": {
        "Bouquet Romántico": {"Rosas": 12, "Lirios": 4, "Margaritas": 0, "Girasoles": 0, "Tulipanes": 0, "Claveles": 0},
        "Bouquet Campestre": {"Rosas": 6, "Lirios": 0, "Margaritas": 10, "Girasoles": 4, "Tulipanes": 0, "Claveles": 0}
    }
}

config_data = load_json(CONFIG_FILE, default_config)
proveedores = config_data.get("proveedores", {})
catalogo_flores = config_data.get("catalogo_flores", {})
bouquets_memoria = config_data.get("bouquets", {})

orders_data = load_json(ORDERS_FILE, [])

# Date courante de référence (3 octobre 2026)
date_aujourdhui = datetime.now().date()

# --- HEADER PRINCIPAL ---
st.title("🌸 Florería Sarai - Sistema de Gestión Logística")
st.markdown("Planificación retroactiva, selección de bouquets predefinidos y control de aprovisionamiento.")

# --- NAVEGACIÓN / PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["📦 Registro y Pedidos", "📊 Órdenes de Compra Consolidadas", "📈 Analítica BI"])

with tab1:
    st.subheader("Registro de Nuevo Pedido de Cliente")

    col1, col2 = st.columns(2)
    with col1:
        cliente_nom = st.text_input("Nombre del Cliente", "Empresa / Cliente S.A.")
    with col2:
        fecha_entrega = st.date_input("Fecha requerida de entrega", date_aujourdhui + timedelta(days=5))

    st.markdown("---")
    st.markdown("### 💐 Carga Rápida desde Bouquet en Memoria")
    noms_bouquets = ["-- Ninguno (Personalizado) --"] + list(bouquets_memoria.keys())
    
    def on_change_bouquet():
        b_choisi = st.session_state.select_bouquet
        if b_choisi != "-- Ninguno (Personalizado) --":
            comp = bouquets_memoria.get(b_choisi, {})
            for fleur in catalogo_flores.keys():
                st.session_state[f"q_{fleur}"] = int(comp.get(fleur, 0))

    bouquet_selectionne = st.selectbox(
        "Seleccionar Bouquet Predefinido", 
        noms_bouquets, 
        key="select_bouquet", 
        on_change=on_change_bouquet
    )

    st.markdown("### 🌷 Composición del Arreglo (Ajustable)")
    fleurs_liste = list(catalogo_flores.keys())
    
    cols = st.columns(3)
    quantites_saisies = {}
    
    for idx, fleur in enumerate(fleurs_liste):
        col_target = cols[idx % 3]
        with col_target:
            if f"q_{fleur}" not in st.session_state:
                st.session_state[f"q_{fleur}"] = 0
                
            quantites_saisies[fleur] = st.number_input(
                f"{fleur}", 
                min_value=0, 
                step=1, 
                key=f"q_{fleur}"
            )

    if st.button("Registrar Pedido y Calcular Plan Logístico", type="primary"):
        details_commande = {f: q for f, q in quantites_saisies.items() if q > 0}
        
        if not details_commande:
            st.error("Por favor, selecciona al menos una flor o un bouquet con cantidad mayor a 0.")
        else:
            erreur_delai = False
            fleurs_en_retard = []
            
            for fleur, qte in details_commande.items():
                prov_nom = catalogo_flores.get(fleur, "Desconocido")
                finfo = proveedores.get(prov_nom, {"lead_time_dias": 2})
                lead_time = finfo["lead_time_dias"]
                
                fecha_compra_ideale = fecha_entrega - timedelta(days=lead_time)
                
                if fecha_compra_ideale < date_aujourdhui:
                    erreur_delai = True
                    fleurs_en_retard.append(f"• **{fleur}** (Proveedor: *{prov_nom}* requiere {lead_time} días de anticipación)")

            if erreur_delai:
                st.error("❌ **Error logístico: Fecha de entrega demasiado próxima.**\n\nNo es posible realizar el aprovisionamiento a tiempo para las siguientes variedades debido a sus plazos de entrega (*lead time*):\n" + "\n".join(fleurs_en_retard) + "\n\nPor favor, selecciona una fecha de entrega posterior.")
            else:
                nouvelle_commande = {
                    "id": len(orders_data) + 1,
                    "cliente": cliente_nom,
                    "bouquet_type": bouquet_selectionne,
                    "fecha_entrega": str(fecha_entrega),
                    "items": details_commande,
                    "fecha_registro": str(date_aujourdhui)
                }
                orders_data.append(nouvelle_commande)
                with open(ORDERS_FILE, "w", encoding="utf-8") as f:
                    json.dump(orders_data, f, indent=4, ensure_ascii=False)
                st.success(f"¡Pedido #{nouvelle_commande['id']} registrado con éxito y optimizado por el motor logístico!")

with tab2:
    st.subheader("🛒 Órdenes de Compra Optimizadas y Consolidadas por Proveedor")
    st.markdown("Agrupación inteligente de requerimientos por proveedor y fecha de compra, considerando la vida útil en tienda para evitar mermas.")
    
    if not orders_data:
        st.info("No hay pedidos registrados todavía. Añade uno en la pestaña anterior.")
    else:
        lignes_brutes = []
        for ord_item in orders_data:
            str_fecha = ord_item.get("fecha_entrega", str(date_aujourdhui))
            try:
                f_entrega = datetime.strptime(str_fecha, "%Y-%m-%d").date()
            except ValueError:
                f_entrega = date_aujourdhui + timedelta(days=3)
            
            items_commande = ord_item.get("items", {})
            for fleur, qte in items_commande.items():
                proveedor_nom = catalogo_flores.get(fleur, "Desconocido")
                finfo = proveedores.get(proveedor_nom, {"lead_time_dias": 2, "vida_util_tienda": 3})
                lead_time = finfo["lead_time_dias"]
                
                # Date d'achat idéale rétroactive
                fecha_compra_ideale = f_entrega - timedelta(days=lead_time)
                
                # Filtrer les achats dont la date est passée
                if fecha_compra_ideale >= date_aujourdhui:
                    lignes_brutes.append({
                        "Fecha Compra (Ret.)": str(fecha_compra_ideale),
                        "Proveedor": proveedor_nom,
                        "Variedad": fleur,
                        "Cantidad": qte
                    })

        if lignes_brutes:
            df_brut = pd.DataFrame(lignes_brutes)
            
            # CONSOLIDATION : Regroupement par Date d'achat, Fournisseur et Variété de fleur
            df_consolide = df_brut.groupby(["Fecha Compra (Ret.)", "Proveedor", "Variedad"])["Cantidad"].sum().reset_index()
            
            # Ajout d'indicateurs d'alerte / statut
            def get_status(row):
                delta = (datetime.strptime(row["Fecha Compra (Ret.)"], "%Y-%m-%d").date() - date_aujourdhui).days
                if delta == 0:
                    return "🟡 Atención (Comprar hoy - Lote consolidado)"
                else:
                    return "🟢 Óptimo (Próximo)"

            df_consolide["Estado Alerta"] = df_consolide.apply(get_status, axis=1)

            # TRI : Du plus proche au plus lointain
            df_consolide = df_consolide.sort_values(by="Fecha Compra (Ret.)", ascending=True).reset_index(drop=True)

            # Réorganisation des colonnes pour un affichage pro
            df_consolide = df_consolide[["Fecha Compra (Ret.)", "Proveedor", "Variedad", "Cantidad", "Estado Alerta"]]

            st.dataframe(df_consolide, use_container_width=True)
        else:
            st.info("No hay compras pendientes programadas (todas las fechas de compra anteriores a hoy han sido eliminadas).")

with tab3:
    st.subheader("📈 Análisis y Business Intelligence (BI)")
    
    if not orders_data:
        st.info("Datos insuficientes para generar gráficos.")
    else:
        all_items = []
        for ord_item in orders_data:
            items_commande = ord_item.get("items", {})
            for fleur, qte in items_commande.items():
                all_items.append({
                    "Flor": fleur,
                    "Cantidad": qte,
                    "Proveedor": catalogo_flores.get(fleur, "Desconocido")
                })
        
        if all_items:
            df_bi = pd.DataFrame(all_items)
            
            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.markdown("**Demanda total consolidada por tipo de flor**")
                df_flores = df_bi.groupby("Flor")["Cantidad"].sum().reset_index()
                st.bar_chart(df_flores.set_index("Flor"))
                
            with col_g2:
                st.markdown("**Distribución de compras por Proveedor**")
                df_prov = df_bi.groupby("Proveedor")["Cantidad"].sum().reset_index()
                st.bar_chart(df_prov.set_index("Proveedor"))
        else:
            st.info("No hay suficientes datos estructurados para generar los gráficos.")