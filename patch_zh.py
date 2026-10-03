# -*- coding: utf-8 -*-
"""KCC 本地化改造脚本：界面中文化、设备列表精简/新增、禁用更新检测。"""
import re
import sys

BASE = '/Users/zhangyifei/WorkBuddy/2026-10-03-13-06-18/kcc/kindlecomicconverter/'
failures = []


def apply_replacements(path, pairs):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    for old, new, expect in pairs:
        n = text.count(old)
        if n != expect:
            failures.append(f'{path}: 期望 {expect} 处, 实际 {n} 处 -> {old[:80]!r}')
            continue
        text = text.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


def apply_regex(path, pattern, new, expect=1, flags=re.DOTALL):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    text2, n = re.subn(pattern, lambda m: new, text, flags=flags)
    if n != expect:
        failures.append(f'{path}: 正则期望 {expect} 处, 实际 {n} 处 -> {pattern[:80]!r}')
        return
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text2)


GUI = BASE + 'KCC_gui.py'

# ============ 1. KCC_gui.py：禁用更新检测 ============
apply_regex(
    GUI,
    r"    def run\(self\):\n        if self\.startNumber2 < 5:.*?\n    def setAnswer",
    "    def run(self):\n"
    "        # 更新检测与推广公告已在本地化改造中禁用\n"
    "        return\n"
    "\n"
    "    def setAnswer",
    expect=1,
)
apply_replacements(GUI, [(
    "        self.worker.sync()\n        self.versionCheck.start()\n        self.tray.show()",
    "        self.worker.sync()\n        # self.versionCheck.start()  # 更新检测已禁用\n        self.tray.show()",
    1)])

# ============ 2. KCC_gui.py：设备列表与格式 ============
NEW_PROFILES = '''        self.profiles = {
            # ---- Kindle（仅保留 Oasis / Scribe / Paperwhite / Colorsoft 四个系列）----
            "Kindle Paperwhite 12": {'PVOptions': True, 'ForceExpert': False, 'DefaultFormat': 0,
                       'DefaultUpscale': True, 'ForceColor': False, 'Label': 'KPW6'},
            "Kindle Paperwhite 11": {'PVOptions': True, 'ForceExpert': False, 'DefaultFormat': 0,
                       'DefaultUpscale': True, 'ForceColor': False, 'Label': 'KPW5'},
            "Kindle Paperwhite 7/10": {'PVOptions': True, 'ForceExpert': False, 'DefaultFormat': 0,
                              'DefaultUpscale': True, 'ForceColor': False, 'Label': 'KPW34'},
            "Kindle Paperwhite 5/6": {'PVOptions': True, 'ForceExpert': False, 'DefaultFormat': 0,
                              'DefaultUpscale': False, 'ForceColor': False, 'Label': 'KPW'},
            "Kindle Oasis 9/10": {'PVOptions': True, 'ForceExpert': False, 'DefaultFormat': 0,
                                 'DefaultUpscale': True, 'ForceColor': False, 'Label': 'KO'},
            "Kindle Oasis 8": {'PVOptions': True, 'ForceExpert': False, 'DefaultFormat': 0,
                             'DefaultUpscale': True, 'ForceColor': False, 'Label': 'KPW34'},
            "Kindle Scribe 1/2": {'PVOptions': True, 'ForceExpert': False, 'DefaultFormat': 0,
                                  'DefaultUpscale': False, 'ForceColor': False, 'Label': 'KS'},
            "Kindle Scribe 3": {'PVOptions': True, 'ForceExpert': False, 'DefaultFormat': 4,
                                'DefaultUpscale': False, 'ForceColor': False, 'Label': 'KS3'},
            "Kindle Scribe Colorsoft": {'PVOptions': True, 'ForceExpert': False, 'DefaultFormat': 4,
                                        'DefaultUpscale': False, 'ForceColor': True, 'Label': 'KSCS'},
            "Kindle Colorsoft": {'PVOptions': True, 'ForceExpert': False, 'DefaultFormat': 0,
                                 'DefaultUpscale': True, 'ForceColor': True, 'Label': 'KCS'},
            # ---- 掌阅 iReader（同分辨率并列，彩色 C 型单独列出）----
            "掌阅 Ocean 1": {'PVOptions': False, 'ForceExpert': False, 'DefaultFormat': 1,
                             'DefaultUpscale': True, 'ForceColor': False, 'Label': 'iRO1'},
            "掌阅 Ocean 2 / 3 / 3 Turbo / 4 / 4 Turbo": {'PVOptions': False, 'ForceExpert': False, 'DefaultFormat': 1,
                             'DefaultUpscale': True, 'ForceColor': False, 'Label': 'iRO234'},
            "掌阅 Ocean 5 / 5 Pro": {'PVOptions': False, 'ForceExpert': False, 'DefaultFormat': 1,
                             'DefaultUpscale': True, 'ForceColor': False, 'Label': 'iRO5'},
            "掌阅 Ocean 4 Plus": {'PVOptions': False, 'ForceExpert': False, 'DefaultFormat': 1,
                             'DefaultUpscale': True, 'ForceColor': False, 'Label': 'iRO4P'},
            "掌阅 Ocean 4C / 5C": {'PVOptions': False, 'ForceExpert': False, 'DefaultFormat': 1,
                             'DefaultUpscale': True, 'ForceColor': True, 'Label': 'iRO45C'},
            "掌阅 Leaf 2 / 3": {'PVOptions': False, 'ForceExpert': False, 'DefaultFormat': 1,
                             'DefaultUpscale': True, 'ForceColor': False, 'Label': 'iRLF23'},
            "掌阅 Leaf 5 / 5+": {'PVOptions': False, 'ForceExpert': False, 'DefaultFormat': 1,
                             'DefaultUpscale': True, 'ForceColor': False, 'Label': 'iRLF5'},
            "掌阅 Leaf 3C / 5C": {'PVOptions': False, 'ForceExpert': False, 'DefaultFormat': 1,
                             'DefaultUpscale': True, 'ForceColor': True, 'Label': 'iRLF35C'},
            # ---- 汉王 Hanvon ----
            "汉王 Clear 6": {'PVOptions': False, 'ForceExpert': False, 'DefaultFormat': 1,
                             'DefaultUpscale': True, 'ForceColor': False, 'Label': 'HVCL6'},
            "汉王 Clear 6 Pro / 6 Pro 二代 / 6 Turbo": {'PVOptions': False, 'ForceExpert': False, 'DefaultFormat': 1,
                             'DefaultUpscale': True, 'ForceColor': False, 'Label': 'HVCL6P'},
            "汉王 Clear 7 / 7 Turbo": {'PVOptions': False, 'ForceExpert': False, 'DefaultFormat': 1,
                             'DefaultUpscale': True, 'ForceColor': False, 'Label': 'HVCL7'},
            "汉王 Clear 7 Turbo+": {'PVOptions': False, 'ForceExpert': False, 'DefaultFormat': 1,
                             'DefaultUpscale': True, 'ForceColor': False, 'Label': 'HVCL7TP'},
            "汉王 Clear 7C": {'PVOptions': False, 'ForceExpert': False, 'DefaultFormat': 1,
                             'DefaultUpscale': True, 'ForceColor': True, 'Label': 'HVCL7C'},
            # ---- 文石 BOOX ----
            "文石 Poke 2 / 3 / 4 / 4 Lite": {'PVOptions': False, 'ForceExpert': False, 'DefaultFormat': 1,
                             'DefaultUpscale': True, 'ForceColor': False, 'Label': 'BxPK234'},
            "文石 Poke 5": {'PVOptions': False, 'ForceExpert': False, 'DefaultFormat': 1,
                             'DefaultUpscale': True, 'ForceColor': False, 'Label': 'BxPK5'},
            "文石 Go 6": {'PVOptions': False, 'ForceExpert': False, 'DefaultFormat': 1,
                             'DefaultUpscale': True, 'ForceColor': False, 'Label': 'BxGO6'},
            "文石 Page": {'PVOptions': False, 'ForceExpert': False, 'DefaultFormat': 1,
                             'DefaultUpscale': True, 'ForceColor': False, 'Label': 'BxPG'},
            "文石 Go 7": {'PVOptions': False, 'ForceExpert': False, 'DefaultFormat': 1,
                             'DefaultUpscale': True, 'ForceColor': False, 'Label': 'BxGO7'},
            "文石 Go Color 7 / (Gen II)": {'PVOptions': False, 'ForceExpert': False, 'DefaultFormat': 1,
                             'DefaultUpscale': True, 'ForceColor': True, 'Label': 'BxGC7'},
            # ---- 其他 ----
            "其他": {'PVOptions': False, 'ForceExpert': True, 'DefaultFormat': 1, 'DefaultUpscale': False, 'ForceColor': False,
                      'Label': 'OTHER'},
        }
        profilesGUI = [
            "Kindle Paperwhite 12",
            "Kindle Paperwhite 11",
            "Kindle Colorsoft",
            "Kindle Scribe Colorsoft",
            "Kindle Scribe 3",
            "Kindle Scribe 1/2",
            "Kindle Oasis 9/10",
            "Kindle Oasis 8",
            "Kindle Paperwhite 7/10",
            "Kindle Paperwhite 5/6",
            "Separator",
            "掌阅 Ocean 2 / 3 / 3 Turbo / 4 / 4 Turbo",
            "掌阅 Ocean 5 / 5 Pro",
            "掌阅 Ocean 4C / 5C",
            "掌阅 Ocean 4 Plus",
            "掌阅 Ocean 1",
            "掌阅 Leaf 2 / 3",
            "掌阅 Leaf 5 / 5+",
            "掌阅 Leaf 3C / 5C",
            "Separator",
            "汉王 Clear 7 / 7 Turbo",
            "汉王 Clear 7 Turbo+",
            "汉王 Clear 7C",
            "汉王 Clear 6 Pro / 6 Pro 二代 / 6 Turbo",
            "汉王 Clear 6",
            "Separator",
            "文石 Poke 2 / 3 / 4 / 4 Lite",
            "文石 Poke 5",
            "文石 Go 6",
            "文石 Page",
            "文石 Go 7",
            "文石 Go Color 7 / (Gen II)",
            "Separator",
            "其他",
        ]'''

