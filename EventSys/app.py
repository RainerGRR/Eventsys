import base64
import os

import calendar
import pandas as pd
import sqlite3
import streamlit as st

st.set_page_config(page_title="EventSys", layout="wide")

conn = sqlite3.connect("eventsys.db", check_same_thread=False)


def init_session_state():
    if "pagina" not in st.session_state:
        st.session_state.pagina = "inicio"

    if "dia_seleccionado" not in st.session_state:
        st.session_state.dia_seleccionado = None

    if "producto_cotizar" not in st.session_state:
        st.session_state.producto_cotizar = None

    if "carrito" not in st.session_state:
        st.session_state.carrito = []


def cargar_productos():
    query = "SELECT id, nombre, precio, categoria, cantidad, descripcion, imagen FROM productos"
    return pd.read_sql_query(query, conn)


def cargar_disponibilidad(mes, anio):
    query = f"SELECT fecha, estado, descripcion FROM disponibilidad WHERE fecha LIKE '{anio}-{mes:02d}-%'"
    return pd.read_sql_query(query, conn)


def get_image_src(imagen_producto):
    if imagen_producto and os.path.exists(imagen_producto):
        return imagen_producto
    if imagen_producto and imagen_producto.startswith("http"):
        return imagen_producto
    return None


def render_styles():
    st.markdown(
        """
        <style>
        body{
        background:#111;
        color:#d6cdea;
        font-family:Arial, sans-serif;
        }

        .hero{
        background:transparent;
        padding:20px 0 10px;
        border-radius:0;
        text-align:center;
        margin-bottom:30px;
        }

        .hero-logo{
        display:block;
        margin:0 auto 20px;
        width:320px;
        max-width:90%;
        height:auto;
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
        """,
        unsafe_allow_html=True,
    )


def calcular_total_carrito():
    return sum(item.get("subtotal", 0) for item in st.session_state.carrito)


def render_carrito():
    st.title("Carrito de Compras")

    if not st.session_state.carrito:
        st.info("El carrito está vacío. Agrega productos desde el inventario.")
    else:
        for index, item in enumerate(st.session_state.carrito):
            cols = st.columns([1, 2, 1])
            with cols[0]:
                if item.get("imagen"):
                    src = get_image_src(item["imagen"])
                    if src:
                        st.image(src, width=160)
                    else:
                        st.image("https://via.placeholder.com/160x120?text=Sin+Imagen", width=160)
                else:
                    st.image("https://via.placeholder.com/160x120?text=Sin+Imagen", width=160)

            with cols[1]:
                st.markdown(f"#### {item['nombre']}")
                if item.get("categoria"):
                    st.write(f"Categoría: {item['categoria']}")
                cantidad_cantidad = st.number_input(
                    "Cantidad",
                    min_value=1,
                    max_value=item.get("max_cantidad", max(1, item.get("cantidad", 1))),
                    value=item["cantidad"],
                    key=f"cantidad_{index}",
                )
                if cantidad_cantidad != item["cantidad"]:
                    item["cantidad"] = cantidad_cantidad
                    item["subtotal"] = item["precio"] * cantidad_cantidad
                st.write(f"Precio unitario: ${item['precio']:.2f}")
                if item.get("descripcion"):
                    st.write(item["descripcion"])

            with cols[2]:
                st.write(f"**Subtotal:** ${item['subtotal']:.2f}")
                if st.button("Eliminar", key=f"eliminar_{index}"):
                    st.session_state.carrito.pop(index)
                    st.rerun()

            st.markdown("---")

        total = calcular_total_carrito()
        st.markdown(f"### Total del carrito: ${total:.2f}")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Seguir comprando"):
                st.session_state.pagina = "inventario"
                st.rerun()
        with c2:
            if st.button("Vaciar carrito"):
                st.session_state.carrito = []
                st.rerun()


def render_navigation():
    n1, n2, n3, n4, n5 = st.columns([1, 1, 1, 1, 1])

    with n1:
        if st.button("Inicio"):
            st.session_state.pagina = "inicio"
            st.rerun()

    with n2:
        if st.button("Inventario"):
            st.session_state.pagina = "inventario"
            st.rerun()

    with n3:
        if st.button("Calendario"):
            st.session_state.pagina = "calendario"
            st.rerun()

    with n4:
        if st.button("Ayuda"):
            st.session_state.pagina = "ayuda"
            st.rerun()

    with n5:
        count = len(st.session_state.carrito)
        total = calcular_total_carrito()
        label = f"🛒 Carrito ({count})" if count else "🛒 Carrito"
        if st.button(label, key="boton_carrito"):
            st.session_state.pagina = "carrito"
            st.rerun()
        if count:
            st.markdown(
                f"<div style='text-align:right; font-size:12px; color:#cdb4db;'>Total: ${total:.2f}</div>",
                unsafe_allow_html=True,
            )


