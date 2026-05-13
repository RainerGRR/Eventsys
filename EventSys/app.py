import streamlit as st
import calendar
import sqlite3
import pandas as pd
import os

st.set_page_config(page_title="EventSys", layout="wide")

# -------------------------
# SESSION STATE
# -------------------------

if "pagina" not in st.session_state:
    st.session_state.pagina = "inicio"

if "dia_seleccionado" not in st.session_state:
    st.session_state.dia_seleccionado = None


# -------------------------
# BASE DE DATOS
# -------------------------

conn = sqlite3.connect("eventsys.db", check_same_thread=False)

def cargar_productos():
    query = "SELECT id, nombre, precio, categoria, cantidad, descripcion, imagen FROM productos"
    df = pd.read_sql_query(query, conn)
    return df

def cargar_disponibilidad(mes, anio):
    query = f"SELECT fecha, estado, descripcion FROM disponibilidad WHERE fecha LIKE '{anio}-{mes:02d}-%'"
    df = pd.read_sql_query(query, conn)
    return df


# -------------------------
# ESTILOS
# -------------------------

st.markdown("""
<style>

body{
background:#111;
color:#d6cdea;
font-family:Arial, sans-serif;
}

.hero{
background:linear-gradient(135deg,#2b2b2b,#000);
padding:60px;
border-radius:20px;
text-align:center;
margin-bottom:40px;
}

h1{
color:#ffd6ff;
}

h2,h3{
color:#e7c6ff;
}

p{
color:#cdb4db;
}

.card{
background:#1e1e1e;
padding:20px;
border-radius:15px;
border:1px solid #333;
margin-bottom:20px;
}

.card h3{
color:#ffc8dd;
}

.card p{
color:#b8c0ff;
}

.feature{
padding:25px;
border-radius:15px;
border:1px solid #ffb3ba;
text-align:center;
}

.feature h3{
color:#333;
}

.feature p{
color:#555;
}

.stButton button {
background: linear-gradient(135deg,#bde0fe,#a2d2ff);
color: #000;
border: none;
border-radius: 10px;
padding: 12px 24px;
font-weight: bold;
font-size: 16px;
margin: 5px;
transition: all 0.3s ease;
}

.stButton button:hover {
background: linear-gradient(135deg,#a2d2ff,#8bb3ff);
transform: scale(1.05);
}

.service{
height:150px;
border-radius:15px;
display:flex;
align-items:flex-end;
padding:20px;
font-weight:bold;
}

.g1{
background:linear-gradient(135deg,#ffc8dd,#ffafcc);
}

.g2{
background:linear-gradient(135deg,#cdb4db,#bde0fe);
}

.g3{
background:linear-gradient(135deg,#b8c0ff,#a2d2ff);
}

</style>
""", unsafe_allow_html=True)


# -------------------------
# NAVEGACIÓN
# -------------------------

n1,n2,n3,n4 = st.columns(4)

with n1:
    if st.button("Inicio"):
        st.session_state.pagina="inicio"
        st.rerun()

with n2:
    if st.button("Inventario"):
        st.session_state.pagina="inventario"
        st.rerun()

with n3:
    if st.button("Calendario"):
        st.session_state.pagina="calendario"
        st.rerun()

with n4:
    if st.button("Ayuda"):
        st.session_state.pagina="ayuda"
        st.rerun()

pagina = st.session_state.pagina


# ======================================================
# INICIO
# ======================================================

if pagina == "inicio":

    st.markdown("""
    <div class="hero">
    <h1>🎉 EventSys</h1>
    <p>Mobiliario premium para tus eventos</p>
    </div>
    """, unsafe_allow_html=True)

    f1,f2,f3 = st.columns(3)

    with f1:
        st.markdown("""
        <div class="feature g1">
        <h3>📦 Amplio Inventario</h3>
        <p>Sillas, mesas, carpas y decoración</p>
        </div>
        """, unsafe_allow_html=True)

    with f2:
        st.markdown("""
        <div class="feature g2">
        <h3>📅 Reservación Fácil</h3>
        <p>Consulta disponibilidad rápidamente</p>
        </div>
        """, unsafe_allow_html=True)

    with f3:
        st.markdown("""
        <div class="feature g3">
        <h3>✨ Calidad Premium</h3>
        <p>Mobiliario limpio y en excelente estado</p>
        </div>
        """, unsafe_allow_html=True)

    st.subheader("Servicios")

    s1,s2,s3 = st.columns(3)

    with s1:
        st.markdown('<div class="service g1">Sillas y Mesas</div>',unsafe_allow_html=True)
        if st.button("Explorar", key="sillas_mesas"):
            st.session_state.pagina = "sillas_mesas"
            st.rerun()

    with s2:
        st.markdown('<div class="service g2">Decoración</div>',unsafe_allow_html=True)
        if st.button("Explorar", key="decoracion"):
            st.session_state.pagina = "decoracion"
            st.rerun()

    with s3:
        st.markdown('<div class="service g3">Carpas</div>',unsafe_allow_html=True)
        if st.button("Explorar", key="carpitas"):
            st.session_state.pagina = "carpitas"
            st.rerun()