apply_regex(
    GUI,
    r"        self\.profiles = \{.*?profilesGUI = \[.*?\n        \]",
    NEW_PROFILES,
    expect=1,
)

# 图标循环：Kobo/reMarkable 图标分支已无用
apply_replacements(GUI, [(
    '''        for profile in profilesGUI:
            if profile == "Other":
                GUI.deviceBox.addItem(self.icons.deviceOther, profile)
            elif profile == "Separator":
                GUI.deviceBox.insertSeparator(GUI.deviceBox.count() + 1)
            elif 'reM' in profile:
                GUI.deviceBox.addItem(self.icons.deviceRmk, profile)
            elif 'Ko' in profile:
                GUI.deviceBox.addItem(self.icons.deviceKobo, profile)
            else:
                GUI.deviceBox.addItem(self.icons.deviceKindle, profile)''',
    '''        for profile in profilesGUI:
            if profile == "其他":
                GUI.deviceBox.addItem(self.icons.deviceOther, profile)
            elif profile == "Separator":
                GUI.deviceBox.insertSeparator(GUI.deviceBox.count() + 1)
            else:
                GUI.deviceBox.addItem(self.icons.deviceKindle, profile)''',
    1)])

# 默认设备：Kindle Paperwhite 12（新列表第 1 项，索引 0）
apply_replacements(GUI, [(
    "        # default is Kindle Paperwhite 12th Gen\n        self.lastDevice = self.settings.value('lastDevice', 3, type=int)",
    "        # 默认设备：Kindle Paperwhite 12（第 12 代）\n        self.lastDevice = self.settings.value('lastDevice', 0, type=int)",
    1)])

# “其他”设备判断
apply_replacements(GUI, [(
    "        if str(GUI.deviceBox.currentText()) == 'Other':\n"
    "            self.addMessage('<a href=\"https://github.com/ciromattia/kcc/wiki/NonKindle-devices\">'\n"
    "                            'List of supported Non-Kindle devices.</a>', 'info')",
    "        if str(GUI.deviceBox.currentText()) == '其他':\n"
    "            self.addMessage('<a href=\"https://github.com/ciromattia/kcc/wiki/NonKindle-devices\">'\n"
    "                            '查看支持的其他设备列表。</a>', 'info')",
    1)])

# 输出格式显示名
apply_replacements(GUI, [
    ('"Folder of images": {\'icon\': \'FOLDER\', \'format\': \'FOLDER\'}',
     '"图像文件夹": {\'icon\': \'FOLDER\', \'format\': \'FOLDER\'}', 1),
    ('"PDF (200MB limit)": {\'icon\': \'EPUB\', \'format\': \'PDF-200MB\'}',
     '"PDF（200MB 限制）": {\'icon\': \'EPUB\', \'format\': \'PDF-200MB\'}', 1),
    ('"KFX (Send to Kindle EPUB)": {\'icon\': \'KFX\', \'format\': \'KFX\'}',
     '"KFX（发送到 Kindle 的 EPUB）": {\'icon\': \'KFX\', \'format\': \'KFX\'}', 1),
    ('"EPUB (200MB limit)": {\'icon\': \'EPUB\', \'format\': \'EPUB-200MB\'}',
     '"EPUB（200MB 限制）": {\'icon\': \'EPUB\', \'format\': \'EPUB-200MB\'}', 1),
    ('"MOBI + EPUB (200MB limit)": {\'icon\': \'MOBI\', \'format\': \'MOBI+EPUB-200MB\'}',
     '"MOBI + EPUB（200MB 限制）": {\'icon\': \'MOBI\', \'format\': \'MOBI+EPUB-200MB\'}', 1),
])

