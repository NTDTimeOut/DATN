import random
import time

def generate_trace(filename, num_requests=1000000):
    """
    Tạo file trace theo định dạng:
    [Time] [Type] [LBA] [Size] [Locality]
    Ví dụ: 480 1 314055630 117 1
    """
    with open(filename, 'w') as f:
        current_time = 0
        for i in range(num_requests):
            # Thời gian (tăng 100-1000)
            current_time += random.randint(100, 1000)
            
            # Type (1=read, 0=write)
            req_type = random.randint(0, 1)
            
            # LBA (địa chỉ logic, khoảng 100M-1B)
            lba = random.randint(100_000_000, 1_000_000_000)
            
            # Size (1-250)
            size = random.randint(1, 250)
            
            # Locality (0 hoặc 1)
            locality = random.randint(0, 1)
            
            # Ghi vào file
            f.write(f"{current_time} {req_type} {lba} {size} {locality}\n")
            
            # In tiến độ
            if (i + 1) % 100000 == 0:
                print(f"Đã tạo {i + 1:,} yêu cầu")

if __name__ == "__main__":
    filename = "workload.trace"
    num_requests = 200_000  # 200k yêu cầu
    
    print(f"Bắt đầu tạo {num_requests:,} yêu cầu...")
    generate_trace(filename, num_requests)
    print("Hoàn thành!")