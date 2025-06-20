"""ユーザー辞書の単体テスト。"""

import json
import sys
from copy import deepcopy
from pathlib import Path

import pytest
from pyopenjtalk import g2p, unset_user_dict

from voicevox_engine.user_dict.constants import (
    PART_OF_SPEECH_DATA,
    USER_DICT_MAX_PRIORITY,
    WordProperty,
    WordTypes,
)
from voicevox_engine.user_dict.model import UserDictInputError, UserDictWord
from voicevox_engine.user_dict.user_dict_manager import UserDictionary

# jsonとして保存される正しい形式の辞書データ
valid_dict_dict_json = {
    "aab7dda2-0d97-43c8-8cb7-3f440dab9b4e": {
        "surface": "テスト",
        "priority": 5,
        "part_of_speech": "名詞",
        "part_of_speech_detail_1": "固有名詞",
        "part_of_speech_detail_2": "一般",
        "part_of_speech_detail_3": "*",
        "inflectional_type": "*",
        "inflectional_form": "*",
        "stem": ["テスト"],
        "yomi": ["テスト"],
        "pronunciation": ["テスト"],
        "accent_type": [1],
        "accent_associative_rule": "*",
    },
}

# APIでやり取りされる正しい形式の辞書データ
valid_dict_dict_api = deepcopy(valid_dict_dict_json)
valid_dict_dict_api["aab7dda2-0d97-43c8-8cb7-3f440dab9b4e"]["priority"] = 5

import_word = UserDictWord(
    surface="テスト２",
    priority=5,
    part_of_speech="名詞",
    part_of_speech_detail_1="固有名詞",
    part_of_speech_detail_2="一般",
    part_of_speech_detail_3="*",
    inflectional_type="*",
    inflectional_form="*",
    stem=["テストツー"],
    yomi=["テストツー"],
    pronunciation=["テストツー"],
    accent_type=[1],
    accent_associative_rule="*",
)


def _get_new_word(user_dict: dict[str, UserDictWord]) -> UserDictWord:
    assert len(user_dict) == 2 or (
        len(user_dict) == 1 and "aab7dda2-0d97-43c8-8cb7-3f440dab9b4e" not in user_dict
    )
    for word_uuid in user_dict.keys():
        if word_uuid == "aab7dda2-0d97-43c8-8cb7-3f440dab9b4e":
            continue
        return user_dict[word_uuid]
    raise AssertionError


def test_read_not_exist_json(tmp_path: Path) -> None:
    user_dict = UserDictionary(user_dict_path=tmp_path / "not_exist.json")
    assert user_dict.get_all_words() == {}


def test_create_word() -> None:
    # 将来的に品詞などが追加された時にテストを増やす
    assert UserDictWord.from_word_property(
        WordProperty(
            surface=["test"],
            pronunciation=["テスト"],
            accent_type=[1],
            word_type=WordTypes.PROPER_NOUN,
            priority=5,
        )
    ) == UserDictWord(
        surface="テスト",
        priority=5,
        part_of_speech="名詞",
        part_of_speech_detail_1="固有名詞",
        part_of_speech_detail_2="一般",
        part_of_speech_detail_3="*",
        inflectional_type="*",
        inflectional_form="*",
        stem=["ｔｅｓｔ"],
        yomi=["テスト"],
        pronunciation=["テスト"],
        accent_type=[1],
        accent_associative_rule="*",
    )


def test_apply_word_without_json(tmp_path: Path) -> None:
    user_dict = UserDictionary(
        user_dict_path=tmp_path / "test_apply_word_without_json.json"
    )
    user_dict.add_word(
        WordProperty(
            surface=["test"],
            pronunciation=["テスト"],
            accent_type=[1],
            word_type=WordTypes.PROPER_NOUN,
            priority=5,
        )
    )
    res = user_dict.get_all_words()
    assert len(res) == 1
    new_word = _get_new_word(res)
    assert (
        new_word.surface,
        new_word.pronunciation,
        new_word.accent_type,
    ) == ("テスト", ["テスト"], [1])


