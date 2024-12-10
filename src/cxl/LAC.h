#pragma once
#include <iostream>
#include <cstdint>
#include <map>

using namespace std;

class LACNode {
public:
    uint64_t page_num{ 0 };
    uint64_t access_count{ 0 };  
    bool dirty{ 0 };
    LACNode* left{ NULL };
    LACNode* right{ NULL };
};

class LAC {
public:
    LAC(); 
    LAC(uint64_t cache_size);  
    ~LAC();  
    
    void add(uint64_t pn);  
    uint64_t pop();        
    void modify(uint64_t pn, bool dirty);  
    
private:
    uint64_t cache_size{ 0 };
    LACNode* head{ NULL };
    LACNode* tail{ NULL };
    map<uint64_t, LACNode*> m;  
    map<uint64_t, uint64_t> access_map;  
};
