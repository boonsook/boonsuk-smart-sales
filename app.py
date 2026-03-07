import os
import zipfile
import pandas as pd
import streamlit as st
from datetime import date, datetime
from urllib.parse import quote as urlquote
from fpdf import FPDF

# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="ร้านบุญสุข Smart Sales v4",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded",
)

STORE_NAME  = "ร้านบุญสุขอิเล็กทรอนิกส์"
STORE_PHONE = "086-2613829"
STORE_WEB   = "https://www.facebook.com/boonsukele/"

INSTALL_CONDITIONS = (
    "1) แถมรางครอบท่อน้ำยาให้ฟรี ไม่เกิน 4 เมตร หากเกินคิดเพิ่ม เมตรละ 200 บาท\n"
    "2) แถมท่อน้ำยา ไม่เกิน 4 เมตร หากเกินคิดเพิ่ม เมตรละ 400 บาท\n"
    "3) แถมท่อน้ำทิ้ง ไม่เกิน 10 เมตร หากเกินคิดเพิ่ม เมตรละ 40 บาท\n"
    "4) แถมสายไฟ ไม่เกิน 10 เมตร หากเกินคิดเพิ่ม เมตรละ 40 บาท\n"
    "5) แถมขาแขวนหรือขายาง สำหรับติดตั้งคอยล์ร้อน\n"
    "6) กรณีไม่มีเบรคเกอร์ แถมให้ฟรี\n"
    "7) รับประกันงานตามเงื่อนไขฟรี ตลอดอายุการใช้งาน"
)

DATA_DIR  = "."
STOCK_CSV = os.path.join(DATA_DIR, "boonsuk_stock.csv")
LOG_CSV   = os.path.join(DATA_DIR, "boonsuk_customer_log.csv")

