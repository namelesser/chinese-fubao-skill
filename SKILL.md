---
name: chinese-fubao-skill
description: Generate Chinese 冥包/袱包 sender and recipient kinship text from a stated family relationship, including married-woman surname forms and optional Ganzhi year/date lines. Use for 冥包、袱包、烧包、祭祀封包称谓填写; do not treat one regional convention as universal.
---

# 中文冥包／袱包称谓生成

根据用户给出的亲属关系、双方姓名和性别，生成可直接抄写的核心文字。

## 输出约定

- 默认只输出两行，不加解释、标题、表格或代码块：
  1. `孝…<送包人姓名>祀`
  2. `故…冥中收用`
- 默认横排，一列一行。用户要求日期时，另起一行输出 `天运<干支>年<农历月日>火化`。
- 默认省略 `讳`、`老大人`、`老孺人`。
- 女性收包人按已婚传统写法时，用 `夫姓+母+娘家姓氏`，如 `杨母陈氏`。夫姓或娘家姓不清楚时先询问，不猜姓。
- 关系称谓按送包人与收包人的实际关系和送包人性别选择，例如 `孝女`、`孝孙女`、`孝外甥女`、`孝媳`、`孝婿`。
- 对兄弟姐妹，必须确认收包人比送包人年长还是年幼，分别生成 `孝胞弟/妹` 或 `孝胞兄/姐`。

## 工作方式

1. 收集足够信息：关系、送包人姓名与性别、收包人姓名；女性传统姓氏格式还需夫姓与娘家姓。
2. 读取 [references/relationships.md](references/relationships.md) 选择称谓。表外或可能有地方差异的关系，再读取 [references/source-tables.md](references/source-tables.md)。
3. 生成两行核心文本。需要确定性结果或批量验证时，运行 `scripts/generate_fubao.py`。
4. 若用户提供的表或本地习俗与通行写法冲突，以用户提供表和用户明确确认的规则为准，并简短提示存在地方习俗差异。

## 日期

- 公历年份只用于换算干支年，不自动把公历日期换算成农历日期。
- 用户若只给公历月日，应先确认其要填写的农历月日。
- 干支算法以 1984 年为甲子年；例如 2025 为乙巳年，2026 为丙午年。

## 边界

- 不擅自补亡者姓名、夫姓、娘家姓、长幼顺序或农历日期。
- 表中没有的复杂姻亲、继亲或地方专称，说明需按当地习俗核实，不硬套。
- 本 Skill 只生成称谓文字，不宣称某一种写法在所有地区都唯一正确。

可运行示例见 [examples/basic.md](examples/basic.md)，脚本参数见仓库 [README.md](README.md)。
