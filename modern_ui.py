import os
from datetime import datetime

import pandas as pd
import streamlit as st

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Boonsuk Smart UI",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------------------------------------
# OPTIONAL SUPABASE
# -------------------------------------------------
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
supabase = None

try:
    if SUPABASE_URL and SUPABASE_KEY:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception:
    supabase = None

# -------------------------------------------------
# STORE INFO
# -------------------------------------------------
STORE_NAME = "บุญสุขอิเล็กทรอนิกส์"
STORE_PHONE = "086-2613829"
STORE_WEB = "https://www.facebook.com/boonsukele/"
APP_VERSION = "Modern UI v2"

# -------------------------------------------------
# STYLE
# -------------------------------------------------
st.markdown("""
<style>
:root{
    --bg: #f4f7fb;
    --card: rgba(255,255,255,0.95);
    --text: #10213a;
    --muted: #6b7a90;
    --line: #e8eef7;
    --primary: linear-gradient(135deg, #0f3d91 0%, #1f66ff 100%);
    --soft-blue: #eaf2ff;
    --soft-green: #eafaf1;
    --soft-orange: #fff3e8;
    --soft-pink: #fff0f5;
    --soft-purple: #f2edff;
    --shadow: 0 10px 30px rgba(15, 61, 145, .10);
    --radius: 22px;
}
.stApp {
    background:
      radial-gradient(circle at top left, rgba(31,102,255,0.08), transparent 22%),
      radial-gradient(circle at top right, rgba(28,203,131,0.07), transparent 20%),
      linear-gradient(180deg, #f7faff 0%, #f4f7fb 100%);
    color: var(--text);
}
.block-container{
    padding-top: 1.1rem;
    padding-bottom: 5.2rem;
    max-width: 1180px;
}
h1,h2,h3{
    color: var(--text);
    letter-spacing: -.02em;
}
.small-muted{
    color: var(--muted);
    font-size: 0.92rem;
}
.hero-card{
    background: var(--primary);
    border-radius: 28px;
    padding: 20px 22px;
    color: #fff;
    box-shadow: 0 18px 40px rgba(15,61,145,.18);
    margin-bottom: 18px;
}
.hero-top{
    display:flex;
    align-items:center;
    gap:14px;
}
.avatar{
    width:64px;
    height:64px;
    min-width:64px;
    border-radius:50%;
    background: rgba(255,255,255,0.20);
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:30px;
    border: 2px solid rgba(255,255,255,0.28);
}
.hero-title{
    font-size: 1.55rem;
    font-weight: 800;
    line-height: 1.15;
}
.hero-sub{
    font-size: .95rem;
    color: rgba(255,255,255,.84);
    margin-top: 3px;
}
.chip-row{
    display:flex;
    gap:10px;
    flex-wrap:wrap;
    margin: 10px 0 18px 0;
}
.chip{
    background:#ffffff;
    border:1px solid var(--line);
    color:#24344d;
    border-radius:999px;
    padding:8px 12px;
    font-size:.92rem;
    box-shadow: 0 6px 18px rgba(16,33,58,.05);
}
.section-title{
    margin: 14px 0 12px 0;
    font-size: 1.28rem;
    font-weight: 800;
}
.kpi-card{
    background: var(--card);
    border: 1px solid rgba(232,238,247,.9);
    border-radius: 24px;
    padding: 18px 18px 16px 18px;
    box-shadow: var(--shadow);
    min-height: 120px;
}
.kpi-top{
    display:flex;
    align-items:center;
    justify-content:space-between;
    margin-bottom:10px;
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
.kpi-label{
    color: var(--muted);
    font-size: 0.95rem;
}
.kpi-value{
    font-size: 2rem;
    font-weight: 800;
    line-height:1.1;
    color: var(--text);
}
.kpi-sub{
    color: var(--muted);
    font-size: 0.88rem;
    margin-top: 6px;
}
.panel{
    background: var(--card);
    border: 1px solid rgba(232,238,247,.95);
    border-radius: 24px;
    padding: 18px;
    box-shadow: var(--shadow);
}
.menu-card{
    text-align:center;
    padding: 18px 10px 8px 10px;
    border-radius: 24px;
    border: 1px solid rgba(232,238,247,.9);
    background: #fff;
    box-shadow: var(--shadow);
    margin-bottom: 10px;
    min-height: 125px;
}
.menu-icon{
    width:62px;
    height:62px;
    border-radius:20px;
    margin: 0 auto 10px auto;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size: 30px;
}
.menu-title{
    font-weight: 700;
    font-size: 1rem;
    color: var(--text);
}
.menu-sub{
    font-size: .82rem;
    color: var(--muted);
    margin-top: 4px;
}
.product-card{
    background:#fff;
    border:1px solid var(--line);
    border-radius:22px;
    padding:16px;
    box-shadow: var(--shadow);
    min-height: 255px;
}
.badge{
    display:inline-block;
    padding: 6px 10px;
    background: #eef4ff;
    color: #1b4fd6;
    border-radius: 999px;
    font-size: .80rem;
    font-weight: 700;
}
.price{
    font-size:1.45rem;
    font-weight:800;
    margin-top:8px;
}
.summary-card{
    background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
    border:1px solid var(--line);
    border-radius:24px;
    padding:18px;
    box-shadow: var(--shadow);
    position: sticky;
    top: 12px;
}
.hr-soft{
    height:1px;
    background: var(--line);
    margin:12px 0;
    border:none;
}
.bottom-nav-wrap{
    position: fixed;
    left: 50%;
    transform: translateX(-50%);
    bottom: 10px;
    width: min(780px, calc(100% - 18px));
    z-index: 99999;
}
.bottom-nav{
    background: rgba(255,255,255,.88);
    backdrop-filter: blur(14px);
    border:1px solid rgba(232,238,247,.95);
    box-shadow: 0 10px 30px rgba(16,33,58,.12);
    border-radius: 24px;
    padding: 8px;
}
div[data-testid="stButton"] > button {
    border-radius: 16px;
    border: 1px solid #dfe7f2;
    min-height: 48px;
    font-weight: 700;
}
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    border-radius: 14px !important;
}
[data-testid="stMetric"]{
    background:#fff;
    border:1px solid var(--line);
    padding:12px;
    border-radius:18px;
}
@media (max-width: 768px){
    .block-container{
        padding-left: 0.85rem;
        padding-right: 0.85rem;
        padding-bottom: 5.4rem;
    }
    .hero-title{ font-size: 1.28rem; }
    .kpi-value{ font-size: 1.55rem; }
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# STATE
# -------------------------------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

if "quote_step" not in st.session_state:
    st.session_state.quote_step = 1

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def fmt_baht(value):
    try:
        return f"{int(float(value)):,}"
    except Exception:
        return "0"

def goto(page_name: str):
    st.session_state.page = page_name

def load_dashboard_data():
    """
    ถ้ามี Supabase จะลองอ่านข้อมูลจริง
    ถ้าไม่มี จะใช้ค่าทดลอง
    """
    demo = {
        "sales_today": 21000,
        "stock_count": 98,
        "quote_count": 5,
        "service_count": 2,
        "recent_customers": [
            {"name": "คุณสมชาย", "phone": "08x-xxx-1122", "job": "ใบเสนอราคา"},
            {"name": "คุณนิดา", "phone": "09x-xxx-9988", "job": "แจ้งซ่อม"},
            {"name": "คุณวรพล", "phone": "08x-xxx-4455", "job": "ติดตั้งใหม่"},
        ]
    }

    if not supabase:
        return demo

    try:
        data = demo.copy()

        # ปรับชื่อ table ภายหลังได้ตามของจริง
        quotes = supabase.table("quotes").select("*").limit(200).execute()
        services = supabase.table("service_jobs").select("*").limit(200).execute()
        customers = supabase.table("customers").select("*").limit(20).execute()
        stock = supabase.table("stock").select("*").limit(500).execute()

        data["quote_count"] = len(quotes.data or [])
        data["service_count"] = len(services.data or [])
        data["stock_count"] = len(stock.data or [])

        # ลองรวมยอดจาก quotes
        total = 0
        for row in (quotes.data or []):
            v = row.get("net_total") or row.get("total") or row.get("price") or 0
            try:
                total += float(v)
            except Exception:
                pass
        data["sales_today"] = int(total) if total > 0 else demo["sales_today"]

        rc = []
        for c in (customers.data or [])[:3]:
            rc.append({
                "name": c.get("name") or c.get("customer_name") or "ลูกค้า",
                "phone": c.get("phone") or c.get("customer_phone") or "-",
                "job": c.get("note") or "ลูกค้าในระบบ"
            })
        if rc:
            data["recent_customers"] = rc

        return data
    except Exception:
        return demo

def kpi_card(icon, label, value, sub, bg):
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

def menu_tile(title, subtitle, icon, color, key, page_target):
    st.markdown(f"""
    <div class="menu-card">
        <div class="menu-icon" style="background:{color};">{icon}</div>
        <div class="menu-title">{title}</div>
        <div class="menu-sub">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(f"เปิด{title}", key=key, use_container_width=True):
        goto(page_target)
        st.rerun()

def render_header():
    now_txt = datetime.now().strftime("%d/%m/%Y %H:%M")
    st.markdown(f"""
    <div class="hero-card">
        <div class="hero-top">
            <div class="avatar">❄️</div>
            <div>
                <div class="hero-title">{STORE_NAME}</div>
                <div class="hero-sub">Smart Sales Platform • {APP_VERSION}</div>
                <div class="hero-sub">อัปเดตล่าสุด {now_txt}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_status_chips(data):
    st.markdown(f"""
    <div class="chip-row">
        <div class="chip">💰 ยอดรวม {fmt_baht(data['sales_today'])} บาท</div>
        <div class="chip">📦 สต๊อก {data['stock_count']} รายการ</div>
        <div class="chip">🧾 ใบเสนอราคา {data['quote_count']} งาน</div>
        <div class="chip">🛠️ งานบริการ {data['service_count']} งาน</div>
    </div>
    """, unsafe_allow_html=True)

def quote_product_cards():
    products = [
        {"name": "Daikin Inverter 12,000 BTU", "price": 12900, "badge": "ประหยัดไฟ", "warranty": "คอมเพรสเซอร์ 5 ปี"},
        {"name": "Mitsubishi 12,000 BTU", "price": 13900, "badge": "เงียบพิเศษ", "warranty": "คอมเพรสเซอร์ 5 ปี"},
        {"name": "Carrier X-Inverter 12,200 BTU", "price": 13500, "badge": "คุ้มค่า", "warranty": "คอมเพรสเซอร์ 10 ปี"},
    ]

    cols = st.columns(3)
    for i, p in enumerate(products):
        with cols[i]:
            st.markdown(f"""
            <div class="product-card">
                <span class="badge">{p['badge']}</span>
                <h4 style="margin:12px 0 8px 0;">{p['name']}</h4>
                <div class="small-muted">รับประกัน {p['warranty']}</div>
                <div class="price">฿ {fmt_baht(p['price'])}</div>
                <div class="small-muted" style="margin-top:8px;">พร้อมติดตั้ง • แนะนำสำหรับบ้านพักอาศัย</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("เลือกรุ่นนี้", key=f"pick_{i}", use_container_width=True):
                st.session_state.selected_model = p["name"]
                st.session_state.selected_price = p["price"]
                st.success(f"เลือกรุ่น {p['name']} แล้ว")

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
        if st.button("📊 Dashboard", use_container_width=True):
            goto("dashboard")
            st.rerun()
    with c5:
        if st.button("⚙️ More", use_container_width=True):
            goto("more")
            st.rerun()
    st.markdown("</div></div>", unsafe_allow_html=True)

# -------------------------------------------------
# PAGES
# -------------------------------------------------
def page_home():
    data = load_dashboard_data()
    render_header()
    render_status_chips(data)

    st.markdown('<div class="section-title">ภาพรวมวันนี้</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("💰", "ยอดขายรวม", fmt_baht(data["sales_today"]), "สรุปจากรายการขาย/ใบเสนอราคา", "#fff3e8")
    with c2:
        kpi_card("📦", "สินค้าในสต๊อก", str(data["stock_count"]), "พร้อมขายและพร้อมติดตั้ง", "#eafaf1")
    with c3:
        kpi_card("🧾", "ใบเสนอราคา", str(data["quote_count"]), "จำนวนเอกสารที่อยู่ในระบบ", "#eaf2ff")
    with c4:
        kpi_card("🛠️", "งานบริการ", str(data["service_count"]), "งานซ่อมและนัดบริการ", "#fff0f5")

    st.markdown('<div class="section-title">เมนูหลัก</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        menu_tile("ใบเสนอราคา", "สร้างเอกสารใหม่", "🧾", "#eaf2ff", "menu_quote", "quote")
    with m2:
        menu_tile("รับงานซ่อม", "แจ้งงานบริการ", "🛠️", "#fff0f5", "menu_service", "service")
    with m3:
        menu_tile("Dashboard", "ดูภาพรวมยอดขาย", "📊", "#f2edff", "menu_dash", "dashboard")
    with m4:
        menu_tile("สต๊อกสินค้า", "ตรวจรายการคงเหลือ", "📦", "#fff3e8", "menu_stock", "stock")

    st.markdown('<div class="section-title">ลูกค้าล่าสุด</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    for row in data["recent_customers"]:
        c1, c2, c3 = st.columns([3, 2, 2])
        with c1:
            st.write(f"**{row['name']}**")
        with c2:
            st.write(row["phone"])
        with c3:
            st.write(row["job"])
        st.divider()
    st.markdown('</div>', unsafe_allow_html=True)

def page_dashboard():
    data = load_dashboard_data()
    render_header()
    st.markdown('<div class="section-title">Dashboard</div>', unsafe_allow_html=True)

    r1, r2, r3 = st.columns([1.2, 1.2, 1])
    with r1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("ยอดขาย")
        st.metric("ยอดขายรวม", f"฿ {fmt_baht(data['sales_today'])}")
        st.metric("ใบเสนอราคา", data["quote_count"])
        st.metric("งานบริการ", data["service_count"])
        st.markdown('</div>', unsafe_allow_html=True)

    with r2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("สต๊อก")
        st.metric("จำนวนสินค้า", data["stock_count"])
        st.progress(min(data["stock_count"] / 120, 1.0))
        st.caption("แถบนี้ใช้ demo ก่อน ถ้าต่อกับ stock จริงจะเปลี่ยนเป็น % คงเหลือได้")
        st.markdown('</div>', unsafe_allow_html=True)

    with r3:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("ร้าน")
        st.write(f"**โทร:** {STORE_PHONE}")
        st.write(f"**เพจ:** {STORE_WEB}")
        st.write(f"**เวอร์ชัน:** {APP_VERSION}")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">รายงานย่อ</div>', unsafe_allow_html=True)
    df = pd.DataFrame({
        "หมวด": ["ใบเสนอราคา", "งานบริการ", "สินค้าในสต๊อก"],
        "จำนวน": [data["quote_count"], data["service_count"], data["stock_count"]]
    })
    st.bar_chart(df.set_index("หมวด"))

def page_quote():
    render_header()
    st.markdown('<div class="section-title">สร้างใบเสนอราคาแบบ Wizard</div>', unsafe_allow_html=True)

    step = st.session_state.quote_step
    progress = {1: 0.2, 2: 0.4, 3: 0.6, 4: 0.8, 5: 1.0}
    st.progress(progress.get(step, 0.2))
    st.caption(f"ขั้นตอน {step}/5")

    if step == 1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("1) ข้อมูลลูกค้า")
        st.text_input("ชื่อลูกค้า", key="q_customer_name")
        st.text_input("เบอร์โทร", key="q_customer_phone")
        st.text_area("ที่อยู่ติดตั้ง", key="q_customer_address")
        c1, c2 = st.columns([1, 1])
        with c2:
            if st.button("ถัดไป", type="primary", use_container_width=True):
                st.session_state.quote_step = 2
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    elif step == 2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("2) ขนาดห้อง")
        room_size = st.number_input("ขนาดห้อง (ตร.ม.)", min_value=1, value=20, step=1, key="q_room_size")
        usage = st.selectbox("ลักษณะการใช้งาน", ["ห้องนอน", "ห้องนั่งเล่น", "สำนักงาน", "ร้านค้า"], key="q_room_type")
        st.info(f"เลือก: {usage}")
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            if st.button("ย้อนกลับ", use_container_width=True):
                st.session_state.quote_step = 1
                st.rerun()
        with c3:
            if st.button("ถัดไป", type="primary", use_container_width=True):
                st.session_state.quote_step = 3
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    elif step == 3:
        room_size = st.session_state.get("q_room_size", 20)
        btu = room_size * 800
        st.session_state.q_btu = btu

        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("3) คำนวณ BTU")
        st.success(f"BTU ที่แนะนำ: {int(btu):,}")
        st.caption("สูตรทดลอง: ขนาดห้อง x 800")
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            if st.button("ย้อนกลับ", use_container_width=True):
                st.session_state.quote_step = 2
                st.rerun()
        with c3:
            if st.button("ถัดไป", type="primary", use_container_width=True):
                st.session_state.quote_step = 4
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    elif step == 4:
        st.subheader("4) เลือกรุ่นแอร์")
        quote_product_cards()
        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            if st.button("ย้อนกลับ", use_container_width=True):
                st.session_state.quote_step = 3
                st.rerun()
        with c3:
            if st.button("ไปสรุปราคา", type="primary", use_container_width=True):
                st.session_state.quote_step = 5
                st.rerun()

    elif step == 5:
        price = st.session_state.get("selected_price", 12900)
        model = st.session_state.get("selected_model", "Daikin Inverter 12,000 BTU")
        install = st.number_input("ค่าติดตั้ง", min_value=0, value=3000, step=100, key="q_install")
        discount = st.number_input("ส่วนลด", min_value=0, value=0, step=100, key="q_discount")
        total = max(price + install - discount, 0)

        left, right = st.columns([1.55, 1])
        with left:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.subheader("5) สรุปราคา")
            st.text_input("รุ่นที่เลือก", value=model, disabled=True)
            st.number_input("BTU", value=int(st.session_state.get("q_btu", 16000)), disabled=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            st.markdown(f"""
            <div class="summary-card">
                <div class="section-title" style="margin-top:0;">สรุปยอด</div>
                <div class="small-muted">ราคาเครื่อง</div>
                <div style="font-weight:700;">฿ {fmt_baht(price)}</div>
                <div class="hr-soft"></div>
                <div class="small-muted">ค่าติดตั้ง</div>
                <div style="font-weight:700;">฿ {fmt_baht(install)}</div>
                <div class="hr-soft"></div>
                <div class="small-muted">ส่วนลด</div>
                <div style="font-weight:700;">฿ {fmt_baht(discount)}</div>
                <div class="hr-soft"></div>
                <div class="small-muted">รวมสุทธิ</div>
                <div style="font-size:2rem;font-weight:800;">฿ {fmt_baht(total)}</div>
            </div>
            """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns([1, 1, 1])
        with c1:
            if st.button("ย้อนกลับ", use_container_width=True):
                st.session_state.quote_step = 4
                st.rerun()
        with c2:
            if st.button("บันทึกร่าง", use_container_width=True):
                st.success("บันทึกร่างแล้ว (เดโม)")
        with c3:
            if st.button("ออกใบเสนอราคา", type="primary", use_container_width=True):
                st.success("พร้อมต่อเข้าระบบ PDF/บันทึกฐานข้อมูลในขั้นถัดไป")

def page_service():
    render_header()
    st.markdown('<div class="section-title">รับงานซ่อม / บริการ</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("ชื่อลูกค้า", key="svc_name")
        st.text_input("เบอร์โทร", key="svc_phone")
        st.selectbox("ประเภทงาน", ["ล้างแอร์", "ซ่อมแอร์", "ติดตั้งใหม่", "ย้ายแอร์"], key="svc_type")
    with c2:
        st.text_input("วันที่นัด", key="svc_date")
        st.selectbox("สถานะ", ["รับเรื่องแล้ว", "รอนัดหมาย", "กำลังดำเนินการ", "เสร็จสิ้น"], key="svc_status")
        st.number_input("ราคาเบื้องต้น", min_value=0, value=500, step=100, key="svc_price")
    st.text_area("อาการ / รายละเอียด", key="svc_note")
    if st.button("บันทึกงานบริการ", type="primary", use_container_width=True):
        st.success("บันทึกงานบริการแล้ว (เดโม)")
    st.markdown('</div>', unsafe_allow_html=True)

def page_stock():
    render_header()
    st.markdown('<div class="section-title">สต๊อกสินค้า</div>', unsafe_allow_html=True)
    df = pd.DataFrame([
        ["Daikin 12000 BTU", 4, 12900, "พร้อมขาย"],
        ["Mitsubishi 12000 BTU", 3, 13900, "พร้อมขาย"],
        ["Carrier 12200 BTU", 1, 13500, "ใกล้หมด"],
    ], columns=["รุ่น", "คงเหลือ", "ราคา", "สถานะ"])
    st.dataframe(df, use_container_width=True, hide_index=True)

def page_more():
    render_header()
    st.markdown('<div class="section-title">เมนูเพิ่มเติม</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("ตั้งค่าระบบ")
        st.write("- เชื่อม Supabase")
        st.write("- เชื่อม LINE")
        st.write("- ตั้งค่าร้าน")
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("เกี่ยวกับ")
        st.write(f"ร้าน: {STORE_NAME}")
        st.write(f"เบอร์โทร: {STORE_PHONE}")
        st.write(f"เวอร์ชัน: {APP_VERSION}")
        st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# ROUTER
# -------------------------------------------------
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
