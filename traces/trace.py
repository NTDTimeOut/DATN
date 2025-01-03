import random
import time
import numpy as np

def generate_mqsim_trace(filename, num_requests=1000000):
    """
    Tạo file trace theo định dạng MQSim:
    [Time_Stamp] [Device_Number] [Type] [LBA] [Size_in_512B_Units] [Locality]
    Ví dụ: 0 0 1 8778 8 0
    """
    # Các tham số
    max_lba = 2**30 - 1  # Giảm max LBA xuống để tránh lỗi int32
    max_size = 256       # Max size in sectors
    current_time = 0
    device_number = 0    # Thường là 0
    
    # Hot spots cho locality
    num_hot_spots = 10
    hot_spots = [random.randint(0, max_lba) for _ in range(num_hot_spots)]  # Sử dụng random.randint thay vì np.random.randint
    hot_spot_probability = 0.7
    
    # Phân phối kích thước thực tế (sectors)
    size_weights = [0.4, 0.3, 0.2, 0.1]
    size_ranges = [(1,8), (9,32), (33,128), (129,256)]
    
    # Tỷ lệ đọc/ghi
    read_probability = 0.7
    
    with open(filename, 'w') as f:
        for i in range(num_requests):
            # Loại yêu cầu (1=read, 0=write)
            req_type = 1 if random.random() < read_probability else 0
            
            # Chọn LBA và xác định locality
            if random.random() < hot_spot_probability:
                base_lba = random.choice(hot_spots)
                lba = min(base_lba + random.randint(0, 1000), max_lba)
                locality = 1  # Hot data
            else:
                lba = random.randint(0, max_lba)
                locality = 0  # Cold data
            
            # Chọn kích thước
            size_range = random.choices(size_ranges, weights=size_weights)[0]
            size = random.randint(size_range[0], size_range[1])
            
            # Tăng thời gian (microseconds)
            current_time += int(np.random.exponential(500))
            
            # Ghi vào file theo định dạng MQSim
            f.write(f"{current_time} {device_number} {req_type} {lba} {size} {locality}\n")
            
            # In tiến độ
            if (i + 1) % 100000 == 0:
                print(f"Đã tạo {i + 1:,} yêu cầu")

def analyze_trace(filename):
    """Phân tích thống kê file trace"""
    reads = 0
    writes = 0
    hot_accesses = 0
    total_size = 0
    sizes = []
    times = []
    last_time = 0
    
    with open(filename, 'r') as f:
        for line in f:
            time, _, req_type, _, size, locality = map(int, line.split())
            
            if req_type == 1:
                reads += 1
            else:
                writes += 1
                
            if locality == 1:
                hot_accesses += 1
                
            total_size += size
            sizes.append(size)
            
            if last_time > 0:
                times.append(time - last_time)
            last_time = time
    
    total_reqs = reads + writes
    
    print("\nThống kê Trace:")
    print(f"Tổng số yêu cầu: {total_reqs:,}")
    print(f"Tỷ lệ đọc/ghi: {reads/total_reqs:.2%}/{writes/total_reqs:.2%}")
    print(f"Tỷ lệ truy cập hot data: {hot_accesses/total_reqs:.2%}")
    print(f"Kích thước trung bình: {np.mean(sizes):.2f} sectors ({np.mean(sizes)*512/1024:.2f}KB)")
    print(f"Kích thước trung vị: {np.median(sizes):.0f} sectors ({np.median(sizes)*512/1024:.2f}KB)")
    print(f"Thời gian trung bình giữa các yêu cầu: {np.mean(times):.2f} microseconds")
    print(f"Tổng thời gian mô phỏng: {last_time/1000000:.2f} giây")

if __name__ == "__main__":
    start_time = time.time()
    
    # Tạo file trace
    filename = "workload.trace"
    num_requests = 1_000_000  # 1 triệu yêu cầu
    
    print(f"Bắt đầu tạo {num_requests:,} yêu cầu...")
    generate_mqsim_trace(filename, num_requests)
    
    end_time = time.time()
    print(f"\nĐã tạo xong file trace trong {end_time - start_time:.2f} giây")
    
    # Phân tích trace
    analyze_trace(filename)