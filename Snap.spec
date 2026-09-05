# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# ============================================================
# 1. 动态收集 config 目录下所有 JSON 文件
# ============================================================
def collect_config_files():
    """递归收集 config 目录下的所有文件"""
    datas = []
    config_dir = 'config'
    if os.path.exists(config_dir):
        for root, dirs, files in os.walk(config_dir):
            for file in files:
                # 只打包 JSON 文件（如果还有其他类型文件，可以去掉 .endswith 限制）
                if file.endswith('.json'):
                    full_path = os.path.join(root, file)
                    # (源文件路径, 目标目录，保持相对路径结构)
                    datas.append((full_path, root))
    return datas

# ============================================================
# 2. 动态收集 .snapsolver 目录下的配置文件（隐藏目录）
# ============================================================
def collect_snapsolver_files():
    """收集 .snapsolver 目录下的所有文件"""
    datas = []
    snapsolver_dir = '.snapsolver'
    if os.path.exists(snapsolver_dir):
        for root, dirs, files in os.walk(snapsolver_dir):
            for file in files:
                full_path = os.path.join(root, file)
                datas.append((full_path, root))
    return datas

# ============================================================
# 3. 动态收集 static 目录下的所有文件（CSS, JS, 图片等）
# ============================================================
def collect_static_files():
    """收集 static 目录下的所有文件"""
    datas = []
    static_dir = 'static'
    if os.path.exists(static_dir):
        for root, dirs, files in os.walk(static_dir):
            for file in files:
                full_path = os.path.join(root, file)
                datas.append((full_path, root))
    return datas

# ============================================================
# 4. 动态收集 templates 目录下的所有 HTML 模板
# ============================================================
def collect_templates_files():
    """收集 templates 目录下的所有文件"""
    datas = []
    templates_dir = 'templates'
    if os.path.exists(templates_dir):
        for root, dirs, files in os.walk(templates_dir):
            for file in files:
                full_path = os.path.join(root, file)
                datas.append((full_path, root))
    return datas

# ============================================================
# 5. 合并所有资源文件
# ============================================================
all_datas = []
all_datas.extend(collect_config_files())        # config/*.json
all_datas.extend(collect_snapsolver_files())    # .snapsolver/*.json
all_datas.extend(collect_static_files())        # static/**/*
all_datas.extend(collect_templates_files())     # templates/*.html

# ============================================================
# 6. Analysis: 分析主程序依赖
# ============================================================
a = Analysis(
    ['app.py'],                      # 入口脚本
    pathex=[],                       # 额外搜索路径
    binaries=[],                     # 需要打包的二进制文件（如 .pyd, .dll）
    datas=all_datas,                 # 📌 所有资源文件
    hiddenimports=[
        # 如果用了 Flask，需要显式导入这些
        'flask',
        'jinja2',
        'markupsafe',
        'werkzeug',
        'flask',
        'flask_socketio',
        'socketio',
        'engineio',
        'engineio.async_drivers.threading', 
        # 所有 models 下的模块（因为是在运行时动态导入的）
        'models.alibaba',
        'models.anthropic',
        'models.baidu_ocr',
        'models.deepseek',
        'models.doubao',
        'models.google',
        'models.mathpix',
        'models.moonshot',
        'models.openai',
        'models.factory',
        'models.base',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除不需要的模块以减小体积（如果有 PyQt、matplotlib 等可以加在这里）
        # 'PyQt5',
        # 'matplotlib',
        # 'pandas',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# ============================================================
# 7. PYZ: 打包 Python 字节码
# ============================================================
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ============================================================
# 8. EXE: 生成可执行文件
# ============================================================
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Snap',                     # EXE 名称
    debug=False,                     # 是否输出调试信息
    bootloader_ignore_signals=False,
    strip=False,                     # 是否去除符号表（减小体积）
    upx=True,                        # 是否用 UPX 压缩（需要安装 UPX）
    upx_exclude=[],                  # 不压缩的文件
    runtime_tmpdir=None,             # 临时目录
    console=True,                    # True=显示控制台，False=隐藏（GUI应用）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app.ico' if os.path.exists('app.ico') else None,  # 图标
)

# ============================================================
# 9. (可选) 如果是 Mac，生成 .app 捆绑包
# ============================================================
# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='Snap',
# )