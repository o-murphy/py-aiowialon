"""Shortcuts to export/import AVL Items to/from .wlp format"""
from enum import IntEnum
from typing import Any, Dict

from aiowialon.api import Wialon
from aiowialon.exceptions import WialonInvalidInput
from aiowialon.types import flags, MultipartField


class WLP:
    """Shortcuts to export/import AVL Items to/from .wlp format"""

    class _ItemTypeId(IntEnum):
        """Available AVL item type ids for export/import"""

        AVL_USER = 1
        AVL_UNIT = 2
        AVL_RESOURCE = 3

    @staticmethod
    async def export_item(client: Wialon, item_id: int) -> bytes:
        """
        Creates a batch of requests for export AVL item to .wlp by item_id
        :param client: Wialon client instance
        :param item_id: AVL item id to export
        :return: bytes representation of .wlp format
        """

        response = await client.core_search_item(id=item_id, flags=flags.UnitsDataFlag.ALL)
        item = response['item']
        item_type = item['cls']
        if item_type == WLP._ItemTypeId.AVL_USER:
            wlp_data = await WLP._fetch_user_wlp(client, item)
        elif item_type == WLP._ItemTypeId.AVL_RESOURCE:
            wlp_data = await WLP._fetch_resource_wlp(client, item)
        elif item_type == WLP._ItemTypeId.AVL_UNIT:
            wlp_data = await WLP._fetch_unit_wlp(client, item)
        else:
            raise WialonInvalidInput(f"Invalid item type: {item_type}")

        return await client.exchange_export_json(fileName=f"{item['id']}", json=wlp_data)

    @staticmethod
    async def import_item(client: Wialon, wlp: bytes) -> Any:
        """
        Creates a batch of requests for import AVL item data from .wlp to the server
        :param client: Wialon client instance
        :param wlp: content of .wlp in bytes representation
        """
        event_hash = "ImportAvlItem"
        file_name = "import.wlp"
        return await client.multipart(
            client.exchange_import_json(eventHash=event_hash),
            MultipartField(name='eventHash', value=event_hash),
            MultipartField(name='import_file',
                           value=wlp,
                           filename=file_name,
                           content_type='application/zip')
        )

    @staticmethod
    async def _fetch_user_wlp(client: Wialon, item: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a batch of requests to get AVL user data and collects it to .wlp dict"""
        user_id = item['id']

        locale = await client.user_get_locale(userId=user_id)
        prp = item.get('prp', {})

        wlp_data = {
            'type': 'avl_unit',
            'version': 'b4',
            'mu': item['mu'],
            'locale': locale
        }

        # pylint: disable=line-too-long
        keys_list = [
            "addr_provider,webg_c,webg_c_id,city,umsp",
            "agrsn,znsn,znsrv,zlg,rtssn",
            "tz,dst",
            "geodata_source",
            "selected_settings",
            "cfmt",
            "complete_copy",
            "user_unit_cmds",
            "us_addr_fmt",
            "ursstp,usuei,usdrva",
            "show_log,user_settings_hotkeys,msc,pnfs,evt_flags,hbacit,hpnl,inf_map,uschs",
            "mfrl,muf,last_tail_points,last_tail_color,last_tail_width,mf_use_sensors,sens_color_tooltip",
            "mu_cmd_btn,mu_gprs,mu_watch,mu_fast_track_ival,mu_photo,mu_video,mu_tracks,mu_sens,mu_gps,mu_move,mu_msgs,mu_messages_filter_ival,mu_reps,mu_route,mu_events,mu_dev_cfg,mont,mu_sms,mu_gps_mode,mu_gps_time,mu_location,mu_loc_mode,mu_fast_report,mu_fast_report_ival,mu_fast_report_tmpl,mu_tag,mu_delete_from_list,wdcheck,mu_driver,mu_drv_mode,mu_trailer,mu_tr_mode,mu_move_durr,mu_gprs_durr,mu_sl_type,mu_sl_gf_filter,mu_loc_gf_filter",
            "umap,mtg,mtmyin2,mtve,wg3,mtyh,mtyahin,mtya,mtks,mtlux,mtnavm,mtgis2,mtgt,mtwikim,mtgom,mthere,mtosm,mtmapbox,mtagis,mtvisicom,mtowm,mtaeris",
            "__sensolator_resource_id,access_templates,apst,autocomplete,drvsvlist,fpnl,language,lastmsgl,m_ge,m_gu,m_ml,m_mm,m_monu,m_mt,m_ui,m_un,minimap_zoom_level,mongr,monu,monuei,monuexpg,monugr,monugv,monuv,msg_aw,mtla10,mtla11,mtla5,mtla6,mtla9,mtlb,mtlg,mu_tbl_cols_sizes,mu_tbl_sort,mugow,muow,pbsd,radd,route_provider,tracks_player_show_params,tracks_player_show_sensors,trlsvlist,us_addr_ordr,used_hw,vsplit,znsvlist"
        ]

        for keys in keys_list:
            sub_keys = keys.split(',')
            sub_data = []
            for key in sub_keys:
                sub_data.append(prp.get(key, ''))
            wlp_data[keys] = sub_data

        wlp_data['acs_tmpl'] = prp.get('access_templates', '')
        wlp_data['usr_ugef,usr_uhom'] = prp.get('usr_ugef,usr_uhom', '')

        return wlp_data

    @staticmethod
    async def _fetch_unit_wlp(client: Wialon, item: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a batch of requests to get AVL unit data and collects it to .wlp dict"""
        unit_id = item['id']
        hw_types = await client.core_get_hw_types(
            filterType='id',
            filterValue=[item.get('hw', None)],
            includeType="1",
            ignoreRename="1"
        )
        if len(hw_types) <= 0:
            raise WialonInvalidInput("Hardware type not found",
                                     "wlp.export_unit", "")
        hw_type = hw_types[0]
        commands_ids = [str(i) for i in range(1, 15)]

        response = await client.batch(
            client.unit_update_hw_params(
                itemId=unit_id,
                hwId=hw_type['id'],
                fullData=1, action='get'
            ),
            client.unit_get_report_settings(itemId=unit_id),
            client.unit_get_activity_settings(itemId=unit_id),
            client.unit_get_messages_filter(itemId=unit_id),
            client.unit_get_command_definition_data(itemId=unit_id, col=commands_ids),
            client.unit_get_drive_rank_settings(itemId=unit_id),
            flags_=flags.BatchFlag.STOP_ON_ERROR
        )
        result = dict(zip((
            "hwParams",
            "reportProps",
            'driver_activity',
            'msgFilter',
            'aliases',
            'driving',
        ), response))

        wlp_data = {
            'type': 'avl_unit',
            'version': 'b4',
            'mu': item['mu'],
            'imgRot': item['prp'].get('img_rot', ''),

            'general': {
                'n': item['nm'],
                'uid': item['uid'],
                'uid2': item['uid2'],
                'ph': item['ph'],
                'ph2': item['ph2'],
                'psw': item['psw'],
                'hw': hw_type['name']
            },
            'hwConfig': {
                'hw': hw_type['name'],
                'fullData': 1,
                'params': result['hwParams']
            },
            'counters': {
                'cfl': item['cfl'],
                'cnm': item['cnm'],
                'cneh': item['cneh'],
                'cnkb': item['cnkb'],
            },
            'advProps': item['prp'],
            'reportProps': result['reportProps'],
            'aliases': result['aliases'],
            'driving': result['driving'],
            'trip': item['rtd'],
            'sensors': tuple(item['sens'].values()),

            # is bellow required
            'fields': list(item['flds'].values()),
            'afields': list(item['aflds'].values()),
            'intervals': list(item['si'].values()),
            'fuel': item['rfc'],
            'profile': list(item['pflds'].values()),
        }

        wlp_data['reportProps']['driver_activity'] = result['driver_activity']
        wlp_data['reportProps']['fuelConsRates'] = item['rfc']['fuelConsRates']  # ? changed

        if wlp_data['advProps'].get('img_rot', False):
            wlp_data['advProps'].pop('img_rot')
            wlp_data['advProps'].pop('idrive')

        wlp_data['advProps']['msgFilter'] = result['msgFilter']
        return wlp_data

    @staticmethod
    async def _fetch_resource_wlp(client: Wialon, item: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a batch of requests to get AVL resource data and collects it to .wlp dict"""

        resource_id = item['id']

        zones_ids = [i['id'] for i in item['zl'].values()]
        jobs_ids = [i['id'] for i in item['ujb'].values()]
        notifs_ids = [i['id'] for i in item['unf'].values()]
        reports_ids = [i['id'] for i in item['rep'].values()]

        response = await client.batch(
            client.resource_get_zone_data(itemId=resource_id, col=zones_ids, flags=0x1C),
            client.resource_get_job_data(itemId=resource_id, col=jobs_ids),
            client.resource_get_notification_data(itemId=resource_id, col=notifs_ids),
            client.report_get_report_data(itemId=resource_id, col=reports_ids),
            flags_=flags.BatchFlag.STOP_ON_ERROR
        )

        result = dict(zip((
            'zones',
            'jobs',
            'notifications',
            'reports',
        ), response))

        wlp_data = {
            'type': 'avl_resource',
            'version': 'b4',
            'mu': item['mu'],
            'drivers': list(item['drvrs'].values()),
            'trailers': list(item['trlrs'].values()),
            'tags': list(item['tags'].values()),
            **result,
        }

        return wlp_data


__all__ = ['WLP']
