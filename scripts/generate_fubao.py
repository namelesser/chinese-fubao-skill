#!/usr/bin/env python3
"""Generate the two core Chinese fubao inscription lines."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass


STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"
COMPOUND_SURNAMES = (
    "欧阳", "司马", "上官", "诸葛", "夏侯", "东方", "皇甫", "尉迟",
    "公孙", "慕容", "司徒", "司空", "令狐", "宇文", "长孙", "南宫",
)


RELATION_ALIASES = {
    "父亲": "father", "爸爸": "father", "老爸": "father",
    "母亲": "mother", "妈妈": "mother", "老妈": "mother",
    "爷爷": "paternal_grandfather", "祖父": "paternal_grandfather",
    "奶奶": "paternal_grandmother", "祖母": "paternal_grandmother",
    "外公": "maternal_grandfather", "外祖父": "maternal_grandfather",
    "外婆": "maternal_grandmother", "外祖母": "maternal_grandmother",
    "哥哥": "older_brother", "兄长": "older_brother",
    "弟弟": "younger_brother", "姐姐": "older_sister", "妹妹": "younger_sister",
    "舅舅": "maternal_uncle", "舅父": "maternal_uncle",
    "舅妈": "maternal_aunt", "舅母": "maternal_aunt", "舅娘": "maternal_aunt",
    "岳父": "wife_father", "岳母": "wife_mother",
    "公公": "husband_father", "婆婆": "husband_mother",
}


RELATIONS = {
    "father": ("故显考", "male", "child"),
    "mother": ("故显妣", "female", "child"),
    "paternal_grandfather": ("故祖考", "male", "grandchild"),
    "paternal_grandmother": ("故祖妣", "female", "grandchild"),
    "maternal_grandfather": ("故外祖考", "male", "maternal_grandchild"),
    "maternal_grandmother": ("故外祖妣", "female", "maternal_grandchild"),
    "older_brother": ("故胞兄", "plain", "younger_sibling"),
    "younger_brother": ("故胞弟", "plain", "older_sibling"),
    "older_sister": ("故胞姐", "plain", "younger_sibling"),
    "younger_sister": ("故胞妹", "plain", "older_sibling"),
    "maternal_uncle": ("故舅考", "male", "maternal_nibling"),
    "maternal_aunt": ("故舅妣", "female", "maternal_nibling"),
    "wife_father": ("故岳考", "male", "son_in_law"),
    "wife_mother": ("故岳妣", "female", "son_in_law"),
    "husband_father": ("故显考", "male", "daughter_in_law"),
    "husband_mother": ("故显妣", "female", "daughter_in_law"),
}


@dataclass(frozen=True)
class Result:
    sender: str
    recipient: str
    date: str | None = None

    def text(self) -> str:
        return "\n".join(x for x in (self.sender, self.recipient, self.date) if x)


def ganzhi_year(year: int) -> str:
    """Return the sexagenary-cycle name; 1984 is 甲子."""
    offset = year - 1984
    return STEMS[offset % 10] + BRANCHES[offset % 12]


def split_name(full_name: str, explicit_surname: str | None = None) -> tuple[str, str]:
    full_name = full_name.strip()
    if explicit_surname:
        surname = explicit_surname.strip()
        if not full_name.startswith(surname):
            raise ValueError("收包人姓名必须以指定姓氏开头")
    else:
        surname = next((s for s in COMPOUND_SURNAMES if full_name.startswith(s)), full_name[:1])
    given_name = full_name[len(surname):]
    if not surname or not given_name:
        raise ValueError("男性收包人需要完整姓名；复姓可用 --recipient-surname 指定")
    return surname, given_name


def sender_title(role: str, gender: str) -> str:
    if gender not in {"male", "female"}:
        raise ValueError("sender_gender 必须是 male 或 female")
    by_gender = {
        "child": ("孝男", "孝女"),
        "grandchild": ("孝孙", "孝孙女"),
        "maternal_grandchild": ("孝外孙", "孝外孙女"),
        "maternal_nibling": ("孝外甥", "孝外甥女"),
        "younger_sibling": ("孝胞弟", "孝胞妹"),
        "older_sibling": ("孝胞兄", "孝胞姐"),
    }
    if role in by_gender:
        return by_gender[role][gender == "female"]
    if role == "son_in_law":
        if gender != "male":
            raise ValueError("岳父/岳母关系要求送包人为女婿；女儿应选择父亲/母亲关系")
        return "孝婿"
    if role == "daughter_in_law":
        if gender != "female":
            raise ValueError("公公/婆婆关系要求送包人为儿媳；儿子应选择父亲/母亲关系")
        return "孝媳"
    raise ValueError(f"未知送包人角色: {role}")


def generate(
    *,
    relationship: str,
    sender_name: str,
    sender_gender: str,
    recipient_name: str | None = None,
    recipient_surname: str | None = None,
    husband_surname: str | None = None,
    maiden_surname: str | None = None,
    year: int | None = None,
    lunar_month: str | None = None,
    lunar_day: str | None = None,
    date_action: str = "火化",
) -> Result:
    relationship = RELATION_ALIASES.get(relationship.strip(), relationship.strip())
    if relationship not in RELATIONS:
        supported = "、".join(RELATIONS)
        raise ValueError(f"不支持的关系 {relationship!r}；可用值：{supported}")
    if not sender_name.strip():
        raise ValueError("送包人姓名不能为空")

    recipient_title, name_style, role = RELATIONS[relationship]
    s_title = sender_title(role, sender_gender)

    if name_style == "male":
        if not recipient_name:
            raise ValueError("男性收包人需要 --recipient-name")
        surname, given_name = split_name(recipient_name, recipient_surname)
        recipient_identity = f"{surname}公{given_name}"
    elif name_style == "female":
        inferred_maiden = None
        if recipient_name:
            inferred_maiden = split_name(recipient_name)[0]
        maiden = (maiden_surname or inferred_maiden or "").strip()
        husband = (husband_surname or "").strip()
        if not husband or not maiden:
            raise ValueError("女性传统写法需要 --husband-surname 和娘家姓；娘家姓可由 --recipient-name 推断")
        recipient_identity = f"{husband}母{maiden}氏"
    else:
        if not recipient_name or not recipient_name.strip():
            raise ValueError("兄弟姐妹收包人需要 --recipient-name")
        recipient_identity = recipient_name.strip()

    date_line = None
    if lunar_month or lunar_day:
        if year is None or not lunar_month or not lunar_day:
            raise ValueError("日期栏需要同时提供 --year、--lunar-month、--lunar-day")
    if year is not None:
        date_line = f"天运{ganzhi_year(year)}年"
        if lunar_month and lunar_day:
            date_line += f"{lunar_month}月{lunar_day}日{date_action}"

    return Result(
        sender=f"{s_title}{sender_name.strip()}祀",
        recipient=f"{recipient_title}{recipient_identity}冥中收用",
        date=date_line,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="生成冥包/袱包送包人与收包人两列核心文字")
    parser.add_argument("--relationship", required=True, help="关系代码或常用中文，如 father、父亲、舅妈、岳父")
    parser.add_argument("--sender-name", required=True)
    parser.add_argument("--sender-gender", required=True, choices=("male", "female"))
    parser.add_argument("--recipient-name")
    parser.add_argument("--recipient-surname", help="男性复姓或需显式指定姓氏时使用")
    parser.add_argument("--husband-surname", help="女性收包人所嫁夫姓")
    parser.add_argument("--maiden-surname", help="女性收包人娘家姓；省略时从 recipient-name 推断")
    parser.add_argument("--year", type=int, help="公历年份，仅用于换算干支年")
    parser.add_argument("--lunar-month", help="农历月份文字，如 七")
    parser.add_argument("--lunar-day", help="农历日期文字，如 十三")
    parser.add_argument("--date-action", default="火化")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        result = generate(**{k: v for k, v in vars(args).items() if k != "json"})
    except ValueError as exc:
        raise SystemExit(f"错误：{exc}") from exc
    if args.json:
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    else:
        print(result.text())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
