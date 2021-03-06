import os

from ryu.services.protocols.bgp.bgpspeaker import RF_VPN_V4
from ryu.services.protocols.bgp.bgpspeaker import RF_L2_EVPN
from ryu.services.protocols.bgp.bgpspeaker import EVPN_MAC_IP_ADV_ROUTE
from ryu.services.protocols.bgp.bgpspeaker import TUNNEL_TYPE_VXLAN


# =============================================================================
# BGP configuration.
# =============================================================================
BGP = {

    # AS number for this BGP instance.
    'local_as': 65001,

    # BGP Router ID.
    'router_id': '172.17.0.1',

    # List of BGP neighbors.
    # The parameters for each neighbor are the same as the arguments of
    # BGPSpeaker.neighbor_add() method.
    'neighbors': [
        {
            'address': '172.17.0.2',
            'remote_as': 65002,
            'enable_ipv4': True,
            'enable_vpnv4': True,
        },
        {
            'address': '172.17.0.3',
            'remote_as': 65000,
            'enable_evpn': True,
        },
    ],

    # List of BGP VRF tables.
    # The parameters for each VRF table are the same as the arguments of
    # BGPSpeaker.vrf_add() method.
    'vrfs': [
        {
            'route_dist': '65001:100',
            'import_rts': ['65001:100'],
            'export_rts': ['65001:100'],
            'route_family': RF_VPN_V4,
        },
        {
            'route_dist': '65000:200',
            'import_rts': ['65000:200'],
            'export_rts': ['65000:200'],
            'route_family': RF_L2_EVPN,
        },
    ],

    # List of BGP routes.
    # The parameters for each route are the same as the arguments of
    # BGPSpeaker.prefix_add() or BGPSpeaker.evpn_prefix_add() method.
    'routes': [
        # Example of IPv4 prefix
        {
            'prefix': '10.10.1.0/24',
        },
        # Example of VPNv4 prefix
        {
            'prefix': '10.20.1.0/24',
            'next_hop': '172.17.0.1',
            'route_dist': '65001:100',
        },
        # Example of EVPN prefix
        {
            'route_type': EVPN_MAC_IP_ADV_ROUTE,
            'route_dist': '65000:200',
            'esi': 0,
            'ethernet_tag_id': 0,
            'tunnel_type': TUNNEL_TYPE_VXLAN,
            'vni': 200,
            'mac_addr': 'aa:bb:cc:dd:ee:ff',
            'ip_addr': '10.30.1.1',
            'next_hop': '172.17.0.1',
        },
    ],
}


# =============================================================================
# SSH server configuration.
# =============================================================================
SSH = {
    'ssh_port': 4990,
    'ssh_host': 'localhost',
    # 'ssh_host_key': '/etc/ssh_host_rsa_key',
    # 'ssh_username': 'ryu',
    # 'ssh_password': 'ryu',
}


# =============================================================================
# Logging configuration.
# =============================================================================
LOGGING = {

    # We use python logging package for logging.
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s ' +
                      '[%(process)d %(thread)d] %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)s ' +
                      '%(message)s'
        },
        'stats': {
            'format': '%(message)s'
        },
    },

    'handlers': {
        # Outputs log to console.
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'console_stats': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'stats'
        },
        # Rotates log file when its size reaches 10MB.
        'log_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('.', 'bgpspeaker.log'),
            'maxBytes': '10000000',
            'formatter': 'verbose'
        },
        'stats_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join('.', 'statistics_bgps.log'),
            'maxBytes': '10000000',
            'formatter': 'stats'
        },
    },

    # Fine-grained control of logging per instance.
    'loggers': {
        'bgpspeaker': {
            'handlers': ['console', 'log_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'stats': {
            'handlers': ['stats_file', 'console_stats'],
            'level': 'INFO',
            'propagate': False,
            'formatter': 'stats',
        },
    },

    # Root loggers.
    'root': {
        'handlers': ['console', 'log_file'],
        'level': 'DEBUG',
        'propagate': True,
    },
}
