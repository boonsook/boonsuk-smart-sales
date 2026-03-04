import os
import streamlit as st
import pandas as pd
from datetime import date
from fpdf import FPDF

st.set_page_config(page_title="Boonsuk Smart Sales PRO", layout="centered")

STORE_NAME = 'ร้านบุญสุขอิเล็กทรอนิกส์'
STORE_PHONE = '086-2613829'
STORE_WEB = 'http://www.bse-eletronics.com/'

PRODUCTS = [{"section": "Midea ฟิกส์speed", "model": "Asmg09c", "btu": 9000, "price_install": 19000, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "10 ปี"}, {"section": "Midea ฟิกส์speed", "model": "Asmg12j", "btu": 12000, "price_install": 21500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "10 ปี"}, {"section": "Midea ฟิกส์speed", "model": "Asaa18j", "btu": 18000, "price_install": 27500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "10 ปี"}, {"section": "Midea ฟิกส์speed", "model": "Asaa24j", "btu": 24000, "price_install": 37500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "10 ปี"}, {"section": "Midea ฟิกส์speed", "model": "Asaa30j", "btu": 30000, "price_install": 43000, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "10 ปี"}, {"section": "Fujitsu dc Inverter ipower ll r410a\nฟูจิสึ ระบบ อินเวอร์เตอร์", "model": "Asmg09jl", "btu": 8500, "price_install": 15500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "10 ปี"}, {"section": "Fujitsu dc Inverter ipower ll r410a\nฟูจิสึ ระบบ อินเวอร์เตอร์", "model": "Asmg12jl", "btu": 11900, "price_install": 16500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "10 ปี"}, {"section": "Fujitsu dc Inverter ipower ll r410a\nฟูจิสึ ระบบ อินเวอร์เตอร์", "model": "Asaa18jc", "btu": 17700, "price_install": 23500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "10 ปี"}, {"section": "Fujitsu dc Inverter ipower ll r410a\nฟูจิสึ ระบบ อินเวอร์เตอร์", "model": "Asaa24jc", "btu": 24200, "price_install": 34500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "10 ปี"}, {"section": "Fujitsu dc Inverter ipower ll r410a\nฟูจิสึ ระบบ อินเวอร์เตอร์", "model": "Asaa30cm", "btu": 27300, "price_install": 40000, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "10 ปี"}, {"section": "Fujitsu Excellence Fix speed r32\nฟูจิสึ ระบบ ธรรมดา", "model": "Asma09r32", "btu": 9100, "price_install": 13800, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "10 ปี"}, {"section": "Fujitsu Excellence Fix speed r32\nฟูจิสึ ระบบ ธรรมดา", "model": "Asma12r32", "btu": 11500, "price_install": 14500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "10 ปี"}, {"section": "Fujitsu Excellence Fix speed r32\nฟูจิสึ ระบบ ธรรมดา", "model": "Asma13r3", "btu": 13906, "price_install": 16700, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "10 ปี"}, {"section": "Fujitsu Excellence Fix speed r32\nฟูจิสึ ระบบ ธรรมดา", "model": "Asma18r410", "btu": 18745, "price_install": 23000, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "10 ปี"}, {"section": "Fujitsu Excellence Fix speed r32\nฟูจิสึ ระบบ ธรรมดา", "model": "Asma24r410", "btu": 24508, "price_install": 32000, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "10 ปี"}, {"section": "Fujitsu Excellence Fix speed r32\nฟูจิสึ ระบบ ธรรมดา", "model": "Asma30r4", "btu": 28800, "price_install": 35500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "10 ปี"}, {"section": "Fujitsu Excellence Fix speed r32\nฟูจิสึ ระบบ ธรรมดา", "model": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "btu": 86, "price_install": 86, "w_install": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "w_parts": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "w_comp": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/"}, {"section": "Carrierรุ่น explorer inverter\nแคเรีย ระบบอินเวอร์เตอร์", "model": "Tvgs010", "btu": 9000, "price_install": 15800, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "Carrierรุ่น explorer inverter\nแคเรีย ระบบอินเวอร์เตอร์", "model": "Tvgs013", "btu": 12000, "price_install": 18500, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "Carrierรุ่น explorer inverter\nแคเรีย ระบบอินเวอร์เตอร์", "model": "Tvgs016", "btu": 15000, "price_install": 22500, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "Carrierรุ่น explorer inverter\nแคเรีย ระบบอินเวอร์เตอร์", "model": "Tvgs018", "btu": 18000, "price_install": 26500, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "Carrierรุ่น explorer inverter\nแคเรีย ระบบอินเวอร์เตอร์", "model": "Tvgs024", "btu": 22000, "price_install": 29500, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "Carrierรุ่น gimini inverter\nแคเรีย ระบบอินเวอร์เตอร์", "model": "Tvegb010", "btu": 9000, "price_install": 15000, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "Carrierรุ่น gimini inverter\nแคเรีย ระบบอินเวอร์เตอร์", "model": "Tvegb013", "btu": 12000, "price_install": 17000, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "Carrierรุ่น gimini inverter\nแคเรีย ระบบอินเวอร์เตอร์", "model": "Tvegb018", "btu": 18000, "price_install": 23500, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "Carrierรุ่น gimini inverter\nแคเรีย ระบบอินเวอร์เตอร์", "model": "Tvegb024", "btu": 22000, "price_install": 27000, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "Carrierรุ่น gimini inverter\nแคเรีย ระบบอินเวอร์เตอร์", "model": "Tvegb025", "btu": 24000, "price_install": 31500, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "Carrierรุ่น gimini inverter\nแคเรีย ระบบอินเวอร์เตอร์", "model": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "btu": 86, "price_install": 86, "w_install": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "w_parts": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "w_comp": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/"}, {"section": "Carrierรุ่น astrony r32 รุ่นใหม่\nแคเรีย ระบบธรรมดา", "model": "AAF010", "btu": 9000, "price_install": 13000, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "7 ปี"}, {"section": "Carrierรุ่น astrony r32 รุ่นใหม่\nแคเรีย ระบบธรรมดา", "model": "AAF013", "btu": 12000, "price_install": 14000, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "7 ปี"}, {"section": "Carrierรุ่น astrony r32 รุ่นใหม่\nแคเรีย ระบบธรรมดา", "model": "AAF018", "btu": 18000, "price_install": 20500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "7 ปี"}, {"section": "Carrierรุ่น astrony r32 รุ่นใหม่\nแคเรีย ระบบธรรมดา", "model": "AAF025", "btu": 25000, "price_install": 26500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "7 ปี"}, {"section": "Carrierรุ่น everest r32 \nแคเรีย ระบบธรรมดา", "model": "Tsgs010", "btu": 9000, "price_install": 14000, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "7 ปี"}, {"section": "Carrierรุ่น everest r32 \nแคเรีย ระบบธรรมดา", "model": "Tsgs013", "btu": 12000, "price_install": 15000, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "7 ปี"}, {"section": "Carrierรุ่น everest r32 \nแคเรีย ระบบธรรมดา", "model": "Tsgs018", "btu": 18000, "price_install": 21000, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "7 ปี"}, {"section": "Carrierรุ่น everest r32 \nแคเรีย ระบบธรรมดา", "model": "Tsgs025", "btu": 24000, "price_install": 27000, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "7 ปี"}, {"section": "Carrierรุ่น everest r32 \nแคเรีย ระบบธรรมดา", "model": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "btu": 86, "price_install": 86, "w_install": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "w_parts": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "w_comp": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/"}, {"section": "Mitsubishi heavy duty 2019แอร์ญี่ปุ่น100%\nDeluxe r32 Jetflow 3d auto ระบบธรรมดา", "model": "Srk10cvs", "btu": 9444, "price_install": 15500, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "5 ปี"}, {"section": "Mitsubishi heavy duty 2019แอร์ญี่ปุ่น100%\nDeluxe r32 Jetflow 3d auto ระบบธรรมดา", "model": "Srk13cvs", "btu": 12039, "price_install": 18000, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "5 ปี"}, {"section": "Mitsubishi heavy duty 2019แอร์ญี่ปุ่น100%\nDeluxe r32 Jetflow 3d auto ระบบธรรมดา", "model": "Srk19cvs", "btu": 19127, "price_install": 29000, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "5 ปี"}, {"section": "Mitsubishi heavy duty 2019แอร์ญี่ปุ่น100%\nDeluxe r32 Jetflow 3d auto ระบบธรรมดา", "model": "Srk25cvs", "btu": 25085, "price_install": 38800, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "5 ปี"}, {"section": "Mitsubishi heavy duty 2019Standard r32               \n มิตซูบิชิเฮฟวี่ดิวตี้ ระบบธรรมดา", "model": "Srk10cvv", "btu": 9239, "price_install": 15000, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "5 ปี"}, {"section": "Mitsubishi heavy duty 2019Standard r32               \n มิตซูบิชิเฮฟวี่ดิวตี้ ระบบธรรมดา", "model": "Srk13cvv", "btu": 11634, "price_install": 17500, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "5 ปี"}, {"section": "Mitsubishi heavy duty 2019Standard r32               \n มิตซูบิชิเฮฟวี่ดิวตี้ ระบบธรรมดา", "model": "Srk15cvv", "btu": 14457, "price_install": 20800, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "5 ปี"}, {"section": "Mitsubishi heavy duty 2019Standard r32               \n มิตซูบิชิเฮฟวี่ดิวตี้ ระบบธรรมดา", "model": "Srk18cvv", "btu": 17305, "price_install": 25500, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "5 ปี"}, {"section": "Mitsubishi heavy duty 2019Standard inverter r32 \n    มิตซูบิชิเฮฟวี่ดิวตี้ ระบบอินเวอร์เตอร์", "model": "Srk10yw", "btu": 8683, "price_install": 16800, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "5 ปี"}, {"section": "Mitsubishi heavy duty 2019Standard inverter r32 \n    มิตซูบิชิเฮฟวี่ดิวตี้ ระบบอินเวอร์เตอร์", "model": "Srk13yw", "btu": 11098, "price_install": 21000, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "5 ปี"}, {"section": "Mitsubishi heavy duty 2019Standard inverter r32 \n    มิตซูบิชิเฮฟวี่ดิวตี้ ระบบอินเวอร์เตอร์", "model": "Srk15yw", "btu": 14457, "price_install": 24000, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "5 ปี"}, {"section": "Mitsubishi heavy duty 2019Standard inverter r32 \n    มิตซูบิชิเฮฟวี่ดิวตี้ ระบบอินเวอร์เตอร์", "model": "Srk18yw", "btu": 17276, "price_install": 28300, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "5 ปี"}, {"section": "Mitsubishi heavy duty 2019Standard inverter r32 \n    มิตซูบิชิเฮฟวี่ดิวตี้ ระบบอินเวอร์เตอร์", "model": "Srk24yw", "btu": 23021, "price_install": 38000, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "5 ปี"}, {"section": "Mitsubishi heavy duty 2019Standard inverter r32 \n    มิตซูบิชิเฮฟวี่ดิวตี้ ระบบอินเวอร์เตอร์", "model": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "btu": 86, "price_install": 86, "w_install": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "w_parts": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "w_comp": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/"}, {"section": "Greeรุ่น fairy series r32 รุ่นใหม่ล่าสุดมาตฐาน ส่งออกทั่วโลก  ระบบธรรมดา", "model": "Gwc09acc", "btu": 9000, "price_install": 13500, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "Greeรุ่น fairy series r32 รุ่นใหม่ล่าสุดมาตฐาน ส่งออกทั่วโลก  ระบบธรรมดา", "model": "Gwc12acc", "btu": 12000, "price_install": 14700, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "Greeรุ่น fairy series r32 รุ่นใหม่ล่าสุดมาตฐาน ส่งออกทั่วโลก  ระบบธรรมดา", "model": "Gwc18acc", "btu": 18000, "price_install": 22500, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "Greeรุ่น fairy series r32 รุ่นใหม่ล่าสุดมาตฐาน ส่งออกทั่วโลก  ระบบธรรมดา", "model": "Gwc24acc", "btu": 24000, "price_install": 26500, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "Greeรุ่น Amberlll series r32 มาตฐาน ส่งออกทั่วโลก\nกรี ระบบธรรมดา", "model": "Gwc09yb3", "btu": 9000, "price_install": 11800, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "Greeรุ่น Amberlll series r32 มาตฐาน ส่งออกทั่วโลก\nกรี ระบบธรรมดา", "model": "Gwc12yc3", "btu": 12000, "price_install": 13500, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "Greeรุ่น Amberlll series r32 มาตฐาน ส่งออกทั่วโลก\nกรี ระบบธรรมดา", "model": "Gwc18yc3", "btu": 18000, "price_install": 20500, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "Greeรุ่น Amberlll series r32 มาตฐาน ส่งออกทั่วโลก\nกรี ระบบธรรมดา", "model": "Gwc24yc3", "btu": 24000, "price_install": 24000, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "รุ่น Amberlll inverter series r32 มีระบบฟอกอากาศ plasma killerระบบอินเวอร์ทำงานได้ต่ำสุดเพียง1HZ\nมาตรฐาน ส่งออกทั่วโลก", "model": "Gwc09qb", "btu": 9000, "price_install": 16000, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "รุ่น Amberlll inverter series r32 มีระบบฟอกอากาศ plasma killerระบบอินเวอร์ทำงานได้ต่ำสุดเพียง1HZ\nมาตรฐาน ส่งออกทั่วโลก", "model": "Gwc12qb", "btu": 12000, "price_install": 17000, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "รุ่น Amberlll inverter series r32 มีระบบฟอกอากาศ plasma killerระบบอินเวอร์ทำงานได้ต่ำสุดเพียง1HZ\nมาตรฐาน ส่งออกทั่วโลก", "model": "Gwc18qb", "btu": 18000, "price_install": 24000, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "รุ่น Amberlll inverter series r32 มีระบบฟอกอากาศ plasma killerระบบอินเวอร์ทำงานได้ต่ำสุดเพียง1HZ\nมาตรฐาน ส่งออกทั่วโลก", "model": "Gwc24qb", "btu": 24000, "price_install": 27300, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "10 ปี"}, {"section": "รุ่น Amberlll inverter series r32 มีระบบฟอกอากาศ plasma killerระบบอินเวอร์ทำงานได้ต่ำสุดเพียง1HZ\nมาตรฐาน ส่งออกทั่วโลก", "model": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "btu": 86, "price_install": 86, "w_install": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "w_parts": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "w_comp": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/"}, {"section": "MAVELL  ระบบธรรมดา", "model": "MVF-09", "btu": 9000, "price_install": 11500, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "12 ปี"}, {"section": "MAVELL  ระบบธรรมดา", "model": "MVF-12", "btu": 12000, "price_install": 13000, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "12 ปี"}, {"section": "MAVELL  ระบบธรรมดา", "model": "MVF-18", "btu": 18000, "price_install": 18000, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "12 ปี"}, {"section": "MAVELL  ระบบธรรมดา", "model": "MVF-25", "btu": 24000, "price_install": 22500, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "12 ปี"}, {"section": "MAVELL  ระบบอินเวอร์เตอร์", "model": "MWF-09INV", "btu": 9000, "price_install": 14000, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "12 ปี"}, {"section": "MAVELL  ระบบอินเวอร์เตอร์", "model": "MWF-12 INV", "btu": 12000, "price_install": 15000, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "12 ปี"}, {"section": "MAVELL  ระบบอินเวอร์เตอร์", "model": "MWF-18 INV", "btu": 18000, "price_install": 19800, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "12 ปี"}, {"section": "MAVELL  ระบบอินเวอร์เตอร์", "model": "MWF-25 INV", "btu": 24000, "price_install": 26000, "w_install": "1 ปี", "w_parts": "5 ปี", "w_comp": "12 ปี"}, {"section": "MAVELL  ระบบอินเวอร์เตอร์", "model": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "btu": 86, "price_install": 86, "w_install": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "w_parts": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "w_comp": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/"}, {"section": "DAIKIN SMASH  ( 2018)\n ระบบธรรมดา", "model": "FTM 09 PV2S", "btu": 9000, "price_install": 14500, "w_install": "1 ปี", "w_parts": "1 ปี", "w_comp": "3 ปี"}, {"section": "DAIKIN SMASH  ( 2018)\n ระบบธรรมดา", "model": "FTM 13 PV2S", "btu": 12000, "price_install": 17000, "w_install": "1 ปี", "w_parts": "1 ปี", "w_comp": "3 ปี"}, {"section": "DAIKIN SMASH  ( 2018)\n ระบบธรรมดา", "model": "FTM 15 PV2S", "btu": 15000, "price_install": 20000, "w_install": "1 ปี", "w_parts": "1 ปี", "w_comp": "3 ปี"}, {"section": "DAIKIN SMASH  ( 2018)\n ระบบธรรมดา", "model": "FTM 18 PV2S", "btu": 18000, "price_install": 25500, "w_install": "1 ปี", "w_parts": "1 ปี", "w_comp": "3 ปี"}, {"section": "DAIKIN SMASH  ( 2018)\n ระบบธรรมดา", "model": "FTM 24 PV2S", "btu": 24000, "price_install": 35500, "w_install": "1 ปี", "w_parts": "1 ปี", "w_comp": "3 ปี"}, {"section": "DAIKIN SMASH  ( 2018)\n ระบบธรรมดา", "model": "FTM 28 PV2S", "btu": 28000, "price_install": 37000, "w_install": "", "w_parts": "", "w_comp": ""}, {"section": "DAIKIN SABAI  INVERTER ( 2019)\nระบบอินเวอร์เตอร์", "model": "FTKQ 09 TV2S", "btu": 9000, "price_install": 15500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "DAIKIN SABAI  INVERTER ( 2019)\nระบบอินเวอร์เตอร์", "model": "FTKQ 13 TV2S", "btu": 12000, "price_install": 18500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "DAIKIN SABAI  INVERTER ( 2019)\nระบบอินเวอร์เตอร์", "model": "FTKQ 15 TV2S", "btu": 15000, "price_install": 21000, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "DAIKIN SABAI  INVERTER ( 2019)\nระบบอินเวอร์เตอร์", "model": "FTKQ 18 TV2S", "btu": 18000, "price_install": 27000, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "DAIKIN SABAI  INVERTER ( 2019)\nระบบอินเวอร์เตอร์", "model": "FTKQ 24 TV2S", "btu": 24000, "price_install": 37000, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "DAIKIN  INVERTER ( SUPER SMILE)\nระบบอินเวอร์เตอร์", "model": "FTKC 09 TV2S", "btu": 9000, "price_install": 19000, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "DAIKIN  INVERTER ( SUPER SMILE)\nระบบอินเวอร์เตอร์", "model": "FTKC 13 TV2S", "btu": 12000, "price_install": 21000, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "DAIKIN  INVERTER ( SUPER SMILE)\nระบบอินเวอร์เตอร์", "model": "FTKC 15 TV2S", "btu": 18000, "price_install": 28500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "DAIKIN  INVERTER ( SUPER SMILE)\nระบบอินเวอร์เตอร์", "model": "FTKC 18 TV2S", "btu": 24000, "price_install": 40500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "DAIKIN  INVERTER ( SUPER SMILE)\nระบบอินเวอร์เตอร์", "model": "FTKC 24 TV2S", "btu": 28000, "price_install": 43500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "DAIKIN  INVERTER ( SUPER SMILE)\nระบบอินเวอร์เตอร์", "model": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "btu": 86, "price_install": 86, "w_install": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "w_parts": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "w_comp": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/"}, {"section": "MITSUBISHI (Mr.SLIM)\n ระบบธรรมดา", "model": "MS-GN 09 VF", "btu": 9000, "price_install": 15500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "MITSUBISHI (Mr.SLIM)\n ระบบธรรมดา", "model": "MS-GN 13 VF", "btu": 13000, "price_install": 18500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "MITSUBISHI (Mr.SLIM)\n ระบบธรรมดา", "model": "MS-GN 15 VF", "btu": 15000, "price_install": 22500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "MITSUBISHI (Mr.SLIM)\n ระบบธรรมดา", "model": "MS-GN 18 VF", "btu": 18000, "price_install": 27000, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "MITSUBISHI (Mr.SLIM)\n ระบบธรรมดา", "model": "MS-GN 24 VF", "btu": 24000, "price_install": 40000, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "MITSUBISHI   HAPPY  INVERTER \nระบบอินเวอร์เตอร์", "model": "MSY-KP 09 VF", "btu": 9000, "price_install": 16800, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "MITSUBISHI   HAPPY  INVERTER \nระบบอินเวอร์เตอร์", "model": "MSY-KP 13 VF", "btu": 13000, "price_install": 19800, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "MITSUBISHI   HAPPY  INVERTER \nระบบอินเวอร์เตอร์", "model": "MSY-KP 15 VF", "btu": 15000, "price_install": 23500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "MITSUBISHI   HAPPY  INVERTER \nระบบอินเวอร์เตอร์", "model": "MSY-KP 18 VF", "btu": 18000, "price_install": 28500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "MITSUBISHI  SLIM  INVERTER \nระบบอินเวอร์เตอร์", "model": "MSY-JP 09 VF", "btu": 9000, "price_install": 17700, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "MITSUBISHI  SLIM  INVERTER \nระบบอินเวอร์เตอร์", "model": "MSY-JP 13 VF", "btu": 13000, "price_install": 21000, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "MITSUBISHI  SLIM  INVERTER \nระบบอินเวอร์เตอร์", "model": "MSY-JP 15 VF", "btu": 15000, "price_install": 24500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "MITSUBISHI  SLIM  INVERTER \nระบบอินเวอร์เตอร์", "model": "MSY-JP 18 VF", "btu": 18000, "price_install": 28500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "MITSUBISHI  SLIM  INVERTER \nระบบอินเวอร์เตอร์", "model": "MSY-JP 24 VF", "btu": 24000, "price_install": 43500, "w_install": "1 ปี", "w_parts": "3 ปี", "w_comp": "5 ปี"}, {"section": "MITSUBISHI  SLIM  INVERTER \nระบบอินเวอร์เตอร์", "model": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "btu": 86, "price_install": 86, "w_install": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "w_parts": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/", "w_comp": "ร้านบุญสุขอิเล็กทรอนิกส์\nมือถือ/Line  086-2613829\nhttp://www.bse-eletronics.com/"}]
INSTALL_CONDITIONS = '1.แถมรางครอบท่อน้ำยาให้ฟรี  ไม่เกิน 4 เมตร หากเกินคิดเพิ่ม เมตรละ 200 บาท\n2.แถมท่อน้ำยา ไม่เกิน 4 เมตร หากเกินคิดเพิ่ม เมตรละ 400 บาท\n3.แถมท่อน้ำทิ้ง ไม่เกิน 10 เมตร หากเกินคิดเพิ่ม เมตรละ 40 บาท\n4.แถมสายไฟ  ไม่เกิน 10 เมตร หากเกินคิดเพิ่ม เมตรละ 40 บาท\n5.แถมขาแขวนหรือขายาง สำหรับติดตั้งคอยล์ร้อน\n6.กรณีไม่มีเบรคเกอร์แถมให้ฟรี\n7.รับประกันงานตามเงื่อนไขฟรี ตลอดอายุการใช้งาน'

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

