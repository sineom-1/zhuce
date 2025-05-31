#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def main():
    # 从图片1中看到的邮箱列表
    image1_emails = [
        "degdc8nicofw@outlook.com",
        "fhpcgdhnymli@outlook.com", 
        "agib15i3ii76@outlook.com",
        "lifgsys9huoc@outlook.com",
        "bjtx31i98a6f@outlook.com",
        "utzh5wcitza2@outlook.com",
        "fvgm7uuf6xrv@outlook.com",
        "zmpi0idpdzpk@outlook.com",
        "wymy59kllffo@outlook.com",
        "wtdi1qobfijj@outlook.com",
        "wgcyrd9q82zy@outlook.com",
        "pznrv6khcxrv@outlook.com",
        "oouc8fjguhuq@outlook.com",
        "agoh8cck874w@outlook.com",
        "nvnafn5uq8f6@outlook.com",
        "ygrmwtwn5pcn@outlook.com",
        "teglbuumm8ml@outlook.com",
        "nmncjg9n3i47@outlook.com",
        "czxjigf1xxh7@outlook.com",
        "fxajn9hjss8s@outlook.com",
        "dwtaor9sram4@outlook.com",
        "epkf5sd3s8wa@outlook.com",
        "yinpjvwpsoh5@outlook.com",
        "nvtspe9q8vsb@outlook.com",
        "ejxy5cj51cgn@outlook.com"
    ]
    
    # 从图片2中看到的邮箱列表  
    image2_emails = [
        "ejxy5cj51cgn@outlook.com",
        "zdsxc7b7i6m9@outlook.com",
        "vzsh3bkivlu7@outlook.com",
        "uybjrcda5bzo@outlook.com",
        "wroadirghdv7@outlook.com",
        "tgtq79ejcleo@outlook.com",
        "llpwob2ndxq8@outlook.com",
        "vgdfvkeb9l59@outlook.com",
        "lvjm4v5zt481@outlook.com",
        "zxmp5zm6nzc9@outlook.com",
        "dswiy4mlg335@outlook.com",
        "xlnnpc3jl7de@outlook.com",
        "gfge8pn3fm0u@outlook.com",
        "wkwt09ntx8gs@outlook.com",
        "ruud4y0qs8xq@outlook.com",
        "dnseggpc3dhx@outlook.com",
        "pfixsuxjr63s@outlook.com"
    ]
    
    # 合并图片中的所有邮箱
    all_image_emails = set(image1_emails + image2_emails)
    
    # 读取文本文件中的邮箱
    file_emails = []
    try:
        with open('output/cursor_accounts.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and '----' in line:
                    email = line.split('----')[0]
                    file_emails.append(email)
    except FileNotFoundError:
        print("找不到文件 output/cursor_accounts.txt")
        return
    
    file_emails_set = set(file_emails)
    
    # 找出在文件中但不在图片中的邮箱
    missing_in_images = file_emails_set - all_image_emails
    
    # 找出在图片中但不在文件中的邮箱
    extra_in_images = all_image_emails - file_emails_set
    
    print("=== 邮箱比较结果 ===")
    print(f"文件中总邮箱数量: {len(file_emails_set)}")
    print(f"图片中总邮箱数量: {len(all_image_emails)}")
    print()
    
    if missing_in_images:
        print("📋 在文件中但不在图片中显示的邮箱:")
        for email in sorted(missing_in_images):
            print(f"  - {email}")
        print()
    else:
        print("✅ 所有文件中的邮箱都在图片中显示了")
        print()
    
    if extra_in_images:
        print("🔍 在图片中但不在文件中的邮箱:")
        for email in sorted(extra_in_images):
            print(f"  - {email}")
        print()
    else:
        print("✅ 图片中的所有邮箱都在文件中")
        print()
    
    # 验证文件中的所有邮箱
    print("📝 文件中的所有邮箱列表:")
    for i, email in enumerate(sorted(file_emails_set), 1):
        status = "✅" if email in all_image_emails else "❌"
        print(f"  {i:2d}. {email} {status}")

if __name__ == "__main__":
    main() 