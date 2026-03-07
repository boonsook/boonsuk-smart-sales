import os
import zipfile
import pandas as pd
import streamlit as st
from datetime import date, datetime
from urllib.parse import quote as urlquote
from fpdf import FPDF

st.set_page_config(page_title="Boonsuk Smart Sales PRO v3", layout="centered")

STORE_NAME = "ร้านบุญสุขอิเล็กทรอนิกส์"
STORE_PHONE = "086-2613829"
STORE_WEB = "https://www.facebook.com/boonsukele/"

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

    # Carrier explorer inverter
    {"section":"Carrier Explorer Inverter","model":"Tvgs010","btu":9000,"price_install":15800,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Carrier Explorer Inverter","model":"Tvgs013","btu":12000,"price_install":18500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Carrier Explorer Inverter","model":"Tvgs016","btu":15000,"price_install":22500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Carrier Explorer Inverter","model":"Tvgs018","btu":18000,"price_install":26500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Carrier Explorer Inverter","model":"Tvgs024","btu":22000,"price_install":29500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},

    # Carrier Gemini inverter
    {"section":"Carrier Gemini Inverter","model":"Tvegb010","btu":9000,"price_install":15000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Carrier Gemini Inverter","model":"Tvegb013","btu":12000,"price_install":17000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Carrier Gemini Inverter","model":"Tvegb018","btu":18000,"price_install":23500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Carrier Gemini Inverter","model":"Tvegb024","btu":22000,"price_install":27000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Carrier Gemini Inverter","model":"Tvegb025","btu":24000,"price_install":31500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},

    # Carrier fixed speed
    {"section":"Carrier Astrony R32","model":"AAF010","btu":9000,"price_install":13000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"7 ปี","stock_qty":0},
    {"section":"Carrier Astrony R32","model":"AAF013","btu":12000,"price_install":14000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"7 ปี","stock_qty":0},
    {"section":"Carrier Astrony R32","model":"AAF018","btu":18000,"price_install":20500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"7 ปี","stock_qty":0},
    {"section":"Carrier Astrony R32","model":"AAF025","btu":25000,"price_install":26500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"7 ปี","stock_qty":0},
    {"section":"Carrier Everest R32","model":"Tsgs010","btu":9000,"price_install":14000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"7 ปี","stock_qty":0},
    {"section":"Carrier Everest R32","model":"Tsgs013","btu":12000,"price_install":15000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"7 ปี","stock_qty":0},
    {"section":"Carrier Everest R32","model":"Tsgs018","btu":18000,"price_install":21000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"7 ปี","stock_qty":0},
    {"section":"Carrier Everest R32","model":"Tsgs025","btu":24000,"price_install":27000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"7 ปี","stock_qty":0},

    # Mitsubishi Heavy Duty
    {"section":"Mitsubishi Heavy Duty Deluxe R32","model":"Srk10cvs","btu":9444,"price_install":15500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Deluxe R32","model":"Srk13cvs","btu":12039,"price_install":18000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Deluxe R32","model":"Srk19cvs","btu":19127,"price_install":29000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Deluxe R32","model":"Srk25cvs","btu":25085,"price_install":38800,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Standard R32","model":"Srk10cvv","btu":9239,"price_install":15000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Standard R32","model":"Srk13cvv","btu":11634,"price_install":17500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Standard R32","model":"Srk15cvv","btu":14457,"price_install":20800,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Standard R32","model":"Srk18cvv","btu":17305,"price_install":25500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Standard Inverter R32","model":"Srk10yw","btu":8683,"price_install":16800,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Standard Inverter R32","model":"Srk13yw","btu":11098,"price_install":21000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Standard Inverter R32","model":"Srk15yw","btu":14457,"price_install":24000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Standard Inverter R32","model":"Srk18yw","btu":17276,"price_install":28300,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"Mitsubishi Heavy Duty Standard Inverter R32","model":"Srk24yw","btu":23021,"price_install":38000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"5 ปี","stock_qty":0},

    # Gree
    {"section":"Gree Fairy Series R32","model":"Gwc09acc","btu":9000,"price_install":13500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Fairy Series R32","model":"Gwc12acc","btu":12000,"price_install":14700,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Fairy Series R32","model":"Gwc18acc","btu":18000,"price_install":22500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Fairy Series R32","model":"Gwc24acc","btu":24000,"price_install":26500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Amber III R32","model":"Gwc09yb3","btu":9000,"price_install":11800,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Amber III R32","model":"Gwc12yc3","btu":12000,"price_install":13500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Amber III R32","model":"Gwc18yc3","btu":18000,"price_install":20500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Amber III R32","model":"Gwc24yc3","btu":24000,"price_install":24000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Amber III Inverter R32","model":"Gwc09qb","btu":9000,"price_install":16000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Amber III Inverter R32","model":"Gwc12qb","btu":12000,"price_install":17000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Amber III Inverter R32","model":"Gwc18qb","btu":18000,"price_install":24000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},
    {"section":"Gree Amber III Inverter R32","model":"Gwc24qb","btu":24000,"price_install":27300,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"10 ปี","stock_qty":0},

    # MAVELL
    {"section":"MAVELL ระบบธรรมดา","model":"MVF-09","btu":9000,"price_install":11500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"12 ปี","stock_qty":0},
    {"section":"MAVELL ระบบธรรมดา","model":"MVF-12","btu":12000,"price_install":13000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"12 ปี","stock_qty":0},
    {"section":"MAVELL ระบบธรรมดา","model":"MVF-18","btu":18000,"price_install":18000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"12 ปี","stock_qty":0},
    {"section":"MAVELL ระบบธรรมดา","model":"MVF-25","btu":24000,"price_install":22500,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"12 ปี","stock_qty":0},
    {"section":"MAVELL ระบบอินเวอร์เตอร์","model":"MWF-09INV","btu":9000,"price_install":14000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"12 ปี","stock_qty":0},
    {"section":"MAVELL ระบบอินเวอร์เตอร์","model":"MWF-12 INV","btu":12000,"price_install":15000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"12 ปี","stock_qty":0},
    {"section":"MAVELL ระบบอินเวอร์เตอร์","model":"MWF-18 INV","btu":18000,"price_install":19800,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"12 ปี","stock_qty":0},
    {"section":"MAVELL ระบบอินเวอร์เตอร์","model":"MWF-25 INV","btu":24000,"price_install":26000,"w_install":"1 ปี","w_parts":"5 ปี","w_comp":"12 ปี","stock_qty":0},

    # Daikin
    {"section":"DAIKIN SMASH (2018)","model":"FTM 09 PV2S","btu":9000,"price_install":14500,"w_install":"1 ปี","w_parts":"1 ปี","w_comp":"3 ปี","stock_qty":0},
    {"section":"DAIKIN SMASH (2018)","model":"FTM 13 PV2S","btu":12000,"price_install":17000,"w_install":"1 ปี","w_parts":"1 ปี","w_comp":"3 ปี","stock_qty":0},
    {"section":"DAIKIN SMASH (2018)","model":"FTM 15 PV2S","btu":15000,"price_install":20000,"w_install":"1 ปี","w_parts":"1 ปี","w_comp":"3 ปี","stock_qty":0},
    {"section":"DAIKIN SMASH (2018)","model":"FTM 18 PV2S","btu":18000,"price_install":25500,"w_install":"1 ปี","w_parts":"1 ปี","w_comp":"3 ปี","stock_qty":0},
    {"section":"DAIKIN SMASH (2018)","model":"FTM 24 PV2S","btu":24000,"price_install":35500,"w_install":"1 ปี","w_parts":"1 ปี","w_comp":"3 ปี","stock_qty":0},
    {"section":"DAIKIN SMASH (2018)","model":"FTM 28 PV2S","btu":28000,"price_install":37000,"w_install":"1 ปี","w_parts":"1 ปี","w_comp":"3 ปี","stock_qty":0},
    {"section":"DAIKIN SABAI INVERTER (2019)","model":"FTKQ 09 TV2S","btu":9000,"price_install":15500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"DAIKIN SABAI INVERTER (2019)","model":"FTKQ 13 TV2S","btu":12000,"price_install":18500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"DAIKIN SABAI INVERTER (2019)","model":"FTKQ 15 TV2S","btu":15000,"price_install":21000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"DAIKIN SABAI INVERTER (2019)","model":"FTKQ 18 TV2S","btu":18000,"price_install":27000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"DAIKIN SABAI INVERTER (2019)","model":"FTKQ 24 TV2S","btu":24000,"price_install":37000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"DAIKIN SUPER SMILE INVERTER","model":"FTKC 09 TV2S","btu":9000,"price_install":19000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"DAIKIN SUPER SMILE INVERTER","model":"FTKC 13 TV2S","btu":12000,"price_install":21000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"DAIKIN SUPER SMILE INVERTER","model":"FTKC 15 TV2S","btu":18000,"price_install":28500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"DAIKIN SUPER SMILE INVERTER","model":"FTKC 18 TV2S","btu":24000,"price_install":40500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"DAIKIN SUPER SMILE INVERTER","model":"FTKC 24 TV2S","btu":28000,"price_install":43500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},

    # Mitsubishi Electric
    {"section":"MITSUBISHI Mr.SLIM","model":"MS-GN 09 VF","btu":9000,"price_install":15500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI Mr.SLIM","model":"MS-GN 13 VF","btu":13000,"price_install":18500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI Mr.SLIM","model":"MS-GN 15 VF","btu":15000,"price_install":22500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI Mr.SLIM","model":"MS-GN 18 VF","btu":18000,"price_install":27000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI Mr.SLIM","model":"MS-GN 24 VF","btu":24000,"price_install":40000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI HAPPY INVERTER","model":"MSY-KP 09 VF","btu":9000,"price_install":16800,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI HAPPY INVERTER","model":"MSY-KP 13 VF","btu":13000,"price_install":19800,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI HAPPY INVERTER","model":"MSY-KP 15 VF","btu":15000,"price_install":23500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI HAPPY INVERTER","model":"MSY-KP 18 VF","btu":18000,"price_install":28500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI SLIM INVERTER","model":"MSY-JP 09 VF","btu":9000,"price_install":17700,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI SLIM INVERTER","model":"MSY-JP 13 VF","btu":13000,"price_install":21000,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI SLIM INVERTER","model":"MSY-JP 15 VF","btu":15000,"price_install":24500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI SLIM INVERTER","model":"MSY-JP 18 VF","btu":18000,"price_install":28500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
    {"section":"MITSUBISHI SLIM INVERTER","model":"MSY-JP 24 VF","btu":24000,"price_install":43500,"w_install":"1 ปี","w_parts":"3 ปี","w_comp":"5 ปี","stock_qty":0},
]


def format_baht(x) -> str:
    try:
        return f"{int(x):,}"
    except Exception:
        return str(x)


def safe_text(value):
    if value is None:
        return "-"
    return str(value).replace("\r", "").strip() or "-"


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
    need_cols = ["section", "model", "btu", "price_install", "w_install", "w_parts", "w_comp", "stock_qty"]
    for c in need_cols:
        if c not in df.columns:
            df[c] = "" if c in ["section", "model", "w_install", "w_parts", "w_comp"] else 0

    df["section"] = df["section"].astype(str).str.strip()
    df["model"] = df["model"].astype(str).str.strip()
    df["btu"] = pd.to_numeric(df["btu"], errors="coerce").fillna(0).astype(int)
    df["price_install"] = pd.to_numeric(df["price_install"], errors="coerce").fillna(0).astype(int)
    df["stock_qty"] = pd.to_numeric(df["stock_qty"], errors="coerce").fillna(0).astype(int)

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
            key = ["section", "model"]
            merged = base.merge(stock[key + ["stock_qty"]], on=key, how="left", suffixes=("", "_stock"))
            merged["stock_qty"] = merged["stock_qty_stock"].fillna(merged["stock_qty"]).astype(int)
            merged = merged.drop(columns=["stock_qty_stock"])
            return merged
        except Exception:
            return base

    return base


def save_stock(df: pd.DataFrame):
    df_out = df.copy()
    df_out = df_out[["section", "model", "btu", "price_install", "w_install", "w_parts", "w_comp", "stock_qty"]].copy()
    df_out.to_csv(STOCK_CSV, index=False, encoding="utf-8-sig")


def _load_thai_font(pdf: FPDF) -> str:
    os.makedirs("fonts", exist_ok=True)
    zip_path = "THSarabunNew.zip"
    extract_dir = "fonts"

    if os.path.exists(zip_path):
        has_ttf = False
        for root, _, files in os.walk(extract_dir):
            for f in files:
                if f.lower().endswith(".ttf"):
                    has_ttf = True
                    break
            if has_ttf:
                break
        if not has_ttf:
            with zipfile.ZipFile(zip_path, "r") as z:
                z.extractall(extract_dir)

    regular_candidates = []
    bold_candidates = []
    for root, _, files in os.walk(extract_dir):
        for f in files:
            full_path = os.path.join(root, f)
            low = f.lower()
            if low.endswith(".ttf"):
                if ("thsarabunnew" in low or "sarabun" in low) and "bold" not in low:
                    regular_candidates.append(full_path)
                if ("thsarabunnew" in low or "sarabun" in low) and "bold" in low:
                    bold_candidates.append(full_path)

    if not regular_candidates:
        raise FileNotFoundError("ไม่พบไฟล์ฟอนต์ภาษาไทย .ttf ใน THSarabunNew.zip")

    font_regular = regular_candidates[0]
    font_bold = bold_candidates[0] if bold_candidates else font_regular

    pdf.add_font("THSarabun", "", font_regular, uni=True)
    pdf.add_font("THSarabun", "B", font_bold, uni=True)
    return "THSarabun"


def draw_wrapped_block(pdf, font, title, value, x, label_w, y, full_w):
    pdf.set_xy(x, y)
    pdf.set_font(font, "B", 12)
    pdf.cell(label_w, 6, title, border=0)
    pdf.set_font(font, "", 12)
    current_x = pdf.get_x()
    current_y = pdf.get_y()
    available_w = full_w - label_w
    pdf.set_xy(current_x, current_y)
    pdf.multi_cell(available_w, 6, safe_text(value))
    return pdf.get_y()


def build_pdf(quote: dict) -> bytes:
    pdf = FPDF(unit="mm", format="A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=12)

    font = _load_thai_font(pdf)
    page_w = 210
    left = 12
    right = 12
    content_w = page_w - left - right

    def section_title(text):
        pdf.ln(2)
        pdf.set_font(font, "B", 15)
        pdf.cell(0, 8, text, ln=1)

    def money_line(label, value, bold=False):
        pdf.set_font(font, "B" if bold else "", 12)
        pdf.cell(120, 7, label, border=0)
        pdf.cell(0, 7, f"{format_baht(value)} บาท", ln=1, align="R")

    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        try:
            pdf.image(logo_path, x=12, y=10, w=24)
        except Exception:
            pass

    pdf.set_font(font, "B", 20)
    pdf.cell(0, 8, "ใบเสนอราคา / QUOTATION", ln=1, align="C")
    pdf.set_font(font, "B", 14)
    pdf.cell(0, 7, STORE_NAME, ln=1, align="C")
    pdf.set_font(font, "", 12)
    pdf.cell(0, 6, f"มือถือ/Line: {STORE_PHONE}", ln=1, align="C")
    pdf.cell(0, 6, f"Website: {STORE_WEB}", ln=1, align="C")

    pdf.ln(3)
    pdf.line(left, pdf.get_y(), page_w - right, pdf.get_y())
    pdf.ln(4)

    pdf.set_font(font, "B", 12)
    pdf.cell(28, 7, "วันที่", border=0)
    pdf.set_font(font, "", 12)
    pdf.cell(62, 7, safe_text(quote["date"]), border=0)
    pdf.set_font(font, "B", 12)
    pdf.cell(30, 7, "เลขที่เอกสาร", border=0)
    pdf.set_font(font, "", 12)
    doc_no = f"QT-{datetime.today().strftime('%Y%m%d')}"
    pdf.cell(0, 7, doc_no, ln=1)

    section_title("ข้อมูลลูกค้า")
    y = pdf.get_y()
    y = draw_wrapped_block(pdf, font, "ชื่อลูกค้า", quote["customer_name"], left, 28, y, content_w)
    y = draw_wrapped_block(pdf, font, "เบอร์โทร", quote["customer_phone"], left, 28, y, content_w)
    y = draw_wrapped_block(pdf, font, "ที่อยู่", quote["customer_address"], left, 28, y, content_w)
    pdf.set_y(y)

    section_title("รายละเอียดห้อง")
    y = pdf.get_y()
    y = draw_wrapped_block(pdf, font, "ขนาดห้อง", f"{quote['room_w']} x {quote['room_l']} เมตร  สูง {quote['room_h']} เมตร", left, 28, y, content_w)
    y = draw_wrapped_block(pdf, font, "โดนแดด", quote["sun"], left, 28, y, content_w)
    y = draw_wrapped_block(pdf, font, "จำนวนคน", str(quote["people"]), left, 28, y, content_w)
    y = draw_wrapped_block(pdf, font, "BTU คำนวณ", f"{quote['btu']:,} BTU", left, 28, y, content_w)
    y = draw_wrapped_block(pdf, font, "ขนาดแนะนำ", f"{quote['suggest_cap']:,} BTU", left, 28, y, content_w)
    pdf.set_y(y)

    section_title("รายการสินค้า")
    product_top = pdf.get_y()
    product_box_h = 42
    pdf.rect(left, product_top, content_w, product_box_h)
    pdf.set_xy(left + 3, product_top + 3)
    pdf.set_font(font, "B", 13)
    pdf.multi_cell(content_w - 6, 6, safe_text(quote["section"]))
    pdf.set_x(left + 3)
    pdf.set_font(font, "", 12)
    pdf.multi_cell(content_w - 6, 6, f"Model: {safe_text(quote['model'])}   |   BTU: {quote['model_btu']:,}")
    pdf.set_x(left + 3)
    pdf.multi_cell(content_w - 6, 6, f"ประกัน: ติดตั้ง {safe_text(quote['w_install'])} / อะไหล่ {safe_text(quote['w_parts'])} / คอมเพรสเซอร์ {safe_text(quote['w_comp'])}")
    if pdf.get_y() < product_top + product_box_h:
        pdf.set_y(product_top + product_box_h)
    else:
        pdf.ln(2)

    section_title("สรุปราคา")
    summary_y = pdf.get_y()
    summary_h = 30
    pdf.rect(left, summary_y, content_w, summary_h)
    pdf.set_xy(left + 4, summary_y + 4)
    money_line("ราคาพร้อมติดตั้ง", quote["base_price"])
    money_line("ส่วนลด", -int(quote["discount"]))
    money_line("ค่าติดตั้งเพิ่ม", int(quote["extra_install"]))
    pdf.line(left + 4, pdf.get_y(), page_w - right - 4, pdf.get_y())
    pdf.ln(2)
    money_line("รวมสุทธิ", quote["net_total"], bold=True)
    if pdf.get_y() < summary_y + summary_h:
        pdf.set_y(summary_y + summary_h)
    else:
        pdf.ln(2)

    section_title("เงื่อนไขการติดตั้ง")
    pdf.set_font(font, "", 11)
    for line in INSTALL_CONDITIONS.split("\n"):
        if line.strip():
            pdf.multi_cell(0, 5.5, line.strip())

    pdf.ln(4)
    pdf.set_font(font, "", 12)
    pdf.cell(85, 8, "ลงชื่อผู้เสนอราคา .................................................", border=0)
    pdf.cell(10, 8, "", border=0)
    pdf.cell(0, 8, "ลงชื่อผู้รับใบเสนอราคา .................................................", ln=1)
    pdf.cell(85, 8, f"({STORE_NAME})", border=0, align="C")
    pdf.cell(10, 8, "", border=0)
    pdf.cell(0, 8, "(..............................................................)", ln=1, align="C")
    pdf.cell(85, 8, "วันที่ ........../........../..........", border=0, align="C")
    pdf.cell(10, 8, "", border=0)
    pdf.cell(0, 8, "วันที่ ........../........../..........", ln=1, align="C")

    out = pdf.output(dest="S")
    if isinstance(out, (bytes, bytearray)):
        return bytes(out)
    return out.encode("latin-1")


def make_line_message_text(quote: dict) -> str:
    lines = [
        f"ใบเสนอราคา - {STORE_NAME}",
        f"วันที่: {quote['date']}",
        f"ลูกค้า: {safe_text(quote['customer_name'])}",
        f"โทร: {safe_text(quote['customer_phone'])}",
        f"รุ่น: {safe_text(quote['model'])}",
        f"ซีรีส์: {safe_text(quote['section']).replace(chr(10), ' / ')}",
        f"BTU รุ่น: {quote['model_btu']:,} BTU",
        f"ราคาพร้อมติดตั้ง: {format_baht(quote['base_price'])} บาท",
        f"ส่วนลด: {format_baht(quote['discount'])} บาท",
        f"ค่าติดตั้งเพิ่ม: {format_baht(quote['extra_install'])} บาท",
        f"รวมสุทธิ: {format_baht(quote['net_total'])} บาท",
        "",
        f"ติดต่อร้าน: {STORE_PHONE}",
        f"{STORE_WEB}",
    ]
    return "\n".join(lines)


def line_share_link(text: str) -> str:
    return "https://line.me/R/msg/text/?" + urlquote(text)


def log_customer_job(quote: dict):
    record = quote.copy()
    record["section"] = str(record["section"]).replace("\n", " | ")
    df_log = pd.DataFrame([record])
    df_log.to_csv(LOG_CSV, mode="a", header=not os.path.exists(LOG_CSV), index=False, encoding="utf-8-sig")


logo_path = os.path.join("assets", "logo.png")
if os.path.exists(logo_path):
    st.image(logo_path, use_container_width=True)

st.markdown(
    f"""
    <div style="text-align:center;">
      <div style="font-size:28px; font-weight:800;">{STORE_NAME}</div>
      <div style="font-size:16px;">มือถือ/Line: <b>{STORE_PHONE}</b> | Website: {STORE_WEB}</div>
      <div style="font-size:13px; opacity:0.75;">Boonsuk Smart Sales PRO v3</div>
    </div>
    """,
    unsafe_allow_html=True
)
st.divider()

df_all = load_stock()

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
st.subheader("❄️ เลือกรุ่นแอร์ + สต๊อก")
q = st.text_input("ค้นหา (รุ่น/ซีรีส์)", value="").strip().lower()

df_view = df_all.copy()
if q:
    df_view = df_view[
        df_view["section"].str.lower().str.contains(q, na=False) |
        df_view["model"].str.lower().str.contains(q, na=False)
    ].copy()

sections = sorted(df_view["section"].dropna().unique().tolist())
if not sections:
    st.warning("ไม่พบข้อมูลสินค้า")
    st.stop()

section = st.selectbox("เลือกซีรีส์/หมวดรุ่น", options=sections)
df_sec = df_view[df_view["section"] == section].copy()
if btu is not None and suggest_cap is not None:
    df_sec["diff"] = (df_sec["btu"] - int(suggest_cap)).abs()
    df_sec = df_sec.sort_values(["diff", "price_install"], ascending=[True, True])
else:
    df_sec = df_sec.sort_values(["price_install"], ascending=[True])

model = st.selectbox("เลือก Model", options=df_sec["model"].tolist())
row = df_sec[df_sec["model"] == model].iloc[0].to_dict()

st.markdown(
    f"""
**BTU รุ่นนี้:** {int(row['btu']):,}  
**ราคา(พร้อมติดตั้ง):** {format_baht(row['price_install'])} บาท  
**สต๊อกคงเหลือ:** {int(row.get('stock_qty', 0))} เครื่อง
"""
)
st.caption(
    f"ประกัน: ติดตั้ง {safe_text(row.get('w_install', ''))} | "
    f"อะไหล่ {safe_text(row.get('w_parts', ''))} | "
    f"คอมฯ {safe_text(row.get('w_comp', ''))}"
)

with st.expander("📋 ตารางสินค้า (ดู/เช็คสต๊อก)", expanded=False):
    show_cols = ["section", "model", "btu", "price_install", "stock_qty", "w_install", "w_parts", "w_comp"]
    st.dataframe(df_view[show_cols], use_container_width=True, hide_index=True)

st.divider()
st.subheader("💰 ปรับราคา")
discount = st.number_input("ส่วนลด (บาท)", min_value=0, step=100, value=0)
extra_install = st.number_input("ค่าติดตั้งเพิ่ม (บาท)", min_value=0, step=100, value=0)
base_price = int(row["price_install"])
net_total = max(0, base_price - int(discount) + int(extra_install))
st.info(f"**รวมสุทธิ:** {format_baht(net_total)} บาท")

st.divider()
today_str = date.today().strftime("%d/%m/%Y")
quote_data = {
    "date": today_str,
    "customer_name": customer_name,
    "customer_phone": customer_phone,
    "customer_address": customer_address,
    "room_w": room_w,
    "room_l": room_l,
    "room_h": room_h,
    "sun": sun,
    "people": int(people),
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

st.subheader("🧾 ใบเสนอราคา (PRO v3)")
c1, c2 = st.columns(2)
if c1.button("💾 บันทึกลูกค้า/งานนี้", use_container_width=True):
    try:
        log_customer_job(quote_data)
        st.success("บันทึกแล้ว ✅")
    except Exception as e:
        st.error(f"บันทึกไม่สำเร็จ: {e}")

if c2.button("📄 สร้าง PDF ใบเสนอราคา", use_container_width=True):
    try:
        pdf_bytes = build_pdf(quote_data)
        pdf_name = f"ใบเสนอราคา_{(customer_name or 'ลูกค้า')}_{today_str.replace('/', '-')}.pdf"
        st.success("สร้าง PDF สำเร็จ ✅")
        st.download_button("⬇️ ดาวน์โหลด PDF", data=pdf_bytes, file_name=pdf_name, mime="application/pdf", use_container_width=True)
    except Exception as e:
        st.error(f"สร้าง PDF ไม่สำเร็จ: {e}")

st.divider()
st.subheader("💬 ส่งข้อความเข้า LINE ลูกค้า")
line_text = make_line_message_text(quote_data)
st.text_area("ข้อความที่จะส่ง (แก้ได้ก่อนส่ง)", value=line_text, height=180)
share_url = line_share_link(line_text)
st.markdown(f"**[ส่งเข้า LINE]({share_url})**")
st.caption("ถ้าเปิดบนมือถือจะสะดวกที่สุด")

st.divider()
st.subheader("📦 จัดการสต๊อกแอร์")
st.info("ปรับจำนวนสต๊อก แล้วกดบันทึกสต๊อก ข้อมูลจะถูกเก็บใน boonsuk_stock.csv")
edit_cols = ["section", "model", "btu", "price_install", "stock_qty", "w_install", "w_parts", "w_comp"]
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

if os.path.exists(LOG_CSV):
    st.divider()
    st.subheader("⬇️ ดาวน์โหลดไฟล์บันทึกลูกค้า")
    with open(LOG_CSV, "rb") as f:
        st.download_button("ดาวน์โหลด boonsuk_customer_log.csv", data=f.read(), file_name="boonsuk_customer_log.csv", mime="text/csv", use_container_width=True)
