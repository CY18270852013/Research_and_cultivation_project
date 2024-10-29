import xarray as xr
import matplotlib.pyplot as plt
import numpy as np

# 读取netcdf数据
data = xr.open_dataset(r'C:\Users\Chen Yong\Desktop\Research and cultivation project\olr-daily_v01r02-preliminary_20230101_20231219.nc')

# 选取时间范围：2023年1月1日到2023年4月30日，选取经度范围：0到150度
data_selected = data.sel(time=slice('2023-01-01', '2023-04-30'), lon=slice(0, 150))

# 找到符合条件的 lat 的掩码，筛选纬度在 -5 到 5 度之间的数据
lat_mask = (data_selected['lat'] >= -5) & (data_selected['lat'] <= 5)

# 根据掩码选择数据，drop=True 表示丢弃不符合条件的数据
data_5deg = data_selected.where(lat_mask, drop=True)

# 针对纬度维度计算平均值，假设 'olr' 是我们关心的变量
# 将纬度维度上的 OLR 进行平均，从而得到 (time, lon) 维度的数据
data_avg = data_5deg['olr'].mean(dim='lat')

# 提取 'lon' 和 'time' 维度用于绘制图像
lon = data_5deg['lon'].values  # 提取经度
time = data_5deg['time'].values  # 提取时间

# 检查 data_avg 的形状，确保是二维数据
print("data_avg shape: ", data_avg.shape)  # 应该是 (time, lon)

# 确保时间是 datetime 格式的并可以被正确展示
time_num = np.arange(len(time))  # 将时间转化为数值，用于绘制

# 绘制Hovmuller图
fig, ax = plt.subplots(figsize=(12, 8))

# 绘制 OLR 的 Hovmuller 图，数据随时间和经度的变化
im = ax.contourf(lon, time_num, data_avg, cmap='RdBu_r', extend='both')

# 添加网格
ax.grid(True, which='both', linestyle='--', linewidth=0.5)

# 设置时间轴为实际日期标签
num_ticks = 12  # 设置显示 12 个时间刻度
yticks = np.linspace(0, len(time) - 1, num_ticks)  # 生成 12 个等间隔的刻度位置
ax.set_yticks(yticks)

# 生成与刻度相对应的时间标签
yticklabels = np.array([str(t)[:10] for t in time[::len(time)//(num_ticks-1)]])
ax.set_yticklabels(yticklabels)

# 设置横纵坐标标签
ax.set_xlabel('Longitude', fontsize=12)
ax.set_ylabel('Time', fontsize=12)

# 设置标题
ax.set_title('Hovmuller Diagram of OLR (5N-5S Average)', fontsize=14)

# 添加颜色条
cbar = fig.colorbar(im, ax=ax)
cbar.set_label('Outgoing Longwave Radiation (W/m²)', fontsize=12)

# 保存图像
plt.savefig('hovmuller_plot_with_selected_range.png')

# 展示图像
plt.show()
