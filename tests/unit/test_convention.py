"""Tests for aiowialon.utils.convention"""

import pytest

from aiowialon.utils.convention import prepare_action_name, prepare_action_params


class TestPrepareActionName:
    def test_simple_service(self):
        assert prepare_action_name("core_search_item") == "core/search_item"

    def test_simple_service_lowercase(self):
        assert prepare_action_name("CORE_SEARCH_ITEM") == "core/search_item"

    def test_unit_group_prefix(self):
        assert prepare_action_name("unit_group_update_groups") == "unit_group/update_groups"

    def test_unit_group_search(self):
        assert prepare_action_name("unit_group_get_groups") == "unit_group/get_groups"

    def test_messages_service(self):
        assert prepare_action_name("messages_load_interval") == "messages/load_interval"

    def test_token_login(self):
        assert prepare_action_name("token_login") == "token/login"

    def test_avl_evts(self):
        assert prepare_action_name("avl_evts") == "avl/evts"

    def test_resource_service(self):
        assert prepare_action_name("resource_upload_driver_image") == "resource/upload_driver_image"

    def test_exchange_export(self):
        assert prepare_action_name("exchange_export_json") == "exchange/export_json"


class TestPrepareActionParams:
    def test_trailing_underscore_stripped(self):
        assert prepare_action_params({"from_": 1}) == {"from": 1}

    def test_leading_underscore_stripped(self):
        assert prepare_action_params({"_id": 42}) == {"id": 42}

    def test_both_underscores_stripped(self):
        assert prepare_action_params({"_type_": "x"}) == {"type": "x"}

    def test_capitalised_key_lowercased(self):
        assert prepare_action_params({"ItemId": 5}) == {"itemId": 5}

    def test_already_lowercase_unchanged(self):
        assert prepare_action_params({"flags": 0xFF}) == {"flags": 0xFF}

    def test_nested_dict_processed(self):
        result = prepare_action_params({"spec": {"from_": 0, "ItemId": 1}})
        assert result == {"spec": {"from": 0, "itemId": 1}}

    def test_list_of_dicts_processed(self):
        result = prepare_action_params({"items": [{"from_": 1}, {"from_": 2}]})
        assert result == {"items": [{"from": 1}, {"from": 2}]}

    def test_list_of_scalars_unchanged(self):
        result = prepare_action_params({"ids": [1, 2, 3]})
        assert result == {"ids": [1, 2, 3]}

    def test_non_dict_passthrough(self):
        assert prepare_action_params("string") == "string"
        assert prepare_action_params(42) == 42

    def test_empty_dict(self):
        assert prepare_action_params({}) == {}

    def test_empty_key_after_strip(self):
        result = prepare_action_params({"_": "val"})
        assert result == {"": "val"}
