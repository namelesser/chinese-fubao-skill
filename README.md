# chinese-fubao-skill

一个可复用的中文 Codex Skill，用亲属关系、性别和姓氏生成冥包／袱包的两列核心称谓。

默认输出横排文字，一列一行：

```text
孝外甥女兰大美祀
故舅妣杨母吴氏冥中收用
```

## 特点

- 自动选择 `孝男/孝女/孝孙/孝孙女/孝外孙女/孝外甥女/孝媳/孝婿` 等称谓。
- 支持父母、祖父母、外祖父母、兄弟姐妹、舅舅舅妈、岳父岳母、公公婆婆等常见关系。
- 支持女性 `夫姓+母+娘家姓氏` 格式，例如 `杨母陈氏`。
- 默认去掉 `讳`、`老大人/老孺人`。
- 可选生成干支年和农历日期栏；2026 年会得到 `丙午年`。
- 包含零依赖 Python 生成器和自动测试。

## 安装

克隆后把整个目录放入 Codex 的 Skills 目录，例如：

```bash
git clone https://github.com/namelesser/chinese-fubao-skill.git
cp -R chinese-fubao-skill ~/.codex/skills/chinese-fubao-skill
```

之后可在对话中使用 `$chinese-fubao-skill`，也可让 Codex 在冥包／袱包称谓请求中自动选择它。

## 需要提供的信息

最少提供：送包人姓名和性别、双方关系、收包人姓名。女性传统姓氏格式还需夫姓和娘家姓；兄弟姐妹还需长幼关系。

可选提供公历年份与农历月日。脚本只把公历年份换算成干支年，不负责公历日期转农历日期。

## 命令行

```bash
python3 scripts/generate_fubao.py \
  --relationship 舅舅 \
  --sender-name 兰大美 \
  --sender-gender female \
  --recipient-name 杨胜贤
```

女性收包人示例：

```bash
python3 scripts/generate_fubao.py \
  --relationship 舅妈 \
  --sender-name 兰大美 \
  --sender-gender female \
  --recipient-name 吴某 \
  --husband-surname 杨
```

带日期：

```bash
python3 scripts/generate_fubao.py \
  --relationship 公公 \
  --sender-name 兰大美 \
  --sender-gender female \
  --recipient-name 杨胜国 \
  --year 2026 \
  --lunar-month 七 \
  --lunar-day 十三
```

机器读取可加 `--json`。完整关系代码可运行 `python3 scripts/generate_fubao.py --help` 查看。

## 三张原始称谓表的整理原则

用户提供的三张表分别覆盖直系祖先，外亲、叔伯、堂亲与兄弟姐妹，以及岳家、继亲、乳亲与姻亲。

表中详细转写见 [references/source-tables.md](references/source-tables.md)，生成器当前稳定支持的常见关系见 [references/relationships.md](references/relationships.md)。原表中的男性送包人称谓会按用户实际性别调整；原表中的 `讳`、`老大人/老孺人` 默认省略。

## 地方习俗说明

冥包／袱包称谓并非全国完全统一。不同地区、家族或仪式体系可能采用不同词序和称谓。本项目以用户提供的三张对照表和已经确认的填写规则为优先依据；表外复杂关系应按当地习俗核实，不应由程序猜测。

## 测试

```bash
python3 -m unittest discover -s tests -v
python3 /path/to/skill-creator/scripts/quick_validate.py .
```

测试覆盖父母、祖母、舅舅舅妈、兄弟姐妹、儿媳/女婿身份、女性姓氏拼接以及 2025/2026 干支年。
