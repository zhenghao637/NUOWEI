# 地图数据来源与许可

本手册使用真实地理数据绘制离线 SVG，所有地图按同一 Web Mercator 投影定位。序号标签可通过引线避让，地点标记本身不移动。

- 城市及罗佛敦海岸线、道路、水域与核对过的景点位置：© OpenStreetMap contributors，https://www.openstreetmap.org/copyright ，Open Database License (ODbL) 1.0，https://opendatacommons.org/licenses/odbl/1-0/ 。经 Overpass API 提取，日期 2026-09-30。
- 中国与欧洲总览陆地边界：Natural Earth 1:10m Land，https://www.naturalearthdata.com/ ，公有领域。来源为 Natural Earth 官方维护者 nvkelso/natural-earth-vector 的 GeoJSON。
- 罗佛敦两天自驾路线：OSRM 公共路由服务规划的道路几何，底层数据为 OpenStreetMap。仅用于行程规划，不代表实时施工、道路开放或现场许可。
- tools/map_assets.json 是本项目用于这些地图的处理后地理数据，OpenStreetMap 衍生部分按 ODbL 1.0 提供；Natural Earth 部分保持公有领域。

网站访问者无需下载外部地图瓦片，离线版本包含同样的底图。总览航班与邮轮虚线仅连接起终点，不是实际航迹。城市图标出访问地点与顺序，实际步行、交通与驾车导航通过 Google Maps 链接打开。