# ======================================================
# SILLAS Y MESAS
# ======================================================

elif pagina == "sillas_mesas":

    st.title("Sillas y Mesas")

    if st.button("Volver al inicio"):
        st.session_state.pagina = "inicio"
        st.rerun()

    products_df = cargar_productos()
    filtered = products_df[products_df["categoria"].isin(["Mesas", "Sillas"])]

    cols = st.columns(3)
    i = 0

    for _,p in filtered.iterrows():

        with cols[i % 3]:

            imagen_producto = p["imagen"] if "imagen" in p and pd.notna(p["imagen"]) else ""
            if imagen_producto and os.path.exists(imagen_producto):
                src = imagen_producto
            elif imagen_producto and imagen_producto.startswith('http'):
                src = imagen_producto
            else:
                src = None
            descripcion_producto = p["descripcion"] if "descripcion" in p else ""
            st.markdown(f"<div style='height:240px; overflow:hidden; border-radius:8px; margin-bottom:12px;'>", unsafe_allow_html=True)
            if src:
                st.image(src, width=320)
            else:
                st.image("https://via.placeholder.com/320x240?text=Sin+Imagen", width=320)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
              <span style='font-weight:bold; font-size:16px; color:#ffd6ff;'>#{p["id"]} {p["nombre"]}</span>
              <span style='font-size:13px; color:#d6cdea; background:#2b2b2b; border:1px solid #444; padding:3px 8px; border-radius:8px;'>{p["categoria"]}</span>
            </div>
            <p style='color:#cdb4db;'><strong>Precio:</strong> ${p["precio"]}</p>
            <p style='color:#cdb4db;'><strong>Disponibles:</strong> {p["cantidad"]}</p>
            <p style='color:#999;'>{descripcion_producto}</p>
            """, unsafe_allow_html=True)

            producto_dict = {
                "nombre": p["nombre"],
                "precio": p["precio"],
                "disp": p["cantidad"],
                "imagen": imagen_producto
            }

            if st.button("Cotizar", key=f"cotizar_sm_{p['id']}"):
                st.session_state.producto_cotizar = producto_dict
                st.session_state.pagina = "cotizacion"
                st.rerun()

        i += 1


# ======================================================
# DECORACIÓN
# ======================================================

elif pagina == "decoracion":

    st.title("Decoración")

    if st.button("Volver al inicio"):
        st.session_state.pagina = "inicio"
        st.rerun()

    productos_df = cargar_productos()
    filtered = productos_df[productos_df["categoria"] == "Decoración"]

    cols = st.columns(3)
    i = 0

    for _,p in filtered.iterrows():

        with cols[i % 3]:

            imagen_producto = p["imagen"] if "imagen" in p and pd.notna(p["imagen"]) else ""
            if imagen_producto and os.path.exists(imagen_producto):
                src = imagen_producto
            elif imagen_producto and imagen_producto.startswith('http'):
                src = imagen_producto
            else:
                src = None
            descripcion_producto = p["descripcion"] if "descripcion" in p else ""
            st.markdown(f"<div style='height:240px; overflow:hidden; border-radius:8px; margin-bottom:12px;'>", unsafe_allow_html=True)
            if src:
                st.image(src, width=320)
            else:
                st.image("https://via.placeholder.com/320x240?text=Sin+Imagen", width=320)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
              <span style='font-weight:bold; font-size:16px; color:#ffd6ff;'>#{p["id"]} {p["nombre"]}</span>
              <span style='font-size:13px; color:#d6cdea; background:#2b2b2b; border:1px solid #444; padding:3px 8px; border-radius:8px;'>{p["categoria"]}</span>
            </div>
            <p style='color:#cdb4db;'><strong>Precio:</strong> ${p["precio"]}</p>
            <p style='color:#cdb4db;'><strong>Disponibles:</strong> {p["cantidad"]}</p>
            <p style='color:#999;'>{descripcion_producto}</p>
            """, unsafe_allow_html=True)

            producto_dict = {
                "nombre": p["nombre"],
                "precio": p["precio"],
                "disp": p["cantidad"],
                "imagen": imagen_producto
            }

            if st.button("Cotizar", key=f"cotizar_dec_{p['id']}"):
                st.session_state.producto_cotizar = producto_dict
                st.session_state.pagina = "cotizacion"
                st.rerun()

        i += 1


