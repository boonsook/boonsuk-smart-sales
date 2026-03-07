import os
import math
import pandas as pd
import streamlit as st
from datetime import date, datetime
from urllib.parse import quote as urlquote
from fpdf import FPDF

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="Boonsuk Smart Sales PRO v2", layout="centered")

STORE_NAME = "ร้านบุญสุขอิเล็กทรอนิกส์"
STORE_PHONE = "086-2613829"
STORE_WEB = "https://www.facebook.com/boonsukele/"

# ถ้าต้องการให้ปุ่ม LINE ส่งไปบัญชีร้าน ให้ใส่ LINE OA หรือ LINE ID (ไม่จำเป็น)
STORE_LINE_ID = ""  # เช่น "@boonsuk" หรือ "boonsukshop" (ถ้ามี)

INSTALL_CONDITIONS = (
    "1) แถมรางครอบท่อน้ำยาให้ฟรี ไม่เกิน 4 เมตร หากเกินคิดเพิ่ม เมตรละ 200 บาท\n"
    "2) แถมท่อน้ำยา ไม่เกิน 4 เมตร หากเกินคิดเพิ่ม เมตรละ 400 บาท\n"
    "3) แถมท่อน้ำทิ้ง ไม่เกิน 10 เมตร หากเกินคิดเพิ่ม เมตรละ 40 บาท\n"
    "4) แถมสายไฟ ไม่เกิน 10 เมตร หากเกินคิดเพิ่ม เมตรละ 40 บาท\n"
    "5) แถมขาแขวนหรือขายาง สำหรับติดตั้งคอยล์ร้อน\n"
    "6) กรณีไม่มีเบรคเกอร์ แถมให้ฟรี\n"
    "7) รับประกันงานตามเงื่อนไขฟรี ตลอดอายุการใช้งาน"
)

DATA_DIR = "."
STOCK_CSV = os.path.join(DATA_DIR, "boonsuk_stock.csv")
LOG_CSV = os.path.join(DATA_DIR, "boonsuk_customer_log.csv")


