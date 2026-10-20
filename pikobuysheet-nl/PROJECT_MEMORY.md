# Pikobuy 外站项目记忆

## 2026-10-20：正式域名发布

- 用户明确要求将pikobuysheet.nl部署到GitHub并连接Cloudflare；正式上线授权已取得，取代下文仅预览的限制。
- 已通过当前Chrome把pikobuysheet.nl与www.pikobuysheet.nl绑定到现有Worker pikobuysheet-nl；未创建重复项目。
- wrangler.jsonc持久记录两个Custom Domains；Worker将www和根域HTTP以301统一到https://pikobuysheet.nl，保留路径与查询参数。
- 正式域内容页允许索引；临时workers.dev及带查询条件的页面仍为noindex。canonical/hreflang/sitemap继续使用正式根域。
- 已通过针对性验证：www/HTTP跳转保留语言路径及搜索参数、正式根域可索引、临时预览保持noindex。
- GitHub PR #9准备合并main，Cloudflare生产分支改为main；仍仅监听pikobuysheet-nl/**。后续更新从main的此独立目录自动部署。
- 正式域名HTTPS、线上商品交互与最终部署状态在发布后继续验证；用户项目记忆文件保存最终结果。

## 2026-10-20：公开临时预览部署

- 用户已明确允许通过当前Chrome发布Pikobuy公开临时预览；授权仅针对本项目，正式域名绑定仍待后续。
- 已在现有Cloudflare账户创建Worker pikobuysheet-nl，连接 hehaize88-code/seo-sites 的 codex/pikobuysheet-nl 分支，根目录 pikobuysheet-nl，构建 npm run build，部署 npx wrangler deploy，NODE_VERSION=24。
- 仅监听 pikobuysheet-nl/** 的变更；复用已存在的Workers Builds凭据，没有创建新凭据。
- 公开预览已发布并在当前Chrome实际打开：https://pikobuysheet-nl.hehaize88.workers.dev 。首次构建030896c6-9a37-4c87-8255-30c65f3955c0成功，代码提交9da8f29f92ea5c1807a05e5fb6922507e7b42776。
- 已验证：首页与真实商品图片、20件商品列表、shoes搜索、全结果价格升序及第2页、商品详情与真实微店7721490300购买链接、10篇文章目录及独立正文、文章语言切换保留路径。
- 标题换行时行间空隙可能漏点，文章卡片标题链接改为块级，使整个标题区域可点击；公开预览已验证修正有效。
- 手机实测发现静态商品图片的height=480压过响应式宽度，新增height:auto让图片保持等比例正方形；同时修正首页装饰商品图。其余数据与业务逻辑不变。
- 独立FAQ页24条问答、展开后的官方来源已在线检查。
- workers_dev=true、preview_urls=false；独立预览不混用既有pikobuysheet.cc或pikobuysheet-preview项目。正式域名pikobuysheet.nl仍未绑定，DNS与main未改。
- 下文2026-10-19访问限制仅作历史记录，以本段已验证的workers.dev公开预览为准。

更新：2026-10-19。本轮内容与移动端更新已通过完整构建及全页面检查。

- 本轮需求：FAQ 20+（已核对24条）、10篇独立SEO文章、顶部文章入口、全站手机布局压缩。研究材料存 docs/research/；每条FAQ均有官方来源，每篇文章均有来源与核对日期。
- 24语全文已完整翻译并整合，共240篇文章页面、576条FAQ答案；禁止用英文正文伪装其他语言，禁止删减翻译。
- 新页面范围为每语17条路由，共408页；首页4篇文章及24条折叠FAQ。文章与FAQ在顶部导航有独立入口。
- 10篇文章覆盖选品、服装尺码、原始链接、QC测量、整体预算、包裹体积、鞋码、包袋尺寸、仓库退货及物流停更。英文每篇约780–850词，翻译保留完整134段正文、10张表和数值示例，不声称实际测试或保证运费/时效。
- 所有语言采用相同英文slug、对应canonical/hreflang与完整站点地图。FAQPage仅在独立FAQ页输出；Google已于2026-05停止FAQ富媒体结果，不承诺搜索特殊展示或排名。
- 用户截图确认 chatgpt.site 预览被访问拦截；不能再声称用户可正常打开。原Cloudflare专用连接失效；2026-10-20获授权后已通过Chrome建立替代公开预览。
- 手机端已修改共享布局和各页面类型；文章表格变纵向卡片，目录默认折叠，首页装饰商品区收起，真实商品列表保留。
- 源数据契约检查已通过；本地窄屏检查覆盖首页、清单、指南、QC、运输、FAQ、文章目录及文章正文，320px/390px下没有横向溢出。已通过Astro构建及check:editorial：24语完整性、408个页面、全部正文、导航、canonical/hreflang、sitemap、结构化数据、真实商品快照及压缩Worker响应均通过。

- 用户最新指示：停止主站后台操作；只调用 cnfanshp.com 公开数据制作外部站。主站没有源码仓库，不得再索取。
- 本轮平台 Pikobuy；正式域名 pikobuysheet.nl；目标仓库 hehaize88-code/seo-sites，独立目录 pikobuysheet-nl/。
- 之前出现的 findspreadsheet 是用户笔误。数据、图片唯一来源 cnfanshp.com；不另建数据库。
- 已实现 Astro 7.4.0 SSG + 无数据库的实时读取 Worker。24 语、每页20件商品、12分类、搜索、全结果排序、详情、正确微店购买跳转。文章HTML预压缩封入Worker，请求时流式解压，避免多语言脚本体积过大。
- 官方 Logo 和 favicon 已安装。注册与购买模板见 README，不得添加未经提供的邀请码。
- 核心关键词 pikobuy spreadsheet；相关词 finds、links、shoes、clothing、hoodies、how to buy/use、shipping、QC。研究依据为竞争页与公开搜索，不声称有搜索量/KD 数据。
- 本地普通 Node fetch 已成功读取公开列表、全部分类、搜索分页、详情、价格脚本。早期 Python 客户端出现 1010，不代表所有访问方式均不可用；没有绕过程序。
- 价格按源脚本 CNY_TO_USD_RATE（核对时 7.26），例条目 6045 对应微店 7721490300、USD45.45。
- 已发现源站搜索排序丢失关键词、搜索报告数量和实际分页数量相差 2 的问题，适配器按真实匹配页处理，详见 README。
- 源站公开页面尚未定位搜图/QC 照片接口；暂不实现假功能、不用商品图冒充 QC。
- 生产域名未绑定，未改 DNS、未部署用户主站、未保存后台密码。
- 本地浏览器预览能加载 UI，但该预览服务读取外站出现网络错误；构建容器直接读取成功。不能把本地浏览器中的接口成功当作已验证。
- 预览地址：https://pikobuysheet-nl.hehaize88.chatgpt.site（owner-private），但用户无法打开。
- 标准 Worker 包已检查：首页、英文指南、图标、关键词目录和商品详情均返回 200；真实微店 ID 映射通过。
- 用户与自动化浏览器访问预览域名均被Cloudflare拦截。此为2026-10-19原预览的历史问题；2026-10-20公开workers.dev预览已实际打开并核验数据，用户授权已取得。
- GitHub 源码已准备在 codex/pikobuysheet-nl 分支，正式域名和 main 分支不自动变更。
- 后续继续使用草稿PR https://github.com/hehaize88-code/seo-sites/pull/9；不要新建重复站点或重复PR。发布版本及访问阻塞详情同时记入用户项目记忆文件。
