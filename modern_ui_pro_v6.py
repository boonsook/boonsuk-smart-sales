import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client
import os

st.set_page_config(
    page_title="Boonsuk Smart Sales PRO",
    page_icon="❄️",
    layout="wide"
)

# ---------------------------
# SUPABASE CONNECT
# ---------------------------

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = None

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ---------------------------
# STYLE
# ---------------------------

st.markdown("""
<style>

body{
background:#f4f7fb;
}

.hero{
background:linear-gradient(135deg,#0f3d91,#1f66ff);
padding:25px;
border-radius:18px;
color:white;
}

.card{
background:white;
padding:20px;
border-radius:18px;
box-shadow:0 10px 25px rgba(0,0,0,0.08);
}

</style>
""",unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------

st.markdown(f"""
<div class="hero">

### ❄️ บุญสุข Smart Sales PRO

{datetime.now().strftime("%d %B %Y")}

</div>
""",unsafe_allow_html=True)

st.divider()

# ---------------------------
# DASHBOARD
# ---------------------------

st.subheader("Dashboard")

sales_today = 0
quotes_total = 0
jobs_total = 0
stock_total = 0

if supabase:

    try:
        quotes = supabase.table("quotes").select("*").execute()
        quotes_total = len(quotes.data)
    except:
        pass

    try:
        jobs = supabase.table("service_jobs").select("*").execute()
        jobs_total = len(jobs.data)
    except:
        pass

    try:
        stock = supabase.table("stock").select("*").execute()
        stock_total = len(stock.data)
    except:
        pass

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.markdown(f'<div class="card"><h3>ยอดขาย</h3><h2>{sales_today}</h2></div>',unsafe_allow_html=True)

with c2:
    st.markdown(f'<div class="card"><h3>ใบเสนอราคา</h3><h2>{quotes_total}</h2></div>',unsafe_allow_html=True)

with c3:
    st.markdown(f'<div class="card"><h3>งานบริการ</h3><h2>{jobs_total}</h2></div>',unsafe_allow_html=True)

with c4:
    st.markdown(f'<div class="card"><h3>สินค้า</h3><h2>{stock_total}</h2></div>',unsafe_allow_html=True)

st.divider()

# ---------------------------
# MENU
# ---------------------------

st.subheader("เมนูหลัก")

m1,m2,m3,m4 = st.columns(4)

if "page" not in st.session_state:
    st.session_state.page = "home"

with m1:
    if st.button("🧾 ใบเสนอราคา",use_container_width=True):
        st.session_state.page="quote"

with m2:
    if st.button("🔧 งานบริการ",use_container_width=True):
        st.session_state.page="service"

with m3:
    if st.button("📦 สต๊อก",use_container_width=True):
        st.session_state.page="stock"

with m4:
    if st.button("🧮 BTU",use_container_width=True):
        st.session_state.page="btu"

st.divider()

# ---------------------------
# QUOTE PAGE
# ---------------------------

if st.session_state.page=="quote":

    st.subheader("สร้างใบเสนอราคา")

    name = st.text_input("ชื่อลูกค้า")
    phone = st.text_input("เบอร์โทร")

    room = st.number_input("ขนาดห้อง (ตรม.)",value=20)

    btu = room * 800

    st.success(f"BTU แนะนำ : {int(btu):,}")

    model = st.text_input("รุ่นแอร์")

    price = st.number_input("ราคา",value=15000)

    if st.button("บันทึกใบเสนอราคา"):

        if supabase:

            data = {
                "customer_name":name,
                "phone":phone,
                "room_size":room,
                "btu":btu,
                "air_model":model,
                "price":price
            }

            supabase.table("quotes").insert(data).execute()

            st.success("บันทึกแล้ว")

# ---------------------------
# SERVICE PAGE
# ---------------------------

if st.session_state.page=="service":

    st.subheader("รับงานบริการ")

    name = st.text_input("ชื่อลูกค้า")

    problem = st.text_area("อาการเสีย")

    date = st.date_input("วันนัด")

    if st.button("บันทึกงาน"):

        if supabase:

            data={
                "customer_name":name,
                "problem":problem,
                "appointment":str(date)
            }

            supabase.table("service_jobs").insert(data).execute()

            st.success("บันทึกงานแล้ว")

# ---------------------------
# STOCK PAGE
# ---------------------------

if st.session_state.page=="stock":

    st.subheader("สต๊อกสินค้า")

    if supabase:

        stock = supabase.table("stock").select("*").execute()

        df = pd.DataFrame(stock.data)

        st.dataframe(df,use_container_width=True)

# ---------------------------
# BTU PAGE
# ---------------------------

if st.session_state.page=="btu":

    st.subheader("คำนวณ BTU")

    room = st.number_input("ขนาดห้อง",value=20)

    btu = room * 800

    st.success(f"BTU ที่แนะนำ : {int(btu):,}")
