import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

def parse_xml_file(filename):
    """Đọc và phân tích file XML để lấy các thông số hiệu năng"""
    tree = ET.parse(filename)
    root = tree.getroot()
    io_flow = root.find('.//Host.IO_Flow')
    
    # Lấy các thông số cơ bản từ XML
    metrics = {
        # Thông số IOPS
        'IOPS': float(io_flow.find('IOPS').text),
        'IOPS_Read': float(io_flow.find('IOPS_Read').text),
        'IOPS_Write': float(io_flow.find('IOPS_Write').text),
        
        # Thông số thời gian phản hồi
        'Response_Time': float(io_flow.find('Device_Response_Time').text),
        'End_to_End_Delay': float(io_flow.find('End_to_End_Request_Delay').text),
        
        # Thông số băng thông (chuyển đổi sang MB/s)
        'Bandwidth': float(io_flow.find('Bandwidth').text) / (1024*1024),
        'Bandwidth_Read': float(io_flow.find('Bandwidth_Read').text) / (1024*1024),
        'Bandwidth_Write': float(io_flow.find('Bandwidth_Write').text) / (1024*1024)
    }
    
    # Lấy thông tin về thời gian của Flash Chips
    flash_chips = root.findall('.//SSDDevice.FlashChips')
    execution_times = []
    idle_times = []
    
    for chip in flash_chips:
        if 'Fraction_of_Time_in_Execution' in chip.attrib:
            execution_times.append(float(chip.attrib['Fraction_of_Time_in_Execution']))
            idle_times.append(float(chip.attrib['Fraction_of_Time_Idle']))
            
    return metrics, execution_times, idle_times

def create_bar_plot(ax, data, metrics, width, colors, title, ylabel, labels=None):
    """Tạo biểu đồ cột với các thông số được chỉ định"""
    x = np.arange(len(metrics))
    bars = []
    
    # Vẽ các cột cho từng workload
    for i, (workload, color) in enumerate(zip(data, colors)):
        bar = ax.bar(x + (i-1)*width, [workload[0][m] for m in metrics], 
                    width, label=f'Workload {i+1}', 
                    color=color, alpha=0.8, edgecolor='black', linewidth=1)
        bars.append(bar)
    
    # Cấu hình trục và nhãn
    ax.set_ylabel(ylabel, fontsize=12, fontweight='bold')
    ax.set_title(title, pad=20, fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(labels if labels else metrics, fontsize=11)
    ax.legend(fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Thêm giá trị lên các cột
    for bar_group in bars:
        for bar in bar_group:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:,.1f}' if height < 1000 else f'{height:,.0f}',
                   ha='center', va='bottom', fontsize=10)
    
    return bars

def create_boxplot(ax, data, colors):
    """Tạo boxplot cho phân phối thời gian của Flash Chips"""
    # Chuẩn bị dữ liệu cho boxplot
    plot_data = [
        data[0][1], data[1][1], data[2][1],  # Execution times
        data[0][2], data[1][2], data[2][2]   # Idle times
    ]
    
    # Vẽ boxplot
    bp = ax.boxplot(plot_data, 
                    labels=['W1\nExec', 'W2\nExec', 'W3\nExec',
                           'W1\nIdle', 'W2\nIdle', 'W3\nIdle'])
    
    # Cấu hình trục và nhãn
    ax.set_ylabel('Fraction of Time', fontsize=12, fontweight='bold')
    ax.set_title('Flash Chips Time Distribution', pad=20, fontsize=14, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.tick_params(axis='both', which='major', labelsize=11)
    
    # Tùy chỉnh màu sắc cho boxplot
    colors_bp = colors * 2  # Duplicate colors for Exec and Idle
    for i, box in enumerate(bp['boxes']):
        plt.setp(box, color=colors_bp[i], alpha=0.8, linewidth=2)
        plt.setp(bp['whiskers'][i*2:i*2+2], color=colors_bp[i], alpha=0.8, linewidth=2)
        plt.setp(bp['caps'][i*2:i*2+2], color=colors_bp[i], alpha=0.8, linewidth=2)
        plt.setp(bp['medians'][i], color='black', linewidth=2)
    
    return bp

def plot_comparison(workload_1, workload_2, workload_3):
    """Tạo biểu đồ so sánh hiệu năng giữa các workload"""
    # Thiết lập cấu hình chung
    plt.rcParams.update({'font.size': 12})
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 14))
    colors = ['#2ecc71', '#3498db', '#e74c3c']
    width = 0.25
    
    # Dữ liệu workload
    workloads = [workload_1, workload_2, workload_3]
    
    # 1. Biểu đồ IOPS
    create_bar_plot(ax1, workloads, 
                   ['IOPS', 'IOPS_Read', 'IOPS_Write'],
                   width, colors, 
                   'IOPS Comparison', 
                   'Operations per Second',
                   ['Total IOPS', 'Read IOPS', 'Write IOPS'])
    
    # 2. Biểu đồ Bandwidth
    create_bar_plot(ax2, workloads,
                   ['Bandwidth', 'Bandwidth_Read', 'Bandwidth_Write'],
                   width, colors,
                   'Bandwidth Comparison',
                   'Bandwidth (MB/s)',
                   ['Total', 'Read', 'Write'])
    
    # 3. Biểu đồ Response Time
    create_bar_plot(ax3, workloads,
                   ['Response_Time', 'End_to_End_Delay'],
                   width, colors,
                   'Response Time Comparison',
                   'Time (ms)',
                   ['Response Time', 'E2E Delay'])
    
    # 4. Boxplot cho Flash Chips
    create_boxplot(ax4, workloads, colors)
    
    # Hoàn thiện biểu đồ
    plt.suptitle('SSD Performance Comparison', 
                fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    # Lưu biểu đồ
    plt.savefig('workload_comparison.png', 
                bbox_inches='tight', dpi=300)
    plt.show()

# Chạy chương trình
if __name__ == "__main__":
    # Đọc dữ liệu từ các file XML
    workload_1 = parse_xml_file('workload_1_scenario_1.xml')
    workload_2 = parse_xml_file('workload_2_scenario_1.xml')
    workload_3 = parse_xml_file('workload_3_scenario_1.xml')
    
    # Vẽ biểu đồ so sánh
    plot_comparison(workload_1, workload_2, workload_3)