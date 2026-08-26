import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from generate_fubao import ganzhi_year, generate  # noqa: E402


class GenerateFubaoTests(unittest.TestCase):
    def test_father_from_daughter(self):
        result = generate(
            relationship="父亲", sender_name="兰大直", sender_gender="female", recipient_name="兰作林"
        )
        self.assertEqual(result.sender, "孝女兰大直祀")
        self.assertEqual(result.recipient, "故显考兰公作林冥中收用")

    def test_mother_uses_husband_and_maiden_surnames(self):
        result = generate(
            relationship="母亲", sender_name="兰大直", sender_gender="female",
            recipient_name="姚顺桥", husband_surname="兰",
        )
        self.assertEqual(result.recipient, "故显妣兰母姚氏冥中收用")

    def test_grandmother_from_granddaughter(self):
        result = generate(
            relationship="奶奶", sender_name="兰大美", sender_gender="female",
            recipient_name="陈某", husband_surname="杨",
        )
        self.assertEqual(result.sender, "孝孙女兰大美祀")
        self.assertEqual(result.recipient, "故祖妣杨母陈氏冥中收用")

    def test_maternal_uncle_from_niece(self):
        result = generate(
            relationship="舅舅", sender_name="兰大美", sender_gender="female", recipient_name="杨胜贤"
        )
        self.assertEqual(result.text(), "孝外甥女兰大美祀\n故舅考杨公胜贤冥中收用")

    def test_maternal_aunt_married_surname_form(self):
        result = generate(
            relationship="舅妈", sender_name="兰大美", sender_gender="female",
            recipient_name="吴某", husband_surname="杨",
        )
        self.assertEqual(result.recipient, "故舅妣杨母吴氏冥中收用")

    def test_older_brother_from_younger_sister(self):
        result = generate(
            relationship="哥哥", sender_name="兰大美", sender_gender="female", recipient_name="李永国"
        )
        self.assertEqual(result.sender, "孝胞妹兰大美祀")
        self.assertEqual(result.recipient, "故胞兄李永国冥中收用")

    def test_daughter_in_law_to_father_in_law(self):
        result = generate(
            relationship="公公", sender_name="兰大美", sender_gender="female", recipient_name="杨胜国"
        )
        self.assertEqual(result.sender, "孝媳兰大美祀")
        self.assertEqual(result.recipient, "故显考杨公胜国冥中收用")

    def test_son_in_law_to_mother_in_law(self):
        result = generate(
            relationship="岳母", sender_name="张伟", sender_gender="male",
            recipient_name="陈某", husband_surname="李",
        )
        self.assertEqual(result.sender, "孝婿张伟祀")
        self.assertEqual(result.recipient, "故岳妣李母陈氏冥中收用")

    def test_ganzhi_and_date(self):
        result = generate(
            relationship="父亲", sender_name="黄录祥", sender_gender="male", recipient_name="黄福珍",
            year=2026, lunar_month="七", lunar_day="十三",
        )
        self.assertEqual(ganzhi_year(2025), "乙巳")
        self.assertEqual(ganzhi_year(2026), "丙午")
        self.assertEqual(result.date, "天运丙午年七月十三日火化")

    def test_missing_husband_surname_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "husband-surname"):
            generate(
                relationship="母亲", sender_name="兰大直", sender_gender="female", recipient_name="姚顺桥"
            )


if __name__ == "__main__":
    unittest.main()