# ============ 3. KCC_gui.py：界面消息中文化 ============
apply_replacements(GUI, [
    # 转换中断
    ("MW.addMessage.emit('<b>Conversion interrupted.</b>', 'error', False)",
     "MW.addMessage.emit('<b>转换已中断。</b>', 'error', False)", 1),
    ("MW.addTrayMessage.emit('Conversion interrupted.', 'Critical')",
     "MW.addTrayMessage.emit('转换已中断。', 'Critical')", 1),
    # 文件融合
    ("MW.addMessage.emit('Attempting file fusion', 'info', False)",
     "MW.addMessage.emit('正在尝试文件融合', 'info', False)", 1),
    ("MW.addMessage.emit('Created fusion at ' + currentJobs[0], 'info', False)",
     "MW.addMessage.emit('融合文件已创建：' + currentJobs[0], 'info', False)", 1),
    ("print('Fusion Failed. ' + str(e))\n                MW.addMessage.emit('Fusion Failed. ' + str(e), 'error', True)",
     "print('文件融合失败。' + str(e))\n                MW.addMessage.emit('文件融合失败。' + str(e), 'error', True)", 1),
    (r"error_message = 'Process Failed. Custom title can\'t be set when processing more than 1 source.\nDid you forget to check fusion?'",
     r"error_message = '处理失败：处理多个来源时无法设置自定义标题。\n是否忘记勾选「文件融合」？'", 1),
    # 来源与进度
    ("MW.addMessage.emit(f'<b>{job_progress_number}Source:</b> ' + job, 'info', False)",
     "MW.addMessage.emit(f'<b>{job_progress_number}来源：</b> ' + job, 'info', False)", 1),
    ("MW.addMessage.emit('Creating CBZ files', 'info', False)\n                GUI.progress.content = 'Creating CBZ files'",
     "MW.addMessage.emit('正在创建 CBZ 文件', 'info', False)\n                GUI.progress.content = '正在创建 CBZ 文件'", 1),
    ("MW.addMessage.emit('Creating folders', 'info', False)\n                GUI.progress.content = 'Creating folders'",
     "MW.addMessage.emit('正在创建文件夹', 'info', False)\n                GUI.progress.content = '正在创建文件夹'", 1),
    ("MW.addMessage.emit('Creating PDF files', 'info', False)\n                GUI.progress.content = 'Creating PDF files'",
     "MW.addMessage.emit('正在创建 PDF 文件', 'info', False)\n                GUI.progress.content = '正在创建 PDF 文件'", 1),
    ("MW.addMessage.emit('Creating EPUB files', 'info', False)\n                GUI.progress.content = 'Creating EPUB files'",
     "MW.addMessage.emit('正在创建 EPUB 文件', 'info', False)\n                GUI.progress.content = '正在创建 EPUB 文件'", 1),
    # 转换出错（2 处相同代码块）
    ("MW.addMessage.emit('Error during conversion! Please consult '\n"
     "                                       '<a href=\"https://github.com/ciromattia/kcc/wiki/Error-messages\">wiki</a> '\n"
     "                                       'for more details.', 'error', False)",
     "MW.addMessage.emit('转换过程中出错！详情请查阅 '\n"
     "                                       '<a href=\"https://github.com/ciromattia/kcc/wiki/Error-messages\">Wiki</a>。', 'error', False)", 2),
    ("MW.addTrayMessage.emit('Error during conversion!', 'Critical')",
     "MW.addTrayMessage.emit('转换过程中出错！', 'Critical')", 2),
    ("MW.showDialog.emit(\"Error during conversion %s:\\n\\n%s\\n\\nTraceback:\\n%s\"\n"
     "                                   % (jobargv[-1], str(err), sanitizeTrace(traceback)), 'error')",
     "MW.showDialog.emit(\"转换 %s 时出错：\\n\\n%s\\n\\n回溯信息：\\n%s\"\n"
     "                                   % (jobargv[-1], str(err), sanitizeTrace(traceback)), 'error')", 1),
    # 完成消息
    ("MW.addMessage.emit('Creating CBZ files... <b>Done!</b>', 'info', True)",
     "MW.addMessage.emit('正在创建 CBZ 文件... <b>完成！</b>', 'info', True)", 1),
    ("MW.addMessage.emit('Creating folders... <b>Done!</b>', 'info', True)",
     "MW.addMessage.emit('正在创建文件夹... <b>完成！</b>', 'info', True)", 1),
    ("MW.addMessage.emit('Creating PDF files... <b>Done!</b>', 'info', True)",
     "MW.addMessage.emit('正在创建 PDF 文件... <b>完成！</b>', 'info', True)", 1),
    ("MW.addMessage.emit('Creating EPUB files... <b>Done!</b>', 'info', True)",
     "MW.addMessage.emit('正在创建 EPUB 文件... <b>完成！</b>', 'info', True)", 1),
    ("MW.progressBarTick.emit(f'{job_progress_number}Creating MOBI files')",
     "MW.progressBarTick.emit(f'{job_progress_number}正在创建 MOBI 文件')", 1),
    ("MW.addMessage.emit('Creating MOBI files', 'info', False)\n                    GUI.progress.content = 'Creating MOBI files'",
     "MW.addMessage.emit('正在创建 MOBI 文件', 'info', False)\n                    GUI.progress.content = '正在创建 MOBI 文件'", 1),
    ("MW.addMessage.emit('Creating MOBI files... <b>Done!</b>', 'info', True)",
     "MW.addMessage.emit('正在创建 MOBI 文件... <b>完成！</b>', 'info', True)", 1),
    ("MW.addMessage.emit('Processing MOBI files', 'info', False)\n                        GUI.progress.content = 'Processing MOBI files'",
     "MW.addMessage.emit('正在处理 MOBI 文件', 'info', False)\n                        GUI.progress.content = '正在处理 MOBI 文件'", 1),
    ("MW.addMessage.emit('Processing MOBI files... <b>Done!</b>', 'info', True)",
     "MW.addMessage.emit('正在处理 MOBI 文件... <b>完成！</b>', 'info', True)", 1),
    ("MW.addMessage.emit('Kindle detected. Uploading covers... <b>Done!</b>', 'info', False)",
     "MW.addMessage.emit('检测到 Kindle，正在上传封面... <b>完成！</b>', 'info', False)", 1),
    ("MW.addMessage.emit('Failed to process MOBI file!', 'error', False)\n                            MW.addTrayMessage.emit('Failed to process MOBI file!', 'Critical')",
     "MW.addMessage.emit('MOBI 文件处理失败！', 'error', False)\n                            MW.addTrayMessage.emit('MOBI 文件处理失败！', 'Critical')", 1),
    ("MW.addMessage.emit('KindleGen failed to create MOBI!', 'error', False)\n                        MW.addMessage.emit(self.kindlegenErrorCode[1], 'error', False)\n                        MW.addTrayMessage.emit('KindleGen failed to create MOBI!', 'Critical')",
     "MW.addMessage.emit('KindleGen 创建 MOBI 失败！', 'error', False)\n                        MW.addMessage.emit(self.kindlegenErrorCode[1], 'error', False)\n                        MW.addTrayMessage.emit('KindleGen 创建 MOBI 失败！', 'Critical')", 1),
    ("MW.showDialog.emit(\"KindleGen error:\\n\\n\" + self.kindlegenErrorCode[1], 'error')",
     "MW.showDialog.emit(\"KindleGen 错误：\\n\\n\" + self.kindlegenErrorCode[1], 'error')", 1),
    ("MW.addMessage.emit('Created EPUB file was too big. Weird file structure?', 'error', False)",
     "MW.addMessage.emit('生成的 EPUB 文件过大。文件结构异常？', 'error', False)", 1),
    ("MW.addMessage.emit('EPUB file: ' + str(epubSize) + 'MB. Supported size: ~350MB.', 'error',\n                               False)",
     "MW.addMessage.emit('EPUB 文件：' + str(epubSize) + 'MB。支持大小：约 350MB。', 'error',\n                               False)", 1),
    ("MW.addMessage.emit('<b>All jobs completed.</b>', 'info', False)\n            MW.addTrayMessage.emit('All jobs completed.', 'Information')",
     "MW.addMessage.emit('<b>全部任务已完成。</b>', 'info', False)\n            MW.addTrayMessage.emit('全部任务已完成。', 'Information')", 1),
    # 文件对话框
    ("dname = QFileDialog.getExistingDirectory(MW, 'Select default output folder', self.defaultOutputFolder)",
     "dname = QFileDialog.getExistingDirectory(MW, '选择默认输出文件夹', self.defaultOutputFolder)", 1),
    ('self.addMessage("Cannot select Kindle as output directory", \'error\')',
     'self.addMessage("无法选择 Kindle 目录作为输出目录", \'error\')', 1),
    ("dname = QFileDialog.getExistingDirectory(MW, 'Select output directory', self.lastPath)",
     "dname = QFileDialog.getExistingDirectory(MW, '选择输出目录', self.lastPath)", 1),
    ("fnames = QFileDialog.getOpenFileNames(MW, 'Select file', self.lastPath,\n"
     "                                                            'Comic (*.cbz *.cbr *.cb7 *.zip *.rar *.7z *.epub *.pdf);;All (*.*)')",
     "fnames = QFileDialog.getOpenFileNames(MW, '选择文件', self.lastPath,\n"
     "                                                            '漫画 (*.cbz *.cbr *.cb7 *.zip *.rar *.7z *.epub *.pdf);;全部 (*.*)')", 1),
    ("fnames = QFileDialog.getOpenFileNames(MW, 'Select file', self.lastPath,\n"
     "                                                            'Comic (*.pdf);;All (*.*)')",
     "fnames = QFileDialog.getOpenFileNames(MW, '选择文件', self.lastPath,\n"
     "                                                            '漫画 (*.pdf);;全部 (*.*)')", 1),
    ("dialog = QFileDialog(MW, 'Select input folder(s)', self.lastPath)",
     "dialog = QFileDialog(MW, '选择输入文件夹', self.lastPath)", 1),
    ("dialog = QFileDialog(MW, 'Select volume directories', self.lastPath)",
     "dialog = QFileDialog(MW, '选择卷目录', self.lastPath)", 1),
    ("fnames = QFileDialog.getOpenFileNames(MW, 'Select file(s)', self.lastPath,\n"
     "                                                          'Comic (*.cbz *.cbr *.cb7)')",
     "fnames = QFileDialog.getOpenFileNames(MW, '选择文件', self.lastPath,\n"
     "                                                          '漫画 (*.cbz *.cbr *.cb7)')", 1),
    ('self.showDialog("Editor is disabled due to a lack of 7z.", \'error\')',
     'self.showDialog("由于缺少 7z，元数据编辑器已停用。", \'error\')', 1),
    ("self.addMessage('<a href=\"https://github.com/ciromattia/kcc#7-zip\">Install 7z (link)</a>'\n"
     "                    ' to enable metadata editing.', 'warning')",
     "self.addMessage('<a href=\"https://github.com/ciromattia/kcc#7-zip\">安装 7z（链接）</a>'\n"
     "                    ' 以启用元数据编辑。', 'warning')", 1),
    ('self.showDialog("Failed to parse metadata!\\n\\n%s\\n\\nTraceback:\\n%s"\n'
     "                                % (str(err), sanitizeTrace(traceback)), 'error')",
     'self.showDialog("元数据解析失败！\\n\\n%s\\n\\n回溯信息：\\n%s"\n'
     "                                % (str(err), sanitizeTrace(traceback)), 'error')", 1),
    # 启动提示
    ("self.addMessage('<a href=\"https://github.com/ciromattia/kcc#7-zip\">Install 7z (link)</a>'\n"
     "                            ' to enable CBZ/CBR/ZIP/etc processing.', 'warning')",
     "self.addMessage('<a href=\"https://github.com/ciromattia/kcc#7-zip\">安装 7z（链接）</a>'\n"
     "                            ' 以启用 CBZ/CBR/ZIP 等格式处理。', 'warning')", 1),
    ("self.addMessage('<b>Tip:</b> Hover mouse over options/buttons to see explanations. Boxes can be partially/fully checked.', 'info')",
     "self.addMessage('<b>提示：</b>将鼠标悬停在选项/按钮上可查看说明。复选框支持半选/全选。', 'info')", 1),
    ("self.addMessage('<b>Tip:</b> You can drag and drop image folders or comic files/archives into this window to convert.', 'info')",
     "self.addMessage('<b>提示：</b>可以将图片文件夹或漫画文件/压缩包直接拖放到本窗口进行转换。', 'info')", 1),
    ("self.addMessage(\"<b>Tip:</b> Calibre may add margins! USB drop directly into the device's documents folder instead.\", 'info')",
     "self.addMessage('<b>提示：</b>通过 Calibre 传输可能会添加白边！建议改用 USB 将文件直接拷贝到设备的 documents 文件夹。', 'info')", 1),
    ("self.addMessage(\"<b>Tip:</b> You can toggle easy/expert mode using button at top right.\", 'info')",
     "self.addMessage('<b>提示：</b>可使用右上角按钮切换简单/专家模式。', 'info')", 1),
    ("self.addMessage('Since you are a new user of <b>KCC</b> please see few '\n"
     "                            '<a href=\"https://github.com/ciromattia/kcc/wiki/Important-tips\">important tips</a>.',\n"
     "                            'info')",
     "self.addMessage('首次使用 <b>KCC</b>，请先阅读 '\n"
     "                            '<a href=\"https://github.com/ciromattia/kcc/wiki/Important-tips\">重要提示</a>。',\n"
     "                            'info')", 1),
    # 状态栏链接
    ("link_dict = {\n"
     "            'README': \"https://github.com/ciromattia/kcc?tab=readme-ov-file#kcc\",\n"
     "            'FAQ': \"https://github.com/ciromattia/kcc/blob/master/README.md#faq\",\n"
     "            'WIKI': \"https://github.com/ciromattia/kcc/wiki\",\n"
     "            'YOUTUBE': \"https://www.youtube.com/@eink-dude\",\n"
     "            'TUTORIAL': \"https://youtu.be/QQ6zJcMF2Iw?si=80rfm6DU6OUJdFqa\",\n"
     "            'EMAIL': \"https://github.com/ciromattia/kcc?tab=readme-ov-file#commissions\",\n"
     "            'DONATE': \"https://github.com/ciromattia/kcc/blob/master/README.md#issues--new-features--donations\",\n"
     "            'FORUM': \"http://www.mobileread.com/forums/showthread.php?t=207461\",\n"
     "            'DISCORD': \"https://discord.com/invite/qj7wpnUHav\",\n"
     "        }",
     "link_dict = {\n"
     "            '说明文档': \"https://github.com/ciromattia/kcc?tab=readme-ov-file#kcc\",\n"
     "            '常见问题': \"https://github.com/ciromattia/kcc/blob/master/README.md#faq\",\n"
     "            '维基': \"https://github.com/ciromattia/kcc/wiki\",\n"
     "            '视频频道': \"https://www.youtube.com/@eink-dude\",\n"
     "            '视频教程': \"https://youtu.be/QQ6zJcMF2Iw?si=80rfm6DU6OUJdFqa\",\n"
     "            '联系作者': \"https://github.com/ciromattia/kcc?tab=readme-ov-file#commissions\",\n"
     "            '捐赠': \"https://github.com/ciromattia/kcc/blob/master/README.md#issues--new-features--donations\",\n"
     "            '论坛': \"http://www.mobileread.com/forums/showthread.php?t=207461\",\n"
     "            'Discord': \"https://discord.com/invite/qj7wpnUHav\",\n"
     "        }", 1),
    # 按钮文本
    ("GUI.convertButton.setText('Convert')", "GUI.convertButton.setText('转换')", 1),
    ("GUI.convertButton.setText('Abort')", "GUI.convertButton.setText('中止')", 1),
    # 条漫提示
    ("self.addMessage('You can choose a taller device profile to get taller cuts in webtoon mode.', 'info')\n"
     "            self.addMessage('Try reading webtoon panels side by side in landscape!', 'info')",
     "self.addMessage('在条漫模式下，可选择更高的设备配置以获得更长的分段。', 'info')\n"
     "            self.addMessage('试试在横屏模式下并排阅读条漫分页！', 'info')", 1),
    # 质量选项警告
    ("self.addMessage('This option is intended for older Kindle models.', 'warning')\n"
     "                self.addMessage('On this device, there will be conversion speed and quality issues.', 'warning')\n"
     "                self.addMessage('Use the Kindle Scribe profile if you want higher resolution when zooming.', 'warning')",
     "self.addMessage('此选项面向旧款 Kindle 机型。', 'warning')\n"
     "                self.addMessage('在当前设备上可能出现转换速度与质量问题。', 'warning')\n"
     "                self.addMessage('如需放大时获得更高分辨率，请使用 Kindle Scribe 配置。', 'warning')", 1),
    ("self.addMessage('Scribe PNG MOBI/EPUB has a lot of problems like blank pages/sections. Use JPG instead.', 'warning')",
     "self.addMessage('Scribe 使用 PNG 的 MOBI/EPUB 存在空白页/空白分节等问题，建议改用 JPG。', 'warning')", 1),
    ("self.addMessage('Colorsoft MOBI/EPUB can have blank pages. Just go back a few pages, exit, and reenter book.', 'info')",
     "self.addMessage('Colorsoft 的 MOBI/EPUB 可能出现空白页。回退几页后退出并重新打开本书即可。', 'info')", 1),
    ("self.addMessage(\"Partially check W/B Margins if you don't want KCC to extend the image margins.\", 'info')",
     "self.addMessage('如果不希望 KCC 扩展图像边距，请将「黑/白边距」设为半选状态。', 'info')", 1),
    # 伽马/裁剪强度
    ("GUI.gammaLabel.setText('Gamma: Auto')", "GUI.gammaLabel.setText('伽马值：自动')", 1),
    ("GUI.gammaLabel.setText('Gamma: ' + str(value))", "GUI.gammaLabel.setText('伽马值：' + str(value))", 1),
    ("GUI.croppingPowerLabel.setText('Cropping Power: ' + str(value))",
     "GUI.croppingPowerLabel.setText('裁剪强度：' + str(value))", 1),
    # 对话框标题
    ("QMessageBox.critical(MW, 'KCC - Error', message, QMessageBox.StandardButton.Ok)",
     "QMessageBox.critical(MW, 'KCC - 错误', message, QMessageBox.StandardButton.Ok)", 1),
    ("GUI.versionCheck.setAnswer(QMessageBox.question(MW, 'KCC - Question', message,",
     "GUI.versionCheck.setAnswer(QMessageBox.question(MW, 'KCC - 询问', message,", 1),
    # 转换启动
    ("self.addMessage('The process will be interrupted. Please wait.', 'warning')",
     "self.addMessage('任务将被中断，请稍候。', 'warning')", 2),
    ("self.addMessage('No files selected! Please choose files to convert.', 'error')",
     "self.addMessage('未选择任何文件！请先添加要转换的文件。', 'error')", 1),
    ("self.addMessage('Target resolution is not set!', 'error')",
     "self.addMessage('未设置目标分辨率！', 'error')", 1),
    ("self.addMessage(\n"
     "            '<a href=\"https://github.com/ciromattia/kcc#kindlegen\"><b>Install KindleGen (link)</b></a> to enable MOBI conversion for Kindles!',\n"
     "            'error'\n"
     "        )",
     "self.addMessage(\n"
     "            '<a href=\"https://github.com/ciromattia/kcc#kindlegen\"><b>安装 KindleGen（链接）</b></a> 即可启用 Kindle 的 MOBI 转换！',\n"
     "            'error'\n"
     "        )", 1),
    ("self.addMessage('Unsupported file type for ' + message, 'error')",
     "self.addMessage('不支持的文件类型：' + message, 'error')", 1),
    # 窗口标题
    ('MW.setWindowTitle("Kindle Comic Converter " + __version__)',
     'MW.setWindowTitle("Kindle Comic Converter 漫画转换器 " + __version__)', 1),
    # 元数据编辑器（批量/单个）
    ("self.statusLabel.setText('CBR files in selection are read-only.')",
     "self.statusLabel.setText('所选文件中包含 CBR，均为只读。')", 1),
    ("self.statusLabel.setText(f'Editing {len(self.files)} files.')",
     "self.statusLabel.setText(f'正在编辑 {len(self.files)} 个文件。')", 1),
    ("field.setPlaceholderText('(multiple files)')",
     "field.setPlaceholderText('（多个文件）')", 2),
    ("line.setPlaceholderText('(multiple values)')",
     "line.setPlaceholderText('（多个值）')", 1),
    ("self.statusLabel.setText('Separate authors with a comma.')",
     "self.statusLabel.setText('多位作者请用英文逗号分隔。')", 1),
    ("self.statusLabel.setText('No changes to apply.')",
     "self.statusLabel.setText('没有需要应用的更改。')", 1),
    ("self.statusLabel.setText(f'Processing {i}/{total}: {os.path.basename(file)}')",
     "self.statusLabel.setText(f'正在处理 {i}/{total}：{os.path.basename(file)}')", 1),
    ("errors.append(f'{os.path.basename(file)}: CBR is read-only')",
     "errors.append(f'{os.path.basename(file)}：CBR 为只读')", 1),
    ('self.showDialog("Some files failed to save:\\n\\n" + "\\n".join(errors[:10]) +\n'
     '                              (f"\\n...and {len(errors) - 10} more" if len(errors) > 10 else ""), \'error\')',
     'self.showDialog("部分文件保存失败：\\n\\n" + "\\n".join(errors[:10]) +\n'
     '                              (f"\\n…另有 {len(errors) - 10} 个错误未显示" if len(errors) > 10 else ""), \'error\')', 1),
    ("self.statusLabel.setText('Errors occurred.')",
     "self.statusLabel.setText('发生错误。')", 1),
    ("self.statusLabel.setText(f'Successfully updated {total} files.')",
     "self.statusLabel.setText(f'已成功更新 {total} 个文件。')", 1),
    ("self.statusLabel.setText(field.objectName().capitalize()[:-4] + ' field must be a number.')",
     "self.statusLabel.setText('「' + field.objectName().capitalize()[:-4] + '」字段必须为数字。')", 1),
    ('GUI.showDialog("Failed to save metadata!\\n\\n%s\\n\\nTraceback:\\n%s"\n'
     "                                   % (str(err), sanitizeTrace(traceback)), 'error')",
     'GUI.showDialog("元数据保存失败！\\n\\n%s\\n\\n回溯信息：\\n%s"\n'
     "                                   % (str(err), sanitizeTrace(traceback)), 'error')", 1),
    ("return None, 'Invalid range format (use start-end)'",
     "return None, '范围格式无效（应为「起始-结束」）'", 1),
    ("return None, 'Volume numbers must be positive'",
     "return None, '卷号必须为正数'", 1),
    ("return None, 'Invalid range: start > end'",
     "return None, '范围无效：起始大于结束'", 1),
    ("return None, 'Invalid range format'",
     "return None, '范围格式无效'", 1),
    ("return None, 'Invalid list format'",
     "return None, '列表格式无效'", 1),
    ("return None, 'Volume number must be positive'",
     "return None, '卷号必须为正数'", 1),
    ("return None, 'Invalid number'",
     "return None, '数字无效'", 1),
    ("return None, 'No valid volume numbers parsed'",
     "return None, '未解析到有效的卷号'", 1),
    ("return None, f'Volume count ({len(volumes)}) != file count ({fileCount})'",
     "return None, f'卷号数量（{len(volumes)}）与文件数量（{fileCount}）不一致'", 1),
    ("self.volumeLine.setPlaceholderText('e.g., 5 or 1-10 or 1,3,5')",
     "self.volumeLine.setPlaceholderText('例如：5 或 1-10 或 1,3,5')", 1),
])

