from aiowialon.exceptions import WialonError as WialonError
from aiowialon.types.event import AvlEvent as AvlEvent, AvlEventFilter as AvlEventFilter, AvlEventHandler as AvlEventHandler
from typing import Any, Callable, Coroutine

class Wialon:
    request_headers: dict
    def __init__(self, scheme: str = 'http', host: str = 'hst-api.wialon.com', port: int = 80, token: str = None, sid: str = None, **extra_params: Any) -> None: ...
    @property
    def sid(self) -> str: ...
    @sid.setter
    def sid(self, eid: str) -> None: ...
    @property
    def token(self) -> str: ...
    @token.setter
    def token(self, token: str) -> None: ...
    def update_extra_params(self, **params: Any) -> None: ...
    def on_session_open(self, callback: Callable[[], Coroutine] | None = None) -> Callable: ...
    def event_handler(self, filter_: AvlEventFilter = None) -> Callable: ...
    async def process_event_handlers(self, event: AvlEvent) -> None: ...
    def start_poling(self, token: str = None, timeout: [int, float] = 2) -> None: ...
    def stop_poling(self) -> None: ...
    async def poling(self, token: str = None, timeout: [float, int] = 2) -> None: ...
    async def avl_evts(self) -> Coroutine[Any, Any, None]: ...
    async def call(self, action_name: str, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def token_login(self, token: str = None, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def request(self, action_name: str, url: str, payload: Any) -> Coroutine[Any, Any, None]: ...
    def __getattr__(self, action_name: str): ...

    """
    There are enumerated methods allowed via Wialon.<method> syntax in section bellow
    """

    """
    References to core method
    https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/core/core
    """
    async def core_logout(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_get_account_data(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_check_items_billing(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_check_accessors(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_create_user(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_create_resource(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_create_unit(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_create_unit_group(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_create_retranslator(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_create_route(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_search_item(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_search_items(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_update_data_flags(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_get_hw_types(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_get_hw_cmds(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_reset_password_request(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_reset_password_perform(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_batch(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_duplicate(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_create_auth_hash(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_check_unique(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_export_file(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def core_set_session_property(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...

    """
    References to item method
    https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/item/item
    """
    async def item_update_name(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def item_delete_item(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def item_update_custom_field(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def item_update_custom_property(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def item_update_admin_field(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def item_add_log_record(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def item_list_backups(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def item_update_measure_units(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def item_update_ftp_property(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def item_update_profile_field(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def item_restore_icons(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...

    """
    References to user method
    https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/user/user
    """
    async def user_verify_auth(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def user_update_auth_params(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def user_update_item_access(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def user_get_items_access(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def user_update_hosts_mask(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def user_update_user_notification(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def user_update_password(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def user_send_sms(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def user_update_user_flags(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def user_update_locale(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def user_get_locale(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def user_get_dst_time(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...

    """
    References to resource method
    https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/resource/resource
    """
    async def resource_get_zone_data(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_update_zone(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_create_zone_by_track(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_get_zones_by_point(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_upload_zone_image(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_update_zones_group(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_get_job_data(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_update_job(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_get_notification_data(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_update_notification(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_update_driver(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_upload_driver_image(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_bind_unit_driver(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_update_driver_units(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_get_driver_bindings(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_get_unit_drivers(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_cleanup_driver_interval(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_upload_tacho_file(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_driver_operate(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_driver_status(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_update_drivers_group(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_update_trailer(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_upload_trailer_image(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_bind_unit_trailer(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_update_trailer_units(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_get_trailer_bindings(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_get_unit_trailers(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_cleanup_trailer_interval(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_update_trailers_group(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_update_tag(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_upload_tag_image(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_bind_unit_tag(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_update_tag_units(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_update_tag_message(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_get_tag_bindings(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_update_tags_group(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_update_email_template(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_get_orders_notification(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def resource_update_orders_notification(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...

    """
    References to account method
    https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/account/account
    """
    async def account_create_account(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def account_delete_account(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def account_get_account_data(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def account_enable_account(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def account_get_billing_plans(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def account_list_change_accounts(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def account_update_billing_plan(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def account_update_plan(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def account_update_sub_plans(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def account_update_dealer_rights(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def account_update_billing_service(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def account_update_flags(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def account_do_payment(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def account_update_min_days(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def account_get_account_history(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def account_update_history_period(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def account_change_account(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def account_trash(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...

    """
    References to unit method
    https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/unit/unit
    """
    async def unit_add_video_packets(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_video_status(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_command_definition(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_exec_cmd(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_get_command_definition_data(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_calc_flags(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_eh_counter(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_traffic_counter(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_mileage_counter(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_device_type(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_image(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_get_fuel_settings(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_fuel_rates_params(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_fuel_math_params(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_fuel_level_params(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]:
        # Deprecated
        ...
    async def unit_update_fuel_impulse_params(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]:
        # Deprecated
        ...
    async def unit_update_fuel_calc_types(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]:
        # Deprecated
        ...
    async def unit_get_accelerometers_calibration(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]:
        # Deprecated
        ...
    async def unit_get_report_settings(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_get_messages_filter(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_get_drive_rank_settings(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_get_trips(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_get_video_settings(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_get_vin_info(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_hw_params(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_phone(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_registry_custom_event(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_registry_fuel_filling_event(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_registry_maintenance_event(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_registry_status_event(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_phone2(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_unique_id2(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_sensor(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_calc_sensors(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_calc_last_message(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_service_interval(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_video_autopay(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_activity_settings(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_get_trip_detector(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_access_password(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_set_active(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_accelerometers_calibration(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]:
        # Deprecated
        ...
    async def unit_update_drive_rank_settings(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_report_settings(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_messages_filter(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_trip_detector(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_update_video_settings(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def unit_upload_image(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...

    """
    References to unit_group method
    https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/unit_group/unit_group
    """
    async def unit_group_update_units(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...

    """
    References to retranslator method
    https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/retranslator/retranslator
    """
    async def retranslator_update_units(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def retranslator_update_operating(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def retranslator_get_stats(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def retranslator_update_config(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...

    """
    References to route method
    https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/route/route
    """
    async def route_route_update_round(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def route_get_round_data(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def route_get_all_rounds(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def route_get_schedule_time(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def route_load_rounds(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def route_update_config(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def route_update_checkpoints(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def route_update_schedule(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def route_optimize(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...

    """
    References to messages method
    https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/messages/messages
    """
    async def messages_unload(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def messages_delete_message(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def messages_get_messages(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def messages_get_message_file(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def messages_get_packed_messages(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def messages_load_last(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def messages_load_interval(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...

    """
    References to report method
    https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/report/report
    """
    async def report_cleanup_result(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def report_exec_report(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def report_export_result(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def report_get_result_chart(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def report_render_json(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def report_hittest_chart(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def report_get_report_tables(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def report_get_result_map(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def report_get_result_subrows(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def report_get_result_photo(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def report_get_report_status(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def report_select_result_rows(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def report_get_result_rows(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def report_get_report_data(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def report_get_result_video(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def report_update_report(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...

    """
    References to exchange method
    https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/exchange/exchange
    """
    async def exchange_export_zones(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def exchange_export_messages(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def exchange_export_json(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def exchange_import_json(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def exchange_import_zones_save(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def exchange_import_messages(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def exchange_import_pois_save(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def exchange_import_zones_read(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def exchange_import_pois_read(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...

    """
    References to render method
    https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/render/render
    """
    async def render_enable_layer(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def render_create_poi_layer(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def render_create_zones_layer(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def render_create_messages_layer(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def render_get_messages(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def render_delete_message(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def render_remove_layer(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def render_remove_all_layers(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def render_set_locale(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def render_calculate_polygon(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def render_calculate_polyline(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...

    """
    References to token method
    https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/token/token
    """
    async def token_update(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def token_list(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    # async def token_login(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...  # HACK: upside

    """
    References to file method
    https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/file/file
    """
    async def file_list(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def file_get(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def file_put(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def file_rm(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def file_read(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def file_write(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def file_library(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def file_mkdir(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def file_type_library(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...

    """
    References to events method
    https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/events/events
    """
    async def events_update_units(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def events_check_updates(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def events_load(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def events_get(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def events_unload(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...

    """
    References to order method
    https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/order/order
    """
    async def order_update(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def order_attach(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def order_list_attachments(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def order_detach(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def order_get_attachment(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def order_complete_from_history(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def order_optimize(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...
    async def order_route_update(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, None]: ...

    """
    References to requests method
    https://sdk.wialon.com/wiki/en/sidebar/remoteapi/apiref/requests/requests
    """
    # TODO: