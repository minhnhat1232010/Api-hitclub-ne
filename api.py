from flask import Flask, jsonify
import random

app = Flask(__name__)

# Danh sách phiên gần nhất để phân tích 10 ván gần đây
lich_su_phien = [
    {"phien": 1001, "xuc_xac": [2, 5, 3]},
    {"phien": 1002, "xuc_xac": [6, 1, 2]},
    {"phien": 1003, "xuc_xac": [4, 5, 6]},
    {"phien": 1004, "xuc_xac": [1, 1, 2]},
    {"phien": 1005, "xuc_xac": [3, 4, 2]},
    {"phien": 1006, "xuc_xac": [5, 5, 6]},
    {"phien": 1007, "xuc_xac": [2, 2, 2]},
    {"phien": 1008, "xuc_xac": [3, 6, 6]},
    {"phien": 1009, "xuc_xac": [4, 1, 2]},
    {"phien": 1010, "xuc_xac": [6, 6, 6]},
]

# VIP logic: nếu tổng >=11 → tài, <11 → xỉu
def du_doan_tai_xiu(danh_sach):
    cau_tai = sum(1 for i in danh_sach if sum(i["xuc_xac"]) >= 11)
    cau_xiu = 10 - cau_tai
    if cau_tai > cau_xiu:
        du_doan = "Tài"
    elif cau_tai < cau_xiu:
        du_doan = "Xỉu"
    else:
        du_doan = "Tài" if random.random() > 0.5 else "Xỉu"

    do_tin_cay = round((max(cau_tai, cau_xiu) / 10) * 100, 2)
    giai_thich = f"Phân tích 10 phiên: {cau_tai} tài - {cau_xiu} xỉu → cầu nghiêng về {du_doan}"
    return du_doan, do_tin_cay, giai_thich

@app.route('/api/taixiu', methods=['GET'])
def api_taixiu():
    current_game = lich_su_phien[-1]
    x1, x2, x3 = current_game["xuc_xac"]
    tong = x1 + x2 + x3
    ket_qua = "Tài" if tong >= 11 else "Xỉu"
    phien = current_game["phien"]

    du_doan, do_tin_cay, giai_thich = du_doan_tai_xiu(lich_su_phien[-10:])

    response = {
        "Phien": phien,
        "Ket_qua": ket_qua,
        "Xuc_xac": f"{x1}-{x2}-{x3}",
        "Tong": tong,
        "Next_phien": phien + 1,
        "Du_doan": du_doan,
        "Do_tin_cay": f"{do_tin_cay}%",
        "Giai_thich": giai_thich
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run()