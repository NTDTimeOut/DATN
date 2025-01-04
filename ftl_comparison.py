import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

def parse_ftl_metrics(filename):
    """Đọc các thông số FTL từ file XML"""
    tree = ET.parse(filename)
    root = tree.getroot()
    ftl = root.find('.//SSDDevice.FTL')
    
    return {
        'Read_Commands': {
            'Normal': int(ftl.get('Issued_Flash_Read_CMD')),
            'Multiplane': int(ftl.get('Issued_Flash_Multiplane_Read_CMD')),
            'Interleaved': int(ftl.get('Issued_Flash_Interleaved_Read_CMD'))
        },
        'Cache_Stats': {
            'Hits': int(ftl.get('CMT_Hits')),
            'Misses': int(ftl.get('CMT_Misses')),
            'Total': int(ftl.get('Total_CMT_Queries'))
        },
        'Maintenance': {
            'GC_Executions': int(ftl.get('Total_GC_Executions')),
            'WL_Executions': int(ftl.get('Total_WL_Executions'))
        }
    }

def plot_ftl_comparison(workload_1, workload_2, workload_3):
    """Vẽ biểu đồ so sánh các thông số FTL"""
    plt.rcParams.update({'font.size': 12})
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    
    # Màu sắc cho các workload
    colors = ['#2ecc71', '#3498db', '#e74c3c']
    width = 0.25
    
    # 1. So sánh các loại lệnh đọc
    read_metrics = ['Normal', 'Multiplane', 'Interleaved']
    x = np.arange(len(read_metrics))
    
    for i, (workload, color) in enumerate([
        (workload_1, colors[0]), 
        (workload_2, colors[1]), 
        (workload_3, colors[2])
    ]):
        values = [workload['Read_Commands'][m] for m in read_metrics]
        bars = ax1.bar(x + i*width, values, width, 
                      label=f'Workload {i+1}', 
                      color=color, alpha=0.8, 
                      edgecolor='black', linewidth=1)
        
        # Thêm giá trị lên các cột
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}',
                    ha='center', va='bottom', fontsize=10)
    
    ax1.set_ylabel('Number of Commands', fontsize=12, fontweight='bold')
    ax1.set_title('Flash Read Commands Comparison', pad=20, fontsize=14, fontweight='bold')
    ax1.set_xticks(x + width)
    ax1.set_xticklabels(read_metrics, fontsize=11)
    ax1.legend(fontsize=11)
    ax1.grid(True, linestyle='--', alpha=0.7)
    
    # 2. So sánh Cache hits/misses
    cache_metrics = ['Hits', 'Misses', 'Total']
    x = np.arange(len(cache_metrics))
    
    for i, (workload, color) in enumerate([
        (workload_1, colors[0]), 
        (workload_2, colors[1]), 
        (workload_3, colors[2])
    ]):
        values = [workload['Cache_Stats'][m] for m in cache_metrics]
        bars = ax2.bar(x + i*width, values, width, 
                      label=f'Workload {i+1}', 
                      color=color, alpha=0.8, 
                      edgecolor='black', linewidth=1)
        
        # Thêm giá trị lên các cột
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height):,}',
                    ha='center', va='bottom', fontsize=10)
    
    ax2.set_ylabel('Number of Operations', fontsize=12, fontweight='bold')
    ax2.set_title('Cache Performance', pad=20, fontsize=14, fontweight='bold')
    ax2.set_xticks(x + width)
    ax2.set_xticklabels(cache_metrics, fontsize=11)
    ax2.legend(fontsize=11)
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    plt.suptitle('FTL Performance Analysis', fontsize=16, fontweight='bold', y=1.05)
    plt.tight_layout()
    plt.savefig('ftl_comparison.png', bbox_inches='tight', dpi=300)
    plt.show()

# Đọc dữ liệu
workload_1 = parse_ftl_metrics('workload_1_scenario_1.xml')
workload_2 = parse_ftl_metrics('workload_2_scenario_1.xml')
workload_3 = parse_ftl_metrics('workload_3_scenario_1.xml')

# Vẽ biểu đồ so sánh
plot_ftl_comparison(workload_1, workload_2, workload_3) 