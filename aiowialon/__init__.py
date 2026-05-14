#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Async Wialon Remote API wrapper for Python 3
"""

__author__ = "o-murphy"
__copyright__ = ("Copyright 2013-2016, Gurtam; ", "Copyright 2022 Dmytro Yaroshenko; ")

__credits__ = [
    "Alex Chernetsky",
    "Aleksey Shmigelski",
    "Mike Turchunovich",
    "Dmytro Yaroshenko",
]

from aiowialon.api import Wialon
from aiowialon.exceptions import (
    WialonError,
    WialonWarning,
    WialonInvalidSession,
    WialonInvalidService,
    WialonInvalidResult,
    WialonInvalidInput,
    WialonErrorPerformingRequest,
    WialonUnknownError,
    WialonAccessDenied,
    WialonInvalidCredentials,
    WialonAuthServerUnavailableError,
    WialonReachedConcurrentRequestLimit,
    WialonPasswordResetError,
    WialonBillingError,
    WialonMessageNotFoundError,
    WialonDuplicateItemError,
    WialonRequestLimitExceededError,
    WialonMessageLimitExceededError,
    WialonExecutionTimeExceededError,
    WialonTwoFactorAuthAttemptsExceededError,
    WialonSessionExpiredOrIPChangedError,
    WialonTransferUnitError,
    WialonAccessDeniedDueToTransferError,
    WialonUserCreationError,
    WialonSensorDeleteForbiddenError,
)
from aiowialon.types import (
    AvlEvent,
    AvlEventData,
    AvlEventCallback,
    AvlEventFilter,
    AvlEventHandler,
    ClientLoginParams,
    ClientLoginCallback,
    ClientLogoutCallback,
    MultipartField,
    flags,
    api_types,
)
from aiowialon.logger import logger
from aiowialon.validators import WialonCallRespValidator
from aiowialon.shortcuts import WLP

__all__ = (
    # client
    "Wialon",
    # base exceptions
    "WialonError",
    "WialonWarning",
    # specific exceptions
    "WialonInvalidSession",
    "WialonInvalidService",
    "WialonInvalidResult",
    "WialonInvalidInput",
    "WialonErrorPerformingRequest",
    "WialonUnknownError",
    "WialonAccessDenied",
    "WialonInvalidCredentials",
    "WialonAuthServerUnavailableError",
    "WialonReachedConcurrentRequestLimit",
    "WialonPasswordResetError",
    "WialonBillingError",
    "WialonMessageNotFoundError",
    "WialonDuplicateItemError",
    "WialonRequestLimitExceededError",
    "WialonMessageLimitExceededError",
    "WialonExecutionTimeExceededError",
    "WialonTwoFactorAuthAttemptsExceededError",
    "WialonSessionExpiredOrIPChangedError",
    "WialonTransferUnitError",
    "WialonAccessDeniedDueToTransferError",
    "WialonUserCreationError",
    "WialonSensorDeleteForbiddenError",
    # event types
    "AvlEvent",
    "AvlEventData",
    "AvlEventCallback",
    "AvlEventFilter",
    "AvlEventHandler",
    # login / session callbacks
    "ClientLoginParams",
    "ClientLoginCallback",
    "ClientLogoutCallback",
    # multipart
    "MultipartField",
    # submodules
    "flags",
    "api_types",
    # logger (for user-side logging config)
    "logger",
    # validator (for custom validation)
    "WialonCallRespValidator",
    # shortcuts
    "WLP",
)
