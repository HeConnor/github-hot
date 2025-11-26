# github-hot

> copy from: [github-hot](https://github.com/shibing624/github-hot)

Tracking the hot Github repos and update daily

1. Automatically grab popular projects every day based on Github Actions [.github/workflows/schedule.yml](.github/workflows/schedule.yml)
2. Support project list output in markdown format, automatically synchronized to github
3. Support custom sorting, select topk hot interest repos

## Usage
```bash
git clone github-hot.git
cd github-hot
pip install -r requirements.txt
python crawler.py
```

<details>
   <summary>👉 点击展开：<strong>ntfy 推送</strong>（开源免费，支持自托管）</summary>
   <br>

   **两种使用方式：**

   ### 方式一：免费使用（推荐新手） 🆓

   **特点**：
   - ✅ 无需注册账号，立即使用
   - ✅ 每天 250 条消息（足够 90% 用户）
   - ✅ Topic 名称即"密码"（需选择不易猜测的名称）
   - ⚠️ 消息未加密，不适合敏感信息, 但适合我们这个项目的不敏感信息

   **快速开始：**

   1. **下载 ntfy 应用**：
      - Android：[Google Play](https://play.google.com/store/apps/details?id=io.heckel.ntfy) / [F-Droid](https://f-droid.org/en/packages/io.heckel.ntfy/)
      - iOS：[App Store](https://apps.apple.com/us/app/ntfy/id1625396347)
      - 桌面：访问 [ntfy.sh](https://ntfy.sh)

   2. **订阅主题**（选择一个难猜的名称）：
      ```
      建议格式：trendradar-{你的名字缩写}-{随机数字}
   
      不能使用中文
      
      ✅ 好例子：trendradar-zs-8492
      ❌ 坏例子：news、alerts（太容易被猜到）
      ```

   3. **配置 GitHub Secret（⚠️ Name 名称必须严格一致）**：
      - **Name（名称）**：`NTFY_TOPIC`（请复制粘贴此名称，不要手打）
      - **Secret（值）**：填写你刚才订阅的主题名称

      - **Name（名称）**：`NTFY_SERVER_URL`（可选配置，请复制粘贴此名称）
      - **Secret（值）**：留空（默认使用 ntfy.sh）

      - **Name（名称）**：`NTFY_TOKEN`（可选配置，请复制粘贴此名称）
      - **Secret（值）**：留空

      **说明**：ntfy 至少需要配置 1 个必需 Secret (NTFY_TOPIC)，后两个为可选配置

   4. **测试**：
      ```bash
      curl -d "测试消息" ntfy.sh/你的主题名称
      ```

   ---

   ### 方式二：自托管（完全隐私控制） 🔒

   **适合人群**：有服务器、追求完全隐私、技术能力强

   **优势**：
   - ✅ 完全开源（Apache 2.0 + GPLv2）
   - ✅ 数据完全自主控制
   - ✅ 无任何限制
   - ✅ 零费用

   **Docker 一键部署**：
   ```bash
   docker run -d \
     --name ntfy \
     -p 80:80 \
     -v /var/cache/ntfy:/var/cache/ntfy \
     binwiederhier/ntfy \
     serve --cache-file /var/cache/ntfy/cache.db
   ```

   **配置 TrendRadar**：
   ```yaml
   NTFY_SERVER_URL: https://ntfy.yourdomain.com
   NTFY_TOPIC: trendradar-alerts  # 自托管可用简单名称
   NTFY_TOKEN: tk_your_token  # 可选：启用访问控制
   ```

   **在应用中订阅**：
   - 点击"Use another server"
   - 输入你的服务器地址
   - 输入主题名称
   - （可选）输入登录凭据

   ---

   **常见问题：**

   <details>
   <summary><strong>Q1: 免费版够用吗？</strong></summary>

   每天 250 条消息对大多数用户足够。按 30 分钟抓取一次计算，每天约 48 次推送，完全够用。
   </details>

   <details>
   <summary><strong>Q2: Topic 名称真的安全吗？</strong></summary>

   如果你选择随机的、足够长的名称（如 `trendradar-zs-8492-news`），暴力破解几乎不可能：
   - ntfy 有严格的速率限制（1 秒 1 次请求）
   - 64 个字符选择（A-Z, a-z, 0-9, _, -）
   - 10 位随机字符串有 64^10 种可能性（需要数年才能破解）
   </details>

   ---

   **推荐选择：**

   | 用户类型 | 推荐方案 | 理由 |
   |---------|---------|------|
   | 普通用户 | 方式一（免费） | 简单快速，够用 |
   | 技术用户 | 方式二（自托管） | 完全控制，无限制 |
   | 高频用户 | 方式三（付费） | 这个自己去官网看吧 |

   **相关链接：**
   - [ntfy 官方文档](https://docs.ntfy.sh/)
   - [自托管教程](https://docs.ntfy.sh/install/)
   - [GitHub 仓库](https://github.com/binwiederhier/ntfy)

   </details>

   <details>
   <summary>👉 点击展开：<strong>Bark 推送</strong>（iOS 专属，简洁高效）</summary>
   <br>

   **GitHub Secret 配置（⚠️ Name 名称必须严格一致）：**
   - **Name（名称）**：`BARK_URL`（请复制粘贴此名称，不要手打）
   - **Secret（值）**：你的 Bark 推送 URL

   <br>

   **Bark 简介：**

   Bark 是一款 iOS 平台的免费开源推送工具，特点是简单、快速、无广告。

   **使用方式：**

   ### 方式一：使用官方服务器（推荐新手） 🆓

   1. **下载 Bark App**：
      - iOS：[App Store](https://apps.apple.com/cn/app/bark-给你的手机发推送/id1403753865)

   2. **获取推送 URL**：
      - 打开 Bark App
      - 复制首页显示的推送 URL（格式如：`https://api.day.app/your_device_key`）
      - 将 URL 配置到 GitHub Secrets 中的 `BARK_URL`

   ### 方式二：自建服务器（完全隐私控制） 🔒

   **适合人群**：有服务器、追求完全隐私、技术能力强

   **Docker 一键部署**：
   ```bash
   docker run -d \
     --name bark-server \
     -p 8080:8080 \
     finab/bark-server
   ```

   **配置 TrendRadar**：
   ```yaml
   BARK_URL: http://your-server-ip:8080/your_device_key
   ```

   ---

   **注意事项：**
   - ✅ Bark 使用 APNs 推送，单条消息最大 4KB
   - ✅ 支持自动分批推送，无需担心消息过长
   - ✅ 推送格式为纯文本（自动去除 Markdown 语法）
   - ⚠️ 仅支持 iOS 平台

   **相关链接：**
   - [Bark 官方网站](https://bark.day.app/)
   - [Bark GitHub 仓库](https://github.com/Finb/Bark)
   - [Bark Server 自建教程](https://github.com/Finb/bark-server)

   </details>

### Result

<img src="./docs/pic.png" width="860" />


## License

授权协议为 [The Apache License 2.0](LICENSE)，可免费用做商业用途。请在产品说明中附加**github-hot**的链接和授权协议。


## Contribute
项目代码还很粗糙，如果大家对代码有所改进，欢迎提交回本项目，在提交之前，注意以下两点：

 - 在`tests`添加相应的单元测试
 - 使用`python -m pytest`来运行所有单元测试，确保所有单测都是通过的

之后即可提交PR。


## Related Projects

- javascript：[vitalets/github-trending-repos](https://github.com/vitalets/github-trending-repos)
