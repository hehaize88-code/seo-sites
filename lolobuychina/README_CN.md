# LoloBuyChina v8 搜索联通主站版

本版本已部署到 GitHub 仓库 `hehaize88-code/seo-sites` 的 `lolobuychina/` 文件夹。

## 本版功能

- 网站可见品牌为 LoloBuyChina。
- 商品卡片直接跳转到目标产品详情页，不再做本地重复产品详情。
- 产品目录直接跳转到对应分类页。
- 价格以美元显示，页面标注最终结算以实际平台汇率和代理结账为准。
- 手机端压缩为 2-3 屏，保留汉堡菜单、语言、精选、目录、SEO 文章和 FAQ 入口。
- 顶部语言下拉支持 EN / ES / FR / DE / IT / PT / JA / KO / ZH，点击后当前页面即时切换文案。
- 搜索框已联通主站：
  - `shoes / sneaker / jordans` → `/shoes/`
  - `hoodie / sweater / sweatshirts` → `/hoodies-sweaters/`
  - `t-shirt / tee / shirts` → `/t-shirts/`
  - `pants / shorts / jeans` → `/pants-shorts/`
  - `accessories / bag / wallet / belt` → `/accessories/`
  - 示例商品 ID 或标题 → 对应产品详情页
  - 其他关键词 → `/AllProducts/?keyword=关键词`

## 部署位置

```text
seo-sites/lolobuychina/
```

Cloudflare Pages 对应域名：

```text
https://lolobuychina.com/
```

## 注意

`/AllProducts/?keyword=关键词` 已由外部站传参。若要让所有关键词都显示精准搜索结果，需要目标站 `/AllProducts/` 页面支持读取 `keyword` 参数并执行筛选。