def test_apply_word_with_json(tmp_path: Path) -> None:
    user_dict_path = tmp_path / "test_apply_word_with_json.json"
    user_dict_path.write_text(
        json.dumps(valid_dict_dict_json, ensure_ascii=False), encoding="utf-8"
    )
    user_dict = UserDictionary(user_dict_path=user_dict_path)
    user_dict.add_word(
        WordProperty(
            surface=["test2"],
            pronunciation=["テストツー"],
            accent_type=[3],
            word_type=WordTypes.PROPER_NOUN,
            priority=5,
        )
    )
    res = user_dict.get_all_words()
    assert len(res) == 2
    new_word = _get_new_word(res)
    assert (
        new_word.surface,
        new_word.pronunciation,
        new_word.accent_type,
    ) == ("テストツー", ["テストツー"], [3])


def test_rewrite_word_invalid_id(tmp_path: Path) -> None:
    user_dict_path = tmp_path / "test_rewrite_word_invalid_id.json"
    user_dict_path.write_text(
        json.dumps(valid_dict_dict_json, ensure_ascii=False), encoding="utf-8"
    )
    user_dict = UserDictionary(user_dict_path=user_dict_path)
    with pytest.raises(UserDictInputError):
        user_dict.update_word(
            "c2be4dc5-d07d-4767-8be1-04a1bb3f05a9",
            WordProperty(
                surface=["test2"],
                pronunciation=["テストツー"],
                accent_type=[2],
                word_type=WordTypes.PROPER_NOUN,
                priority=5,
            ),
        )


def test_rewrite_word_valid_id(tmp_path: Path) -> None:
    user_dict_path = tmp_path / "test_rewrite_word_valid_id.json"
    user_dict_path.write_text(
        json.dumps(valid_dict_dict_json, ensure_ascii=False), encoding="utf-8"
    )
    user_dict = UserDictionary(user_dict_path=user_dict_path)
    user_dict.update_word(
        "aab7dda2-0d97-43c8-8cb7-3f440dab9b4e",
        WordProperty(
            surface=["test2"],
            pronunciation=["テストツー"],
            accent_type=[2],
            word_type=WordTypes.PROPER_NOUN,
            priority=5,
        ),
    )
    new_word = user_dict.get_all_words()["aab7dda2-0d97-43c8-8cb7-3f440dab9b4e"]
    assert (new_word.surface, new_word.pronunciation, new_word.accent_type) == (
        "テストツー",
        ["テストツー"],
        [2],
    )


def test_delete_word_invalid_id(tmp_path: Path) -> None:
    user_dict_path = tmp_path / "test_delete_word_invalid_id.json"
    user_dict_path.write_text(
        json.dumps(valid_dict_dict_json, ensure_ascii=False), encoding="utf-8"
    )
    user_dict = UserDictionary(user_dict_path=user_dict_path)
    with pytest.raises(UserDictInputError):
        user_dict.delete_word(word_uuid="c2be4dc5-d07d-4767-8be1-04a1bb3f05a9")


def test_delete_word_valid_id(tmp_path: Path) -> None:
    user_dict_path = tmp_path / "test_delete_word_valid_id.json"
    user_dict_path.write_text(
        json.dumps(valid_dict_dict_json, ensure_ascii=False), encoding="utf-8"
    )
    user_dict = UserDictionary(user_dict_path=user_dict_path)
    user_dict.delete_word(word_uuid="aab7dda2-0d97-43c8-8cb7-3f440dab9b4e")
    assert len(user_dict.get_all_words()) == 0


def test_priority() -> None:
    for pos in PART_OF_SPEECH_DATA:
        for i in range(USER_DICT_MAX_PRIORITY + 1):
            assert (
                UserDictWord.from_word_property(
                    WordProperty(
                        surface=["test"],
                        pronunciation=["テスト"],
                        accent_type=[1],
                        word_type=pos,
                        priority=i,
                    )
                ).priority
                == i
            )


def test_import_dict(tmp_path: Path) -> None:
    user_dict_path = tmp_path / "test_import_dict.json"
    user_dict_path.write_text(
        json.dumps(valid_dict_dict_json, ensure_ascii=False), encoding="utf-8"
    )
    user_dict = UserDictionary(user_dict_path=user_dict_path)
    user_dict.import_dictionary(
        {"b1affe2a-d5f0-4050-926c-f28e0c1d9a98": import_word}, override=False
    )
    assert (
        user_dict.get_all_words()["b1affe2a-d5f0-4050-926c-f28e0c1d9a98"] == import_word
    )
    assert user_dict.get_all_words()[
        "aab7dda2-0d97-43c8-8cb7-3f440dab9b4e"
    ] == UserDictWord(
        **valid_dict_dict_api["aab7dda2-0d97-43c8-8cb7-3f440dab9b4e"]  # type: ignore
    )


