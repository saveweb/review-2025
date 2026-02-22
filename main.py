import csv

flag = 0
markdown = """# review-2025

WTF happened in 2025?

- 2024 年的年终总结见：[saveweb/review-2024](https://github.com/saveweb/review-2024)
- 2025 年：就是这里！

保持传统，本项目将长期维护（直到2027年初）。

**想要添加您的年终总结？请发 Issue 或编辑 metadata.md 发 PR**
**（不需要填写博客ID，不要编辑 README.md）。**

**删除收录，也可联系 take-down[at]saveweb.org


---

"""

metadata_file = "metadata.csv"
lines = []

def escape(text: str) -> str:
    return text.replace('|', '\\|')

blog_id_set = set()

with open(metadata_file, 'r') as csvfd:
    reader = csv.reader(csvfd)
    header = next(reader)
    for row in reader:
        article_name, article_url, blog, blog_id, archive_url = row
        if blog_id:
            assert blog_id not in blog_id_set, f"Duplicate BlogID found: {blog_id}"
            blog_id_set.add(blog_id)
        assert "|" not in archive_url, f"Archive URL should not contain '|', but got: {archive_url}"
        assert ")" not in archive_url, f"Archive URL should not contain ')', but got: {archive_url}"
        line = f'| [{escape(article_name)} - {escape(blog)}]({article_url}) | {blog_id or "Null"} | {"[IA]" if "archive.org" in archive_url else "[Other]" if archive_url else "Null"}{f"({archive_url})" if archive_url else ""} |'
        lines.append(line)

with open('README.md', 'w') as f:
    f.write(markdown+'计数: '+str(len(lines))+' 篇。下表每次 CI 乱序输出。\n\n')
    f.write('| Article | BlogID | Archive\n')
    f.write('| --- | --- | ---\n')
    f.write('\n'.join(lines))