# 批量字段提示（HTML 表头）
apply_replacements(GUI, [
    ("note = '<p><em>Note: Changing this field will overwrite all values in all selected files.</em></p>'",
     "note = '<p><em>注意：修改此字段将覆盖所有所选文件中的值。</em></p>'", 1),
    ("'<th style=\"padding:2px 6px; text-align:left;\">File</th>'\n"
     "            '<th style=\"padding:2px 6px; text-align:left;\">Value</th>'",
     "'<th style=\"padding:2px 6px; text-align:left;\">文件</th>'\n"
     "            '<th style=\"padding:2px 6px; text-align:left;\">值</th>'", 1),
    ("'<th style=\"padding:2px 6px; text-align:left;\">Value</th>'\n"
     "                '<th style=\"padding:2px 6px; text-align:right;\">Count</th>'",
     "'<th style=\"padding:2px 6px; text-align:left;\">值</th>'\n"
     "                '<th style=\"padding:2px 6px; text-align:right;\">数量</th>'", 1),
])

# ============ 4. KCC_spread_label.py ============
apply_replacements(BASE + 'KCC_spread_label.py', [
    ('self.setWindowTitle("TODO: Filename goes here")',
     'self.setWindowTitle("跨页标记预览")', 1),
    ('label2.setText("not a spread")', 'label2.setText("非跨页")', 1),
    ('''        help_text = [
            "Use arrows to change index.",
            "Use space bar to confirm spreads.",
            "Use spread shift option to offset by 1.",
            "Use enter key to confirm all spreads."
            "Close window to cancel."
        ]''',
     '''        help_text = [
            "用 ←/→ 方向键切换页面。",
            "用空格键标记/取消跨页。",
            "如需整体偏移 1 页，请使用「跨页位移」选项。",
            "用回车键确认全部跨页。",
            "关闭窗口取消。",
        ]''', 1),
    ("self.label2.setText('spread')", "self.label2.setText('跨页')", 3),
    ("self.label2.setText('not a spread')", "self.label2.setText('非跨页')", 3),
    ('if self.label2.text() == "not a spread":', 'if self.label2.text() == "非跨页":', 1),
])