def render_hero():
    # Aquí está el bloque principal del encabezado de la página.
    # Si colocas tu logo como logo.png, logo.jpg o logo.jpeg dentro de la carpeta del proyecto,
    # se mostrará centrado en la parte superior.
    logo_candidates = ["logo.png", "logo.jpg", "logo.jpeg"]
    logo_path = next((path for path in logo_candidates if os.path.exists(path)), None)

    if logo_path:
        ext = os.path.splitext(logo_path)[1].lower().replace(".", "")
        with open(logo_path, "rb") as f:
            encoded_logo = base64.b64encode(f.read()).decode()
        logo_src = f"data:image/{ext};base64,{encoded_logo}"
        st.markdown(
            f"""
            <div class="hero">
            <img src="{logo_src}" class="hero-logo" />
            <p>Mobiliario premium para tus eventos</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="hero">
            <h1>🎉 EventSys</h1>
            <p>Mobiliario premium para tus eventos</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_feature_cards():
    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown(
            """
            <div class="feature g1">
            <h3>📦 Amplio Inventario</h3>
            <p>Sillas, mesas, carpas y decoración</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with f2:
        st.markdown(
            """
            <div class="feature g2">
            <h3>📅 Reservación Fácil</h3>
            <p>Consulta disponibilidad rápidamente</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with f3:
        st.markdown(
            """
            <div class="feature g3">
            <h3>✨ Calidad Premium</h3>
            <p>Mobiliario limpio y en excelente estado</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_service_links():
    s1, s2, s3 = st.columns(3)

    with s1:
        st.markdown('<div class="service g1">Sillas y Mesas</div>', unsafe_allow_html=True)
        if st.button("Explorar", key="sillas_mesas"):
            st.session_state.pagina = "sillas_mesas"
            st.rerun()

    with s2:
        st.markdown('<div class="service g2">Decoración</div>', unsafe_allow_html=True)
        if st.button("Explorar", key="decoracion"):
            st.session_state.pagina = "decoracion"
            st.rerun()

    with s3:
        st.markdown('<div class="service g3">Carpas</div>', unsafe_allow_html=True)
        if st.button("Explorar", key="carpitas"):
            st.session_state.pagina = "carpitas"
            st.rerun()


def render_home():
    render_hero()
    render_feature_cards()
    st.subheader("Servicios")
    render_service_links()


def render_product_card(product, key_prefix):
    imagen_producto = product["imagen"] if "imagen" in product and pd.notna(product["imagen"]) else ""
    src = get_image_src(imagen_producto)
    descripcion_producto = product.get("descripcion", "")

    st.markdown(
        "<div style='height:240px; overflow:hidden; border-radius:8px; margin-bottom:12px;'>",
        unsafe_allow_html=True,
    )
    if src:
        st.image(src, width=320)
    else:
        st.image("https://via.placeholder.com/320x240?text=Sin+Imagen", width=320)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;'>
          <span style='font-weight:bold; font-size:16px; color:#ffd6ff;'>#{product['id']} {product['nombre']}</span>
          <span style='font-size:13px; color:#d6cdea; background:#2b2b2b; border:1px solid #444; padding:3px 8px; border-radius:8px;'>{product['categoria']}</span>
        </div>
        <p style='color:#cdb4db;'><strong>Precio:</strong> ${product['precio']}</p>
        <p style='color:#cdb4db;'><strong>Disponibles:</strong> {product['cantidad']}</p>
        <p style='color:#999;'>{descripcion_producto}</p>
        """,
        unsafe_allow_html=True,
    )

    producto_dict = {
        "id": product["id"],
        "nombre": product["nombre"],
        "precio": product["precio"],
        "disp": product["cantidad"],
        "imagen": imagen_producto,
        "categoria": product["categoria"],
        "descripcion": descripcion_producto,
    }

    if st.button("Cotizar", key=f"{key_prefix}_{product['id']}"):
        st.session_state.producto_cotizar = producto_dict
        st.session_state.pagina = "cotizacion"
        st.rerun()


def render_category_page(title, categories, key_prefix):
    st.title(title)

    if st.button("Volver al inicio"):
        st.session_state.pagina = "inicio"
        st.rerun()

    productos_df = cargar_productos()
    filtered = (
        productos_df[productos_df["categoria"].isin(categories)]
        if isinstance(categories, list)
        else productos_df[productos_df["categoria"] == categories]
    )

    cols = st.columns(3)
    for index, (_, product) in enumerate(filtered.iterrows()):
        with cols[index % 3]:
            render_product_card(product, f"cotizar_{key_prefix}")


def render_inventory():
    st.title("Inventario Disponible")

    productos_df = cargar_productos()

    col1, col2 = st.columns([3, 1])
    with col1:
        busqueda = st.text_input("Buscar producto")
    with col2:
        categorias = ["Todas"] + sorted(productos_df["categoria"].unique())
        categoria = st.selectbox("Categoría", categorias)

    cols = st.columns(3)
    for index, (_, product) in enumerate(productos_df.iterrows()):
        if categoria != "Todas" and product["categoria"] != categoria:
            continue
        if busqueda and busqueda.lower() not in product["nombre"].lower():
            continue

        with cols[index % 3]:
            render_product_card(product, f"cotizar_{product['nombre']}")


def render_cotizacion():
    producto = st.session_state.producto_cotizar
    if producto is None:
        st.warning("No hay producto seleccionado")
        if st.button("Volver al inventario"):
            st.session_state.pagina = "inventario"
            st.rerun()

        return

    st.title("Cotización de Producto")
    st.subheader(producto["nombre"])
    st.write("Precio por unidad:", "$", producto["precio"])

    cantidad = st.number_input(
        "Cantidad",
        min_value=1,
        max_value=producto["disp"],
        value=1,
    )

    total = cantidad * producto["precio"]
    st.write("### Precio Total")
    st.success(f"${total}")

    st.text_area("Descripción del pedido")
    correo = st.text_input("Correo electrónico")
    telefono = st.text_input("Número telefónico")
    metodo_pago = st.selectbox("Método de pago", ["Transferencia", "Tarjeta", "Efectivo"])

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Confirmar pedido"):
            item = {
                "id": producto.get("id"),
                "nombre": producto["nombre"],
                "categoria": producto.get("categoria", ""),
                "descripcion": producto.get("descripcion", ""),
                "precio": float(producto["precio"]),
                "cantidad": cantidad,
                "subtotal": total,
                "imagen": producto.get("imagen", ""),
                "max_cantidad": producto.get("disp", cantidad),
            }
            st.session_state.carrito.append(item)
            st.success("Producto agregado al carrito correctamente")
            st.session_state.pagina = "carrito"
            st.rerun()

    with c2:
        if st.button("Volver"):
            st.session_state.pagina = "inventario"
            st.rerun()


def render_calendar():
    st.title("Calendario de Disponibilidad")
    st.markdown(
        """
        **Leyenda:**  
        🟢 Disponible  
        🟡 Disponibilidad limitada  
        🔴 Reservado
        """
    )

    year = 2026
    month = 3
    cal = calendar.monthcalendar(year, month)
    df_disp = cargar_disponibilidad(month, year)
    disp_dict = {row["fecha"]: (row["estado"], row["descripcion"]) for _, row in df_disp.iterrows()}
    dias = ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"]

    header = st.columns(7)
    for index, dia in enumerate(dias):
        header[index].markdown(f"**{dia}**")

    for semana in cal:
        cols = st.columns(7)
        for index, dia in enumerate(semana):
            if dia == 0:
                cols[index].write("")
                continue

            fecha = f"{year}-{month:02d}-{dia:02d}"
            estado, desc = disp_dict.get(fecha, ("disponible", "Disponible"))
            emoji = "🟢" if estado == "disponible" else "🔴" if estado == "reservado" else "🟡"

            if cols[index].button(f"{emoji} {dia}", key=f"dia_cal_{dia}"):
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


def render_help():
    st.title("Centro de Ayuda")
    st.write(
        """
    1. Ve a **Inventario**
    2. Busca los productos
    3. Consulta disponibilidad en **Calendario**
    4. Presiona **Cotizar**
    """
    )
    st.info("Contacto: soporte@eventsys.com")
    st.subheader("Contacto")
    st.write("Teléfono: +52 55 1234 5678")
    st.write("Email: info@eventsys.com")
    st.subheader("Horario")
    st.write("Lunes a viernes: 9:00 - 19:00")
    st.write("Sábado: 10:00 - 17:00")
    st.write("Domingo: Cerrado")


def main():
    init_session_state()
    render_styles()
    render_navigation()

    pagina = st.session_state.pagina

    if pagina == "inicio":
        render_home()
    elif pagina == "sillas_mesas":
        render_category_page("Sillas y Mesas", ["Mesas", "Sillas"], "sm")
    elif pagina == "decoracion":
        render_category_page("Decoración", "Decoración", "dec")
    elif pagina == "carpitas":
        render_category_page("Carpas", "Carpas", "car")
    elif pagina == "inventario":
        render_inventory()
    elif pagina == "cotizacion":
        render_cotizacion()
    elif pagina == "carrito":
        render_carrito()
    elif pagina == "calendario":
        render_calendar()
    elif pagina == "ayuda":
        render_help()


if __name__ == "__main__":
    main()