# ======================================================
# CARPAS
# ======================================================

elif pagina == "carpitas":

    st.title("Carpas")

    if st.button("Volver al inicio"):
        st.session_state.pagina = "inicio"
        st.rerun()

    productos_df = cargar_productos()
    filtered = productos_df[productos_df["categoria"] == "Carpas"]

    cols = st.columns(3)
    i = 0

    for _,p in filtered.iterrows():

        with cols[i % 3]:

            imagen_producto = p["imagen"] if "imagen" in p and pd.notna(p["imagen"]) else ""
            if imagen_producto and os.path.exists(imagen_producto):
                src = imagen_producto
            elif imagen_producto and imagen_producto.startswith('http'):
                src = imagen_producto
            else:
                src = None
            descripcion_producto = p["descripcion"] if "descripcion" in p else ""
            st.markdown(f"<div style='height:240px; overflow:hidden; border-radius:8px; margin-bottom:12px;'>", unsafe_allow_html=True)
            if src:
                st.image(src, width=320)
            else:
                st.image("https://via.placeholder.com/320x240?text=Sin+Imagen", width=320)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
              <span style='font-weight:bold; font-size:16px; color:#ffd6ff;'>#{p["id"]} {p["nombre"]}</span>
              <span style='font-size:13px; color:#d6cdea; background:#2b2b2b; border:1px solid #444; padding:3px 8px; border-radius:8px;'>{p["categoria"]}</span>
            </div>
            <p style='color:#cdb4db;'><strong>Precio:</strong> ${p["precio"]}</p>
            <p style='color:#cdb4db;'><strong>Disponibles:</strong> {p["cantidad"]}</p>
            <p style='color:#999;'>{descripcion_producto}</p>
            """, unsafe_allow_html=True)

            producto_dict = {
                "nombre": p["nombre"],
                "precio": p["precio"],
                "disp": p["cantidad"],
                "imagen": imagen_producto
            }

            if st.button("Cotizar", key=f"cotizar_car_{p['id']}"):
                st.session_state.producto_cotizar = producto_dict
                st.session_state.pagina = "cotizacion"
                st.rerun()

        i += 1


# ======================================================
# INVENTARIO
# ======================================================

elif pagina == "inventario":

    st.title("Inventario Disponible")

    productos_df = cargar_productos()

    col1,col2 = st.columns([3,1])

    with col1:
        busqueda = st.text_input("Buscar producto")

    with col2:
        categorias = ["Todas"] + sorted(productos_df["categoria"].unique())
        categoria = st.selectbox("Categoría", categorias)

    cols = st.columns(3)
    i = 0

    for _,p in productos_df.iterrows():

        if categoria != "Todas" and p["categoria"] != categoria:
            continue

        if busqueda and busqueda.lower() not in p["nombre"].lower():
            continue

        with cols[i % 3]:

            imagen_producto = p["imagen"] if "imagen" in p and pd.notna(p["imagen"]) else ""
            if imagen_producto and os.path.exists(imagen_producto):
                src = imagen_producto
            elif imagen_producto and imagen_producto.startswith('http'):
                src = imagen_producto
            else:
                src = None
            descripcion_producto = p["descripcion"] if "descripcion" in p else ""
            st.markdown(f"<div style='height:240px; overflow:hidden; border-radius:8px; margin-bottom:12px;'>", unsafe_allow_html=True)
            if src:
                st.image(src, width=320)
            else:
                st.image("https://via.placeholder.com/320x240?text=Sin+Imagen", width=320)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
              <span style='font-weight:bold; font-size:16px; color:#ffd6ff;'>#{p["id"]} {p["nombre"]}</span>
              <span style='font-size:13px; color:#d6cdea; background:#2b2b2b; border:1px solid #444; padding:3px 8px; border-radius:8px;'>{p["categoria"]}</span>
            </div>
            <p style='color:#cdb4db;'><strong>Precio:</strong> ${p["precio"]}</p>
            <p style='color:#cdb4db;'><strong>Disponibles:</strong> {p["cantidad"]}</p>
            <p style='color:#999;'>{descripcion_producto}</p>
            """, unsafe_allow_html=True)

            producto_dict = {
                "nombre": p["nombre"],
                "precio": p["precio"],
                "disp": p["cantidad"],
                "imagen": imagen_producto
            }

            if st.button("Cotizar", key=f"cotizar_{p['nombre']}"):
                st.session_state.producto_cotizar = producto_dict
                st.session_state.pagina = "cotizacion"
                st.rerun()

        i += 1