def format_baht(x):
    try:
        return "{:,}".format(int(x))
    except Exception:
        return str(x)

def build_pdf(quote):
    pdf = FPDF(unit="mm", format="A4")
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=12)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "QUOTATION / ใบเสนอราคา", ln=1, align="C")

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, STORE_NAME, ln=1)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, f"มือถือ/Line: {STORE_PHONE}", ln=1)
    pdf.cell(0, 6, f"Website: {STORE_WEB}", ln=1)
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, f"วันที่: {quote['date']}", ln=1)
    pdf.cell(0, 6, f"ลูกค้า: {quote['customer_name']}   โทร: {quote['customer_phone']}", ln=1)
    pdf.multi_cell(0, 6, f"ที่อยู่: {quote['customer_address']}")
    pdf.ln(1)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, "รายละเอียดห้อง / Room Details", ln=1)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, f"ขนาดห้อง: {quote['room_w']} x {quote['room_l']} ม.  สูง {quote['room_h']} ม.", ln=1)
    pdf.cell(0, 6, f"โดนแดด: {quote['sun']}   จำนวนคน: {quote['people']}", ln=1)
    pdf.cell(0, 6, f"BTU ที่แนะนำ: {quote['btu']:,}  (แนะนำไซส์: {quote['suggest_cap']:,})", ln=1)
    pdf.ln(1)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, "รายการสินค้า / Item", ln=1)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, f"รุ่น/ซีรีส์: {quote['section']}")
    pdf.cell(0, 6, f"Model: {quote['model']}   BTU: {quote['model_btu']:,}", ln=1)
    pdf.cell(0, 6, f"ประกัน (ติดตั้ง/อะไหล่/คอมฯ): {quote['w_install']} / {quote['w_parts']} / {quote['w_comp']}", ln=1)
    pdf.cell(0, 6, f"ราคาพร้อมติดตั้ง: {format_baht(quote['base_price'])} บาท", ln=1)
    pdf.ln(1)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, "สรุปราคา / Price Summary", ln=1)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 6, f"ราคาพร้อมติดตั้ง: {format_baht(quote['base_price'])} บาท", ln=1)
    pdf.cell(0, 6, f"ส่วนลด: -{format_baht(quote['discount'])} บาท", ln=1)
    pdf.cell(0, 6, f"ค่าติดตั้งเพิ่ม: +{format_baht(quote['extra_install'])} บาท", ln=1)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, f"รวมสุทธิ: {format_baht(quote['net_total'])} บาท", ln=1)
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, "เงื่อนไขการติดตั้ง", ln=1)
    pdf.set_font("Helvetica", "", 10)
    for line in INSTALL_CONDITIONS.split("\n"):
        if line.strip():
            pdf.multi_cell(0, 5, line.strip())
    pdf.ln(2)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, "ลงชื่อผู้รับใบเสนอราคา: ____________________________", ln=1)
    pdf.cell(0, 8, "วันที่: ____ / ____ / ______", ln=1)

    return pdf.output(dest="S").encode("latin-1")

