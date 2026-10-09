# 小红书育儿图文 / Xiaohongshu Parenting Notes

面向小红书的**育儿图文**素材库：每篇笔记含标题、正文、话题标签，以及竖版（3:4）封面与内容卡片图，方便直接发布。

A small library of Xiaohongshu-ready parenting image-text notes (covers + tip cards + publishable copy).

## 目录结构

```
RULES.md                 # 8 条站立规则（v2，后续笔记必遵）
notes/
  01-naifen-chongtiao/   # 第一篇：0–6 月冲奶避坑
    note.md              # 可发布文案
    preview.html         # 本地预览页
    images/
      cover.png
      card-01.png … card-06.png  # 含标准流程清单
      checklist.png              # 清单卡别名
topics.md                # 选题池与状态
generate_images.py       # Pillow 生成 3:4 粉彩配图
```

## 笔记组织方式

- 每篇一个子目录：`notes/序号-拼音短名/`
- `note.md` 是发布底稿；`images/` 放竖版配图
- `topics.md` 记录选题池与状态
- 新篇请先读 `RULES.md`

## 第一篇（v2）

**0–6月冲奶5坑｜先水后粉别搞反**

封面主标题：冲奶避坑。配图：封面 + 5 张避坑卡（误区→正确做法→后果）+ 1 张冲奶标准流程清单。

## License

内容与配图供个人账号发布使用；请勿冒充医疗机构或具体品牌背书。冲调请以罐上说明为准。
