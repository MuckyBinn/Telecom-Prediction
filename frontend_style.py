import streamlit as st

def inject_yellow_theme():
    st.markdown(
        """
        <style>
        /* สีหลักโทนเหลือง-ดำ */
        :root {
            --primary-color: #FFD700;
            --secondary-color: #2d2d2d;
            --accent-color: #f1c40f;
            --bg-color: #fff8dc;
        }

        /* พื้นหลัง */
        .stApp {
            background: linear-gradient(to bottom right, var(--bg-color), #fff);
            font-family: 'Kanit', sans-serif;
        }

        /* หัวข้อ */
        h1, h2, h3, h4, h5 {
            color: var(--secondary-color);
        }

        /* ปุ่ม */
        div.stButton > button {
            background-color: var(--primary-color);
            color: black;
            font-weight: bold;
            border-radius: 10px;
            border: none;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.2s ease;
        }
        div.stButton > button:hover {
            background-color: var(--accent-color);
            transform: scale(1.03);
        }

        /* กล่องข้อความ และฟอร์ม */
        .stTextInput, .stSelectbox, .stNumberInput, .stSlider {
            background-color: #fff;
            border-radius: 10px;
        }

        /* กล่องผลลัพธ์ */
        .stMetric {
            background: var(--primary-color);
            border-radius: 10px;
            padding: 10px;
            color: black;
        }

        /* ส่วนหัวคล้ายแบนเนอร์ AIS */
        .custom-header {
            background: linear-gradient(90deg, var(--primary-color), #ffe97f);
            padding: 1rem;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 2rem;
        }
        .custom-header h1 {
            color: #2d2d2d;
            font-size: 2rem;
            font-weight: 800;
            margin: 0;
        }
        .custom-header p {
            color: #444;
            font-size: 1.1rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
def show_custom_header():
    st.markdown(
        """
        <div class="custom-header">
            <h1>📶 Cooper Thailand</h1>
            <p>บริการวิเคราะห์ความเสี่ยงการยกเลิกสัญญาคูเปอร์</p>
        </div>
        """,
        unsafe_allow_html=True
    )
