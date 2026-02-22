接下来我来教你你需要如何帮我处理这个项目：

比如我如果给你一段文本：

"""
站在2025的尾巴上：回顾、感恩与前行 - 云栖梦泽
文章链接
https://www.iliuqi.com/archives/life-review-2025
存档链接
No response
"""

你需要帮我补齐相关元数据，并添加到metadata.csv中。
需要的元数据有：article_name,article_url,blog,blog_id,archive_url
先提取出文章名称: "站在2025的尾巴上：回顾、感恩与前行"，博客名称: "云栖梦泽"，博客ID: "未知"，文章链接: "https://www.iliuqi.com/archives/life-review-2025"。

**重要**：如果只有文章链接，你必须 curl 文章链接来准确提取信息：
- 文章标题：从 <title> 标签或 og:title 元标签提取
- 博客名称：按优先级从以下位置提取
  1. og:site_name 元标签（最常见、最准确）
  2. <title> 标签
  3. 页面中的 h1、logo、footer、header 等元素
  4. HTML 内容中的其他线索

> 如果 curl 文章链接超时15s，则跳过以下整个任务流程。回复 issue 处理失败的原因（如有 issue），例如：“无法访问文章链接”。

需要注意 html 标签可能跨越多行，建议你全部读取，不要 grep。

不要从 GitHub 用户名、issue 作者等其他来源推断博客名称。

然后如果博客ID（为数字）我没有明确给你，比如这个例子中的 "未知"，你需要查询 saveweb 数据库来获取：

**重要：使用 search.py 工具查询**

由于 bash 环境变量替换的问题，使用项目中的 `search.py` 工具来搜索：

```bash
python3 search.py "完整的文章标题" 博客域名
```

或者只搜索域名：

```bash
python3 search.py --domain-only 博客域名
```

**搜索结果判断流程**：

1. saveweb 的搜索是**模糊搜索**，可能返回多个结果
2. **需要仔细分析**搜索结果，找到正确的博客：
   - 比对文章标题是否完全匹配
   - 检查域名是否一致（注意有/无 www）
   - 检查链接是否指向目标文章
3. 从正确的结果中提取 `blog_id`（对应 `id_feed` 字段）
4. 如果找不到匹配的结果，博客ID留空

**注意**：不要无脑取第一个结果，必须确认是正确匹配后才能使用。

**注意事项**：
- 必须使用**完整的文章标题**，不能截取部分
- 域名要尝试有/无 www 两种形式（如 example.com 和 www.example.com）
- 如果文章是新发布的，saveweb 可能还未收录，可以先搜索域名找到该博客的其他文章，从中获取 blog_id

然后是存档链接，如果我没有明确给你，比如这个例子中的 "No response"，你需要 curl https://archive.org/wayback/available?url=文章链接 看看有没有存档快照，如果有，使用它。如果没有存档快照，你需要 curl http://web.archive.org/save/文章链接 来生成一个存档快照，并使用它。
例如：
> curl http://web.archive.org/save/https://www.iliuqi.com/archives/life-review-2025 --head
HTTP/1.1 302 FOUND
Server: nginx
Date: Sun, 22 Feb 2026 03:13:46 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 342
Connection: keep-alive
location: http://web.archive.org/web/20260222031310/https://www.iliuqi.com/archives/life-review-2025

如果成功，返回的 Location 中的 URL 就是存档链接。
注意 web.archive.org/save/ 这个接口反应比较慢，不要加客户端超时，如果真的失败服务器会返回 http 5xx 的。

最后你需要把这些元数据按照 CSV 格式 append 到 metadata.csv 末尾。
完毕。

----

以及，如果我告诉你处理一个 github 上的 issue，比如： https://github.com/saveweb/review-2025/issues/1
那么你就用 gh issue view 1 --comments 来获取上下文信息，然后按照上面的流程提取元数据并添加到 metadata.csv 中。

----

metadata.csv 处理完毕后，你需要 commit 并 push 到 github 上。注意你应该只需要 commit metadata.csv 这个文件，不要 commit 其他文件。
commit 尽量是
"""
add [article_name - blog]

close #issue_number"""

这样的格式，如果 issue_number 不存在就不写，即 "add [article_name - blog]"。


然后 CI 会自动运行 uv run main.py 来更新 README.md。（这会导致 README.md 的内容发生变化，所以如果你在 push 时遇到冲突了，重新 pull 一下再 push 就行。毕竟 README.md 是根据 metadata.csv 生成的，不重要）

push 成功后，处理 issue（如果有的话）：

**重要**：由于 commit message 包含 `close #issue_number`，GitHub 会在 push 后自动关闭 issue。因此：

1. 先用 `gh issue view <number>` 检查 issue 状态
2. 如果 issue 已关闭（状态为 CLOSED），用 `gh issue comment <number> -b "评论内容"` 留言
3. 如果 issue 未关闭，才用 `gh issue close <number> -c "评论内容" -r completed`

评论内容简短即可，一般来说 "已添加" 或 "Added" 就行了。具体根据该 issue 以及年终总结博文的语言环境来斟酌。