header_html = (
    f"<div style='text-align:center; padding:8px 0 0 0;'>"
    f"<div style='font-size:28px; font-weight:800;'>{STORE_NAME}</div>"
    f"<div style='font-size:16px;'>มือถือ/Line: <b>{STORE_PHONE}</b> | Website: {STORE_WEB}</div>"
    f"<div style='font-size:13px; opacity:0.75;'>Boonsuk Smart Sales PRO (ดีไซน์ชั่วคราวแทนโลโก้)</div>"
    f"</div>"
)
st.markdown(header_html, unsafe_allow_html=True)
st.divider()

df = pd.DataFrame(PRODUCTS)

with st.expander("🧑‍💼 ข้อมูลลูกค้า", expanded=True):
    colA, colB = st.columns(2)
    customer_name = colA.text_input("ชื่อลูกค้า", value="")
    customer_phone = colB.text_input("เบอร์โทร", value="")
    customer_address = st.text_area("ที่อยู่/สถานที่ติดตั้ง", value="", height=70)

st.divider()

st.subheader("🏠 คำนวณ BTU")
c1, c2, c3 = st.columns(3)
room_w = c1.number_input("กว้าง (เมตร)", min_value=0.0, step=0.1)
room_l = c2.number_input("ยาว (เมตร)", min_value=0.0, step=0.1)
room_h = c3.number_input("สูง (เมตร)", min_value=0.0, step=0.1, value=2.6)

