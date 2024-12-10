#include "LAC.h"

LAC::LAC(uint64_t cache_size) : cache_size(cache_size) {
    head = new LACNode();
    tail = new LACNode();
    head->right = tail;
    tail->left = head;
}

LAC::~LAC() {
    LACNode* current = head;
    while (current != NULL) {
        LACNode* next = current->right;
        delete current;
        current = next;
    }
}

void LAC::add(uint64_t pn) {
    if (m.find(pn) != m.end()) {
        access_map[pn]++;  
        return;
    }

    if (m.size() >= cache_size) {
        pop();
    }

    LACNode* new_node = new LACNode();
    new_node->page_num = pn;
    new_node->access_count = 1;  
    new_node->dirty = false; 

    m[pn] = new_node;

    new_node->right = head->right;
    new_node->left = head;
    head->right->left = new_node;
    head->right = new_node;

    access_map[pn] = 1;
}

uint64_t LAC::pop() {
    uint64_t evict_page = 0;
    uint64_t min_access_count = UINT64_MAX;

    for (const auto& entry : access_map) {
        uint64_t page_num = entry.first;
        uint64_t access_count = entry.second;
        if (access_count < min_access_count) {
            min_access_count = access_count;
            evict_page = page_num;
        }
    }

    if (evict_page != 0) {
        LACNode* node_to_remove = m[evict_page];
        
        node_to_remove->left->right = node_to_remove->right;
        node_to_remove->right->left = node_to_remove->left;

        m.erase(evict_page);
        access_map.erase(evict_page);

        delete node_to_remove;
    }

    return evict_page;
}

void LAC::modify(uint64_t pn, bool dirty) {
    if (m.find(pn) != m.end()) {
        LACNode* node = m[pn];
        
        node->dirty = dirty;
        
        access_map[pn]++;
    }
}
