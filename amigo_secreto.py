import csv
from pathlib import Path

import pandas as pd
import streamlit as st

# ---------- CONFIGURACIÓN ----------
ARCHIVO_APORTES = Path("aportes.csv")

# Imagen de portada (debe estar en el mismo repo)
IMAGEN_PORTADA = "portada_posada.jpeg"  # cambia el nombre si quieres

# Opciones y cupos máximos
OPCIONES = {
    1: {"nombre": "Alfajores",                 "max": 2},
    2: {"nombre": "Petipanes para todos",      "max": 1},
    3: {"nombre": "Empanaditas surtidas",      "max": 2},
    4: {"nombre": "Wafers o dulces",           "max": 2},
    5: {"nombre": "Chips / chifles / papitas", "max": 3},
    6: {"nombre": "Gaseosa grande",            "max": 3},
    7: {"nombre": "Bebida no alcohólica",      "max": 3},
    8: {"nombre": "Bebida alcohólica",         "max": 3},
    9: {"nombre": "Otro (especificar)",        "max": 2},
}

# Lista fija de participantes (menú desplegable)
PARTICIPANTES = [
    "Katherine Silvestre",
    "Marden Ferruzo",
    "Rocio Dominguez",
    "George Aliaga",
    "Janet Rivera",
    "Ana Raez",
    "Israel Juarez",
    "Luis Moreano",
    "Yessevel Calvo",
    "Yelitza Arias",
    "Eduardo Pinto",
    "Millary Antunez",
    "Manuel Reyes",
    "Vladimir Tucto",
    "Rocio Arango",
    "Axel Fuentes",
    "Camila Alva",
    "Ricardo Céspedes",
]

# ---------- FUNCIONES AUXILIARES ----------

def cargar_aportes():
    """Lee el archivo de aportes (si existe) y retorna un DataFrame."""
    if ARCHIVO_APORTES.exists():
        return pd.read_csv(ARCHIVO_APORTES, dtype=str)
    else:
        return pd.DataFrame(columns=["nombre", "opcion", "detalle"])


def guardar_aportes(df_aportes: pd.DataFrame):
    """Guarda los aportes en CSV."""
    df_aportes.to_csv(ARCHIVO_APORTES, index=False, encoding="utf-8")


def contar_cupos_usados(df_aportes: pd.DataFrame):
    """Cuenta cuántas veces se ha elegido cada opción."""
    usados = {num: 0 for num in OPCIONES.keys()}
    if not df_aportes.empty:
        for _, fila in df_aportes.iterrows():
            try:
                num = int(fila["opcion"])
                if num in usados:
                    usados[num] += 1
            except (ValueError, TypeError):
                continue
    return usados


# ---------- APP STREAMLIT ----------