def test_import_dict_no_override(tmp_path: Path) -> None:
    user_dict_path = tmp_path / "test_import_dict_no_override.json"
    user_dict_path.write_text(
        json.dumps(valid_dict_dict_json, ensure_ascii=False), encoding="utf-8"
    )
    user_dict = UserDictionary(user_dict_path=user_dict_path)
    user_dict.import_dictionary(
        {"aab7dda2-0d97-43c8-8cb7-3f440dab9b4e": import_word}, override=False
    )
    assert user_dict.get_all_words()[
        "aab7dda2-0d97-43c8-8cb7-3f440dab9b4e"
    ] == UserDictWord(
        **valid_dict_dict_api["aab7dda2-0d97-43c8-8cb7-3f440dab9b4e"]  # type: ignore
    )


def test_import_dict_override(tmp_path: Path) -> None:
    user_dict_path = tmp_path / "test_import_dict_override.json"
    user_dict_path.write_text(
        json.dumps(valid_dict_dict_json, ensure_ascii=False), encoding="utf-8"
    )
    user_dict = UserDictionary(user_dict_path=user_dict_path)
    user_dict.import_dictionary(
        {"aab7dda2-0d97-43c8-8cb7-3f440dab9b4e": import_word}, override=True
    )
    assert (
        user_dict.get_all_words()["aab7dda2-0d97-43c8-8cb7-3f440dab9b4e"] == import_word
    )


def test_import_invalid_word(tmp_path: Path) -> None:
    user_dict_path = tmp_path / "test_import_invalid_dict.json"
    invalid_accent_associative_rule_word = deepcopy(import_word)
    invalid_accent_associative_rule_word.accent_associative_rule = "invalid"
    user_dict_path.write_text(
        json.dumps(valid_dict_dict_json, ensure_ascii=False), encoding="utf-8"
    )
    user_dict = UserDictionary(user_dict_path=user_dict_path)
    with pytest.raises(AssertionError):
        user_dict.import_dictionary(
            {
                "aab7dda2-0d97-43c8-8cb7-3f440dab9b4e": invalid_accent_associative_rule_word
            },
            override=True,
        )
    invalid_pos_word = deepcopy(import_word)
    invalid_pos_word.context_id = 2
    # @model_validator(mode="after") のバリデーションをバイパスする
    object.__setattr__(invalid_pos_word, "part_of_speech", "フィラー")
    object.__setattr__(invalid_pos_word, "part_of_speech_detail_1", "*")
    object.__setattr__(invalid_pos_word, "part_of_speech_detail_2", "*")
    object.__setattr__(invalid_pos_word, "part_of_speech_detail_3", "*")
    with pytest.raises(UserDictInputError):
        user_dict.import_dictionary(
            {"aab7dda2-0d97-43c8-8cb7-3f440dab9b4e": invalid_pos_word},
            override=True,
        )


# Windows では pytest 下での辞書の更新ができないためテストをスキップする
if sys.platform != "win32":

    def test_update_dict(tmp_path: Path) -> None:
        user_dict_path = tmp_path / "test_update_dict.json"
        user_dict = UserDictionary(user_dict_path=user_dict_path)
        user_dict.apply_jtalk_dictionary()
        test_text = "テスト用の文字列"
        success_pronunciation = "デフォルトノジショデハゼッタイニセイセイサレナイヨミ"

        # 既に辞書に登録されていないか確認する
        assert g2p(text=test_text, kana=True) != success_pronunciation

        user_dict.add_word(
            WordProperty(
                surface=[test_text],
                pronunciation=[success_pronunciation],
                accent_type=[1],
                word_type=WordTypes.PROPER_NOUN,
                priority=10,
            )
        )
        assert g2p(text=test_text, kana=True) == success_pronunciation

        # 疑似的にエンジンを再起動する
        unset_user_dict()
        user_dict.apply_jtalk_dictionary()

        assert g2p(text=test_text, kana=True) == success_pronunciation
