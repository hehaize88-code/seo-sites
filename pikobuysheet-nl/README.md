# PikobuySheet.nl

Pikobuy 外部商品推荐站。唯一商品数据源为 `https://cnfanshp.com`。

## 技术与目录

- Astro **7.4.0**（实施时核对 npm latest），Node >=22.22。
- Astro 生成 SEO HTML；同一站点 Worker 实时读取主站公开商品页面，提供同源 `/api/catalog/` 和 `/api/product/`。
- 没有数据库、后台、主站管理操作或用户账户系统。内存缓存仅保留 5 分钟。
- 正式 GitHub 目标：`hehaize88-code/seo-sites/pikobuysheet-nl/`，每个域名单独目录。
- 正式域名：`pikobuysheet.nl`。预览部署不修改该域名 DNS。
- GitHub Pages 只能托管静态部分，不能运行此实时适配器；正式运行需要 Worker 等服务端环境。

```sh
npm ci
npm run dev
npm run build
npm run check:source
npm run check:editorial
npm run check:catalog
```

构建输出 `dist/server/index.js` 为标准 Worker ESM 默认导出。静态资源一并封装，避免部署端遗漏资源。`worker/index.mjs` 负责正式请求；Astro 的 `src/pages/api/` 只用于开发预览。不可把 `.astro-out/` 单独部署作为完整功能站。

## 页面与多语言

荷兰语默认 `/`，其他语言采用 `/en/`、`/de/` 等前缀。共 24 种语言，每种包含首页、商品清单、购买指南、QC 指南、运输说明、FAQ、文章目录及 13 篇独立文章、3 个独立商品分类页，共 23 条路由、552 个页面；切换语言保留页面及查询条件。商品原始名称保持主站文本。

包含自引用 canonical、24 语 hreflang 与 x-default、sitemap、WebSite / Article / BreadcrumbList / FAQPage 结构化数据。鞋类、卫衣及 T 恤分类有独立可索引入口；其他筛选、搜索和详情弹窗不生成重复 SEO 页面。正式域名以外及带查询参数的响应添加 noindex。

## 数据契约

- 商品 ID：`/AllProducts/{entryId}.html` 为主站内部条目 ID。
- 购买 ID：从详情的微店链接提取真正 `itemID`；绝不能拿 entryId 生成购买链接。
- 商品图：只取主站 `/uploads/` 中的真实 `data-src`，不取懒加载占位 SVG，不生成替代图。
- USD：读取主站脚本中的 `CNY_TO_USD_RATE`，遵循原脚本的人民币/美元转换规则；未取得规则时返回错误，不猜价格。
- 源站每页 60 条，外站每页 20 条；最后一页按真实下一页链接判断。
- 分类 ID 从主站排序按钮解析，不凭空编造。
- 主站搜索的排序参数会丢失关键词过滤：关键词搜索先读取完整匹配分页，再依据主站价格/浏览量排序。超过 1,200 条提示细化关键词，以限制主站请求量；不会只排序当前 20 件。
- 主站 `shoes` 搜索计数曾显示 325，而完整公开分页实际为 323。排序返回实际可读取数量，并保留源报告数量供诊断。
- 仅短期缓存，不复制维护商品数据库。构建页面中的商品 HTML 是主站当次构建的快照；目录交互和详情实时调用主站。

## 尚未具备的源能力

公开商品页面尚未发现可调用的搜图和商品关联 QC 接口。当前不展示虚假搜图按钮，也不把商品图当 QC 图。QC 页面仅解释检查流程；取得主站真实接口后再接入。

主站 HTML 结构、网络限制或删除商品会影响外站；失败时显示明确错误与重试。没有绕过验证码或访问控制的代码。

## 业务链接

注册：`https://www.pikobuy.com/?mode=register&redirect=/home`

购买：将 `https://weidian.com/item.html?itemID={productId}` 编码为 `https://www.pikobuy.com/product/detail` 的 `productUrl` 参数。没有自行添加邀请码。

Logo / favicon 来源见 `BRAND_ASSETS.md`。页面标明独立商品指南身份。

## 文章、FAQ 与维护

- `/articles/` 为独立文章目录；13 篇文章覆盖选品、服装尺码、链接、QC 测量、预算、包裹体积、鞋码、包袋尺寸、仓库退货和物流停更。原有英文基稿每篇约 780–850 词；2026-10-29 新增运费计算、欧洲配送、仓库合包三篇，每篇约 1,200–1,250 词，并完整翻译至全部 24 语种。
- 首页优先呈现新发布文章，共 4 篇及 24 条可展开 FAQ；`/faq/` 为完整独立页面。每个答案都有官方来源，文章列出核对日期与官方资料。
- 文稿在 `src/content/editorial/<locale>.json`，稳定英文 slug 跨语言保持一致。每语保留全部正文、段落、示例和表格；构建检查拒绝整篇英文回退或内容遗漏。
- 官方及竞争关键词研究在 `docs/research/`；这是搜索意图和内容差异研究，没有搜索量或难度数值。
- 手机端共享紧凑导航，首页装饰图片区收起；文章目录默认折叠，表格改纵向卡片。所有商品页依旧两列、每页20件。
- 预生成 HTML 在构建时按语言分组 gzip 压缩后封入 Worker，请求时按字节偏移读取，最多缓存两个解压后的语种，避免多语言内容造成脚本过大；不增建数据库。
- 新内容发布前执行三项检查：源数据契约回归与全部页面/本地化/结构化数据检查。政策更新须重新核对官方链接及核对日期。

## 2026-10-29 SEO 更新

发布范围、官方事实边界和复查指标见 `docs/SEO_UPDATE_2026-10-29.md`。新增分类采用真实链接导航，服务端输出对应商品；分页和排序维持分类，搜索回到商品总页。实时源失败会终止构建，避免把空商品列表发布到正式站。GA4 新增 `view_item`、`purchase_click`、`signup_click`、`category_select`、`catalog_search`，其中 `purchase_click` 和 `signup_click` 只代表链接点击，不等同于成交或注册完成。
