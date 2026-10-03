# -*- coding: utf-8 -*-
"""修正补丁脚本：处理 6 处缩进/命名差异的替换点。"""
import sys

PATH = '/Users/zhangyifei/WorkBuddy/2026-10-03-13-06-18/kcc/kindlecomicconverter/KCC_gui.py'
failures = []

with open(PATH, 'r', encoding='utf-8') as f:
    text = f.read()

pairs = [
    # 1. wiki 出错消息（两处缩进不同，分开替换）
    ("                    MW.addMessage.emit('Error during conversion! Please consult '\n"
     "                                       '<a href=\"https://github.com/ciromattia/kcc/wiki/Error-messages\">wiki</a> '\n"
     "                                       'for more details.', 'error', False)",
     "                    MW.addMessage.emit('转换过程中出错！详情请查阅 '\n"
     "                                       '<a href=\"https://github.com/ciromattia/kcc/wiki/Error-messages\">Wiki</a>。', 'error', False)",
     1),
    ("                MW.addMessage.emit('Error during conversion! Please consult '\n"
     "                                   '<a href=\"https://github.com/ciromattia/kcc/wiki/Error-messages\">wiki</a> '\n"
     "                                   'for more details.', 'error', False)",
     "                MW.addMessage.emit('转换过程中出错！详情请查阅 '\n"
     "                                   '<a href=\"https://github.com/ciromattia/kcc/wiki/Error-messages\">Wiki</a>。', 'error', False)",
     1),
    # 2. EPUB 过大提示（续行缩进不同）
    ("MW.addMessage.emit('EPUB file: ' + str(epubSize) + 'MB. Supported size: ~350MB.', 'error',\n"
     "                                               False)",
     "MW.addMessage.emit('EPUB 文件：' + str(epubSize) + 'MB。支持大小：约 350MB。', 'error',\n"
     "                                               False)",
     1),
    # 3. '(multiple files)' 两处命名与缩进不同
    ("                field.setPlaceholderText('(multiple files)')",
     "                field.setPlaceholderText('（多个文件）')", 1),
    ("            self.volumeLine.setPlaceholderText('(multiple files)')",
     "            self.volumeLine.setPlaceholderText('（多个文件）')", 1),
    # 4. GUI.showDialog（非 self.showDialog）
    ('GUI.showDialog("Some files failed to save:\\n\\n" + "\\n".join(errors[:10]) +\n'
     '                              (f"\\n...and {len(errors) - 10} more" if len(errors) > 10 else ""), \'error\')',
     'GUI.showDialog("部分文件保存失败：\\n\\n" + "\\n".join(errors[:10]) +\n'
     '                              (f"\\n…另有 {len(errors) - 10} 个错误未显示" if len(errors) > 10 else ""), \'error\')',
     1),
    # 5. 卷号必须为正数（2 处）
    ("return None, 'Volume numbers must be positive'",
     "return None, '卷号必须为正数'", 2),
    # 6. 表头 文件/值（16 空格缩进）
    ("'<th style=\"padding:2px 6px; text-align:left;\">File</th>'\n"
     "                '<th style=\"padding:2px 6px; text-align:left;\">Value</th>'",
     "'<th style=\"padding:2px 6px; text-align:left;\">文件</th>'\n"
     "                '<th style=\"padding:2px 6px; text-align:left;\">值</th>'", 1),
]

for old, new, expect in pairs:
    n = text.count(old)
    if n != expect:
        failures.append(f'期望 {expect} 处, 实际 {n} 处 -> {old[:70]!r}')
        continue
    text = text.replace(old, new)

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(text)

if failures:
    for f_ in failures:
        print('FAIL:', f_)
    sys.exit(1)
print('修正替换全部成功')
