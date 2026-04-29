# -*- coding: utf-8 -*-
"""
在 %USERPROFILE%\.claude 下查找所有 settings_xxx.json,
列出供选择, 选中后复制覆盖 settings.json.
"""
import os
import sys
import shutil
import glob


def main():
    claude_dir = os.path.join(os.environ.get("USERPROFILE", ""), ".claude")
    if not os.path.isdir(claude_dir):
        print("目录不存在: %s" % claude_dir)
        sys.exit(1)

    pattern = os.path.join(claude_dir, "settings_*.json")
    files = sorted(glob.glob(pattern))
    if not files:
        print("未在 %s 中找到 settings_*.json" % claude_dir)
        sys.exit(1)

    target = os.path.join(claude_dir, "settings.json")

    print("可用的配置文件:")
    for i, f in enumerate(files, 1):
        name = os.path.basename(f)
        print("  [%d] %s" % (i, name))

    try:
        choice = input("请选择编号 (回车取消): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n已取消")
        return

    if not choice:
        print("已取消")
        return

    try:
        idx = int(choice)
        if not 1 <= idx <= len(files):
            raise ValueError
    except ValueError:
        print("无效输入")
        sys.exit(1)

    src = files[idx - 1]
    print("将用 %s 覆盖 %s" % (os.path.basename(src), os.path.basename(target)))
    confirm = input("确认? (y/N): ").strip().lower()
    if confirm != "y":
        print("已取消")
        return

    # 备份现有 settings.json
    if os.path.isfile(target):
        backup = target + ".bak"
        shutil.copy2(target, backup)
        print("已备份原文件到 %s" % os.path.basename(backup))

    shutil.copy2(src, target)
    print("已切换到 %s" % os.path.basename(src))


if __name__ == "__main__":
    main()
