#ifndef LAC_H
#define LAC_H

#include <unordered_map>
#include <cstdint>

struct LACNode {
    uint64_t page_num;    // Số hiệu trang
    bool dirty;           // Trạng thái sạch/bẩn
    uint64_t access_count; // Số lần truy cập
    LACNode* left;        // Con trỏ tới nút trước
    LACNode* right;       // Con trỏ tới nút sau
};

class LAC {
private:
    uint64_t cache_size;                      // Kích thước bộ nhớ đệm
    LACNode* head;                            // Đầu danh sách
    LACNode* tail;                            // Cuối danh sách
    std::unordered_map<uint64_t, LACNode*> m; // Bảng băm lưu thông tin trang

public:
    LAC(uint64_t size);        // Constructor
    ~LAC();                    // Destructor
    void add(uint64_t pn);     // Thêm trang vào cache
    uint64_t pop();            // Loại bỏ trang theo chiến lược LAC
    void modify(uint64_t pn, bool dirty); // Sửa đổi trạng thái của trang
};

#endif // LAC_H
