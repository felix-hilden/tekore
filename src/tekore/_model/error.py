from enum import Enum


class PlayerErrorReason(Enum):
    """Reasons for errors in player actions."""

    NO_PREV_TRACK = (
        "The command requires a previous track, but there is none in the context."
    )
    NO_NEXT_TRACK = (
        "The command requires a next track, but there is none in the context."
    )
    NO_SPECIFIC_TRACK = "The requested track does not exist."
    ALREADY_PAUSED = "The command requires playback to not be paused."
    NOT_PAUSED = "The command requires playback to be paused."
    NOT_PLAYING_LOCALLY = "The command requires playback on the local device."
    NOT_PLAYING_TRACK = "The command requires that a track is currently playing."
    NOT_PLAYING_CONTEXT = "The command requires that a context is currently playing."
    ENDLESS_CONTEXT = "The shuffle command cannot be applied on an endless context."
    CONTEXT_DISALLOW = "The command could not be performed on the context."
    ALREADY_PLAYING = (
        "The track should not be restarted if the same track "
        "and context is already playing, and there is a resume point."
    )
    RATE_LIMITED = (
        "The user is rate limited due to too frequent track play,"
        "also known as cat-on-the-keyboard spamming."
    )
    REMOTE_CONTROL_DISALLOW = "The context cannot be remote-controlled."
    DEVICE_NOT_CONTROLLABLE = "Not possible to remote control the device."
    VOLUME_CONTROL_DISALLOW = "Not possible to remote control the device's volume."
    NO_ACTIVE_DEVICE = "Requires an active device and the user has none."
    PREMIUM_REQUIRED = "The request is prohibited for non-premium users."
    UNKNOWN = "Certain actions are restricted because of unknown reasons."
