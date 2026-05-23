=== BÁO CÁO ĐÁNH GIÁ MÔ HÌNH: FinetuneNewLoss-1(best) ===
Cấu hình HeadQK: 256
----------------------------------------
1. Sinh JSON hợp lệ (Valid JSON) : 100.00%
2. Chọn đúng Tool (Intent Acc)   : 85.00%
3. Copy đúng ID (Args Exact Match): 11.00%
----------------------------------------
Precision (Weighted): 0.8549
Recall (Weighted)   : 0.8500
F1 Score (Weighted) : 0.8511
----------------------------------------
CHI TIẾT PHÂN LOẠI TOOL:
                  precision    recall  f1-score   support

 check_inventory       1.00      0.93      0.97        15
    create_order       0.81      0.76      0.79        17
    delete_order       0.77      0.89      0.83        19
       get_order       0.77      0.77      0.77        13
revenue_analysis       1.00      0.92      0.96        12
    update_order       0.83      0.83      0.83        24

        accuracy                           0.85       100
       macro avg       0.86      0.85      0.86       100
    weighted avg       0.85      0.85      0.85       100


=== BÁO CÁO ĐÁNH GIÁ MÔ HÌNH: Finetune220(best) ===
Cấu hình HeadQK: 256
----------------------------------------
1. Sinh JSON hợp lệ (Valid JSON) : 99.00%
2. Chọn đúng Tool (Intent Acc)   : 91.00%
3. Copy đúng ID (Args Exact Match): 12.00%
----------------------------------------
Precision (Weighted): 0.9245
Recall (Weighted)   : 0.9100
F1 Score (Weighted) : 0.9126
----------------------------------------
CHI TIẾT PHÂN LOẠI TOOL:
                  precision    recall  f1-score   support

 check_inventory       0.93      0.93      0.93        15
    create_order       1.00      0.76      0.87        17
    delete_order       0.90      1.00      0.95        19
       get_order       0.91      0.77      0.83        13
    invalid_json       0.00      0.00      0.00         0
revenue_analysis       1.00      1.00      1.00        12
    update_order       0.85      0.96      0.90        24

        accuracy                           0.91       100
       macro avg       0.80      0.78      0.78       100
    weighted avg       0.92      0.91      0.91       100