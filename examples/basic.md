# 使用示例

## 对话式生成

用户：兰大美，女，写给舅舅杨胜贤。

```text
孝外甥女兰大美祀
故舅考杨公胜贤冥中收用
```

用户：兰大美，女，写给舅妈。舅家姓杨，舅妈娘家姓吴。

```text
孝外甥女兰大美祀
故舅妣杨母吴氏冥中收用
```

用户：兰大美是儿媳，写给公公杨胜国，日期是 2026 年农历七月十三。

```text
孝媳兰大美祀
故显考杨公胜国冥中收用
天运丙午年七月十三日火化
```

## 命令行生成

```bash
python3 scripts/generate_fubao.py \
  --relationship 舅妈 \
  --sender-name 兰大美 \
  --sender-gender female \
  --recipient-name 吴某 \
  --husband-surname 杨
```

默认输出两行；加入 `--year 2026 --lunar-month 七 --lunar-day 十三` 后会增加日期行。