c4, c5 = st.columns(2)
sun = c4.selectbox("ห้องโดนแดดไหม?", ["ไม่โดนแดด", "โดนแดด"])
people = c5.number_input("จำนวนคนในห้อง", min_value=1, step=1, value=1)

btu = None
suggest_cap = None
if room_w > 0 and room_l > 0:
    btu = calculate_btu(room_w, room_l, room_h, sun, int(people))
    suggest_cap = suggest_capacity(btu)
    st.success(f"BTU ที่แนะนำ: **{btu:,} BTU**  |  แนะนำไซส์: **{suggest_cap:,} BTU**")
else:
    st.info("กรอกกว้าง/ยาว เพื่อคำนวณ BTU")

st.divider()

st.subheader("❄️ เลือกรุ่นแอร์จากรายการร้าน")
sections = sorted([s for s in df["section"].dropna().unique() if str(s).strip()])
section = st.selectbox("เลือกซีรีส์/หมวดรุ่น", options=sections)

df_sec = df[df["section"] == section].copy()
if btu is not None:
    df_sec["diff"] = (df_sec["btu"] - suggest_cap).abs()
    df_sec = df_sec.sort_values(["diff", "price_install"], ascending=[True, True])

models = df_sec["model"].tolist()
model = st.selectbox("เลือก Model", options=models)

