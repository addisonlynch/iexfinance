import os


def using_cloud():
    """
    Used to run v1 tests only. Returns true if using IEX cloud
    """
    return os.getenv("IEX_API_VERSION") in ("iexcloud-beta", "iexcloud-v1")