# ============ 5. KCC_ui.py：主窗口全文案翻译 ============
UI = BASE + 'KCC_ui.py'
with open(UI, 'r', encoding='utf-8') as f:
    ui_text = f.read()
marker = '    def retranslateUi(self, mainWindow):'
idx = ui_text.index(marker)
NEW_UI_RETRANSLATE = '''    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QCoreApplication.translate("mainWindow", u"Kindle Comic Converter 漫画转换器", None))
#if QT_CONFIG(tooltip)
        self.jobList.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p>双击来源文件可在元数据编辑器中打开。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.preserveMarginLabel.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p>计算裁剪边界后，按指定百分比向内「回退」。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.preserveMarginLabel.setText(QCoreApplication.translate("mainWindow", u"保留边距 %", None))
        self.croppingPowerLabel.setText(QCoreApplication.translate("mainWindow", u"裁剪强度：", None))
        self.gammaLabel.setText(QCoreApplication.translate("mainWindow", u"伽马值：自动", None))
#if QT_CONFIG(tooltip)
        self.hLabel.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p style='white-space:pre'>目标设备的分辨率。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.hLabel.setText(QCoreApplication.translate("mainWindow", u"自定义高度：", None))
#if QT_CONFIG(tooltip)
        self.widthBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p style='white-space:pre'>目标设备的分辨率。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.wLabel.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p style='white-space:pre'>目标设备的分辨率。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.wLabel.setText(QCoreApplication.translate("mainWindow", u"自定义宽度：", None))
#if QT_CONFIG(tooltip)
        self.heightBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p style='white-space:pre'>目标设备的分辨率。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.directoryButton.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p style='white-space:pre'>将包含 JPG、PNG 或 GIF 文件的文件夹加入队列。<br/><span style=\\" font-weight:600;\\">其中包含的 CBR、CBZ 和 CB7 文件将不会被处理！</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.directoryButton.setText(QCoreApplication.translate("mainWindow", u"添加输入文件夹", None))
#if QT_CONFIG(tooltip)
        self.formatBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p style='white-space:pre'>输出格式。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.deviceBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p style='white-space:pre'>目标设备。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.clearButton.setText(QCoreApplication.translate("mainWindow", u"清空列表", None))
#if QT_CONFIG(tooltip)
        self.fileButton.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p style='white-space:pre'>将 CBR、CBZ、CB7 或 PDF 文件加入队列。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.fileButton.setText(QCoreApplication.translate("mainWindow", u"添加输入文件", None))
#if QT_CONFIG(tooltip)
        self.convertButton.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p style='white-space:pre'>Shift+点击 可为本列表选择输出目录。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.convertButton.setText(QCoreApplication.translate("mainWindow", u"转换", None))
#if QT_CONFIG(tooltip)
        self.qualityBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p style='white-space:pre'><span style=\\" font-weight:600; text-decoration: underline;\\">不勾选 - 4 分栏<br/></span>分别放大每个角落。</p><p style='white-space:pre'><span style=\\" font-weight:600; text-decoration: underline;\\">半选 - 2 分栏<br/></span>仅放大页面上部和下部。</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">全选 - 4 高质量分栏<br/></span>分别放大每个角落，并尝试提高放大质量。详见 Wiki。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.qualityBox.setText(QCoreApplication.translate("mainWindow", u"分栏视图 4/2/高质量", None))
#if QT_CONFIG(tooltip)
        self.legacyExtractBox.setToolTip(QCoreApplication.translate("mainWindow", u"使用旧版 KCC 的 PDF/EPUB 图像提取方式。\\n\\n如果标准提取因故失败，可使用此选项。", None))
#endif // QT_CONFIG(tooltip)
        self.legacyExtractBox.setText(QCoreApplication.translate("mainWindow", u"旧版提取", None))
#if QT_CONFIG(tooltip)
        self.outputSplit.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p style='white-space:pre'><span style=\\" font-weight:600; text-decoration: underline;\\">不勾选 - 自动模式<br/></span>输出将自动分卷。</p><p style='white-space:pre'><span style=\\" font-weight:600; text-decoration: underline;\\">全选 - 分卷模式<br/></span>每个子目录将被视为单独的一卷。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.outputSplit.setText(QCoreApplication.translate("mainWindow", u"输出分卷", None))
#if QT_CONFIG(tooltip)
        self.disableProcessingBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p style='white-space:pre'>不对任何图像进行处理，忽略设备配置与处理选项。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.disableProcessingBox.setText(QCoreApplication.translate("mainWindow", u"禁用图像处理", None))
#if QT_CONFIG(tooltip)
        self.upscaleBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p><span style=\\" font-weight:600; text-decoration: underline;\\">不勾选 - 不处理<br/></span>小于设备分辨率的图像不会被缩放。</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">半选 - 拉伸<br/></span>小于设备分辨率的图像将被缩放，但不保持宽高比。</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">全选 - 放大<br/></span>小于设备分辨率的图像将被缩放，并保持宽高比。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.upscaleBox.setText(QCoreApplication.translate("mainWindow", u"拉伸/放大", None))
#if QT_CONFIG(tooltip)
        self.interPanelCropBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p><span style=\\" font-weight:600; text-decoration: underline;\\">不勾选 - 禁用<br/></span>禁用</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">半选 - 横向<br/></span>裁剪分格之间的空白横线。</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">全选 - 双向<br/></span>裁剪分格之间的空白横线和竖线。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.interPanelCropBox.setText(QCoreApplication.translate("mainWindow", u"分格间裁剪", None))
#if QT_CONFIG(tooltip)
        self.languageEdit.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p>默认 EPUB 语言为 en-US（美式英语）。</p><p>仅当你的 EPUB 阅读器对英文字体支持有问题时才需修改。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.languageEdit.setPlaceholderText(QCoreApplication.translate("mainWindow", u"EPUB 语言", None))
#if QT_CONFIG(tooltip)
        self.webtoonBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p style='white-space:pre'>启用针对韩式条漫的特殊解析模式。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.webtoonBox.setText(QCoreApplication.translate("mainWindow", u"条漫模式", None))
#if QT_CONFIG(tooltip)
        self.noRotateBox.setToolTip(QCoreApplication.translate("mainWindow", u"在跨页拆分选项中不旋转跨页大图。", None))
#endif // QT_CONFIG(tooltip)
        self.noRotateBox.setText(QCoreApplication.translate("mainWindow", u"不旋转", None))
#if QT_CONFIG(tooltip)
        self.deleteBox.setToolTip(QCoreApplication.translate("mainWindow", u"删除输入文件或目录。此操作不可恢复！", None))
#endif // QT_CONFIG(tooltip)
        self.deleteBox.setText(QCoreApplication.translate("mainWindow", u"删除输入文件", None))
#if QT_CONFIG(tooltip)
        self.invertDirectionBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p>反转翻页方向。</p><p>通常用于从右到左的日漫，但希望从左到右翻页的情况。此时跨页拆分仍按从右到左进行。</p><p>可能破坏部分功能，如横屏模式的页序。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.invertDirectionBox.setText(QCoreApplication.translate("mainWindow", u"反转翻页方向", None))
#if QT_CONFIG(tooltip)
        self.noQuantizeBox.setToolTip(QCoreApplication.translate("mainWindow", u"不将 PNG 图像量化为 16 色（4 位）\\n\\n文件体积会翻倍，但可保留全部 256 色（8 位）。\\n\\n电子墨水屏只有 16 级灰度，一般不建议开启。", None))
#endif // QT_CONFIG(tooltip)
        self.noQuantizeBox.setText(QCoreApplication.translate("mainWindow", u"不量化", None))
#if QT_CONFIG(tooltip)
        self.rotateFirstBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p>当跨页拆分选项为半选状态时：</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">不勾选 - 旋转靠后<br/></span>将旋转后的跨页放在拆分页之后。</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">全选 - 旋转优先<br/></span>将旋转后的跨页放在拆分页之前。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.rotateFirstBox.setText(QCoreApplication.translate("mainWindow", u"旋转优先", None))
#if QT_CONFIG(tooltip)
        self.croppingBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p><span style=\\" font-weight:600; text-decoration: underline;\\">不勾选 - 禁用</span></p><p>禁用</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">半选 - 仅裁白边<br/></span>裁剪页边距</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">全选 - 白边+页码<br/></span>裁剪页边距和页码</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.croppingBox.setText(QCoreApplication.translate("mainWindow", u"裁剪模式", None))
#if QT_CONFIG(tooltip)
        self.authorEdit.setToolTip(QCoreApplication.translate("mainWindow", u"默认作者为 KCC", None))
#endif // QT_CONFIG(tooltip)
        self.authorEdit.setPlaceholderText(QCoreApplication.translate("mainWindow", u"默认作者", None))
#if QT_CONFIG(tooltip)
        self.mozJpegBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p><span style=\\" font-weight:600; text-decoration: underline;\\">不勾选 - JPEG<br/></span>使用 JPEG 文件</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">半选 - 强制 PNG<br/></span>黑白图像改用 PNG 而非 JPEG</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">全选 - mozJpeg<br/></span>同等画质下 JPEG 体积减小 10-20%，但处理时间翻倍</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.mozJpegBox.setText(QCoreApplication.translate("mainWindow", u"JPEG/PNG/mozJpeg", None))
#if QT_CONFIG(tooltip)
        self.lightnovelBox.setToolTip(QCoreApplication.translate("mainWindow", u"仅缩放图像并保留原始文件结构。\\n\\n除 JPEG 质量、彩色模式、输出文件夹外，忽略大多数其他选项。", None))
#endif // QT_CONFIG(tooltip)
        self.lightnovelBox.setText(QCoreApplication.translate("mainWindow", u"轻小说模式", None))
#if QT_CONFIG(tooltip)
        self.metadataTitleBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p><span style=\\" font-weight:600; text-decoration: underline;\\">不勾选 - 不使用元数据标题<br/></span>写入默认标题。</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">半选 - 将元数据标题追加到默认规则<br/></span>写入默认标题，并附加来自 ComicInfo.xml 等内嵌元数据的标题。</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">全选 - 仅使用元数据标题<br/></span>写入来自 ComicInfo.xml 等内嵌元数据的标题。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.metadataTitleBox.setText(QCoreApplication.translate("mainWindow", u"元数据标题", None))
#if QT_CONFIG(tooltip)
        self.fileFusionBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p>将所有选中的文件合并为一个文件。（适合把多个章节合并成一卷。）</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.fileFusionBox.setText(QCoreApplication.translate("mainWindow", u"文件融合", None))
#if QT_CONFIG(tooltip)
        self.forcePngRgbBox.setToolTip(QCoreApplication.translate("mainWindow", u"强制全彩图像以无损 PNG 格式保存，文件体积会显著增大。", None))
#endif // QT_CONFIG(tooltip)
        self.forcePngRgbBox.setText(QCoreApplication.translate("mainWindow", u"强制 PNG RGB", None))
#if QT_CONFIG(tooltip)
        self.wallpaperBox.setToolTip(QCoreApplication.translate("mainWindow", u"自动勾选适用于 KOreader 壁纸的多个选项。\\n\\n同时会将图像居中裁剪以铺满屏幕。", None))
#endif // QT_CONFIG(tooltip)
        self.wallpaperBox.setText(QCoreApplication.translate("mainWindow", u"壁纸模式", None))
#if QT_CONFIG(tooltip)
        self.maximizeStrips.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p><span style=\\" font-weight:600; text-decoration: underline;\\">不勾选 - 1x4<br/></span>保持 1x4 长条分栏格式。</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">全选 - 2x2<br/></span>将 1x4 长条转为 2x2，充分利用屏幕。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.maximizeStrips.setText(QCoreApplication.translate("mainWindow", u"1x4 转 2x2 长条", None))
#if QT_CONFIG(tooltip)
        self.autoLevelBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p>默认情况下，KCC 将最暗的像素值映射为纯黑（黑点）。</p><p>极值黑点会将黑点设为最常见的暗部像素值。</p><p>适用于文字为纯黑但画面偏灰的情况。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.autoLevelBox.setText(QCoreApplication.translate("mainWindow", u"极值黑点", None))
#if QT_CONFIG(tooltip)
        self.ebokBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p>强制将 Kindle MOBI 的类型标记为 EBOK 而非 PDOC。</p><p>若离线超过一个月后联网，USB 导入的书籍可能被删除。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.ebokBox.setText(QCoreApplication.translate("mainWindow", u"强制 EBOK", None))
#if QT_CONFIG(tooltip)
        self.pdfWidthBox.setToolTip(QCoreApplication.translate("mainWindow", u"将矢量 PDF 按设备宽度而非高度渲染。\\n\\n适用于打算裁掉上下少量内容以铺满屏幕的情况。", None))
#endif // QT_CONFIG(tooltip)
        self.pdfWidthBox.setText(QCoreApplication.translate("mainWindow", u"按宽度渲染 PDF", None))
#if QT_CONFIG(tooltip)
        self.autocontrastBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p><span style=\\" font-weight:600; text-decoration: underline;\\">不勾选 - 仅黑白页<br/></span>仅对黑白页面做自动对比度。对缺少接近黑/白的页面无效。</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">半选 - 禁用<br/></span>禁用自动对比度</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">全选 - 黑白+彩色<br/></span>黑白与彩色图像均做自动对比度。对缺少接近黑/白的页面无效。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.autocontrastBox.setText(QCoreApplication.translate("mainWindow", u"自定义自动对比度", None))
#if QT_CONFIG(tooltip)
        self.defaultOutputFolderBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p><span style=\\" font-weight:600; text-decoration: underline;\\">不勾选 - 源文件旁<br/></span>输出文件放在源文件旁边</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">半选 - 源文件旁的文件夹<br/></span>输出文件放在源文件旁边的文件夹中</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">全选 - 自定义<br/></span>输出文件放在右侧按钮指定的目录中</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.defaultOutputFolderBox.setText(QCoreApplication.translate("mainWindow", u"输出文件夹", None))
#if QT_CONFIG(tooltip)
        self.defaultOutputFolderButton.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p>点击选择默认输出目录。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.defaultOutputFolderButton.setText("")
#if QT_CONFIG(tooltip)
        self.pngLegacyBox.setToolTip(QCoreApplication.translate("mainWindow", u"使用兼容性更好的 8 位 PNG 代替 4 位。", None))
#endif // QT_CONFIG(tooltip)
        self.pngLegacyBox.setText(QCoreApplication.translate("mainWindow", u"PNG 兼容模式", None))
#if QT_CONFIG(tooltip)
        self.rotateRightBox.setToolTip(QCoreApplication.translate("mainWindow", u"以与常规相反的方向旋转跨页大图。", None))
#endif // QT_CONFIG(tooltip)
        self.rotateRightBox.setText(QCoreApplication.translate("mainWindow", u"向右旋转", None))
#if QT_CONFIG(tooltip)
        self.vertical4PanelBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p>在虚拟分栏模式下：</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">不勾选 - 横向<br/></span>前两个分栏为上方的分栏。</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">全选 - 纵向<br/></span>前两个分栏为两侧的分栏。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.vertical4PanelBox.setText(QCoreApplication.translate("mainWindow", u"竖排四格分栏", None))
#if QT_CONFIG(tooltip)
        self.borderBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p><span style=\\" font-weight:600; text-decoration: underline;\\">不勾选 - 自动检测<br/></span>自动检测边距填充颜色。</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">半选 - 白色<br/></span>保持边距不变。</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">全选 - 黑色<br/></span>边距以黑色填充。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.borderBox.setText(QCoreApplication.translate("mainWindow", u"黑/白边距", None))
#if QT_CONFIG(tooltip)
        self.eraseRainbowBox.setToolTip(QCoreApplication.translate("mainWindow", u"通过衰减干扰频率，消除彩色墨水屏上的彩虹纹", None))
#endif // QT_CONFIG(tooltip)
        self.eraseRainbowBox.setText(QCoreApplication.translate("mainWindow", u"彩虹纹消除", None))
#if QT_CONFIG(tooltip)
        self.webpBox.setToolTip(QCoreApplication.translate("mainWindow", u"将 JPG 替换为有损 WebP，PNG 替换为无损 WebP（含 JPEG 质量设置）。\\n\\n对 Kindle EPUB/MOBI 和所有 PDF 无效。\\n\\n可大幅减小彩色内容的文件体积。\\n\\n对黑白内容收益甚微且更耗资源，不建议使用。", None))
#endif // QT_CONFIG(tooltip)
        self.webpBox.setText(QCoreApplication.translate("mainWindow", u"WebP", None))
#if QT_CONFIG(tooltip)
        self.rotateBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p><span style=\\" font-weight:600; text-decoration: underline;\\">不勾选 - 拆分<br/></span>跨页大图将被切成两个独立页面。</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">半选 - 拆分并旋转<br/></span>跨页大图显示两次：先拆分再旋转。</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">全选 - 旋转<br/></span>跨页大图将被旋转。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.rotateBox.setText(QCoreApplication.translate("mainWindow", u"跨页拆分", None))
#if QT_CONFIG(tooltip)
        self.chunkSizeCheckBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p><span style=\\" font-weight:700; text-decoration: underline;\\">不勾选<br/></span>输出文件最大体积：条漫 100 MB，其他 400 MB，超过后自动分卷。</p><p><span style=\\" font-weight:700; text-decoration: underline;\\">全选</span><br/>按下方「分卷大小 MB」指定的体积分卷。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.chunkSizeCheckBox.setText(QCoreApplication.translate("mainWindow", u"分卷大小", None))
#if QT_CONFIG(tooltip)
        self.jpegQualityBox.setToolTip(QCoreApplication.translate("mainWindow", u"JPEG 质量，范围 0（最差）到 95（最佳）。\\n\\n大多数设备默认 85，Kindle Scribe 和 Colorsoft 默认 90。\\n\\n数值越高体积越大、画质越好，还可解决空白页问题。", None))
#endif // QT_CONFIG(tooltip)
        self.jpegQualityBox.setText(QCoreApplication.translate("mainWindow", u"自定义 JPEG 质量", None))
#if QT_CONFIG(tooltip)
        self.gammaBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p>设置自定义伽马校正。</p><p>1.0 为默认值（禁用）。<br/>小于 1.0 使图像变亮。<br/>大于 1.0 使图像变暗。</p><p>KCC 9.1.0 及更早版本的默认值为 1.8。</p><p>适用于想让中间调变暗的情况。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.gammaBox.setText(QCoreApplication.translate("mainWindow", u"自定义伽马", None))
#if QT_CONFIG(tooltip)
        self.mangaBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p style='white-space:pre'>启用从右到左的阅读顺序。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.mangaBox.setText(QCoreApplication.translate("mainWindow", u"从右到左（日漫）", None))
#if QT_CONFIG(tooltip)
        self.colorBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p style='white-space:pre'>禁用转换为灰度。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.colorBox.setText(QCoreApplication.translate("mainWindow", u"彩色模式", None))
#if QT_CONFIG(tooltip)
        self.titleEdit.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p>默认标题</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.titleEdit.setPlaceholderText(QCoreApplication.translate("mainWindow", u"默认标题", None))
#if QT_CONFIG(tooltip)
        self.coverFillBox.setToolTip(QCoreApplication.translate("mainWindow", u"先按宽高比中心裁剪，再将封面缩放到与设备分辨率完全一致。\\n可能根据源图宽高比裁掉上下或左右，Kindle Scribe 暂不支持。", None))
#endif // QT_CONFIG(tooltip)
        self.coverFillBox.setText(QCoreApplication.translate("mainWindow", u"封面填充", None))
#if QT_CONFIG(tooltip)
        self.smartCoverCropBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p>尝试从宽幅图像中裁出主封面。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.smartCoverCropBox.setText(QCoreApplication.translate("mainWindow", u"智能封面裁剪", None))
#if QT_CONFIG(tooltip)
        self.spreadShiftBox.setToolTip(QCoreApplication.translate("mainWindow", u"在横屏模式下将首页移到另一侧，以对齐跨页", None))
#endif // QT_CONFIG(tooltip)
        self.spreadShiftBox.setText(QCoreApplication.translate("mainWindow", u"跨页位移", None))
#if QT_CONFIG(tooltip)
        self.onePageLandscapeBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p><span style=\\" font-weight:600; text-decoration: underline;\\">不勾选 - 双页横屏<br/></span>左右页各占一个视口</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">全选 - 单页横屏<br/></span>单页居中占一个视口</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.onePageLandscapeBox.setText(QCoreApplication.translate("mainWindow", u"单页横屏", None))
#if QT_CONFIG(tooltip)
        self.keepComicInfoBox.setToolTip(QCoreApplication.translate("mainWindow", u"保留原始 ComicInfo.xml 文件。\\n\\n保留该文件可能导致部分阅读器崩溃，如 Kobo 原生 CBZ 阅读器。", None))
#endif // QT_CONFIG(tooltip)
        self.keepComicInfoBox.setText(QCoreApplication.translate("mainWindow", u"保留 ComicInfo.xml", None))
#if QT_CONFIG(tooltip)
        self.tempDirBox.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p><span style=\\" font-weight:600; text-decoration: underline;\\">不勾选 - 系统盘<br/></span>使用系统所在盘的专用临时目录。</p><p><span style=\\" font-weight:600; text-decoration: underline;\\">全选 - 源文件所在盘<br/></span>在源文件所在盘创建临时目录。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.tempDirBox.setText(QCoreApplication.translate("mainWindow", u"临时目录", None))
#if QT_CONFIG(tooltip)
        self.legacyPanelViewBox.setToolTip(QCoreApplication.translate("mainWindow", u"使用 KCC 6 的旧版分栏视图方法。\\n\\n在固件 5.19.2（回退版）和 5.19.3+ 上基本可用", None))
#endif // QT_CONFIG(tooltip)
        self.legacyPanelViewBox.setText(QCoreApplication.translate("mainWindow", u"旧版分栏视图", None))
        self.jpegQualityLabel.setText(QCoreApplication.translate("mainWindow", u"JPEG 质量：", None))
#if QT_CONFIG(tooltip)
        self.labelSpreadsButton.setToolTip(QCoreApplication.translate("mainWindow", u"按住 Shift 点击可生成低质量预览。", None))
#endif // QT_CONFIG(tooltip)
        self.labelSpreadsButton.setText(QCoreApplication.translate("mainWindow", u"标记跨页", None))
        self.kofiButton.setText(QCoreApplication.translate("mainWindow", u"在 Ko-fi 支持作者", None))
#if QT_CONFIG(tooltip)
        self.editorButton.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p style='white-space:pre'>Shift+点击 可编辑目录。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.editorButton.setText(QCoreApplication.translate("mainWindow", u"元数据编辑器", None))
        self.humbleButton.setText(QCoreApplication.translate("mainWindow", u"Humble Bundle 推广", None))
#if QT_CONFIG(tooltip)
        self.expertButton.setToolTip(QCoreApplication.translate("mainWindow", u"切换简单/专家模式", None))
#endif // QT_CONFIG(tooltip)
        self.expertButton.setText(QCoreApplication.translate("mainWindow", u"简单/专家模式", None))
#if QT_CONFIG(tooltip)
        self.chunkSizeWidget.setToolTip(QCoreApplication.translate("mainWindow", u"<html><head/><body><p>警告：分卷大小超过默认值可能导致性能/电池问题，在旧设备上尤为明显。</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.chunkSizeLabel.setText(QCoreApplication.translate("mainWindow", u"分卷大小 MB：", None))
        self.chunkSizeWarnLabel.setText(QCoreApplication.translate("mainWindow", u"大于默认值可能导致旧阅读器出现性能问题。", None))
        self.easyLabel.setText(QCoreApplication.translate("mainWindow", u"将鼠标悬停在任意选项/按钮上可查看说明！选项支持半选或全选！", None))
    # retranslateUi
'''
ui_text = ui_text[:idx] + NEW_UI_RETRANSLATE
with open(UI, 'w', encoding='utf-8') as f:
    f.write(ui_text)