row = df_sec[df_sec["model"] == model].iloc[0].to_dict()
st.write(f"**BTU รุ่นนี้:** {int(row['btu']):,}  •  **ราคา(พร้อมติดตั้ง):** {format_baht(row['price_install'])} บาท")
st.caption(f"ประกัน: ติดตั้ง {row['w_install']} | อะไหล่ {row['w_parts']} | คอมฯ {row['w_comp']}")

st.divider()

st.subheader("💰 ปรับราคา")
p1, p2 = st.columns(2)
discount = p1.number_input("ส่วนลด (บาท)", min_value=0, step=100, value=0)
extra_install = p2.number_input("ค่าติดตั้งเพิ่ม (บาท)", min_value=0, step=100, value=0)

base_price = int(row["price_install"])
net_total = max(0, base_price - int(discount) + int(extra_install))
st.info(f"**รวมสุทธิ:** {format_baht(net_total)} บาท")

st.divider()

st.subheader("🧾 บันทึก & ออกใบเสนอราคา")
today_str = date.today().strftime("%d/%m/%Y")

quote = {
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
    "w_install": row["w_install"],
    "w_parts": row["w_parts"],
    "w_comp": row["w_comp"],
    "base_price": base_price,
    "discount": int(discount),
    "extra_install": int(extra_install),
    "net_total": net_total,
}

