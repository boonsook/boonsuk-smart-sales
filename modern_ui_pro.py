import streamlit as st
import pandas as pd
from supabase import create_client
import os

st.set_page_config(
    page_title="Boonsuk Smart Sales PRO",
    page_icon="❄️",
    layout="wide"
)

# -----------------------
# SUPABASE CONNECT
# -----------------------

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------
# HEADER
# -----------------------

st.title("❄️ บุญสุข Smart Sales PRO")

menu = st.sidebar.selectbox(
    "เมนู",
    ["Dashboard","ใบเสนอราคา","งานบริการ","สต๊อก","BTU"]
)

# -----------------------
# DASHBOARD
# -----------------------

if menu == "Dashboard":

    st.subheader("Dashboard")

    col1,col2,col3 = st.columns(3)

    jobs_total = 0
    service_total = 0
    stock_total = 0

    if supabase:

        try:
            jobs_total = len(supabase.table("jobs").select("*").execute().data)
        except:
            pass

        try:
            service_total = len(supabase.table("service_jobs").select("*").execute().data)
        except:
            pass

        try:
            stock_total = len(supabase.table("stock").select("*").execute().data)
        except:
            pass

    col1.metric("ใบเสนอราคา",jobs_total)
    col2.metric("งานบริการ",service_total)
    col3.metric("สินค้า",stock_total)

# -----------------------
# QUOTE
# -----------------------

if menu == "ใบเสนอราคา":

    st.subheader("สร้างใบเสนอราคา")

    name = st.text_input("ชื่อลูกค้า")
    phone = st.text_input("เบอร์โทร")

    room = st.number_input("ขนาดห้อง (ตรม.)",20)

    btu = room * 800

    st.success(f"BTU แนะนำ {btu}")

    model = st.text_input("รุ่นแอร์")

    price = st.number_input("ราคา",15000)

    if st.button("บันทึก"):

        if supabase:

            supabase.table("jobs").insert({

                "customer_name":name,
                "customer_phone":phone,
                "model":model,
                "btu":btu,
                "base_price":price

            }).execute()

            st.success("บันทึกแล้ว")

# -----------------------
# SERVICE
# -----------------------

if menu == "งานบริการ":

    st.subheader("รับงานบริการ")

    name = st.text_input("ชื่อลูกค้า")
    phone = st.text_input("เบอร์โทร")
    symptom = st.text_area("อาการเสีย")

    if st.button("บันทึกงาน"):

        if supabase:

            supabase.table("service_jobs").insert({

                "customer_name":name,
                "customer_phone":phone,
                "symptom":symptom

            }).execute()

            st.success("บันทึกแล้ว")

# -----------------------
# STOCK
# -----------------------

if menu == "สต๊อก":

    st.subheader("สต๊อกสินค้า")

    if supabase:

        data = supabase.table("stock").select("*").execute()

        df = pd.DataFrame(data.data)

        st.dataframe(df)

# -----------------------
# BTU
# -----------------------

if menu == "BTU":

    st.subheader("คำนวณ BTU")

    room = st.number_input("ขนาดห้อง",20)

    btu = room * 800

    st.success(f"BTU ที่แนะนำ {btu}")