# ──────────────────────────────────────────────
# PRODUCT CATALOGUE
# ──────────────────────────────────────────────
PRODUCTS = [
    # Midea
    {"section":"Midea ฟิกส์speed","model":"Asmg09c","btu":9000,"price_install":19000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Midea ฟิกส์speed","model":"Asmg12j","btu":12000,"price_install":21500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Midea ฟิกส์speed","model":"Asaa18j","btu":18000,"price_install":27500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Midea ฟิกส์speed","model":"Asaa24j","btu":24000,"price_install":37500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Midea ฟิกส์speed","model":"Asaa30j","btu":30000,"price_install":43000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"10 ปี","stock_qty":0},
    # Fujitsu inverter
    {"section":"Fujitsu DC Inverter iPower II R410A","model":"Asmg09jl","btu":8500,"price_install":15500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Fujitsu DC Inverter iPower II R410A","model":"Asmg12jl","btu":11900,"price_install":16500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Fujitsu DC Inverter iPower II R410A","model":"Asaa18jc","btu":17700,"price_install":23500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Fujitsu DC Inverter iPower II R410A","model":"Asaa24jc","btu":24200,"price_install":34500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Fujitsu DC Inverter iPower II R410A","model":"Asaa30cm","btu":27300,"price_install":40000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"10 ปี","stock_qty":0},
    # Fujitsu fix speed
    {"section":"Fujitsu Excellence Fix Speed R32","model":"Asma09r32","btu":9100,"price_install":13800,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Fujitsu Excellence Fix Speed R32","model":"Asma12r32","btu":11500,"price_install":14500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Fujitsu Excellence Fix Speed R32","model":"Asma13r3","btu":13906,"price_install":16700,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Fujitsu Excellence Fix Speed R32","model":"Asma18r410","btu":18745,"price_install":23000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Fujitsu Excellence Fix Speed R32","model":"Asma24r410","btu":24508,"price_install":32000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Fujitsu Excellence Fix Speed R32","model":"Asma30r4","btu":28800,"price_install":35500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"10 ปี","stock_qty":0},
    # Carrier Explorer Inverter
    {"section":"Carrier Explorer Inverter","model":"Tvgs010","btu":9000,"price_install":15800,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Carrier Explorer Inverter","model":"Tvgs013","btu":12000,"price_install":18500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Carrier Explorer Inverter","model":"Tvgs016","btu":15000,"price_install":22500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Carrier Explorer Inverter","model":"Tvgs018","btu":18000,"price_install":26500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Carrier Explorer Inverter","model":"Tvgs024","btu":22000,"price_install":29500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    # Carrier Gemini
    {"section":"Carrier Gemini Inverter","model":"Tvegb010","btu":9000,"price_install":15000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Carrier Gemini Inverter","model":"Tvegb013","btu":12000,"price_install":17000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Carrier Gemini Inverter","model":"Tvegb018","btu":18000,"price_install":23500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Carrier Gemini Inverter","model":"Tvegb024","btu":22000,"price_install":27000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Carrier Gemini Inverter","model":"Tvegb025","btu":24000,"price_install":31500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    # Carrier Astrony
    {"section":"Carrier Astrony R32","model":"AAF010","btu":9000,"price_install":13000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"7 ปี","stock_qty":0},
    {"section":"Carrier Astrony R32","model":"AAF013","btu":12000,"price_install":14000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"7 ปี","stock_qty":0},
    {"section":"Carrier Astrony R32","model":"AAF018","btu":18000,"price_install":20500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"7 ปี","stock_qty":0},
    {"section":"Carrier Astrony R32","model":"AAF025","btu":25000,"price_install":26500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"7 ปี","stock_qty":0},
    # Carrier Everest
    {"section":"Carrier Everest R32","model":"Tsgs010","btu":9000,"price_install":14000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"7 ปี","stock_qty":0},
    {"section":"Carrier Everest R32","model":"Tsgs013","btu":12000,"price_install":15000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"7 ปี","stock_qty":0},
    {"section":"Carrier Everest R32","model":"Tsgs018","btu":18000,"price_install":21000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"7 ปี","stock_qty":0},
    {"section":"Carrier Everest R32","model":"Tsgs025","btu":24000,"price_install":27000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"7 ปี","stock_qty":0},
    # Mitsubishi Heavy Deluxe
    {"section":"Mitsubishi Heavy Duty Deluxe R32","model":"Srk10cvs","btu":9444,"price_install":15500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Deluxe R32","model":"Srk13cvs","btu":12039,"price_install":18000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Deluxe R32","model":"Srk19cvs","btu":19127,"price_install":29000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Deluxe R32","model":"Srk25cvs","btu":25085,"price_install":38800,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    # Mitsubishi Heavy Standard
    {"section":"Mitsubishi Heavy Duty Standard R32","model":"Srk10cvv","btu":9239,"price_install":15000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Standard R32","model":"Srk13cvv","btu":11634,"price_install":17500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Standard R32","model":"Srk15cvv","btu":14457,"price_install":20800,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Standard R32","model":"Srk18cvv","btu":17305,"price_install":25500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    # Mitsubishi Heavy Inverter
    {"section":"Mitsubishi Heavy Duty Standard Inverter R32","model":"Srk10yw","btu":8683,"price_install":16800,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Standard Inverter R32","model":"Srk13yw","btu":11098,"price_install":21000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Standard Inverter R32","model":"Srk15yw","btu":14457,"price_install":24000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Standard Inverter R32","model":"Srk18yw","btu":17276,"price_install":28300,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Standard Inverter R32","model":"Srk24yw","btu":23021,"price_install":38000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    # Gree Fairy
    {"section":"Gree Fairy Series R32","model":"Gwc09acc","btu":9000,"price_install":13500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Fairy Series R32","model":"Gwc12acc","btu":12000,"price_install":14700,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Fairy Series R32","model":"Gwc18acc","btu":18000,"price_install":22500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Fairy Series R32","model":"Gwc24acc","btu":24000,"price_install":26500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    # Gree Amber III
    {"section":"Gree Amber III R32","model":"Gwc09yb3","btu":9000,"price_install":11800,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Amber III R32","model":"Gwc12yc3","btu":12000,"price_install":13500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Amber III R32","model":"Gwc18yc3","btu":18000,"price_install":20500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Amber III R32","model":"Gwc24yc3","btu":24000,"price_install":24000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    # Gree Amber III Inverter
    {"section":"Gree Amber III Inverter R32","model":"Gwc09qb","btu":9000,"price_install":16000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Amber III Inverter R32","model":"Gwc12qb","btu":12000,"price_install":17000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Amber III Inverter R32","model":"Gwc18qb","btu":18000,"price_install":24000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Amber III Inverter R32","model":"Gwc24qb","btu":24000,"price_install":27300,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    # MAVELL ธรรมดา
    {"section":"MAVELL ระบบธรรมดา","model":"MVF-09","btu":9000,"price_install":11500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"12 ปี","stock_qty":0},
    {"section":"MAVELL ระบบธรรมดา","model":"MVF-12","btu":12000,"price_install":13000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"12 ปี","stock_qty":0},
    {"section":"MAVELL ระบบธรรมดา","model":"MVF-18","btu":18000,"price_install":18000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"12 ปี","stock_qty":0},
    {"section":"MAVELL ระบบธรรมดา","model":"MVF-25","btu":24000,"price_install":22500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"12 ปี","stock_qty":0},
    # MAVELL อินเวอร์เตอร์
    {"section":"MAVELL ระบบอินเวอร์เตอร์","model":"MWF-09INV","btu":9000,"price_install":14000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"12 ปี","stock_qty":0},
    {"section":"MAVELL ระบบอินเวอร์เตอร์","model":"MWF-12 INV","btu":12000,"price_install":15000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"12 ปี","stock_qty":0},
    {"section":"MAVELL ระบบอินเวอร์เตอร์","model":"MWF-18 INV","btu":18000,"price_install":19800,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"12 ปี","stock_qty":0},
    {"section":"MAVELL ระบบอินเวอร์เตอร์","model":"MWF-25 INV","btu":24000,"price_install":26000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"12 ปี","stock_qty":0},
    # Daikin SMASH
    {"section":"DAIKIN SMASH (2018)","model":"FTM 09 PV2S","btu":9000,"price_install":14500,"w_install":"1 ปี","w_parts":"1 ปี","w_comp":"3 ปี","stock_qty":0},
    {"section":"DAIKIN SMASH (2018)","model":"FTM 13 PV2S","btu":12000,"price_install":17000,"w_install":"1 ปี","w_parts":"1 ปี","w_comp":"3 ปี","stock_qty":0},
    {"section":"DAIKIN SMASH (2018)","model":"FTM 15 PV2S","btu":15000,"price_install":20000,"w_install":"1 ปี","w_parts":"1 ปี","w_comp":"3 ปี","stock_qty":0},
    {"section":"DAIKIN SMASH (2018)","model":"FTM 18 PV2S","btu":18000,"price_install":25500,"w_install":"1 ปี","w_parts":"1 ปี","w_comp":"3 ปี","stock_qty":0},
    {"section":"DAIKIN SMASH (2018)","model":"FTM 24 PV2S","btu":24000,"price_install":35500,"w_install":"1 ปี","w_parts":"1 ปี","w_comp":"3 ปี","stock_qty":0},
    {"section":"DAIKIN SMASH (2018)","model":"FTM 28 PV2S","btu":28000,"price_install":37000,"w_install":"1 ปี","w_parts":"1 ปี","w_comp":"3 ปี","stock_qty":0},
    # Daikin SABAI
    {"section":"DAIKIN SABAI INVERTER (2019)","model":"FTKQ 09 TV2S","btu":9000,"price_install":15500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"DAIKIN SABAI INVERTER (2019)","model":"FTKQ 13 TV2S","btu":12000,"price_install":18500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"DAIKIN SABAI INVERTER (2019)","model":"FTKQ 15 TV2S","btu":15000,"price_install":21000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"DAIKIN SABAI INVERTER (2019)","model":"FTKQ 18 TV2S","btu":18000,"price_install":27000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"DAIKIN SABAI INVERTER (2019)","model":"FTKQ 24 TV2S","btu":24000,"price_install":37000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    # Daikin SUPER SMILE
    {"section":"DAIKIN SUPER SMILE INVERTER","model":"FTKC 09 TV2S","btu":9000,"price_install":19000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"DAIKIN SUPER SMILE INVERTER","model":"FTKC 13 TV2S","btu":12000,"price_install":21000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"DAIKIN SUPER SMILE INVERTER","model":"FTKC 15 TV2S","btu":18000,"price_install":28500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"DAIKIN SUPER SMILE INVERTER","model":"FTKC 18 TV2S","btu":24000,"price_install":40500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"DAIKIN SUPER SMILE INVERTER","model":"FTKC 24 TV2S","btu":28000,"price_install":43500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    # Mitsubishi Electric Mr.Slim
    {"section":"MITSUBISHI Mr.SLIM","model":"MS-GN 09 VF","btu":9000,"price_install":15500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI Mr.SLIM","model":"MS-GN 13 VF","btu":13000,"price_install":18500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI Mr.SLIM","model":"MS-GN 15 VF","btu":15000,"price_install":22500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI Mr.SLIM","model":"MS-GN 18 VF","btu":18000,"price_install":27000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI Mr.SLIM","model":"MS-GN 24 VF","btu":24000,"price_install":40000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    # Mitsubishi HAPPY INVERTER
    {"section":"MITSUBISHI HAPPY INVERTER","model":"MSY-KP 09 VF","btu":9000,"price_install":16800,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI HAPPY INVERTER","model":"MSY-KP 13 VF","btu":13000,"price_install":19800,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI HAPPY INVERTER","model":"MSY-KP 15 VF","btu":15000,"price_install":23500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI HAPPY INVERTER","model":"MSY-KP 18 VF","btu":18000,"price_install":28500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    # Mitsubishi SLIM INVERTER
    {"section":"MITSUBISHI SLIM INVERTER","model":"MSY-JP 09 VF","btu":9000,"price_install":17700,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI SLIM INVERTER","model":"MSY-JP 13 VF","btu":13000,"price_install":21000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI SLIM INVERTER","model":"MSY-JP 15 VF","btu":15000,"price_install":24500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI SLIM INVERTER","model":"MSY-JP 18 VF","btu":18000,"price_install":28500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI SLIM INVERTER","model":"MSY-JP 24 VF","btu":24000,"price_install":43500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
]

# ──────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────
def fmt_baht(x) -> str:
    try:
        return f"{int(x):,}"
    except Exception:
        return str(x)


def safe_text(value) -> str:
    if value is None:
        return "-"
    return str(value).replace("\r", "").strip() or "-"


def calculate_btu(width: float, length: float, height: float, sun_exposure: str, people: int) -> int:
    base = width * length * 900
    if height > 2.7:
        base *= 1.10
    if sun_exposure == "โดนแดด":
        base *= 1.15
    base += max(0, people - 1) * 600
    return int(round(base))


def suggest_capacity(btu: int) -> int:
    for step in [9000, 12000, 15000, 18000, 22000, 24000, 25000, 28000, 30000]:
        if btu <= step:
            return step
    return 30000


# ──────────────────────────────────────────────
# DATA LAYER
# ──────────────────────────────────────────────
def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    defaults = {"section": "", "model": "", "w_install": "", "w_parts": "", "w_comp": "",
                "btu": 0, "price_install": 0, "stock_qty": 0}
    for col, default in defaults.items():
        if col not in df.columns:
            df[col] = default
    df["section"]       = df["section"].astype(str).str.strip()
    df["model"]         = df["model"].astype(str).str.strip()
    df["btu"]           = pd.to_numeric(df["btu"], errors="coerce").fillna(0).astype(int)
    df["price_install"] = pd.to_numeric(df["price_install"], errors="coerce").fillna(0).astype(int)
    df["stock_qty"]     = pd.to_numeric(df["stock_qty"], errors="coerce").fillna(0).astype(int)
    df = df[(df["btu"] >= 1000) & (df["price_install"] >= 1000)]
    df = df[(df["section"] != "") & (df["model"] != "")]
    return df.copy()


@st.cache_data(ttl=60)
def load_stock() -> pd.DataFrame:
    base = clean_df(pd.DataFrame(PRODUCTS))
    if os.path.exists(STOCK_CSV):
        try:
            saved = clean_df(pd.read_csv(STOCK_CSV, encoding="utf-8-sig"))
            key   = ["section", "model"]
            merged = base.merge(saved[key + ["stock_qty"]], on=key, how="left", suffixes=("", "_s"))
            merged["stock_qty"] = merged["stock_qty_s"].fillna(merged["stock_qty"]).astype(int)
            return merged.drop(columns=["stock_qty_s"])
        except Exception:
            pass
    return base


def save_stock(df: pd.DataFrame):
    cols = ["section", "model", "btu", "price_install", "w_install", "w_parts", "w_comp", "stock_qty"]
    df[cols].to_csv(STOCK_CSV, index=False, encoding="utf-8-sig")
    st.cache_data.clear()


def load_log() -> pd.DataFrame:
    if os.path.exists(LOG_CSV):
        try:
            return pd.read_csv(LOG_CSV, encoding="utf-8-sig")
        except Exception:
            pass
    return pd.DataFrame()


def log_customer_job(quote: dict):
    record = {k: str(v).replace("\n", " | ") if isinstance(v, str) else v for k, v in quote.items()}
    pd.DataFrame([record]).to_csv(
        LOG_CSV, mode="a", header=not os.path.exists(LOG_CSV), index=False, encoding="utf-8-sig"
    )


# ──────────────────────────────────────────────
# PDF BUILDER
# ──────────────────────────────────────────────
def _load_thai_font(pdf: FPDF) -> str:
    os.makedirs("fonts", exist_ok=True)
    zip_path = "THSarabunNew.zip"
    extract_dir = "fonts"
    if os.path.exists(zip_path):
        has_ttf = any(f.lower().endswith(".ttf") for _, _, files in os.walk(extract_dir) for f in files)
        if not has_ttf:
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(extract_dir)
    regular, bold = [], []
    for root, _, files in os.walk(extract_dir):
        for f in files:
            if f.lower().endswith(".ttf") and ("thsarabunnew" in f.lower() or "sarabun" in f.lower()):
                path = os.path.join(root, f)
                (bold if "bold" in f.lower() else regular).append(path)
    if not regular:
        raise FileNotFoundError("ไม่พบฟอนต์ภาษาไทย .ttf")
    pdf.add_font("THSarabun", "",  regular[0], uni=True)
    pdf.add_font("THSarabun", "B", (bold or regular)[0], uni=True)
    return "THSarabun"


def build_pdf(q: dict) -> bytes:
    pdf = FPDF(unit="mm", format="A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=12)
    font = _load_thai_font(pdf)

    # ---- layout constants ----
    PAGE_W = 210
    L = 15          # left margin
    R = 15          # right margin
    CW = PAGE_W - L - R   # = 180 mm content width

    # always reset X to left margin before each row
    def go_left():
        pdf.set_x(L)

    # logo
    logo = os.path.join("assets", "logo.png")
    if os.path.exists(logo):
        try:
            pdf.image(logo, x=L, y=10, w=22)
        except Exception:
            pass

    # ---- header ----
    pdf.set_font(font, "B", 20)
    go_left(); pdf.cell(CW, 8, "ใบเสนอราคา / QUOTATION", ln=1, align="C")
    pdf.set_font(font, "B", 14)
    go_left(); pdf.cell(CW, 7, STORE_NAME, ln=1, align="C")
    pdf.set_font(font, "", 12)
    go_left(); pdf.cell(CW, 6, f"มือถือ/Line: {STORE_PHONE}", ln=1, align="C")
    go_left(); pdf.cell(CW, 6, f"Website: {STORE_WEB}", ln=1, align="C")
    pdf.ln(3)
    pdf.line(L, pdf.get_y(), PAGE_W - R, pdf.get_y())
    pdf.ln(4)

    # ---- date / doc no ----
    doc_no = f"QT-{datetime.today().strftime('%Y%m%d')}"
    go_left()
    pdf.set_font(font, "B", 12); pdf.cell(25, 7, "วันที่")
    pdf.set_font(font, "",  12); pdf.cell(60, 7, safe_text(q["date"]))
    pdf.set_font(font, "B", 12); pdf.cell(35, 7, "เลขที่เอกสาร")
    pdf.set_font(font, "",  12); pdf.cell(CW - 25 - 60 - 35, 7, doc_no, ln=1)

    # ---- helpers ----
    def section_title(t):
        pdf.ln(2)
        go_left()
        pdf.set_font(font, "B", 14)
        pdf.cell(CW, 8, t, ln=1)

    def row(label, value, lw=32):
        go_left()
        pdf.set_font(font, "B", 12)
        pdf.cell(lw, 6, label)
        pdf.set_font(font, "", 12)
        pdf.multi_cell(CW - lw, 6, safe_text(value))

    def money_row(label, value, bold=False):
        go_left()
        pdf.set_font(font, "B" if bold else "", 12)
        lw = 130
        vw = CW - lw          # = 50 mm — always positive since CW=180
        pdf.cell(lw, 7, label)
        pdf.cell(vw, 7, f"{fmt_baht(value)} บาท", ln=1, align="R")

    # ---- customer ----
    section_title("ข้อมูลลูกค้า")
    row("ชื่อลูกค้า", q["customer_name"])
    row("เบอร์โทร",  q["customer_phone"])
    row("ที่อยู่",   q["customer_address"])

    # ---- room ----
    section_title("รายละเอียดห้อง")
    row("ขนาดห้อง",  f"{q['room_w']} x {q['room_l']} เมตร  สูง {q['room_h']} เมตร")
    row("โดนแดด",   q["sun"])
    row("จำนวนคน",  str(q["people"]))
    row("BTU คำนวณ", f"{q['btu']:,} BTU")
    row("ขนาดแนะนำ", f"{q['suggest_cap']:,} BTU")

    # ---- product box ----
    section_title("รายการสินค้า")
    top = pdf.get_y()
    box_h = 42
    pdf.rect(L, top, CW, box_h)
    pdf.set_xy(L + 3, top + 3)
    pdf.set_font(font, "B", 13)
    pdf.multi_cell(CW - 6, 6, safe_text(q["section"]))
    pdf.set_x(L + 3)
    pdf.set_font(font, "", 12)
    pdf.multi_cell(CW - 6, 6, f"Model: {safe_text(q['model'])}   |   BTU: {q['model_btu']:,}")
    pdf.set_x(L + 3)
    pdf.multi_cell(CW - 6, 6,
        f"ประกัน: ติดตั้ง {safe_text(q['w_install'])} / "
        f"อะไหล่ {safe_text(q['w_parts'])} / "
        f"คอมเพรสเซอร์ {safe_text(q['w_comp'])}")
    if pdf.get_y() < top + box_h:
        pdf.set_y(top + box_h)
    else:
        pdf.ln(2)

    # ---- summary box ----
    section_title("สรุปราคา")
    sy = pdf.get_y()
    sum_h = 34
    pdf.rect(L, sy, CW, sum_h)
    pdf.set_xy(L + 4, sy + 4)
    money_row("ราคาพร้อมติดตั้ง", q["base_price"])
    money_row("ส่วนลด",          -int(q["discount"]))
    money_row("ค่าติดตั้งเพิ่ม",  int(q["extra_install"]))
    pdf.line(L + 4, pdf.get_y(), PAGE_W - R - 4, pdf.get_y())
    pdf.ln(2)
    money_row("รวมสุทธิ", q["net_total"], bold=True)
    if pdf.get_y() < sy + sum_h:
        pdf.set_y(sy + sum_h)
    else:
        pdf.ln(2)

    # ---- conditions ----
    section_title("เงื่อนไขการติดตั้ง")
    pdf.set_font(font, "", 11)
    for cline in INSTALL_CONDITIONS.split("\n"):
        if cline.strip():
            go_left()
            pdf.multi_cell(CW, 5.5, cline.strip())

    # ---- signatures ----
    pdf.ln(4)
    pdf.set_font(font, "", 11)
    col = CW // 2 - 3   # ~87 mm each column
    gap = CW - col * 2

    go_left()
    pdf.cell(col, 8, "ลงชื่อผู้เสนอราคา .................................................")
    pdf.cell(gap, 8, "")
    pdf.cell(col, 8, "ลงชื่อผู้รับใบเสนอราคา .................................................", ln=1)

    go_left()
    pdf.cell(col, 8, f"({STORE_NAME})", align="C")
    pdf.cell(gap, 8, "")
    pdf.cell(col, 8, "(..............................................)", ln=1, align="C")

    go_left()
    pdf.cell(col, 8, "วันที่ ........../........../..........", align="C")
    pdf.cell(gap, 8, "")
    pdf.cell(col, 8, "วันที่ ........../........../..........", ln=1, align="C")

    out = pdf.output(dest="S")
    return bytes(out) if isinstance(out, (bytes, bytearray)) else out.encode("latin-1")


def line_share_link(text: str) -> str:
    return "https://line.me/R/msg/text/?" + urlquote(text)


def make_line_text(q: dict) -> str:
    return "\n".join([
        f"ใบเสนอราคา - {STORE_NAME}",
        f"วันที่: {q['date']}",
        f"ลูกค้า: {safe_text(q['customer_name'])}",
        f"โทร: {safe_text(q['customer_phone'])}",
        f"รุ่น: {safe_text(q['model'])}  ({safe_text(q['section'])})",
        f"BTU รุ่น: {q['model_btu']:,} BTU",
        f"ราคาพร้อมติดตั้ง: {fmt_baht(q['base_price'])} บาท",
        f"ส่วนลด: {fmt_baht(q['discount'])} บาท",
        f"ค่าติดตั้งเพิ่ม: {fmt_baht(q['extra_install'])} บาท",
        f"รวมสุทธิ: {fmt_baht(q['net_total'])} บาท",
        "",
        f"ติดต่อร้าน: {STORE_PHONE}",
        STORE_WEB,
    ])


# ──────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stSidebar"] { background: linear-gradient(180deg,#0d47a1 0%,#1565c0 100%); }
[data-testid="stSidebar"] * { color: #fff !important; }
.metric-card {
    background: #f0f4ff; border-radius: 12px; padding: 16px 20px;
    border-left: 5px solid #1565c0; margin-bottom: 10px;
}
.metric-card h4 { margin:0; color:#1565c0; font-size:13px; }
.metric-card h2 { margin:4px 0 0; color:#0d47a1; font-size:26px; font-weight:800; }
.badge-in  { background:#e8f5e9; color:#2e7d32; padding:2px 10px; border-radius:20px; font-weight:700; }
.badge-out { background:#fce4ec; color:#c62828; padding:2px 10px; border-radius:20px; font-weight:700; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────
with st.sidebar:
    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    st.markdown(f"## ❄️ {STORE_NAME}")
    st.markdown(f"📞 **{STORE_PHONE}**")
    st.markdown(f"🌐 [Facebook]({STORE_WEB})")
    st.divider()
    page = st.radio("เมนู", ["🧾 สร้างใบเสนอราคา", "📦 จัดการสต๊อก", "📊 Dashboard / ประวัติ"],
                    label_visibility="collapsed")

df_all = load_stock()

# ══════════════════════════════════════════════
# PAGE 1 : QUOTATION
# ══════════════════════════════════════════════
if page == "🧾 สร้างใบเสนอราคา":
    st.title("🧾 สร้างใบเสนอราคา")

    # ── Step 1: Customer ──────────────────────
    with st.expander("👤 ขั้นตอน 1 — ข้อมูลลูกค้า", expanded=True):
        c1, c2 = st.columns(2)
        customer_name  = c1.text_input("ชื่อลูกค้า")
        customer_phone = c2.text_input("เบอร์โทร")
        customer_address = st.text_area("ที่อยู่/สถานที่ติดตั้ง", height=68)

    # ── Step 2: Room / BTU ───────────────────
    with st.expander("🏠 ขั้นตอน 2 — ขนาดห้องและ BTU", expanded=True):
        c1, c2, c3 = st.columns(3)
        room_w = c1.number_input("กว้าง (เมตร)", min_value=0.0, step=0.1)
        room_l = c2.number_input("ยาว (เมตร)",   min_value=0.0, step=0.1)
        room_h = c3.number_input("สูง (เมตร)",   min_value=0.0, step=0.1, value=2.6)
        c4, c5 = st.columns(2)
        sun    = c4.selectbox("ห้องโดนแดด?", ["ไม่โดนแดด", "โดนแดด"])
        people = c5.number_input("จำนวนคน", min_value=1, step=1, value=1)

        btu = suggest_cap = None
        if room_w > 0 and room_l > 0:
            btu = calculate_btu(room_w, room_l, room_h, sun, int(people))
            suggest_cap = suggest_capacity(btu)
            m1, m2 = st.columns(2)
            m1.metric("BTU ที่คำนวณได้", f"{btu:,} BTU")
            m2.metric("ขนาดแอร์แนะนำ",  f"{suggest_cap:,} BTU")
        else:
            st.info("กรอกขนาดห้องเพื่อคำนวณ BTU")

    # ── Step 3: Product ──────────────────────
    with st.expander("❄️ ขั้นตอน 3 — เลือกรุ่นแอร์", expanded=True):
        q_search = st.text_input("🔍 ค้นหา (รุ่น/ซีรีส์)", placeholder="เช่น Fujitsu, 12000, inverter").strip().lower()
        df_view = df_all.copy()
        if q_search:
            mask = (df_view["section"].str.lower().str.contains(q_search, na=False) |
                    df_view["model"].str.lower().str.contains(q_search, na=False))
            df_view = df_view[mask]

        # filter by BTU range
        if btu and suggest_cap:
            btu_filter = st.checkbox(f"แสดงเฉพาะรุ่น BTU ใกล้เคียง ({suggest_cap:,} BTU)", value=False)
            if btu_filter:
                df_view = df_view[
                    (df_view["btu"] >= suggest_cap * 0.8) &
                    (df_view["btu"] <= suggest_cap * 1.3)
                ]

        sections = sorted(df_view["section"].dropna().unique().tolist())
        if not sections:
            st.warning("ไม่พบสินค้าตามที่ค้นหา")
            st.stop()

        col_s, col_m = st.columns([2, 2])
        section = col_s.selectbox("ซีรีส์/หมวดรุ่น", options=sections)
        df_sec  = df_view[df_view["section"] == section].copy()
        if btu and suggest_cap:
            df_sec["_diff"] = (df_sec["btu"] - suggest_cap).abs()
            df_sec = df_sec.sort_values(["_diff", "price_install"])
        else:
            df_sec = df_sec.sort_values("price_install")

        model = col_m.selectbox("Model", options=df_sec["model"].tolist())
        row   = df_sec[df_sec["model"] == model].iloc[0].to_dict()

        stock_qty = int(row.get("stock_qty", 0))
        badge     = f'<span class="badge-in">มีสต๊อก {stock_qty} เครื่อง</span>' if stock_qty > 0 \
                    else '<span class="badge-out">สต๊อกหมด</span>'

        ca, cb, cc, cd = st.columns(4)
        ca.metric("BTU", f"{int(row['btu']):,}")
        cb.metric("ราคา (พร้อมติดตั้ง)", f"{fmt_baht(row['price_install'])} ฿")
        cc.metric("ประกันคอมฯ", row.get("w_comp", "-"))
        cd.markdown(f"**สต๊อก**<br>{badge}", unsafe_allow_html=True)
        st.caption(f"ประกันติดตั้ง {safe_text(row.get('w_install'))} | ประกันอะไหล่ {safe_text(row.get('w_parts'))}")

    # ── Step 4: Pricing ──────────────────────
    with st.expander("💰 ขั้นตอน 4 — ปรับราคา", expanded=True):
        p1, p2 = st.columns(2)
        discount      = p1.number_input("ส่วนลด (บาท)", min_value=0, step=100, value=0)
        extra_install = p2.number_input("ค่าติดตั้งเพิ่ม (บาท)", min_value=0, step=100, value=0)
        base_price = int(row["price_install"])
        net_total  = max(0, base_price - int(discount) + int(extra_install))

        st.markdown(f"""
        <div class="metric-card">
          <h4>สรุปราคา</h4>
          <h2>฿ {fmt_baht(net_total)}</h2>
          <small>ราคาพร้อมติดตั้ง {fmt_baht(base_price)} | ส่วนลด {fmt_baht(discount)} | ติดตั้งเพิ่ม {fmt_baht(extra_install)}</small>
        </div>
        """, unsafe_allow_html=True)

    # ── Build quote dict ──────────────────────
    today_str  = date.today().strftime("%d/%m/%Y")
    quote_data = dict(
        date=today_str, customer_name=customer_name, customer_phone=customer_phone,
        customer_address=customer_address, room_w=room_w, room_l=room_l, room_h=room_h,
        sun=sun, people=int(people),
        btu=int(btu) if btu else 0, suggest_cap=int(suggest_cap) if suggest_cap else 0,
        section=section, model=model, model_btu=int(row["btu"]),
        w_install=row.get("w_install", ""), w_parts=row.get("w_parts", ""), w_comp=row.get("w_comp", ""),
        base_price=base_price, discount=int(discount), extra_install=int(extra_install), net_total=int(net_total),
    )

    # ── Actions ──────────────────────────────
    st.divider()
    st.subheader("📤 ดำเนินการ")
    a1, a2, a3 = st.columns(3)

    if a1.button("💾 บันทึกงาน", use_container_width=True):
        log_customer_job(quote_data)
        st.success("บันทึกแล้ว ✅")

    if a2.button("📄 สร้าง PDF", use_container_width=True):
        try:
            pdf_bytes = build_pdf(quote_data)
            fname     = f"ใบเสนอราคา_{customer_name or 'ลูกค้า'}_{today_str.replace('/', '-')}.pdf"
            st.success("สร้าง PDF สำเร็จ ✅")
            st.download_button("⬇️ ดาวน์โหลด PDF", data=pdf_bytes, file_name=fname,
                               mime="application/pdf", use_container_width=True)
        except Exception as e:
            st.error(f"สร้าง PDF ไม่สำเร็จ: {e}")

    line_text = make_line_text(quote_data)
    share_url = line_share_link(line_text)
    a3.markdown(f"""
    <a href="{share_url}" target="_blank" style="
        display:block; text-align:center; background:#00c300; color:white;
        padding:10px; border-radius:8px; text-decoration:none; font-weight:700; font-size:15px;">
        💬 ส่ง LINE
    </a>""", unsafe_allow_html=True)

    with st.expander("📝 ดูข้อความ LINE"):
        st.text_area("ข้อความ", value=line_text, height=180)

# ══════════════════════════════════════════════
# PAGE 2 : STOCK MANAGEMENT
# ══════════════════════════════════════════════
elif page == "📦 จัดการสต๊อก":
    st.title("📦 จัดการสต๊อกแอร์")
    st.info("แก้ไขจำนวนสต๊อกในตาราง แล้วกด **บันทึกสต๊อก**")

    edit_cols = ["section", "model", "btu", "price_install", "stock_qty", "w_install", "w_parts", "w_comp"]
    edited = st.data_editor(
        df_all[edit_cols].copy(),
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        column_config={
            "stock_qty":     st.column_config.NumberColumn("สต๊อก",    min_value=0, step=1),
            "price_install": st.column_config.NumberColumn("ราคา (฿)", min_value=0, step=100),
            "btu":           st.column_config.NumberColumn("BTU",       min_value=0, step=100),
        },
    )
    if st.button("✅ บันทึกสต๊อก", use_container_width=True, type="primary"):
        try:
            save_stock(clean_df(edited))
            st.success("บันทึกสต๊อกแล้ว ✅")
        except Exception as e:
            st.error(f"บันทึกไม่สำเร็จ: {e}")

    # low stock alert
    low = df_all[df_all["stock_qty"] == 0]
    if not low.empty:
        st.divider()
        st.warning(f"⚠️ สินค้าสต๊อกหมด {len(low)} รายการ")
        st.dataframe(low[["section", "model", "btu", "price_install"]],
                     use_container_width=True, hide_index=True)

    if os.path.exists(STOCK_CSV):
        with open(STOCK_CSV, "rb") as f:
            st.download_button("⬇️ Export สต๊อก CSV", data=f.read(),
                               file_name="boonsuk_stock.csv", mime="text/csv")

# ══════════════════════════════════════════════
# PAGE 3 : DASHBOARD
# ══════════════════════════════════════════════
elif page == "📊 Dashboard / ประวัติ":
    st.title("📊 Dashboard & ประวัติการขาย")

    df_log = load_log()

    if df_log.empty:
        st.info("ยังไม่มีข้อมูลการบันทึก กรุณาบันทึกงานจากหน้าใบเสนอราคาก่อน")
    else:
        # ensure types
        if "net_total" in df_log.columns:
            df_log["net_total"] = pd.to_numeric(df_log["net_total"], errors="coerce").fillna(0)
        if "date" in df_log.columns:
            df_log["date_parsed"] = pd.to_datetime(df_log["date"], dayfirst=True, errors="coerce")

        total_jobs  = len(df_log)
        total_sales = int(df_log["net_total"].sum()) if "net_total" in df_log.columns else 0
        avg_sale    = int(df_log["net_total"].mean()) if total_jobs else 0

        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<div class="metric-card"><h4>งานทั้งหมด</h4><h2>{total_jobs}</h2></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="metric-card"><h4>ยอดรวม (บาท)</h4><h2>{fmt_baht(total_sales)}</h2></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="metric-card"><h4>เฉลี่ย/งาน (บาท)</h4><h2>{fmt_baht(avg_sale)}</h2></div>', unsafe_allow_html=True)

        st.divider()

        # brand chart
        if "section" in df_log.columns:
            st.subheader("📈 ยอดขายแยกตามซีรีส์")
            brand_df = df_log.groupby("section")["net_total"].sum().reset_index()
            brand_df.columns = ["ซีรีส์", "ยอดรวม (บาท)"]
            brand_df = brand_df.sort_values("ยอดรวม (บาท)", ascending=False).head(15)
            st.bar_chart(brand_df.set_index("ซีรีส์"))

        st.divider()
        st.subheader("🔍 ค้นหาประวัติลูกค้า")
        search_log = st.text_input("ค้นหาชื่อ / เบอร์ / รุ่น").strip().lower()
        show_df = df_log.copy()
        if search_log:
            mask = pd.Series(False, index=show_df.index)
            for col in ["customer_name", "customer_phone", "model", "section"]:
                if col in show_df.columns:
                    mask |= show_df[col].astype(str).str.lower().str.contains(search_log, na=False)
            show_df = show_df[mask]

        st.dataframe(show_df, use_container_width=True, hide_index=True)

        with open(LOG_CSV, "rb") as f:
            st.download_button("⬇️ Export ประวัติ CSV", data=f.read(),
                               file_name="boonsuk_customer_log.csv", mime="text/csv")
