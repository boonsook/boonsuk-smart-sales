# 1. ส่วนการบันทึกข้อมูลลูกค้า
    try:
        log_customer_job(quote_data)
        st.success("✅ บันทึกข้อมูลและประวัติงานเรียบร้อยแล้ว!")
    except Exception as e:
        st.error(f"❌ บันทึกข้อมูลไม่สำเร็จ: {e}")

# 2. ส่วนการสร้างและดาวน์โหลด PDF
try:
    pdf_bytes = build_pdf(quote_data)
    c2.download_button(
        label="📄 ดาวน์โหลดใบเสนอราคา (PDF)",
        data=pdf_bytes,
        file_name=f"Quotation_{customer_name or 'Customer'}_{datetime.now().strftime('%Y%m%d')}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
except Exception as e:
    st.info("💡 กรุณาตรวจสอบไฟล์ฟอนต์ THSarabunNew.zip เพื่อเปิดใช้งานระบบ PDF")

st.divider()

# 3. ส่วนการแชร์ข้อมูลผ่าน LINE
st.subheader("📲 ส่งข้อมูลให้ลูกค้า")
line_msg = make_line_message_text(quote_data)
# แสดง Preview ข้อความ
with st.expander("ดูตัวอย่างข้อความที่จะส่ง"):
    st.text(line_msg)

link = line_share_link(line_msg)
st.markdown(
    f'<a href="{link}" target="_blank" style="text-decoration:none;">'
    '<button style="width:100%; background-color:#06C755; color:white; border:none; '
    'padding:12px; border-radius:8px; cursor:pointer; font-weight:bold; font-size:16px;">'
    '🟢 ส่งข้อมูลไปยัง LINE</button></a>',
    unsafe_allow_html=True
)

# 4. Sidebar สำหรับจัดการระบบ (Admin Panel)
with st.sidebar:
    st.header("⚙️ จัดการระบบหลังบ้าน")
    
    # แก้ไขสต๊อกแบบด่วน
    st.subheader("📦 อัปเดตสต๊อกด่วน")
    st.write(f"รุ่น: **{model}**")
    current_stock = int(row.get('stock_qty', 0))
    new_stock = st.number_input("จำนวนสต๊อกใหม่", min_value=0, value=current_stock)
    
    if st.button("บันทึกจำนวนสต๊อก"):
        # อัปเดตใน DataFrame หลัก
        idx = df_all[(df_all['section'] == section) & (df_all['model'] == model)].index
        df_all.loc[idx, 'stock_qty'] = new_stock
        save_stock(df_all)
        st.success("อัปเดตสต๊อกสำเร็จ!")
        st.rerun()

    st.divider()
    
    # ดาวน์โหลดประวัติลูกค้า
    st.subheader("📊 ข้อมูลการขาย")
    if os.path.exists(LOG_CSV):
        df_log_show = pd.read_csv(LOG_CSV)
        st.write(f"บันทึกแล้ว: {len(df_log_show)} รายการ")
        with open(LOG_CSV, "rb") as f:
            st.download_button("📥 Export รายชื่อลูกค้า (CSV)", f, file_name="sales_log.csv", mime="text/csv")
    else:
        st.caption("ยังไม่มีประวัติการบันทึก")
