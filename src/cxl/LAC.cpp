#include "LAC.h"

LAC::LAC(uint64_t size) : cache_size(size), head(nullptr), tail(nullptr) {}

LAC::~LAC() {
    while (head != nullptr && head != tail) {
        LACNode* temp = head->right;
        delete head;
        head = temp;
    }
    if (head != nullptr) delete head;
    m.clear();
}

void LAC::add(uint64_t pn) {
    if (m.find(pn) != m.end()) return; // Trang đã tồn tại, không cần thêm

    if (m.size() >= cache_size) {
        pop(); // Loại bỏ trang nếu bộ nhớ đệm đã đầy
    }

    LACNode* new_node = new LACNode{ pn, false, 1, nullptr, head };

    if (head == nullptr) {  // Danh sách trống
        head = tail = new_node;
    } else {
        head->left = new_node;
        head = new_node;
    }

    m.emplace(pn, new_node);
}

uint64_t LAC::pop() {
    LACNode* current = tail;
    LACNode* target = nullptr;

    // Tìm trang sạch có số lần truy cập thấp nhất
    while (current != nullptr) {
        if (!current->dirty) {
            if (target == nullptr || current->access_count < target->access_count) {
                target = current;
            }
        }
        current = current->left;
    }

    // Nếu không có trang sạch, tìm trang bẩn ít được truy cập nhất
    if (target == nullptr) {
        current = tail;
        while (current != nullptr) {
            if (target == nullptr || current->access_count < target->access_count) {
                target = current;
            }
            current = current->left;
        }
    }

    // Loại bỏ trang được chọn
    uint64_t evict_page = target->page_num;

    if (target == head) {
        head = head->right;
        if (head) head->left = nullptr;
    } else if (target == tail) {
        tail = tail->left;
        if (tail) tail->right = nullptr;
    } else {
        target->left->right = target->right;
        target->right->left = target->left;
    }

    m.erase(target->page_num);
    delete target;

    return evict_page;
}

void LAC::modify(uint64_t pn, bool dirty) {
    auto it = m.find(pn);
    if (it == m.end()) return; // Trang không tồn tại

    LACNode* target = it->second;

    // Cập nhật trạng thái dirty
    if (!target->dirty) target->dirty = dirty;

    // Tăng số lần truy cập
    target->access_count++;

    // Nếu trang không ở đầu, đưa nó lên đầu danh sách
    if (target != head) {
        if (target == tail) {
            tail = target->left;
            tail->right = nullptr;
        } else {
            target->left->right = target->right;
            target->right->left = target->left;
        }

        target->right = head;
        head->left = target;
        target->left = nullptr;
        head = target;
    }
}
