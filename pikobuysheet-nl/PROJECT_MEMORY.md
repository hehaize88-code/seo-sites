# Pikobuy 外站项目记忆

更新：2026-10-19。

- 用户最新指示：停止主站后台操作；只调用 cnfanshp.com 公开数据制作外部站。主站没有源码仓库，不得再索取。
- 本轮平台 Pikobuy；正式域名 pikobuysheet.nl；目标仓库 hehaize88-code/seo-sites，独立目录 pikobuysheet-nl/。
- 之前出现的 findspreadsheet 是用户笔误。数据、图片唯一来源 cnfanshp.com；不另建数据库。
- 已实现 Astro 7.4.0 SSG + 无数据库的实时读取 Worker。24 语、每语 5 类页面、每页 20 件商品、12 分类、搜索、全结果排序、详情、正确微店购买跳转。
- 官方 Logo 和 favicon 已安装。注册与购买模板见 README，不得添加未经提供的邀请码。
- 核心关键词 pikobuy spreadsheet；相关词 finds、links、shoes、clothing、hoodies、how to buy/use、shipping、QC。研究依据为竞争页与公开搜索，不声称有搜索量/KD 数据。
- 本地普通 Node fetch 已成功读取公开列表、全部分类、搜索分页、详情、价格脚本。早期 Python 客户端出现 1010，不代表所有访问方式均不可用；没有绕过程序。
- 价格按源脚本 CNY_TO_USD_RATE（核对时 7.26），例条目 6045 对应微店 7721490300、USD45.45。
- 已发现源站搜索排序丢失关键词、搜索报告数量和实际分页数量相差 2 的问题，适配器按真实匹配页处理，详见 README。
- 源站公开页面尚未定位搜图/QC 照片接口；暂不实现假功能、不用商品图冒充 QC。
- 生产域名未绑定，未改 DNS、未部署用户主站、未保存后台密码。
- 本地浏览器预览能加载 UI，但该预览服务读取外站出现网络错误；构建容器直接读取成功。不能把本地浏览器中的接口成功当作已验证。
- 发布结果、源码提交与最终验证结果由本轮完成时补充。

## 本轮交付结果

- Sites 预览已发布成功：https://pikobuysheet-nl.hehaize88.chatgpt.site（保持 owner-private）。
- 已发布源码提交：8bd569a432ff669784e77c35b27f69e0064b2f10。
- 真实数据回归检查通过；标准 Worker 包内首页、英文指南、图标、关键词商品接口与商品详情接口均在 Node 运行检查返回 200。
- 当前浏览器访问预览域名被 Cloudflare 拦截，线上浏览器交互仍未验证；不代表用户的浏览器不可访问。
- 源码本轮提交至目标仓库 codex/pikobuysheet-nl 分支；正式域名与 main 分支不自动变更。
