# 挪威与英国旅行手册 · 2026年10月2–11日

两人同行。网页正文、SVG地图、样式和交互全部放在 `public/index.html`，没有外部字体、图片、脚本或地图加载依赖。Google导航和官方预约链接仅在点击时打开。

## 一次性部署步骤

使用已创建的 GitHub 仓库 `zhenghao637/NUOWEI`，连接 Cloudflare Workers Free。连接完成后，提交到 `main` 会自动检查并部署。访客直接打开 Cloudflare 给出的正式网址，无须账号或 App。

**GitHub 建仓库和上传文件已处理；剩下的 Cloudflare 登录、授权、配置与查看网址都可以在手机浏览器完成，没有技术上必须用电脑的步骤。全程不要求安装 Node、Git 或 GitHub App。**

| 步骤 | 需要亲手做的操作 | 电脑要求 |
| --- | --- | --- |
| 1 | 登录 Cloudflare，进入 `Workers & Pages → Create application → Import a repository / Connect to Git`。选择 GitHub；授权时选 `Only select repositories`，只选择 `NUOWEI`。 | 手机可做 |
| 2 | 选择 `zhenghao637/NUOWEI` 并填写下面的配置，点击 `Save and Deploy`。Cloudflare 会安装部署依赖并执行检查。账户保持 Workers **Free** 计划。 | 手机可做 |
| 3 | 等部署显示成功，打开 Worker 的 `Visit` / `workers.dev` 正式网址并保存。若首次要求设置账户的 `workers.dev` 子域名，按页面选择一个可用名称。复制面板实际给出的网址，无需购买域名。 | 手机可做 |
| 4 | 用无痕窗口或另一部手机打开网址，确认访客不需要登录。再在手机普通浏览器在线打开一次、停留至缓存完成，断网重开网址确认离线。 | 手机验证 |

仓库根目录应该直接看到 `worker.js`、`wrangler.jsonc` 和 `package.json`，网页路径是 `public/index.html`。当前仓库名称 `NUOWEI` 与 Worker 名称不同是正常的；Cloudflare 面板的 Worker 名称必须与配置文件中的名称一致。

### Cloudflare 需要填写的值

| 配置项 | 填写值 |
| --- | --- |
| Worker / Project name | `norway-uk-travel-2026`，必须与 `wrangler.jsonc` 的 `name` 一致 |
| Production branch | `main` |
| Root directory | 仓库根目录；保留默认值或留空，不要选 `public` |
| Build command | `npm run check` |
| Deploy command | `npm run deploy` |
| API token | 使用 Cloudflare 默认自动生成的部署令牌，无须把令牌填进 GitHub 或聊天 |
| Build variables / secrets | 无须添加；`.nvmrc` 已指定 Node 24 |
| Framework preset | 如出现，选 `None` |

`npm run check` 只检查内容与代码，不编译网页。Cloudflare 会自动安装 `package.json` 中锁定的 Wrangler 部署工具；这些依赖不会被访客的浏览器下载。不要选择 Cloudflare Pages，也不需要 GitHub Actions。正式网址使用 Worker 的 `workers.dev` 地址；此手册不设置访客登录保护。

若部署日志说找不到 `wrangler.jsonc` 或 `public`，先检查有没有多套一层目录。若出现 Worker 名称不一致，保持面板名称与配置文件相同后再部署。

## 后续更新

以后只要把更新后的 HTML 放回同一仓库的 `public/index.html`，提交到 `main`，Cloudflare 就会自动部署。GitHub 网页上也能上传替换这个文件，不要求电脑使用命令行。需要看到生产部署成功后，再刷新公开网址查看。

办完待办、补酒店或租车订单后，告知更新内容，再替换整份 HTML；所有在线访问者都会看到同一份公开清单。离线保存的旧文件要重新下载，浏览器离线缓存要联网刷新后才能获取新内容。页面正文不显示修改日志。

## 部署包备用上传

ZIP 是部署文件的下载备份。如果以后需要另建仓库，建议用电脑解压，进入 `travel-manual` 文件夹，把里面的根文件、`public` 与 `tests`、`tools` 文件夹一起上传到新仓库根目录。保留文件路径；不要上传 ZIP 本身，也不要多套一层 `travel-manual`。这项备用操作建议电脑完成，手机也可分别创建或上传文件。

## 文件作用

| 文件 | 作用 |
| --- | --- |
| `public/index.html` | 可单独打开的完整旅行手册，正文、SVG、CSS、JS和行程数据都内嵌 |
| `worker.js` | Cloudflare 入口，分发 HTML、缓存控制和 `/sw.js` 离线缓存脚本 |
| `wrangler.jsonc` | Worker 名称和静态文件目录配置 |
| `package.json`、`package-lock.json` | 锁定自动部署工具与检查命令 |
| `.nvmrc` | Cloudflare 构建使用 Node 24 |
| `tests/check.mjs` | 检查时区、事件、嵌入资源和导航链接 |
| `tools/build_manual.py` | 用 Python 标准库维护行程和生成 HTML；Cloudflare 不需要运行它 |
| `.gitignore` | 防止本地依赖、临时文件和环境配置被提交 |

网页本身是一份 HTML。为实现“曾在线打开的公开网址，断网后仍能重开”，Worker 额外提供同站点的 `/sw.js` 缓存入口；没有外部服务依赖。首次加载必须在线，浏览器若清空站点数据或处于无痕模式，需要重新在线缓存。导航和预约仍需网络。

下载的 HTML 是另一个离线备份。用可运行网页脚本的浏览器打开可以显示倒计时；手机文件管理器的预览可能只显示静态内容。手机出发前优先验证公开网址的离线重开功能。

维护源文件时可以修改 `tools/build_manual.py`，再用 Python 3 运行它，生成 `public/index.html`。直接替换已生成的 HTML 也能发布；部署过程不会自动重新生成或覆盖它。

## 免费额度

Cloudflare 当前 Workers Free 计划的 Worker 调用额度为每日100,000次。此项目每次页面或离线脚本请求都会经过 Worker，计入该额度；通常两人旅行和亲友查看远低于此限额。保持 Free 计划即可，无需开通付费套餐或绑定自定义域名。

## 已完成的验证

10天行程，86个带明确 UTC 偏移和 IANA 时区的倒计时事件。检查覆盖手机375/390像素布局、上海／伦敦／洛杉矶设备时区结果一致、每秒倒计时、昼夜配色、十天地图展开、全部导航链接、断网刷新和下载文件离线打开；Cloudflare 部署预演通过。

## 官方设置依据

- [Cloudflare Workers Builds](https://developers.cloudflare.com/workers/ci-cd/builds/)
- [构建与部署配置](https://developers.cloudflare.com/workers/ci-cd/builds/configuration/)
- [GitHub 连接](https://developers.cloudflare.com/workers/ci-cd/builds/git-integration/github-integration/)
- [构建环境与 Node 版本](https://developers.cloudflare.com/workers/ci-cd/builds/build-image/)
- [Cloudflare Workers 定价](https://developers.cloudflare.com/workers/platform/pricing/)
