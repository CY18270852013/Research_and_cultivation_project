import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# 读取数据
tcFile = r'C:\Users\Chen Yong\Desktop\Research and cultivation project\IBTrACS.ALL.v04r00.nc'
infile = xr.open_dataset(tcFile)

# 打印数据集的信息，找出所有可用的变量
print(infile)

# 定义要查找的热带气旋ID
storm_ids = [b'2023037S12119', b'2023061S22036']  # 第一个和第二个阶段的SID
titles = ['First Stage Path of Tropical Cyclone Freddy', 'Second Stage Path of Tropical Cyclone Freddy']
figures = []

for storm_id, title in zip(storm_ids, titles):
    # 查找与指定 storm_id 相关的数据
    storm_mask = infile['sid'] == storm_id
    storm_data = infile.where(storm_mask, drop=True)

    # 提取经纬度
    lat = storm_data['usa_lat'].values.flatten()
    lon = storm_data['usa_lon'].values.flatten()

    # 检查经纬度是否存在
    if len(lat) == 0 or len(lon) == 0:
        raise ValueError(f"未找到指定的热带气旋数据：{storm_id}。请检查 SID。")

    # 创建路径图
    fig, ax = plt.subplots(figsize=(20, 10), subplot_kw={'projection': ccrs.PlateCarree(central_longitude=180)})
    ax.set_extent([30, 120, -25, -5])
    ax.coastlines()
    ax.add_feature(cfeature.LAND, edgecolor='black')
    ax.add_feature(cfeature.OCEAN)
    ax.gridlines(draw_labels=True)

    # 绘制路径
    ax.plot(lon, lat, color='red', linewidth=2, transform=ccrs.PlateCarree())
    ax.scatter(lon, lat, c='blue', s=10, transform=ccrs.PlateCarree())

    # 设置标题
    ax.set_title(title, fontsize=20, loc='center')

    # 保存图像
    plt.savefig(f"C:\\Users\\Chen Yong\\Desktop\\Research and cultivation project\\{title.replace(' ', '_').lower()}.png", dpi=300)
    figures.append(fig)

# 强度图绘制
fig, ax = plt.subplots(figsize=(20, 10))
for storm_id in storm_ids:
    storm_mask = infile['sid'] == storm_id
    storm_data = infile.where(storm_mask, drop=True)

    # 提取强度，确保使用正确的变量名
    # 请根据实际情况替换为存在的变量名
    intensity_variable = 'max_sustained_wind'  # 替换为实际的强度数据变量名
    if intensity_variable not in storm_data:
        print(f"未找到强度数据：{intensity_variable}，请检查数据集。")
        continue

    intensity = storm_data[intensity_variable].values.flatten()
    time_data = storm_data['iso_time'].values.flatten()  # 获取时间数据

    # 检查强度数据是否存在
    if len(intensity) == 0:
        continue

    ax.plot(time_data, intensity, label=storm_id.decode('utf-8'))  # 使用decode将bytes转换为字符串

# 设置强度图的标题和标签
ax.set_title('Intensity of Tropical Cyclone Freddy', fontsize=20)
ax.set_xlabel('Date', fontsize=15)
ax.set_ylabel('Max Sustained Wind (knots)', fontsize=15)
ax.legend()
plt.xticks(rotation=45)

# 保存强度图
plt.savefig(r"C:\Users\Chen Yong\Desktop\Research and cultivation project\intensity_tropical_cyclone_freddy.png", dpi=300)
plt.close(fig)

print("所有图像已成功保存。")
