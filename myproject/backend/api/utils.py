import pandas as pd
from pathlib import Path
from django.conf import settings
from slugify import slugify
from collections import defaultdict

import re

def load_peraturan_with_slug(csv_path="data/data_aturan.xlsx"):
    df = pd.read_excel(csv_path)
    df = df.fillna("-")
    aturan_dict = {}

    for idx, row in df.iterrows():
        for col in df.columns:
            if col.startswith("ATURAN."):
                aturan_text = row[col]
                match_nomor_tahun = re.search(r"(\d+)[/](\d+)", aturan_text)
                if aturan_text and aturan_text.strip() not in ["", "-"]:
                    slug = slugify(aturan_text.strip())
                    item = {
                        "slug": slug,
                        "text": aturan_text.strip(),
                        "row": row.to_dict(),
                        "source_col": col,
                        "topik": row.get("LEVEL.4", ""),
                        "jenis": row.get("LEVEL.2", ""),
                        "nomor": match_nomor_tahun.group(1) if match_nomor_tahun else "",
                        "tahun": match_nomor_tahun.group(2) if match_nomor_tahun else "",
                        "tentang": aturan_text.strip().split(" - ", 1)[-1] if " - " in aturan_text  else "",
                        "status": row.get("STATUS.1", ""),
                        "link": row.get(f"LINK.{col.split('.')[-1]}", ""),
                        "remark": "\n".join(
                            str(row[k]) for k in row.keys()
                            if k.startswith("REMARK.") and str(row[k]).strip() != "-" and str(row[k]).strip() != ""
                        ),
                    }
                    aturan_dict.setdefault(slug, []).append(item)

    return aturan_dict
    
def filter_grouped_peraturan(semua_aturan, level_filters=None, search_query=""):
    grouped_dict_level1 = defaultdict(lambda: defaultdict(list))

    for items in semua_aturan.values():
        for item in items:
            row = item["row"]
            slug = item["slug"]
            aturan_text = item["text"]
            remark_col = f"REMARK.{item['source_col'].split('.')[-1]}"
            remark = row.get(remark_col)
            link_col = f"LINK.{item['source_col'].split('.')[-1]}"
            link = row.get(link_col)

            level1 = str(row.get('LEVEL.1')).strip()

            # Filter berdasarkan level
            if level_filters:
                match = True
                for key, val in level_filters.items():
                    if val and row.get(key) != val:
                        match = False
                        break
                if not match:
                    continue

            # Filter berdasarkan search
            if search_query:
                search_area = f"{aturan_text} {remark or ''} {row.get('LEVEL.2', '')} {row.get('LEVEL.3', '')}"
                if search_query.lower() not in search_area.lower():
                    continue

            grouped_dict_level1[level1][aturan_text].append({
                'remark': remark,
                'slug': slug,
                'link': link
            })

    cleaned_dict = {}

    for lvl1, aturan_dict in grouped_dict_level1.items():
        cleaned_dict[lvl1] = {}
        for aturan, remarks in aturan_dict.items():
            seen = set()
            unique_remarks = []
            for r in remarks:
                key = (r['remark'], r['link'])
                if key not in seen:
                    seen.add(key)
                    unique_remarks.append(r)
            cleaned_dict[lvl1][aturan] = unique_remarks

    return cleaned_dict