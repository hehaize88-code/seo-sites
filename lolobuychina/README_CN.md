# LoloBuyChina v6

本版新增桌面端 FAQ 和 SEO Articles 区块：

- 顶部导航新增 Guides / FAQ
- 移动端汉堡菜单新增 Guides / FAQ
- 首页新增 4 篇 SEO 文章：下单流程、QC 照片、运费、优惠券
- 首页新增 10 个 FAQ
- 价格继续显示美元
- 商品和目录继续直接跳转到目标源站页面
- 可见页面不展示目标主站名称

部署：上传 `lolobuychina_v6_site` 目录到 lolobuychina.com 根目录。


## v7 手机端压缩说明
- 手机端首页已压缩为 2-3 屏：Hero、4 个精选商品、8 个分类、3 个关键词入口、4 个 SEO Guide 卡片、4 个 FAQ 卡片。
- 桌面端保持完整 FAQ 和 SEO 文章内容。
- 商品和目录仍然直接跳转到 https://cnfanshm.com 对应页面。
- 若想让手机端显示更多商品，把 CSS 中 `#productGrid .card:nth-child(n+5)` 改成 `nth-child(n+7)` 或删除该规则。