colS, colP, colD = st.columns([1, 1, 1])

if colS.button("💾 บันทึกลูกค้า/งานนี้"):
    record = quote.copy()
    record["section"] = str(record["section"]).replace("\n", " | ")
    log_path = "boonsuk_customer_log.csv"
    df_log = pd.DataFrame([record])
    try:
        df_log.to_csv(log_path, mode="a", header=not os.path.exists(log_path), index=False, encoding="utf-8-sig")
        st.success("บันทึกแล้ว ✅")
    except Exception as e:
        st.error(f"บันทึกไม่สำเร็จ: {e}")

pdf_bytes = build_pdf(quote)
pdf_name = f"ใบเสนอราคา_{customer_name or 'ลูกค้า'}_{today_str.replace('/','-')}.pdf"
colP.download_button("⬇️ Export ใบเสนอราคา PDF", data=pdf_bytes, file_name=pdf_name, mime="application/pdf")

log_path = "boonsuk_customer_log.csv"
if os.path.exists(log_path):
    with open(log_path, "rb") as f:
        colD.download_button("⬇️ ดาวน์โหลดไฟล์บันทึกลูกค้า (CSV)", data=f.read(),
                             file_name="boonsuk_customer_log.csv", mime="text/csv")
else:
    colD.write("ยังไม่มีไฟล์บันทึก")

with st.expander("📌 เงื่อนไขการติดตั้ง (แสดงในใบเสนอราคา)", expanded=False):
    st.text(INSTALL_CONDITIONS)
