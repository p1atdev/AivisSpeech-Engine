"""
モーラと音素の対応関係。

以下のモーラ対応表はOpenJTalkのソースコードから取得し、
カタカナ表記とモーラが一対一対応するように改造した。
ライセンス表記：
-----------------------------------------------------------------
          The Japanese TTS System "Open JTalk"
          developed by HTS Working Group
          http://open-jtalk.sourceforge.net/
-----------------------------------------------------------------

 Copyright (c) 2008-2014  Nagoya Institute of Technology
                          Department of Computer Science

All rights reserved.

Redistribution and use in source and binary forms, with or
without modification, are permitted provided that the following
conditions are met:

- Redistributions of source code must retain the above copyright
  notice, this list of conditions and the following disclaimer.
- Redistributions in binary form must reproduce the above
  copyright notice, this list of conditions and the following
  disclaimer in the documentation and/or other materials provided
  with the distribution.
- Neither the name of the HTS working group nor the names of its
  contributors may be used to endorse or promote products derived
  from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS
BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

from typing import Literal

from .phoneme import BaseVowel, Consonant

# AquesTalk 風記法で記述されるモーラ（無声化 `_` を除く）
_MoraKana = Literal[
    "ァ",
    "ア",
    "ィ",
    "イ",
    "イェ",
    "ゥ",
    "ウ",
    "ウィ",
    "ウェ",
    "ウォ",
    "ェ",
    "エ",
    "ォ",
    "オ",
    "カ",
    "ガ",
    "キ",
    "キェ",
    "キャ",
    "キュ",
    "キョ",
    "ギ",
    "ギェ",
    "ギャ",
    "ギュ",
    "ギョ",
    "ク",
    "クァ",
    "クィ",
    "クゥ",
    "クェ",
    "クォ",
    "クヮ",
    "グ",
    "グァ",
    "グィ",
    "グゥ",
    "グェ",
    "グォ",
    "グヮ",
    "ケ",
    "ゲ",
    "コ",
    "ゴ",
    "サ",
    "ザ",
    "シ",
    "シィ",  # pyopenjtalk-plus で追加されたモーラ
    "シェ",
    "シャ",
    "シュ",
    "ショ",
    "ジ",
    "ジェ",
    "ジャ",
    "ジュ",
    "ジョ",
    "ス",
    "スィ",
    "ズ",
    "ズィ",
    "セ",
    "ゼ",
    "ソ",
    "ゾ",
    "タ",
    "ダ",
    "チ",
    "チェ",
    "チャ",
    "チュ",
    "チョ",
    "ヂ",
    "ヂェ",
    "ヂャ",
    "ヂュ",
    "ヂョ",
    "ッ",
    "ツ",
    "ツァ",
    "ツィ",
    "ツェ",
    "ツォ",
    "ヅ",
    "テ",
    "ティ",
    "テャ",
    "テュ",
    "テョ",
    "デ",
    "ディ",
    "デェ",
    "デャ",
    "デュ",
    "デョ",
    "ト",
    "トゥ",
    "ド",
    "ドゥ",
    "ナ",
    "ニ",
    "ニェ",
    "ニャ",
    "ニュ",
    "ニョ",
    "ヌ",
    "ネ",
    "ノ",
    "ハ",
    "バ",
    "パ",
    "ヒ",
    "ヒェ",
    "ヒャ",
    "ヒュ",
    "ヒョ",
    "ビ",
    "ビェ",
    "ビャ",
    "ビュ",
    "ビョ",
    "ピ",
    "ピェ",
    "ピャ",
    "ピュ",
    "ピョ",
    "フ",
    "ファ",
    "フィ",
    "フェ",
    "フォ",
    "フュ",  # pyopenjtalk-plus で追加されたモーラ
    "ブ",
    "プ",
    "ヘ",
    "ベ",
    "ペ",
    "ホ",
    "ボ",
    "ポ",
    "マ",
    "ミ",
    "ミェ",
    "ミャ",
    "ミュ",
    "ミョ",
    "ム",
    "メ",
    "モ",
    "ャ",
    "ヤ",
    "ュ",
    "ユ",
    "ョ",
    "ヨ",
    "ラ",
    "リ",
    "リェ",
    "リャ",
    "リュ",
    "リョ",
    "ル",
    "レ",
    "ロ",
    "ヮ",
    "ワ",
    "ヰ",
    "ヱ",
    "ヲ",
    "ン",
    "ヴ",
    "ヴァ",
    "ヴィ",
    "ヴェ",
    "ヴォ",
    "ヴャ",
    "ヴュ",
    "ヴョ",
    "ヶ",
]

_mora_list_minimum: list[tuple[_MoraKana, Consonant | None, BaseVowel]] = [
    ("ヴォ", "v", "o"),
    ("ヴェ", "v", "e"),
    ("ヴィ", "v", "i"),
    ("ヴァ", "v", "a"),
    ("ヴ", "v", "u"),
    ("ン", None, "N"),
    ("ワ", "w", "a"),
    ("ロ", "r", "o"),
    ("レ", "r", "e"),
    ("ル", "r", "u"),
    ("リョ", "ry", "o"),
    ("リュ", "ry", "u"),
    ("リャ", "ry", "a"),
    ("リェ", "ry", "e"),
    ("リ", "r", "i"),
    ("ラ", "r", "a"),
    ("ヨ", "y", "o"),
    ("ユ", "y", "u"),
    ("ヤ", "y", "a"),
    ("モ", "m", "o"),
    ("メ", "m", "e"),
    ("ム", "m", "u"),
    ("ミョ", "my", "o"),
    ("ミュ", "my", "u"),
    ("ミャ", "my", "a"),
    ("ミェ", "my", "e"),
    ("ミ", "m", "i"),
    ("マ", "m", "a"),
    ("ポ", "p", "o"),
    ("ボ", "b", "o"),
    ("ホ", "h", "o"),
    ("ペ", "p", "e"),
    ("ベ", "b", "e"),
    ("ヘ", "h", "e"),
    ("プ", "p", "u"),
    ("ブ", "b", "u"),
    ("フュ", "fy", "u"),  # pyopenjtalk-plus で追加されたモーラ
    ("フォ", "f", "o"),
    ("フェ", "f", "e"),
    ("フィ", "f", "i"),
    ("ファ", "f", "a"),
    ("フ", "f", "u"),
    ("ピョ", "py", "o"),
    ("ピュ", "py", "u"),
    ("ピャ", "py", "a"),
    ("ピェ", "py", "e"),
    ("ピ", "p", "i"),
    ("ビョ", "by", "o"),
    ("ビュ", "by", "u"),
    ("ビャ", "by", "a"),
    ("ビェ", "by", "e"),
    ("ビ", "b", "i"),
    ("ヒョ", "hy", "o"),
    ("ヒュ", "hy", "u"),
    ("ヒャ", "hy", "a"),
    ("ヒェ", "hy", "e"),
    ("ヒ", "h", "i"),
    ("パ", "p", "a"),
    ("バ", "b", "a"),
    ("ハ", "h", "a"),
    ("ノ", "n", "o"),
    ("ネ", "n", "e"),
    ("ヌ", "n", "u"),
    ("ニョ", "ny", "o"),
    ("ニュ", "ny", "u"),
    ("ニャ", "ny", "a"),
    ("ニェ", "ny", "e"),
    ("ニ", "n", "i"),
    ("ナ", "n", "a"),
    ("ドゥ", "d", "u"),
    ("ド", "d", "o"),
    ("トゥ", "t", "u"),
    ("ト", "t", "o"),
    ("デョ", "dy", "o"),
    ("デュ", "dy", "u"),
    ("デャ", "dy", "a"),
    ("デェ", "dy", "e"),  # pyopenjtalk-plus で追加されたモーラ
    ("ディ", "d", "i"),
    ("デ", "d", "e"),
    ("テョ", "ty", "o"),
    ("テュ", "ty", "u"),
    ("テャ", "ty", "a"),
    ("ティ", "t", "i"),
    ("テ", "t", "e"),
    ("ツォ", "ts", "o"),
    ("ツェ", "ts", "e"),
    ("ツィ", "ts", "i"),
    ("ツァ", "ts", "a"),
    ("ツ", "ts", "u"),
    ("ッ", None, "cl"),
    ("チョ", "ch", "o"),
    ("チュ", "ch", "u"),
    ("チャ", "ch", "a"),
    ("チェ", "ch", "e"),
    ("チ", "ch", "i"),
    ("ダ", "d", "a"),
    ("タ", "t", "a"),
    ("ゾ", "z", "o"),
    ("ソ", "s", "o"),
    ("ゼ", "z", "e"),
    ("セ", "s", "e"),
    ("ズィ", "z", "i"),
    ("ズ", "z", "u"),
    ("スィ", "s", "i"),
    ("ス", "s", "u"),
    ("ジョ", "j", "o"),
    ("ジュ", "j", "u"),
    ("ジャ", "j", "a"),
    ("ジェ", "j", "e"),
    ("ジ", "j", "i"),
    ("ショ", "sh", "o"),
    ("シュ", "sh", "u"),
    ("シャ", "sh", "a"),
    ("シェ", "sh", "e"),
    ("シ", "sh", "i"),
    ("ザ", "z", "a"),
    ("サ", "s", "a"),
    ("ゴ", "g", "o"),
    ("コ", "k", "o"),
    ("ゲ", "g", "e"),
    ("ケ", "k", "e"),
    ("グヮ", "gw", "a"),  # pyopenjtalk-plus で追加されたモーラ
    ("グォ", "gw", "o"),  # pyopenjtalk-plus で追加されたモーラ
    ("グェ", "gw", "e"),  # pyopenjtalk-plus で追加されたモーラ
    ("グゥ", "gw", "u"),  # pyopenjtalk-plus で追加されたモーラ
    ("グィ", "gw", "i"),  # pyopenjtalk-plus で追加されたモーラ
    ("グ", "g", "u"),
    ("クヮ", "kw", "a"),  # pyopenjtalk-plus で追加されたモーラ
    ("クォ", "kw", "o"),  # pyopenjtalk-plus で追加されたモーラ
    ("クェ", "kw", "e"),  # pyopenjtalk-plus で追加されたモーラ
    ("クゥ", "kw", "u"),  # pyopenjtalk-plus で追加されたモーラ
    ("クィ", "kw", "i"),  # pyopenjtalk-plus で追加されたモーラ
    ("ク", "k", "u"),
    ("ギョ", "gy", "o"),
    ("ギュ", "gy", "u"),
    ("ギャ", "gy", "a"),
    ("ギェ", "gy", "e"),
    ("ギ", "g", "i"),
    ("キョ", "ky", "o"),
    ("キュ", "ky", "u"),
    ("キャ", "ky", "a"),
    ("キェ", "ky", "e"),
    ("キ", "k", "i"),
    ("ガ", "g", "a"),
    ("カ", "k", "a"),
    ("オ", None, "o"),
    ("エ", None, "e"),
    ("ウォ", "w", "o"),
    ("ウェ", "w", "e"),
    ("ウィ", "w", "i"),
    ("ウ", None, "u"),
    ("イェ", "y", "e"),
    ("イ", None, "i"),
    ("ア", None, "a"),
]
_mora_list_additional: list[tuple[_MoraKana, Consonant | None, BaseVowel]] = [
    ("ヴョ", "by", "o"),
    ("ヴュ", "by", "u"),
    ("ヴャ", "by", "a"),
    ("ヲ", None, "o"),
    ("ヱ", None, "e"),
    ("ヰ", None, "i"),
    ("ヮ", "w", "a"),
    ("ョ", "y", "o"),
    ("ュ", "y", "u"),
    ("ヅ", "z", "u"),
    ("ヂョ", "j", "o"),  # pyopenjtalk-plus には存在しないエイリアス
    ("ヂュ", "j", "u"),  # pyopenjtalk-plus には存在しないエイリアス
    ("ヂャ", "j", "a"),  # pyopenjtalk-plus には存在しないエイリアス
    ("ヂェ", "j", "e"),  # pyopenjtalk-plus には存在しないエイリアス
    ("ヂ", "j", "i"),
    ("シィ", "s", "i"),  # pyopenjtalk-plus で追加されたモーラ
    ("グァ", "gw", "a"),  # pyopenjtalk-plus で追加されたモーラ
    ("クァ", "kw", "a"),  # pyopenjtalk-plus で追加されたモーラ
    ("ヶ", "k", "e"),
    ("ャ", "y", "a"),
    ("ォ", None, "o"),
    ("ェ", None, "e"),
    ("ゥ", None, "u"),
    ("ィ", None, "i"),
    ("ァ", None, "a"),
]

# 「hi」→「ヒ」
mora_phonemes_to_mora_kana: dict[str, _MoraKana] = {
    (consonant or "") + vowel: kana for [kana, consonant, vowel] in _mora_list_minimum
}
# 「ヒ」→「hi」
mora_kana_to_mora_phonemes: dict[_MoraKana, tuple[Consonant | None, BaseVowel]] = {
    kana: (consonant, vowel)
    for [kana, consonant, vowel] in _mora_list_minimum + _mora_list_additional
}