# ======================================================
# COTIZACIÓN
# ======================================================

elif pagina == "cotizacion":

    producto = st.session_state.producto_cotizar

    if producto is None:
        st.warning("No hay producto seleccionado")

        if st.button("Volver al inventario"):
            st.session_state.pagina="inventario"
            st.rerun()

    else:

        st.title("Cotización de Producto")

        st.subheader(producto["nombre"])

        st.write("Precio por unidad:", "$", producto["precio"])

        cantidad = st.number_input(
            "Cantidad",
            min_value=1,
            max_value=producto["disp"],
            value=1
        )

        total = cantidad * producto["precio"]

        st.write("### Precio Total")
        st.success(f"${total}")

        descripcion = st.text_area("Descripción del pedido")

        correo = st.text_input("Correo electrónico")

        telefono = st.text_input("Número telefónico")

        metodo_pago = st.selectbox(
            "Método de pago",
            ["Transferencia","Tarjeta","Efectivo"]
        )

        c1,c2 = st.columns(2)

        with c1:
            if st.button("Confirmar pedido"):

                st.success("Pedido enviado correctamente")

                st.write("Producto:", producto["nombre"])
                st.write("Cantidad:", cantidad)
                st.write("Total:", total)
                st.write("Correo:", correo)
                st.write("Teléfono:", telefono)
                st.write("Pago:", metodo_pago)

        with c2:
            if st.button("Volver"):
                st.session_state.pagina="inventario"
                st.rerun()


# ======================================================
# CALENDARIO
# ======================================================

elif pagina == "calendario":

    st.title("Calendario de Disponibilidad")

    st.markdown("""
    **Leyenda:**  
    🟢 Disponible  
    🟡 Disponibilidad limitada  
    🔴 Reservado
    """)

    year = 2026
    month = 3

    cal = calendar.monthcalendar(year, month)

    df_disp = cargar_disponibilidad(month, year)
    disp_dict = {row['fecha']: (row['estado'], row['descripcion']) for _, row in df_disp.iterrows()}

    dias = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"]

    header = st.columns(7)

    for i, d in enumerate(dias):
        header[i].markdown(f"**{d}**")

    for semana in cal:

        cols = st.columns(7)

        for i, dia in enumerate(semana):

            if dia == 0:
                cols[i].write("")
            else:
                fecha = f"{year}-{month:02d}-{dia:02d}"
                estado, desc = disp_dict.get(fecha, ("disponible", "Disponible"))

                if estado == "disponible":
                    emoji = "🟢"
                elif estado == "reservado":
                    emoji = "🔴"
                else:  # parcial
                    emoji = "🟡"

                if cols[i].button(
                    f"{emoji} {dia}",
                    key=f"dia_cal_{dia}"
                ):
                    st.session_state.dia_seleccionado = dia
                    st.rerun()

    if st.session_state.dia_seleccionado:
        dia = st.session_state.dia_seleccionado
        fecha = f"{year}-{month:02d}-{dia:02d}"
        estado, desc = disp_dict.get(fecha, ("disponible", "Disponible"))
        st.subheader(f"Detalles de la fecha seleccionada: {dia}/03/2026")
        st.write(f"**Estado:** {estado.capitalize()}")
        st.write(f"**Descripción:** {desc}")
        if estado == "disponible":
            st.success("¡Esta fecha está disponible para reservación!")
        elif estado == "parcial":
            st.warning("Disponibilidad limitada en esta fecha.")
        else:
            st.error("Esta fecha ya está reservada.")


# ======================================================
# AYUDA
# ======================================================

elif pagina == "ayuda":

    st.title("Centro de Ayuda")

    st.write("""
1. Ve a **Inventario**
2. Busca los productos
3. Consulta disponibilidad en **Calendario**
4. Presiona **Cotizar**
""")

    st.info("Contacto: soporte@eventsys.com")

    st.subheader("Contacto")

    st.write("Teléfono: +52 55 1234 5678")
    st.write("Email: info@eventsys.com")

    st.subheader("Horario")

    st.write("Lunes a viernes: 9:00 - 19:00")
    st.write("Sábado: 10:00 - 17:00")
    st.write("Domingo: Cerrado")