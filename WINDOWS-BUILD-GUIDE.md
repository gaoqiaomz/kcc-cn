# KCC 中文版 · Windows 打包指令（交给 Windows 端 Agent 执行）

本项目是 https://github.com/ciromattia/kcc v12.0.0 的中文改造版，已完成：
1. 界面全部简体中文（无英文语言入口）
2. 删除 Kobo / reMarkable 全部机型；Kindle 仅保留 Oasis / Scribe / Paperwhite / Colorsoft 四系列
3. 新增掌阅（Ocean/Leaf）、汉王（Clear）、文石 BOOX 机型；同分辨率并列、C 彩色单独、按面板代际分条
4. 禁用更新检测（不请求 GitHub API）
5. macOS 版已打包验证通过；本包用于产出 Windows exe

源码目录结构：`kindlecomicconverter/`（核心代码）、`kcc.py`（入口）、`setup.py`（打包脚本）、`requirements.txt`、`icons/`（含 comic2ebook.ico）。

---

## 一、环境准备（Windows 10/11 x64）

1. 安装 Python 3.11（或 3.12/3.13）x64：https://www.python.org/downloads/
   - 安装时必须勾选 **Add python.exe to PATH**
   - 验证：`python --version`
2. 确认可联网（pip 需从 PyPI 下载依赖）。

## 二、构建步骤（在源码解压目录下执行）

```bat
cd /d <解压后的kcc源码目录>

:: 1. 升级 pip
python -m pip install --upgrade pip

:: 2. 安装运行依赖
pip install -r requirements.txt

:: 3. 安装打包工具
pip install certifi pyinstaller

:: 4. 一键打包（官方标准方式）
python setup.py build_binary
```

构建完成后产物为 **单文件 exe**：

```
dist\KCC_AMD64_12.0.0.exe
```

- 单文件、双击即用、无控制台黑窗、带 KCC 图标
- 无需安装、免 Python 环境即可在任何 Windows 10/11 x64 机器上运行

### 备选：直接调 PyInstaller（与上面第 4 步等价）

```bat
pyinstaller --hidden-import=_cffi_backend -y -F -i icons\comic2ebook.ico -n KCC_AMD64_12.0.0 -w --noupx kcc.py
```

## 三、打包后验收清单（必须逐项确认）

1. **启动**：双击 exe，10 秒内出现主窗口，无报错弹窗。
2. **中文界面**：按钮显示「转换」「清空列表」「添加输入文件」「元数据编辑器」等，鼠标悬停提示为中文。
3. **窗口标题**：`Kindle Comic Converter 漫画转换器 12.0.0`。
4. **设备列表**：下拉框中
   - 有且仅有 10 个 Kindle 型号（Paperwhite 12/11/7-10/5-6、Colorsoft、Scribe Colorsoft、Scribe 3、Scribe 1/2、Oasis 9/10、Oasis 8）
   - 有「掌阅 Ocean/Leaf」「汉王 Clear」「文石 Poke/Page/Go」分组
   - **完全没有** Kobo、reMarkable、Kindle 1/2/DX/Voyage 等旧机型
5. **更新检测已禁用**：启动后日志区**不会**出现 "The new version is available!" 或任何英文推广公告，且不发起对 api.github.com 的网络请求（可用防火墙/抓包验证）。
6. **功能冒烟**：随便拖入几张图片 → 点「转换」（默认设备 Kindle Paperwhite 12、默认格式 MOBI/AZW3）→ 应正常输出电子书文件；再选一台「掌阅」机型（默认格式应为 EPUB）转换一次。
7. 若本机装了 7-Zip，CBZ/CBR 输入也应可用（没有则提示安装 7z，属正常）。

## 四、常见问题排查

| 现象 | 处理 |
|---|---|
| `pip install` 某些包装不上 | 确认 Python 是 **x64**；重试 `pip install -r requirements.txt` |
| 打包后启动闪退 | 用带控制台方式重建看报错：把 `-w` 改成 `-c` 再跑一次，把 traceback 发回来 |
| 杀毒软件报毒 | PyInstaller 单文件 exe 常见误报；可改用目录模式：`pyinstaller --hidden-import=_cffi_backend -y -D -i icons\comic2ebook.ico -n KCC -w --noupx kcc.py`（产物为 dist\KCC\ 文件夹） |
| 缺少 `_cffi_backend` 报错 | 命令里已有 `--hidden-import=_cffi_backend`，不要删掉 |

## 五、注意事项

- **不要**重新执行 `gen_ui_files.bat` 或用 Qt Designer 重新生成 `KCC_ui.py` / `KCC_ui_editor.py`——中文翻译直接写在生成文件里，重新生成会丢失。
- **不要**升级/改动 `requirements.txt` 中的依赖版本。
- 除打包外无需任何其他改动；如需同时产出命令行工具（可选），执行 `python setup.py build_c2e` 与 `python setup.py build_c2p`。
- 转换 Kindle MOBI/KFX 时若提示 KindleGen 缺失，属运行时可选依赖，与本次打包无关。