# =========================
# YOUR PRODUCTS (replace with your full list)
# Add "stock_qty" if you want (optional). If not, system will default to 0.
# =========================
PRODUCTS = [
    {"section": "Midea ฟิกส์speed", "model": "Asmg09c", "btu": 9000, "price_install": 19000,
     "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "10 ปี", "stock_qty": 1},
    {"section": "Midea ฟิกส์speed", "model": "Asmg12j", "btu": 12000, "price_install": 21500,
     "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "10 ปี", "stock_qty": 2},
]


# =========================
# HELPERS
# =========================
def format_baht(x) -> str:
    try:
        return f"{int(x):,}"
    except Exception:
        return str(x)

def calculate_btu(width, length, height, sun_exposure, people):
    area = width * length
    base_btu = area * 900
    if height > 2.7:
        base_btu *= 1.10
    if sun_exposure == "โดนแดด":
        base_btu *= 1.15
    base_btu += max(0, (people - 1)) * 600
    return int(round(base_btu))

def suggest_capacity(btu):
    steps = [9000, 12000, 15000, 18000, 22000, 24000, 25000, 28000, 30000]
    for s in steps:
        if btu <= s:
            return s
    return 30000

def clean_products_df(df: pd.DataFrame) -> pd.DataFrame:
    # Normalize columns
    need_cols = ["section","model","btu","price_install","w_install","w_parts","w_comp","stock_qty"]
    for c in need_cols:
        if c not in df.columns:
            df[c] = "" if c in ["section","model","w_install","w_parts","w_comp"] else 0

    df["section"] = df["section"].astype(str).str.strip()
    df["model"] = df["model"].astype(str).str.strip()

    df["btu"] = pd.to_numeric(df["btu"], errors="coerce").fillna(0).astype(int)
    df["price_install"] = pd.to_numeric(df["price_install"], errors="coerce").fillna(0).astype(int)
    df["stock_qty"] = pd.to_numeric(df["stock_qty"], errors="coerce").fillna(0).astype(int)

    # Drop obvious junk rows (your old data had btu/price=86 etc.)
    df = df[(df["btu"] >= 1000) & (df["price_install"] >= 1000)].copy()
    df = df[df["section"] != ""]
    df = df[df["model"] != ""]
    return df

def load_stock() -> pd.DataFrame:
    base = clean_products_df(pd.DataFrame(PRODUCTS))

    if os.path.exists(STOCK_CSV):
        try:
            stock = pd.read_csv(STOCK_CSV, encoding="utf-8-sig")
            stock = clean_products_df(stock)
            # Merge stock_qty by (section, model)
            key = ["section","model"]
            merged = base.merge(stock[key + ["stock_qty"]], on=key, how="left", suffixes=("","_stock"))
            merged["stock_qty"] = merged["stock_qty_stock"].fillna(merged["stock_qty"]).astype(int)
            merged = merged.drop(columns=["stock_qty_stock"])
            return merged
        except Exception:
            # If stock file broken, fallback to base
            return base

    return base

def save_stock(df: pd.DataFrame):
    df_out = df.copy()
    # keep only needed columns for persistence
    df_out = df_out[["section","model","btu","price_install","w_install","w_parts","w_comp","stock_qty"]].copy()
    df_out.to_csv(STOCK_CSV, index=False, encoding="utf-8-sig")

def _load_thai_font(pdf: FPDF) -> str:
    font_regular = os.path.join("fonts", "THSarabunNew.ttf")
    font_bold = os.path.join("fonts", "THSarabunNew Bold.ttf")
    if not os.path.exists(font_regular):
        raise FileNotFoundError("ไม่พบฟอนต์ไทย: fonts/THSarabunNew.ttf (ต้องใส่ไฟล์ฟอนต์ก่อน)")

    pdf.add_font("THSarabun", "", font_regular, uni=True)
    if os.path.exists(font_bold):
        pdf.add_font("THSarabun", "B", font_bold, uni=True)
    else:
        pdf.add_font("THSarabun", "B", font_regular, uni=True)
    return "THSarabun"

def build_pdf(quote: dict) -> bytes:
    pdf = FPDF(unit="mm", format="A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=12)

    font = _load_thai_font(pdf)

    # Header
    pdf.set_font(font, "B", 18)
    pdf.cell(0, 10, "QUOTATION / ใบเสนอราคา", ln=1, align="C")

    pdf.set_font(font, "B", 14)
    pdf.cell(0, 7, STORE_NAME, ln=1)
    pdf.set_font(font, "", 12)
    pdf.cell(0, 6, f"มือถือ/Line: {STORE_PHONE}", ln=1)
    pdf.cell(0, 6, f"Website: {STORE_WEB}", ln=1)
    pdf.ln(2)

    # Customer
    pdf.set_font(font, "", 12)
    pdf.cell(0, 6, f"วันที่: {quote['date']}", ln=1)
    pdf.cell(0, 6, f"ลูกค้า: {quote['customer_name']}   โทร: {quote['customer_phone']}", ln=1)
    pdf.multi_cell(0, 6, f"ที่อยู่: {quote['customer_address']}")
    pdf.ln(1)

    # Room
    pdf.set_font(font, "B", 14)
    pdf.cell(0, 7, "รายละเอียดห้อง / Room Details", ln=1)
    pdf.set_font(font, "", 12)
    pdf.cell(0, 6, f"ขนาดห้อง: {quote['room_w']} x {quote['room_l']} ม.  สูง {quote['room_h']} ม.", ln=1)
    pdf.cell(0, 6, f"โดนแดด: {quote['sun']}   จำนวนคน: {quote['people']}", ln=1)
    pdf.cell(0, 6, f"BTU ที่แนะนำ: {quote['btu']:,}  (แนะนำไซส์: {quote['suggest_cap']:,})", ln=1)
    pdf.ln(1)

    # Item
    pdf.set_font(font, "B", 14)
    pdf.cell(0, 7, "รายการสินค้า / Item", ln=1)
    pdf.set_font(font, "", 12)
    pdf.multi_cell(0, 6, f"รุ่น/ซีรีส์: {quote['section']}")
    pdf.cell(0, 6, f"Model: {quote['model']}   BTU: {quote['model_btu']:,}", ln=1)
    pdf.cell(0, 6, f"ประกัน (ติดตั้ง/อะไหล่/คอมฯ): {quote['w_install']} / {quote['w_parts']} / {quote['w_comp']}", ln=1)
    pdf.cell(0, 6, f"ราคาพร้อมติดตั้ง: {format_baht(quote['base_price'])} บาท", ln=1)
    pdf.ln(1)

    # Summary
    pdf.set_font(font, "B", 14)
    pdf.cell(0, 7, "สรุปราคา / Price Summary", ln=1)
    pdf.set_font(font, "", 12)
    pdf.cell(0, 6, f"ราคาพร้อมติดตั้ง: {format_baht(quote['base_price'])} บาท", ln=1)
    pdf.cell(0, 6, f"ส่วนลด: -{format_baht(quote['discount'])} บาท", ln=1)
    pdf.cell(0, 6, f"ค่าติดตั้งเพิ่ม: +{format_baht(quote['extra_install'])} บาท", ln=1)
    pdf.set_font(font, "B", 14)
    pdf.cell(0, 8, f"รวมสุทธิ: {format_baht(quote['net_total'])} บาท", ln=1)
    pdf.ln(2)

    # Conditions
    pdf.set_font(font, "B", 14)
    pdf.cell(0, 7, "เงื่อนไขการติดตั้ง", ln=1)
    pdf.set_font(font, "", 11)
    for line in INSTALL_CONDITIONS.split("\n"):
        if line.strip():
            pdf.multi_cell(0, 5, line.strip())
    pdf.ln(2)

    pdf.set_font(font, "", 12)
    pdf.cell(0, 8, "ลงชื่อผู้รับใบเสนอราคา: ____________________________", ln=1)
    pdf.cell(0, 8, "วันที่: ____ / ____ / ______", ln=1)

    out = pdf.output(dest="S")
    if isinstance(out, (bytes, bytearray)):
        return bytes(out)
    return out.encode("latin-1")

def make_line_message_text(quote: dict) -> str:
    lines = [
        f"ใบเสนอราคา - {STORE_NAME}",
        f"วันที่: {quote['date']}",
        f"ลูกค้า: {quote['customer_name']}  โทร: {quote['customer_phone']}",
        f"รุ่น: {quote['section']} / {quote['model']} ({quote['model_btu']:,} BTU)",
        f"ราคา: {format_baht(quote['base_price'])} บาท",
        f"ส่วนลด: {format_baht(quote['discount'])} บาท",
        f"ติดตั้งเพิ่ม: {format_baht(quote['extra_install'])} บาท",
        f"รวมสุทธิ: {format_baht(quote['net_total'])} บาท",
        "",
        f"ติดต่อ: {STORE_PHONE}",
        f"เพจ: {STORE_WEB}",
    ]
    return "\n".join(lines)

def line_share_link(text: str) -> str:
    # Universal share link (works on mobile & desktop with LINE)
    return "https://line.me/R/msg/text/?" + urlquote(text)

def log_customer_job(quote: dict):
    record = quote.copy()
    record["section"] = str(record["section"]).replace("\n", " | ")
    df_log = pd.DataFrame([record])
    df_log.to_csv(
        LOG_CSV,
        mode="a",
        header=not os.path.exists(LOG_CSV),
        index=False,
        encoding="utf-8-sig"
    )


# =========================
# UI HEADER (logo optional)
# =========================
logo_path = os.path.join("assets", "logo.png")
if os.path.exists(logo_path):
    st.image(logo_path, use_container_width=True)

st.markdown(
    f"""
    <div style="text-align:center;">
      <div style="font-size:28px; font-weight:800;">{STORE_NAME}</div>
      <div style="font-size:16px;">มือถือ/Line: <b>{STORE_PHONE}</b> | Website: {STORE_WEB}</div>
      <div style="font-size:13px; opacity:0.75;">Boonsuk Smart Sales PRO v2</div>
    </div>
    """,
    unsafe_allow_html=True
)
st.divider()

# =========================
# LOAD STOCK
# =========================
df_all = load_stock()

# =========================
# CUSTOMER + ROOM FORM (mobile friendly)
# =========================
with st.expander("🧑‍💼 ข้อมูลลูกค้า", expanded=True):
    customer_name = st.text_input("ชื่อลูกค้า", value="")
    customer_phone = st.text_input("เบอร์โทร", value="")
    customer_address = st.text_area("ที่อยู่/สถานที่ติดตั้ง", value="", height=80)

st.subheader("🏠 คำนวณ BTU")
room_w = st.number_input("กว้าง (เมตร)", min_value=0.0, step=0.1)
room_l = st.number_input("ยาว (เมตร)", min_value=0.0, step=0.1)
room_h = st.number_input("สูง (เมตร)", min_value=0.0, step=0.1, value=2.6)
sun = st.selectbox("ห้องโดนแดดไหม?", ["ไม่โดนแดด", "โดนแดด"])
people = st.number_input("จำนวนคนในห้อง", min_value=1, step=1, value=1)

btu = None
suggest_cap = None
if room_w > 0 and room_l > 0:
    btu = calculate_btu(room_w, room_l, room_h, sun, int(people))
    suggest_cap = suggest_capacity(btu)
    st.success(f"BTU ที่แนะนำ: **{btu:,} BTU**  |  แนะนำไซส์: **{suggest_cap:,} BTU**")
else:
    st.info("กรอกกว้าง/ยาว เพื่อคำนวณ BTU")

st.divider()

# =========================
# PRODUCT PICKER + TABLE
# =========================
st.subheader("❄️ เลือกรุ่นแอร์ + สต๊อก")

# Filters
q = st.text_input("ค้นหา (รุ่น/ซีรีส์)", value="").strip().lower()

df_view = df_all.copy()
if q:
    df_view = df_view[
        df_view["section"].str.lower().str.contains(q, na=False) |
        df_view["model"].str.lower().str.contains(q, na=False)
    ].copy()

sections = sorted(df_view["section"].dropna().unique().tolist())
if not sections:
    st.warning("ไม่พบข้อมูลสินค้า (เช็ค PRODUCTS หรือไฟล์ stock)")
    st.stop()

section = st.selectbox("เลือกซีรีส์/หมวดรุ่น", options=sections)

df_sec = df_view[df_view["section"] == section].copy()
if btu is not None and suggest_cap is not None:
    df_sec["diff"] = (df_sec["btu"] - int(suggest_cap)).abs()
    df_sec = df_sec.sort_values(["diff", "price_install"], ascending=[True, True])
else:
    df_sec = df_sec.sort_values(["price_install"], ascending=[True])

models = df_sec["model"].tolist()
model = st.selectbox("เลือก Model", options=models)

row = df_sec[df_sec["model"] == model].iloc[0].to_dict()

st.markdown(
    f"""
**BTU รุ่นนี้:** {int(row['btu']):,}  
**ราคา(พร้อมติดตั้ง):** {format_baht(row['price_install'])} บาท  
**สต๊อกคงเหลือ:** {int(row.get('stock_qty',0))} เครื่อง  
"""
)

st.caption(f"ประกัน: ติดตั้ง {row.get('w_install','')} | อะไหล่ {row.get('w_parts','')} | คอมฯ {row.get('w_comp','')}")

with st.expander("📋 ตารางสินค้า (ดู/เช็คสต๊อก)", expanded=False):
    show_cols = ["section","model","btu","price_install","stock_qty","w_install","w_parts","w_comp"]
    st.dataframe(df_view[show_cols], use_container_width=True, hide_index=True)

st.divider()

# =========================
# PRICE ADJUST
# =========================
st.subheader("💰 ปรับราคา")
discount = st.number_input("ส่วนลด (บาท)", min_value=0, step=100, value=0)
extra_install = st.number_input("ค่าติดตั้งเพิ่ม (บาท)", min_value=0, step=100, value=0)

base_price = int(row["price_install"])
net_total = max(0, base_price - int(discount) + int(extra_install))
st.info(f"**รวมสุทธิ:** {format_baht(net_total)} บาท")

st.divider()

# =========================
# QUOTE OBJECT
# =========================
today_str = date.today().strftime("%d/%m/%Y")
quote_data = {
    "date": today_str,
    "customer_name": customer_name,
    "customer_phone": customer_phone,
    "customer_address": customer_address,
    "room_w": room_w, "room_l": room_l, "room_h": room_h,
    "sun": sun, "people": int(people),
    "btu": int(btu) if btu is not None else 0,
    "suggest_cap": int(suggest_cap) if suggest_cap is not None else 0,
    "section": section,
    "model": model,
    "model_btu": int(row["btu"]),
    "w_install": row.get("w_install", ""),
    "w_parts": row.get("w_parts", ""),
    "w_comp": row.get("w_comp", ""),
    "base_price": base_price,
    "discount": int(discount),
    "extra_install": int(extra_install),
    "net_total": int(net_total),
}

# =========================
# ACTIONS (PDF + LINE + LOG)
# =========================
st.subheader("🧾 ใบเสนอราคา (PRO v2)")

c1, c2 = st.columns(2)

if c1.button("💾 บันทึกลูกค้า/งานนี้", use_container_width=True):
    try:
        log_customer_job(quote_data)
        st.success("บันทึกแล้ว ✅")
    except Exception as e:
        st.error(f"บันทึกไม่สำเร็จ: {e}")

# Create PDF on-demand
if c2.button("📄 สร้าง PDF ใบเสนอราคา", use_container_width=True):
    try:
        pdf_bytes = build_pdf(quote_data)
        pdf_name = f"ใบเสนอราคา_{(customer_name or 'ลูกค้า')}_{today_str.replace('/','-')}.pdf"
        st.success("สร้าง PDF สำเร็จ ✅ กดดาวน์โหลดได้เลย")
        st.download_button(
            "⬇️ ดาวน์โหลด PDF",
            data=pdf_bytes,
            file_name=pdf_name,
            mime="application/pdf",
            use_container_width=True
        )
    except Exception as e:
        st.error(f"สร้าง PDF ไม่สำเร็จ: {e}")

# LINE share
st.divider()
st.subheader("💬 ส่งข้อความเข้า LINE ลูกค้า")
line_text = make_line_message_text(quote_data)
st.text_area("ข้อความที่จะส่ง (แก้ได้ก่อนส่ง)", value=line_text, height=180)

share_url = line_share_link(line_text)
st.markdown(f"✅ กดเพื่อเปิด LINE และส่งข้อความ: **[ส่งเข้า LINE]({share_url})**")

st.caption("หมายเหตุ: ถ้าเปิดบนมือถือจะส่งง่ายที่สุด / บนคอมต้องมี LINE ติดตั้งหรือใช้งาน LINE ที่รองรับลิงก์แชร์")

# =========================
# STOCK MANAGER
# =========================
st.divider()
st.subheader("📦 จัดการสต๊อกแอร์ (แก้แล้วบันทึก)")

st.info("ปรับจำนวนสต๊อก แล้วกด 'บันทึกสต๊อก' (ข้อมูลจะถูกเก็บใน boonsuk_stock.csv)")

edit_cols = ["section","model","btu","price_install","stock_qty","w_install","w_parts","w_comp"]
df_edit = df_all[edit_cols].copy()

edited = st.data_editor(
    df_edit,
    use_container_width=True,
    hide_index=True,
    num_rows="fixed",
    column_config={
        "stock_qty": st.column_config.NumberColumn("stock_qty", min_value=0, step=1),
        "price_install": st.column_config.NumberColumn("price_install", min_value=0, step=100),
        "btu": st.column_config.NumberColumn("btu", min_value=0, step=100),
    },
)

if st.button("✅ บันทึกสต๊อก", use_container_width=True):
    try:
        edited = clean_products_df(edited)
        save_stock(edited)
        st.success("บันทึกสต๊อกแล้ว ✅")
    except Exception as e:
        st.error(f"บันทึกสต๊อกไม่สำเร็จ: {e}")

# Customer log download
if os.path.exists(LOG_CSV):
    st.divider()
    st.subheader("⬇️ ดาวน์โหลดไฟล์บันทึกลูกค้า")
    with open(LOG_CSV, "rb") as f:
        st.download_button(
            "ดาวน์โหลด boonsuk_customer_log.csv",
            data=f.read(),
            file_name="boonsuk_customer_log.csv",
            mime="text/csv",
            use_container_width=True
        )
