class WhitelistedIpAddresses:
    def __init__(self, whitelisted_ip_addresses: tuple[str]):
        self.__whitelisted_ip_addresses = whitelisted_ip_addresses

    def __contains__(self, item):
        return item in self.__whitelisted_ip_addresses