# ============ 6. KCC_ui_editor.py：元数据编辑器翻译 ============
ED = BASE + 'KCC_ui_editor.py'
with open(ED, 'r', encoding='utf-8') as f:
    ed_text = f.read()
marker_ed = '    def retranslateUi(self, editorDialog):'
idx_ed = ed_text.index(marker_ed)
NEW_ED_RETRANSLATE = '''    def retranslateUi(self, editorDialog):
        editorDialog.setWindowTitle(QCoreApplication.translate("editorDialog", u"元数据编辑器", None))
        self.label_1.setText(QCoreApplication.translate("editorDialog", u"系列：", None))
        self.label_2.setText(QCoreApplication.translate("editorDialog", u"卷：", None))
#if QT_CONFIG(tooltip)
        self.bulkVolumeCheck.setToolTip(QCoreApplication.translate("editorDialog", u"<b>批量设置卷号</b><br>勾选此框可为多个文件批量分配卷号。<br><br><b>输入格式：</b><br><code>5</code> \\u2192 从 5 开始的连续编号（5、6、7...）<br><code>1-10</code> \\u2192 1 到 10 的范围<br><code>1, 3, 5</code> \\u2192 指定值<br><br><i>注意：分配前文件会按名称排序。</i>", None))
#endif // QT_CONFIG(tooltip)
        self.bulkVolumeCheck.setText("")
        self.label_3.setText(QCoreApplication.translate("editorDialog", u"期号：", None))
        self.label_4.setText(QCoreApplication.translate("editorDialog", u"文字作者：", None))
        self.label_5.setText(QCoreApplication.translate("editorDialog", u"铅笔稿：", None))
        self.label_6.setText(QCoreApplication.translate("editorDialog", u"描线：", None))
        self.label_7.setText(QCoreApplication.translate("editorDialog", u"上色：", None))
        self.label_8.setText(QCoreApplication.translate("editorDialog", u"标题：", None))
        self.statusLabel.setText("")
        self.okButton.setText(QCoreApplication.translate("editorDialog", u"保存", None))
        self.cancelButton.setText(QCoreApplication.translate("editorDialog", u"取消", None))
    # retranslateUi
'''
ed_text = ed_text[:idx_ed] + NEW_ED_RETRANSLATE
with open(ED, 'w', encoding='utf-8') as f:
    f.write(ed_text)

print('==== 补丁结果 ====')
if failures:
    for f_ in failures:
        print('FAIL:', f_)
    sys.exit(1)
print('全部替换成功')
