import json
import random

# Hàm sinh ID động (Giữ cấu trúc giống lúc train nhưng tiền tố và số chưa từng xuất hiện)
def generate_ood_order_id():
    prefix = random.choice(["ITEM", "TICKET", "BILL", "M", "ID", "DH", "GIAO", "CODE"])
    number = random.randint(1000, 9999)
    return f"{prefix}-{number}"

def generate_ood_product_id():
    prefix = random.choice(["PHONE", "LAPTOP", "TABLET", "WATCH", "TV", "MAC", "PC"])
    number = random.randint(10, 99)
    suffix = random.choice(["PRO", "MAX", "PLUS", "LITE", "ULTRA", "X"])
    return f"{prefix}-{number}-{suffix}"

# Hàm sinh Địa chỉ động
STREETS = ["Đường Hoa Lan", "Đường Mây Trắng", "Phố Cổ Dịch", "Đường Số 8", "Đại lộ Tự Do", "Đường Bình Minh", "Phố Ánh Sao", "Hẻm 404"]
WARDS = ["Phường Hạnh Phúc", "Phường An Lạc", "Xã Bình Yên", "Thị trấn Gió Ngàn", "Phường Ánh Sáng", "Phường 99"]
DISTRICTS = ["Quận Alpha", "Quận Beta", "Huyện Mây Ngàn", "Thành phố Tương Lai", "Thị xã Bình Minh", "Huyện Vùng Cao"]

def generate_ood_address():
    number = random.randint(1, 999)
    street = random.choice(STREETS)
    ward = random.choice(WARDS)
    district = random.choice(DISTRICTS)
    return f"Số {number} {street}, {ward}, {district}"

def generate_ood_samples(num_samples=5000):
    samples = []
    
    for _ in range(num_samples):
        # Đã thêm get_order vào danh sách!
        intent = random.choice(["delete_order", "create_order", "revenue_analysis", "update_order", "check_inventory", "get_order"])
        
        if intent == "delete_order":
            order_id = generate_ood_order_id()
            templates = [
                f"Ê bạn, xóa gấp giùm mình cái đơn {order_id} nha.",
                f"Tôi đổi ý rồi, hủy ngay đơn {order_id} đi shop.",
                f"Làm ơn cancel cái đơn {order_id} giúp tớ.",
                f"Hủy cái hóa đơn mã {order_id} lẹ cho mình nha.",
                f"Không mua nữa, xóa đơn {order_id} đi.",
                f"Shop ơi hủy giúp em mã {order_id} với ạ.",
                f"Mã {order_id} tôi lỡ đặt nhầm, gỡ đi shop."
            ]
            prompt = random.choice(templates)
            arguments = {"order_id": order_id}
            
        elif intent == "create_order":
            product_id = generate_ood_product_id()
            address = generate_ood_address()
            quantity = random.randint(10, 99)
            templates = [
                f"Cho mình {quantity} món {product_id} về địa chỉ {address} nhé.",
                f"Giao lẹ {quantity} hộp {product_id} tới {address}.",
                f"Mua thêm {quantity} cái {product_id}, ship hỏa tốc qua {address}.",
                f"Order {quantity} sản phẩm {product_id} chuyển tới {address} nha shop.",
                f"Chốt đơn {quantity} chiếc {product_id} giao tận nơi tại {address}.",
                f"Shop gửi {quantity} cái {product_id} đến {address} cho tớ.",
                f"Lên đơn {quantity} {product_id} về {address} giùm nha."
            ]
            prompt = random.choice(templates)
            arguments = {"product_id": product_id, "quantity": quantity, "address": address}
            
        elif intent == "revenue_analysis":
            start = f"{random.randint(2027, 2029)}-0{random.randint(1,9)}-{random.randint(10,28)}"
            end = f"{random.randint(2027, 2029)}-1{random.randint(0,2)}-{random.randint(10,28)}"
            templates = [
                f"Từ {start} tới {end} bán được bao nhiêu tiền vậy?",
                f"Xuất báo cáo doanh số kỳ từ {start} qua {end} cho anh.",
                f"Tính tổng thu nhập từ ngày {start} đến {end}.",
                f"Doanh thu từ {start} tới ngày {end} là bao nhiêu?",
                f"Thống kê tiền lời từ {start} qua {end} xem nào.",
                f"In cho chị doanh số bắt đầu từ {start} kết thúc vào {end}.",
                f"Kỳ báo cáo {start} tới {end} thu được bao nhiêu?"
            ]
            prompt = random.choice(templates)
            arguments = {"start_date": start, "end_date": end}
            
        elif intent == "update_order":
            order_id = generate_ood_order_id()
            address = generate_ood_address()
            quantity = random.randint(11, 99)
            templates = [
                f"Sửa lại đơn {order_id} thành {quantity} món và ship qua {address} giùm.",
                f"Đơn {order_id} của mình á, đổi địa chỉ thành {address} và lấy {quantity} cái thôi.",
                f"Cập nhật bill {order_id}: lấy {quantity} sản phẩm, giao tới {address}.",
                f"Mã {order_id} mình đổi ý lấy {quantity} cái nha, giao qua {address}.",
                f"Cho cái đơn {order_id} dời về {address} với số lượng {quantity} nha.",
                f"Update lại mã {order_id} giùm, {quantity} món tới {address}.",
                f"Hóa đơn {order_id} chuyển số lượng thành {quantity} gửi đi {address}."
            ]
            prompt = random.choice(templates)
            arguments = {"order_id": order_id, "quantity": quantity, "address": address}
            
        elif intent == "check_inventory":
            product_id = generate_ood_product_id()
            templates = [
                f"Trong kho còn con {product_id} không shop?",
                f"Check tồn kho mã {product_id} giúp chị.",
                f"Hàng {product_id} bao giờ thì về thêm vậy em?",
                f"Xem giúp em cái {product_id} còn hàng sẵn không?",
                f"Mã {product_id} còn mấy cái trong kho vậy?",
                f"Tồn kho con {product_id} còn nhiều không?",
                f"Mã {product_id} có sẵn không báo giá em với."
            ]
            prompt = random.choice(templates)
            arguments = {"product_id": product_id}
            
        elif intent == "get_order":
            order_id = generate_ood_order_id()
            templates = [
                f"Kiểm tra tình trạng đơn {order_id} cho mình.",
                f"Xem giúp đơn {order_id} tới đâu rồi shop ơi.",
                f"Tra cứu mã vận đơn {order_id} giùm tớ.",
                f"Đơn {order_id} sao chưa giao tới nữa vậy?",
                f"Check xem hóa đơn {order_id} đã được gửi đi chưa.",
                f"Cho mình hỏi đơn {order_id} trạng thái hiện tại là gì?",
                f"Follow up giùm mình cái bill {order_id} nha."
            ]
            prompt = random.choice(templates)
            arguments = {"order_id": order_id}

        tool_call_str = json.dumps({"name": intent, "arguments": arguments}, ensure_ascii=False)
        text = f"<|im_start|>system\nHãy thực hiện theo yêu cầu<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n<tool_call>\n{tool_call_str}\n</tool_call><|im_end|>\n"
        
        samples.append({"text": text})
        
    return samples

if __name__ == "__main__":
    output_file = "data/test_ood_data.jsonl"
    import os
    os.makedirs("data", exist_ok=True)
    
    samples = generate_ood_samples(5000)
    
    with open(output_file, "w", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
            
    try:
        print(f"Đã tạo thành công {len(samples)} mẫu OOD (phiên bản cân bằng + FULL 6 Intents) tại {output_file}")
    except:
        pass
