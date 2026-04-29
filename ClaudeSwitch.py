# -*- coding: utf-8 -*-
"""
在 %USERPROFILE%\.claude 下查找所有 settings_xxx.json,
列出供选择, 选中后复制覆盖 settings.json.
"""
import os
import sys
import shutil
import glob
import json
from urllib.parse import urlparse


def load_json(path):
    """读取 JSON 文件，失败返回 None"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def extract_info(data):
    """从 settings JSON 中提取: 域名(env.ANTHROPIC_BASE_URL) 和 model"""
    if not data:
        return "", ""
    env = data.get("env", {})
    base_url = env.get("ANTHROPIC_BASE_URL", "")
    domain = ""
    if base_url:
        parsed = urlparse(base_url)
        domain = parsed.hostname or base_url
    model = data.get("model", "")
    return domain, model


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

    # ---- 显示当前正在使用的 settings.json 信息 ----
    current_data = load_json(target)
    if current_data:
        current_domain, current_model = extract_info(current_data)
        # 检查是否与某个 settings_xxx.json 相同
        matched_name = None
        for f in files:
            fdata = load_json(f)
            if fdata == current_data:
                matched_name = os.path.basename(f)
                break

        print("=" * 56)
        print("  当前配置: settings.json")
        print("  %-12s %s" % ("model:", current_model or "(未设置)"))
        print("  %-12s %s" % ("endpoint:", current_domain or "(未设置)"))
        if matched_name:
            print("  %-12s %s" % ("匹配:", matched_name))
        else:
            print("  %-12s (未匹配任何预设配置)" % "匹配:")
        print("=" * 56)
    else:
        print("=" * 56)
        print("  当前 settings.json 不存在或无法读取")
        print("=" * 56)

    # ---- 列出所有预设配置 ----
    print("\n可用的配置文件:")
    print("-" * 56)
    print("  %-4s %-24s %-20s %s" % ("编号", "文件名", "model", "endpoint"))
    print("-" * 56)
    for i, f in enumerate(files, 1):
        name = os.path.basename(f)
        data = load_json(f)
        domain, model = extract_info(data)
        model_str = model or "(未设置)"
        domain_str = domain or "(未设置)"
        print("  [%d]  %-24s %-20s %s" % (i, name, model_str, domain_str))
    print("-" * 56)

    # ---- 选择 ----
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
    src_data = load_json(src)
    src_domain, src_model = extract_info(src_data)

    print("\n目标配置: %s" % os.path.basename(src))
    print("  model:    %s" % (src_model or "(未设置)"))
    print("  endpoint: %s" % (src_domain or "(未设置)"))
    print("将用此覆盖 settings.json")
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
