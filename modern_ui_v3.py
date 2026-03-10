import os
from datetime import datetime

import pandas as pd
import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Boonsuk Smart Sales v6",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# OPTIONAL SUPABASE
# =========================================================
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
supabase = None

try:
    if SUPABASE_URL and SUPABASE_KEY:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception:
    supabase = None

# =========================================================
# STORE INFO
# =========================================================
STORE_NAME = "บุญสุขอิเล็กทรอนิกส์"
STORE_SUB = "Boonsuk Smart Sales Platform"
APP_VERSION = "v6 Modern Pro"
STORE_PHONE = "086-2613829"

# =========================================================
# SESSION STATE
# =========================================================
if "page" not in st.session_state:
    st.session_state.page = "home"

if "quote_step" not in st.session_state:
    st.session_state.quote_step = 1

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "Daikin Inverter 12,000 BTU"

if "selected_price" not in st.session_state:
    st.session_state.selected_price = 12900

# =========================================================
# STYLE
# =========================================================
st.markdown("""
<style>
:root{
  --bg1:#f4f8ff;
  --bg2:#eef4ff;
  --card:#ffffff;
  --text:#10233f;
  --muted:#6a7b92;
  --line:#e7eef8;
  --blue1:#0f3d91;
  --blue2:#1f66ff;
  --green:#21b573;
  --orange:#ffad42;
  --pink:#ff6ba6;
  --purple:#7a68ff;
  --shadow:0 12px 30px rgba(16,35,63,.08);
  --radius:24px;
}
.stApp{
  background:
    radial-gradient(circle at top left, rgba(31,102,255,.08), transparent 23%),
    radial-gradient(circle at top right, rgba(33,181,115,.06), transparent 20%),
    linear-gradient(180deg,#f8fbff 0%, #f4f8ff 100%);
  color:var(--text);
}
.block-container{
  max-width:1180px;
  padding-top:1rem;
  padding-bottom:6rem;
}
.hero{
  background:linear-gradient(135deg,var(--blue1) 0%, var(--blue2) 100%);
  border-radius:28px;
  padding:22px;
  color:#fff;
  box-shadow:0 18px 40px rgba(15,61,145,.20);
  margin-bottom:16px;
}
.hero-row{
  display:flex;
  align-items:center;
  gap:16px;
}
.hero-avatar{
  width:68px;
  height:68px;
  min-width:68px;
  border-radius:50%;
  display:flex;
  align-items:center;
  justify-content:center;
  background:rgba(255,255,255,.18);
  border:2px solid rgba(255,255,255,.25);
  font-size:30px;
}
.hero-title{
  font-size:1.6rem;
  font-weight:800;
  line-height:1.1;
}
.hero-sub{
  color:rgba(255,255,255,.86);
  font-size:.95rem;
  margin-top:4px;
}
.chips{
  display:flex;
  gap:10px;
  flex-wrap:wrap;
  margin:10px 0 18px 0;
}
.chip{
  background:#fff;
  border:1px solid var(--line);
  color:#28405f;
  border-radius:999px;
  padding:8px 12px;
  font-size:.9rem;
  box-shadow:0 6px 16px rgba(16,35,63,.05);
}
.section-title{
  font-size:1.28rem;
  font-weight:800;
  margin:14px 0 12px 0;
}
.card{
  background:var(--card);
  border:1px solid var(--line);
  border-radius:24px;
  padding:18px;
  box-shadow:var(--shadow);
}
.kpi-card{
  background:#fff;
  border:1px solid var(--line);
  border-radius:24px;
  padding:18px;
  box-shadow:var(--shadow);
  min-height:122px;
}
.kpi-top{
  display:flex;
  justify-content:space-between;
  align-items:center;
  margin-bottom:10px;
}
.kpi-label{
  font-size:.95rem;
  color:var(--muted);
}
.kpi-icon{
  width:42px;
  height:42px;
  border-radius:14px;
  display:flex;
  align-items:center;
  justify-content:center;
  font-size:22px;
}
.kpi-value{
  font-size:2rem;
  font-weight:800;
  line-height:1.1;
}
.kpi-sub{
  color:var(--muted);
  font-size:.88rem;
  margin-top:6px;
}
.menu-card{
  background:#fff;
  border:1px solid var(--line);
  border-radius:24px;
  padding:18px 12px 12px 12px;
  text-align:center;
  box-shadow:var(--shadow);
  min-height:150px;
}
.menu-icon{
  width:64px;
  height:64px;
  border-radius:20px;
  display:flex;
  align-items:center;
  justify-content:center;
  margin:0 auto 10px auto;
  font-size:30px;
}
.menu-title{
  font-size:1rem;
  font-weight:800;
}
.menu-sub{
  color:var(--muted);
  font-size:.83rem;
  margin-top:4px;
}
.product-card{
  background:#fff;
  border:1px solid var(--line);
  border-radius:24px;
  padding:16px;
  box-shadow:var(--shadow);
  min-height:250px;
}
.badge{
  display:inline-block;
  background:#edf4ff;
  color:#1e56d8;
  border-radius:999px;
  padding:6px 10px;
  font-weight:700;
  font-size:.8rem;
}
.price{
  font-size:1.5rem;
  font-weight:800;
  margin-top:8px;
}
.summary-card{
  background:linear-gradient(180deg,#ffffff 0%,#f7fbff 100%);
  border:1px solid var(--line);
  border-radius:24px;
  padding:18px;
  box-shadow:var(--shadow);
  position:sticky;
  top:12px;
}
.muted{
  color:var(--muted);
  font-size:.9rem;
}
.bottom-nav-wrap{
  position:fixed;
  left:50%;
  transform:translateX(-50%);
  bottom:10px;
  width:min(800px, calc(100% - 18px));
  z-index:99999;
}
.bottom-nav{
  background:rgba(255,255,255,.88);
  backdrop-filter:blur(14px);
  border:1px solid var(--line);
  border-radius:24px;
  padding:8px;
  box-shadow:0 10px 30px rgba(16,35,63,.12);
}
div[data-testid="stButton"] > button{
  border-radius:16px;
  border:1px solid #dbe5f2;
  min-height:48px;
  font-weight:700;
}
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
div[data-testid="stTextArea"] textarea,
div[data-testid="stSelectbox"] div[data-baseweb="select"]{
  border-radius:14px !important;
}
hr{
  border:none;
  height:1px;
  background:var(--line);
  margin:12px 0;
}
@media (max-width:768px){
  .block-container{
    padding-left:.8rem;
    padding-right:.8rem;
    padding-bottom:6rem;
  }
  .hero-title{
    font-size:1.28rem;
  }
  .kpi-value{
    font-size:1.55rem;
  }
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================
def fmt_baht(value):
    try:
        return f"{int(float(value)):,}"
    except Exception:
        return "0"

def goto(page_name):
    st.session_state.page = page_name

def try_table_count(table_names):
    if not supabase:
        return None
    for name in table_names:
        try:
            res = supabase.table(name).select("*").limit(500).execute()
            return len(res.data or [])
        except Exception:
            continue
    return None

def try_table_rows(table_names, limit=20):
    if not supabase:
        return None
    for name in table_names:
        try:
            res = supabase.table(name).select("*").limit(limit).execute()
            return res.data or []
        except Exception:
            continue
    return None

def load_dashboard():
    data = {
        "sales_today": 28500,
        "stock_count": 206,
        "quote_count": 12,
        "service_count": 5,
        "customers": [
            {"name": "คุณสมชาย", "phone": "08x-xxx-1122", "job": "ใบเสนอราคาใหม่"},
            {"name": "คุณวรพล", "phone": "09x-xxx-7788", "job": "ล้างแอร์"},
            {"name": "คุณนิดา", "phone": "08x-xxx-4455", "job": "ติดตั้งใหม่"},
        ]
    }

    if not supabase:
        return data

    try:
        q_count = try_table_count(["quotes", "quotations", "quote"])
        s_count = try_table_count(["service_jobs", "service_job", "jobs", "service"])
        stock_count = try_table_count(["stock", "stocks", "inventory", "products"])
        customers = try_table_rows(["customers", "customer", "clients"], limit=5)

        if q_count is not None:
            data["quote_count"] = q_count
        if s_count is not None:
            data["service_count"] = s_count
        if stock_count is not None:
            data["stock_count"] = stock_count

        if customers:
            rows = []
            for c in customers:
                rows.append({
                    "name": c.get("name") or c.get("customer_name") or "ลูกค้า",
                    "phone": c.get("phone") or c.get("customer_phone") or "-",
                    "job": c.get("note") or c.get("status") or "ลูกค้าในระบบ",
                })
            data["customers"] = rows

        quote_rows = try_table_rows(["quotes", "quotations", "quote"], limit=200)
        if quote_rows:
            total = 0
            for row in quote_rows:
                val = row.get("net_total") or row.get("total") or row.get("price") or row.get("grand_total") or 0
                try:
                    total += float(val)
                except Exception:
                    pass
            if total > 0:
                data["sales_today"] = int(total)

        return data
    except Exception:
        return data

def render_header():
    now_txt = datetime.now().strftime("%d/%m/%Y %H:%M")
    st.markdown(f"""
    <div class="hero">
      <div class="hero-row">
        <div class="hero-avatar">❄️</div>
        <div>
          <div class="hero-title">{STORE_NAME}</div>
          <div class="hero-sub">{STORE_SUB} • {APP_VERSION}</div>
          <div class="hero-sub">อัปเดตล่าสุด {now_txt} • โทร {STORE_PHONE}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

def render_chips(data):
    st.markdown(f"""
    <div class="chips">
      <div class="chip">💰 ยอดรวม {fmt_baht(data["sales_today"])} บาท</div>
      <div class="chip">📦 สต๊อก {data["stock_count"]} รายการ</div>
      <div class="chip">🧾 ใบเสนอราคา {data["quote_count"]} งาน</div>
      <div class="chip">🛠️ งานบริการ {data["service_count"]} งาน</div>
    </div>
    """, unsafe_allow_html=True)

def kpi(icon, label, value, sub, bg):
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-top">
        <div class="kpi-label">{label}</div>
        <div class="kpi-icon" style="background:{bg};">{icon}</div>
      </div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

def menu_box(icon, title, subtitle, color, key, target):
    st.markdown(f"""
    <div class="menu-card">
      <div class="menu-icon" style="background:{color};">{icon}</div>
      <div class="menu-title">{title}</div>
      <div class="menu-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(f"เปิด{title}", key=key, use_container_width=True):
        goto(target)
        st.rerun()

def render_bottom_nav():
    st.markdown('<div class="bottom-nav-wrap"><div class="bottom-nav">', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        if st.button("🏠 Home", use_container_width=True):
            goto("home")
            st.rerun()
    with c2:
        if st.button("🧾 Quote", use_container_width=True):
            goto("quote")
            st.rerun()
    with c3:
        if st.button("🛠️ Service", use_container_width=True):
            goto("service")
            st.rerun()
    with c4:
        if st.button("📦 Stock", use_container_width=True):
            goto("stock")
            st.rerun()
    with c5:
        if st.button("📊 More", use_container_width=True):
            goto("more")
            st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)

# =========================================================
# PAGES
# =========================================================
def page_home():
    data = load_dashboard()
    render_header()
    render_chips(data)

    st.markdown('<div class="section-title">ภาพรวมวันนี้</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi("💰", "ยอดขายรวม", fmt_baht(data["sales_today"]), "สรุปจากใบเสนอราคา/ยอดขาย", "#fff3e8")
    with c2:
        kpi("📦", "สินค้าในสต๊อก", str(data["stock_count"]), "พร้อมขายและพร้อมติดตั้ง", "#eafaf1")
    with c3:
        kpi("🧾", "ใบเสนอราคา", str(data["quote_count"]), "เอกสารทั้งหมดในระบบ", "#eaf2ff")
    with c4:
        kpi("🛠️", "งานบริการ", str(data["service_count"]), "งานซ่อมและนัดหมาย", "#fff0f5")

    st.markdown('<div class="section-title">เมนูหลัก</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        menu_box("🧾", "ใบเสนอราคา", "สร้างเอกสารใหม่", "#eaf2ff", "m_quote", "quote")
    with m2:
        menu_box("🛠️", "รับงานซ่อม", "แจ้งงานบริการ", "#fff0f5", "m_service", "service")
    with m3:
        menu_box("📦", "สต๊อกสินค้า", "ตรวจคงเหลือ", "#fff3e8", "m_stock", "stock")
    with m4:
        menu_box("📊", "Dashboard", "ดูภาพรวมธุรกิจ", "#f2edff", "m_dash", "dashboard")

    st.markdown('<div class="section-title">ลูกค้าล่าสุด</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    for row in data["customers"]:
        a, b, c = st.columns([3, 2, 2])
        with a:
            st.write(f"**{row['name']}**")
        with b:
            st.write(row["phone"])
        with c:
            st.write(row["job"])
        st.divider()
    st.markdown("</div>", unsafe_allow_html=True)

def page_dashboard():
    data = load_dashboard()
    render_header()
    st.markdown('<div class="section-title">Dashboard Pro</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.2, 1.2, 1])
    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("สรุปยอด")
        st.metric("ยอดขายรวม", f"฿ {fmt_baht(data['sales_today'])}")
        st.metric("ใบเสนอราคา", data["quote_count"])
        st.metric("งานบริการ", data["service_count"])
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("สถานะสต๊อก")
        st.metric("สินค้าคงเหลือ", data["stock_count"])
        percent = min(data["stock_count"] / 250, 1.0)
        st.progress(percent)
        st.caption("ตัวอย่างแถบความพร้อมสินค้า")
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("ข้อมูลร้าน")
        st.write(f"**ร้าน:** {STORE_NAME}")
        st.write(f"**โทร:** {STORE_PHONE}")
        st.write(f"**เวอร์ชัน:** {APP_VERSION}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">รายงานย่อ</div>', unsafe_allow_html=True)
    chart_df = pd.DataFrame({
        "หมวด": ["ใบเสนอราคา", "งานบริการ", "สินค้าในสต๊อก"],
        "จำนวน": [data["quote_count"], data["service_count"], data["stock_count"]]
    }).set_index("หมวด")
    st.bar_chart(chart_df)

def page_quote():
    render_header()
    st.markdown('<div class="section-title">สร้างใบเสนอราคาแบบ Wizard</div>', unsafe_allow_html=True)

    step = st.session_state.quote_step
    st.progress({1:0.2, 2:0.4, 3:0.6, 4:0.8, 5:1.0}.get(step, 0.2))
    st.caption(f"ขั้นตอน {step}/5")

    if step == 1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("1) ข้อมูลลูกค้า")
        st.text_input("ชื่อลูกค้า", key="q_name")
        st.text_input("เบอร์โทร", key="q_phone")
        st.text_area("ที่อยู่ติดตั้ง", key="q_address")
        x1, x2 = st.columns([1,1])
        with x2:
            if st.button("ถัดไป", type="primary", use_container_width=True):
                st.session_state.quote_step = 2
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    elif step == 2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("2) ขนาดห้อง")
        room = st.number_input("ขนาดห้อง (ตร.ม.)", min_value=1, value=20, step=1, key="q_room")
        st.selectbox("ลักษณะการใช้งาน", ["ห้องนอน", "ห้องนั่งเล่น", "สำนักงาน", "ร้านค้า"], key="q_usage")
        st.caption(f"ขนาดห้องที่เลือก: {room} ตร.ม.")
        a, b, c = st.columns(3)
        with a:
            if st.button("ย้อนกลับ", use_container_width=True):
                st.session_state.quote_step = 1
                st.rerun()
        with c:
            if st.button("ถัดไป", type="primary", use_container_width=True):
                st.session_state.quote_step = 3
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    elif step == 3:
        room = st.session_state.get("q_room", 20)
        btu = room * 800
        st.session_state.q_btu = btu
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("3) คำนวณ BTU")
        st.success(f"BTU ที่แนะนำ: {int(btu):,}")
        st.caption("สูตรทดลอง: ขนาดห้อง x 800")
        a, b, c = st.columns(3)
        with a:
            if st.button("ย้อนกลับ", use_container_width=True):
                st.session_state.quote_step = 2
                st.rerun()
        with c:
            if st.button("ถัดไป", type="primary", use_container_width=True):
                st.session_state.quote_step = 4
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    elif step == 4:
        st.subheader("4) เลือกรุ่นแอร์")
        products = [
            {"name":"Daikin Inverter 12,000 BTU", "price":12900, "badge":"ประหยัดไฟ", "warranty":"คอมเพรสเซอร์ 5 ปี"},
            {"name":"Mitsubishi 12,000 BTU", "price":13900, "badge":"เงียบพิเศษ", "warranty":"คอมเพรสเซอร์ 5 ปี"},
            {"name":"Carrier X-Inverter 12,200 BTU", "price":13500, "badge":"คุ้มค่า", "warranty":"คอมเพรสเซอร์ 10 ปี"},
        ]
        cols = st.columns(3)
        for i, p in enumerate(products):
            with cols[i]:
                st.markdown(f"""
                <div class="product-card">
                  <span class="badge">{p["badge"]}</span>
                  <h4 style="margin:12px 0 8px 0;">{p["name"]}</h4>
                  <div class="muted">รับประกัน {p["warranty"]}</div>
                  <div class="price">฿ {fmt_baht(p["price"])}</div>
                  <div class="muted" style="margin-top:8px;">พร้อมติดตั้ง • แนะนำสำหรับบ้านพักอาศัย</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("เลือกรุ่นนี้", key=f"pick_{i}", use_container_width=True):
                    st.session_state.selected_model = p["name"]
                    st.session_state.selected_price = p["price"]
                    st.success(f"เลือก {p['name']} แล้ว")
        a, b, c = st.columns(3)
        with a:
            if st.button("ย้อนกลับ", use_container_width=True):
                st.session_state.quote_step = 3
                st.rerun()
        with c:
            if st.button("ไปสรุปราคา", type="primary", use_container_width=True):
                st.session_state.quote_step = 5
                st.rerun()

    elif step == 5:
        model = st.session_state.get("selected_model", "Daikin Inverter 12,000 BTU")
        price = st.session_state.get("selected_price", 12900)
        install = st.number_input("ค่าติดตั้ง", min_value=0, value=3000, step=100)
        extra = st.number_input("ค่าอุปกรณ์เพิ่ม", min_value=0, value=0, step=100)
        discount = st.number_input("ส่วนลด", min_value=0, value=0, step=100)
        total = max(price + install + extra - discount, 0)

        left, right = st.columns([1.5, 1])
        with left:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("5) สรุปรายการ")
            st.text_input("รุ่นที่เลือก", value=model, disabled=True)
            st.number_input("BTU", value=int(st.session_state.get("q_btu", 16000)), disabled=True)
            st.text_area("หมายเหตุเพิ่มเติม", placeholder="เช่น ท่อเพิ่ม, รางครอบ, เบรกเกอร์", key="q_note")
            st.markdown("</div>", unsafe_allow_html=True)

        with right:
            st.markdown(f"""
            <div class="summary-card">
              <div class="section-title" style="margin-top:0;">สรุปยอด</div>
              <div class="muted">ราคาเครื่อง</div>
              <div style="font-weight:700;">฿ {fmt_baht(price)}</div>
              <hr>
              <div class="muted">ค่าติดตั้ง</div>
              <div style="font-weight:700;">฿ {fmt_baht(install)}</div>
              <hr>
              <div class="muted">ค่าอุปกรณ์เพิ่ม</div>
              <div style="font-weight:700;">฿ {fmt_baht(extra)}</div>
              <hr>
              <div class="muted">ส่วนลด</div>
              <div style="font-weight:700;">฿ {fmt_baht(discount)}</div>
              <hr>
              <div class="muted">รวมสุทธิ</div>
              <div style="font-size:2rem;font-weight:800;">฿ {fmt_baht(total)}</div>
            </div>
            """, unsafe_allow_html=True)

        a, b, c = st.columns(3)
        with a:
            if st.button("ย้อนกลับ", use_container_width=True):
                st.session_state.quote_step = 4
                st.rerun()
        with b:
            if st.button("บันทึกร่าง", use_container_width=True):
                st.success("บันทึกร่างแล้ว (เดโม)")
        with c:
            if st.button("ออกใบเสนอราคา", type="primary", use_container_width=True):
                st.success("พร้อมต่อเข้าระบบ PDF/ฐานข้อมูลจริง")

def page_service():
    render_header()
    st.markdown('<div class="section-title">รับงานซ่อม / บริการ</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    a, b = st.columns(2)
    with a:
        st.text_input("ชื่อลูกค้า", key="svc_name")
        st.text_input("เบอร์โทร", key="svc_phone")
        st.selectbox("ประเภทงาน", ["ล้างแอร์", "ซ่อมแอร์", "ติดตั้งใหม่", "ย้ายแอร์"])
    with b:
        st.text_input("วันที่นัด", key="svc_date")
        st.selectbox("สถานะ", ["รับเรื่องแล้ว", "รอนัดหมาย", "กำลังดำเนินการ", "เสร็จสิ้น"])
        st.number_input("ราคาเบื้องต้น", min_value=0, value=500, step=100)
    st.text_area("อาการ / รายละเอียด")
    if st.button("บันทึกงานบริการ", type="primary", use_container_width=True):
        st.success("บันทึกงานบริการแล้ว (เดโม)")
    st.markdown("</div>", unsafe_allow_html=True)

def page_stock():
    render_header()
    st.markdown('<div class="section-title">สต๊อกสินค้า</div>', unsafe_allow_html=True)
    rows = try_table_rows(["stock", "stocks", "inventory", "products"], limit=100)

    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        df = pd.DataFrame([
            ["Daikin 12000 BTU", 4, 12900, "พร้อมขาย"],
            ["Mitsubishi 12000 BTU", 3, 13900, "พร้อมขาย"],
            ["Carrier 12200 BTU", 1, 13500, "ใกล้หมด"],
        ], columns=["รุ่น", "คงเหลือ", "ราคา", "สถานะ"])
        st.dataframe(df, use_container_width=True, hide_index=True)

def page_more():
    render_header()
    st.markdown('<div class="section-title">เมนูเพิ่มเติม</div>', unsafe_allow_html=True)
    a, b = st.columns(2)
    with a:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("ตั้งค่าระบบ")
        st.write("- เชื่อม Supabase")
        st.write("- เชื่อม LINE")
        st.write("- ตั้งค่าร้าน")
        st.write("- เพิ่มสิทธิ์ผู้ใช้")
        st.markdown("</div>", unsafe_allow_html=True)
    with b:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("เกี่ยวกับระบบ")
        st.write(f"**ร้าน:** {STORE_NAME}")
        st.write(f"**เบอร์โทร:** {STORE_PHONE}")
        st.write(f"**เวอร์ชัน:** {APP_VERSION}")
        st.write("**ดีไซน์:** Modern Mobile UI")
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ROUTER
# =========================================================
page = st.session_state.page

if page == "home":
    page_home()
elif page == "dashboard":
    page_dashboard()
elif page == "quote":
    page_quote()
elif page == "service":
    page_service()
elif page == "stock":
    page_stock()
else:
    page_more()

render_bottom_nav()