def main():
    st.set_page_config(
        page_title="Aportes Posada Territorial 2025",
        page_icon="🎄",
        layout="centered",
    )

    # ---- Estilos personalizados (colores, tipografía, etc.) ----
    st.markdown(
        """
        <style>
        /* Fondo suave */
        .stApp {
            background: linear-gradient(180deg, #fff7f0 0%, #ffffff 40%);
        }

        /* Títulos */
        .titulo-principal {
            font-size: 2.1rem;
            font-weight: 700;
            text-align: center;
            color: #234;
            margin-bottom: 0.2rem;
        }
        .subtitulo {
            text-align: center;
            color: #555;
            font-size: 0.95rem;
            margin-bottom: 1.2rem;
        }

        /* Cuadros tipo tarjeta */
        .card {
            background-color: #ffffff;
            padding: 1.2rem 1rem;
            border-radius: 0.8rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border: 1px solid #f0e0d2;
        }

        /* Tabla compacta */
        .small-table td, .small-table th {
            font-size: 0.85rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---- Portada ----
    if Path(IMAGEN_PORTADA).exists():
        st.image(IMAGEN_PORTADA, use_column_width=True)
    st.markdown('<div class="titulo-principal">🎄 Aportes Posada Territorial 2025 🎁</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitulo">Elige qué vas a llevar para que la mesa quede súper variada y rica ✨</div>',
        unsafe_allow_html=True,
    )

    # Cargamos aportes actuales
    df_aportes = cargar_aportes()
    cupos_usados = contar_cupos_usados(df_aportes)

    # ---- Layout en columnas: izquierda formulario, derecha resumen ----
    col_izq, col_der = st.columns([1.1, 0.9])

    # ----- Columna derecha: opciones y cupos -----
    with col_der:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("🍽️ Opciones y cupos")

        tabla_opciones = []
        for num, info in OPCIONES.items():
            usados = cupos_usados[num]
            maximo = info["max"]
            lleno = usados >= maximo
            estado = "✅ Disponible" if not lleno else "🚫 LLENO"
            tabla_opciones.append(
                {
                    "N.º": num,
                    "Opción": info["nombre"],
                    "Usados": f"{usados}/{maximo}",
                    "Estado": estado,
                }
            )

        df_tabla = pd.DataFrame(tabla_opciones)
        st.table(df_tabla)
        st.markdown('</div>', unsafe_allow_html=True)

    # Verificar si todo está lleno
    if all(cupos_usados[n] >= OPCIONES[n]["max"] for n in OPCIONES):
        st.warning("⚠️ Todas las opciones están llenas. ¡Ya no hay cupos disponibles!")
        if not df_aportes.empty:
            st.subheader("Aportes registrados")
            st.dataframe(df_aportes, use_container_width=True)
        return

    # ----- Columna izquierda: formulario -----
    with col_izq:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("📝 Registrar tu aporte")

        with st.form("form_aporte"):
            nombre = st.selectbox(
                "Selecciona tu nombre:",
                PARTICIPANTES,
            )

            # Selectbox con todas las opciones, indicando cupos
            def etiqueta_opcion(num):
                info = OPCIONES[num]
                usados = cupos_usados[num]
                maximo = info["max"]
                lleno = " – 🚫 LLENO" if usados >= maximo else ""
                return f"{num}. {info['nombre']} ({usados}/{maximo}){lleno}"

            opcion_seleccionada = st.selectbox(
                "Elige la opción que vas a llevar:",
                options=list(OPCIONES.keys()),
                format_func=etiqueta_opcion,
            )

            detalle = ""
            if opcion_seleccionada == 9:
                detalle = st.text_input("Describe brevemente qué vas a llevar (Otro):")

            enviado = st.form_submit_button("✅ Registrar aporte")

        # Procesar envío
        if enviado:
            if not nombre.strip():
                st.error("Por favor selecciona tu nombre.")
                st.stop()

            # Evitar duplicados por persona
            if not df_aportes.empty and nombre in df_aportes["nombre"].values:
                st.error("Ya registraste tu aporte antes. Si necesitas cambiarlo, avisa a la organización.")
                st.stop()

            opcion = int(opcion_seleccionada)

            if opcion not in OPCIONES:
                st.error("La opción seleccionada no existe.")
                st.stop()

            if cupos_usados[opcion] >= OPCIONES[opcion]["max"]:
                st.error("Esa opción ya está llena, por favor elige otra.")
                st.stop()

            if opcion == 9 and not detalle.strip():
                st.error("Por favor describe qué vas a llevar en 'Otro'.")
                st.stop()

            # Agregar aporte
            nuevo = {
                "nombre": nombre.strip(),
                "opcion": str(opcion),
                "detalle": detalle.strip() if detalle else "",
            }

            df_aportes = pd.concat([df_aportes, pd.DataFrame([nuevo])], ignore_index=True)
            guardar_aportes(df_aportes)

            st.success(f"¡Listo, {nombre}! Llevarás **{OPCIONES[opcion]['nombre']}** 🎉")
            if detalle:
                st.info(f"Detalle: {detalle}")

            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # ---- Aportes registrados ----
    if not df_aportes.empty:
        st.subheader("📋 Aportes registrados hasta ahora")

        df_mostrar = df_aportes.copy()
        df_mostrar["opcion_desc"] = df_mostrar["opcion"].astype(int).map(
            {k: v["nombre"] for k, v in OPCIONES.items()}
        )
        df_mostrar = df_mostrar[["nombre", "opcion_desc", "detalle"]]
        df_mostrar.rename(
            columns={
                "nombre": "Nombre",
                "opcion_desc": "Opción elegida",
                "detalle": "Detalle",
            },
            inplace=True,
        )

        # Ordenar por nombre para que se vea más organizado
        df_mostrar = df_mostrar.sort_values("Nombre").reset_index(drop=True)

        st.dataframe(df_mostrar, use_container_width=True)

        # Quiénes faltan
        nombres_ya = set(df_aportes["nombre"].tolist())
        faltan = [n for n in PARTICIPANTES if n not in nombres_ya]
        if faltan:
            st.markdown("### 🙋‍♀️ Personas que aún no registran su aporte")
            st.write(", ".join(faltan))
        else:
            st.success("🎉 ¡Todos los participantes ya registraron su aporte!")


if __name__ == "__main__":
    main()
