import os, sys, gc
import torch
import torch.nn.functional as F
import numpy as np

# Cấu hình môi trường CUDA
try:
    os.environ["CUDA_VISIBLE_DEVICES"] = sys.argv[1]
except:
    pass
torch.backends.cudnn.benchmark = True
torch.backends.cudnn.allow_tf32 = True
torch.backends.cuda.matmul.allow_tf32 = True
np.set_printoptions(precision=4, suppress=True, linewidth=200)

# 1. CẤU HÌNH ĐƯỜNG DẪN VÀ THAM SỐ MÔ HÌNH
import types
args = types.SimpleNamespace()
args.RUN_DEVICE = "cuda"
args.FLOAT_MODE = "fp32" 
os.environ["RWKV_JIT_ON"] = '1' 

MODEL_NAME = '/kaggle/input/models/hykhangg/spikegpt-agency/pytorch/default/1/updated_2_model_weights(best)'

args.MODEL_NAME = MODEL_NAME
args.n_layer = 18
args.n_embd = 768
args.ctx_len = 1024
args.vocab_size = 50277
args.head_qk = 0
args.pre_ffn = 0
args.grad_cp = 0
args.my_pos_emb = 0
os.environ["RWKV_RUN_DEVICE"] = args.RUN_DEVICE

MAX_NEW_TOKENS = 80 # Giống hệt max_new_tokens=80 của GPT-2

print(f"Đang tải SpikeGPT từ: {MODEL_NAME}...")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.model_run import RWKV_RNN
from src.utils import TOKENIZER

model = RWKV_RNN(args)
gc.collect()
torch.cuda.empty_cache()

# 2. TẢI TOKENIZER 
WORD_NAME = ["20B_tokenizer.json", "20B_tokenizer.json"]
tokenizer = TOKENIZER(WORD_NAME, UNKNOWN_CHAR=None)

# 3. DANH SÁCH CÁC CÂU TEST 
test_cases = [
    "Hủy cho mình cái đơn hàng mã #99812 nhé.",
    "Mình muốn đặt 5 cái điện thoại iPhone-15-Pro, giao đến số 10 Phạm Ngọc Thạch, Quận 3, TP.HCM.",
    "Thống kê doanh thu từ ngày 2024-01-01 đến 2024-03-31 cho sếp xem nha.",
    "Chào em, hôm qua chị có đặt đơn ORD-776, nhưng chị nhập sai địa chỉ. Đổi lại số lượng thành 2 cho chị nhé.",
    "Kiểm tra xem mã SP-990 còn hàng không em?"
]

print(f"\nBắt đầu chạy test {len(test_cases)} kịch bản liên tiếp (Chế độ Greedy Search)...\n")
print("="*50)

# 4. VÒNG LẶP CHẠY TEST TỰ ĐỘNG
with torch.no_grad():
    for i, user_input in enumerate(test_cases, 1):
        
        # Đóng gói đúng format ChatML
        prompt = f"<|im_start|>system\nHãy thực hiện theo yêu cầu<|im_end|>\n<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant\n"
        
        ctx = tokenizer.tokenizer.encode(prompt)
        src_len = len(ctx)
        
        # RESET TRẠNG THÁI RNN 
        init_state = None
        mem1 = None
        mem2 = None
        
        # --- ĐỌC HIỂU PROMPT (PREPROCESS) ---
        for j in range(src_len):
            x = ctx[: j + 1]
            if j == src_len - 1:
                out, init_state, mem1, mem2 = model.forward(x, init_state, mem1, mem2)
            else:
                init_state, mem1, mem2 = model.forward(x, init_state, mem1, mem2, preprocess_only=True)

        generated_text = ""
        out_last = src_len
        state = init_state.clone()

        # --- SINH VĂN BẢN (GENERATION) VỚI GREEDY SEARCH ---
        for k in range(src_len, src_len + MAX_NEW_TOKENS):
            x = ctx[: k + 1]
            x = x[-args.ctx_len:] # Cắt bớt nếu vượt quá cửa sổ ngữ cảnh

            if k > src_len:
                out, state, mem1, mem2 = model.forward(x, state, mem1, mem2)

            out[0] = -999999999  # Vô hiệu hóa thẻ kết thúc mặc định của Pile
            
            # CHIẾN THUẬT GREEDY SEARCH: Lấy token có xác suất cao nhất (Giống GPT-2 do_sample=False)
            probs = F.softmax(out, dim=-1)
            ttt = int(torch.argmax(probs))
            ctx += [ttt]

            # Giải mã sang ký tự
            char = tokenizer.tokenizer.decode(ctx[out_last:])
            if '\ufffd' not in char: # Đảm bảo ký tự UTF-8 hợp lệ
                generated_text += char
                out_last = k + 1
                
                # Điều kiện dừng: Gặp thẻ đóng
                if "<|im_end|>" in generated_text:
                    generated_text = generated_text.replace("<|im_end|>", "").strip()
                    break
        
        # IN KẾT QUẢ ĐỐI CHIẾU
        print(f"TEST {i}: {user_input}")
        print(f"AI TRẢ LỜI:\n{generated_text.strip()}")
        print("-" * 50)

print("\nĐã test xong toàn bộ!")