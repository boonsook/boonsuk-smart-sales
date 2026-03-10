import streamlit as st

st.set_page_config(
    page_title="Boonsuk Smart UI",
    page_icon="❄️",
    layout="wide"
)

# ---------- STYLE ----------
st.markdown("""
<style>

body {
background:#f4f6fb;
}

.card {
background:white;
padding:25px;
border-radius:18px;
box-shadow:0 10px 20px rgba(0,0,0,0.08);
text-align:center;
}

.bigbutton button {
height:70px;
font-size:20px;
border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.title("❄️ บุญสุขอิเล็กทรอนิกส์")
st.caption("Modern UI Demo")

st.divider()

# ---------- DASHBOARD ----------
st.subheader("Dashboard")

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.markdown('<div class="card">💰<br>ยอดขายวันนี้<br><h2>21,000</h2></div>',unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card">📦<br>สินค้าในสต๊อก<br><h2>98</h2></div>',unsafe_allow_html=True)

with c3:
    st.markdown('<div class="card">🧾<br>ใบเสนอราคา<br><h2>5</h2></div>',unsafe_allow_html=True)

with c4:
    st.markdown('<div class="card">🔧<br>งานบริการ<br><h2>2</h2></div>',unsafe_allow_html=True)

st.divider()

# ---------- MENU ----------
st.subheader("เมนูหลัก")

m1,m2,m3 = st.columns(3)

with m1:
    st.button("📄 สร้างใบเสนอราคา",use_container_width=True)

with m2:
    st.button("👥 ลูกค้า",use_container_width=True)

with m3:
    st.button("📦 สต๊อกสินค้า",use_container_width=True)

st.divider()

st.subheader("ทดลอง UI")

room = st.number_input("ขนาดห้อง (ตรม.)",value=20)

btu = room * 800

st.success(f"BTU ที่แนะนำ : {int(btu):,}")
