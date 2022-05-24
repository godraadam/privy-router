from typing import Optional
import uuid

import requests
from app.model.daemon import PrivyDaemon
from app.model.user import PrivyUser, PrivyUserCreate
from app.service import daemon_service
from app import store, util
from app.service.docker_service import exists_privyd_container


def add_account(payload: PrivyUserCreate) -> PrivyUser:
    return add_or_create_account(payload, "remote")


def create_account(payload: PrivyUserCreate) -> PrivyUser:
    return add_or_create_account(payload, "origin")


def add_or_create_account(payload: PrivyUserCreate, type: str) -> PrivyUser:
    daemon_name = f"{payload.username}-{type}"
    
    daemon = PrivyDaemon(
        id=uuid.uuid4().hex,
        type=type,
        name=daemon_name,
        repo=uuid.uuid4().hex,
    )
    user = PrivyUser(
        username=payload.username,
        password=payload.password,
        daemons=[daemon],
        private_daemon=daemon,
    )
    daemon_service.start_daemon(daemon=daemon, user=user)
    return store.save_user(user)


def remove_account(user: PrivyUser):
    daemon_service.remove_daemons_for_user(user)
    store.remove_user(user.username)


def add_proxy_to_account(user_name: str, proxy_pubkey: str):
    user: Optional[PrivyUser] = store.get_user_by_name(username=user_name)
    if user is None:
        return
    proxy_daemon = PrivyDaemon(
        type="proxy",
        name=f"{user.username}-proxy-{proxy_pubkey[0:8]}",
        proxy_pubkey=proxy_pubkey,
        repo=uuid.uuid4().hex,
    )
    user.daemons.append(proxy_daemon)
    daemon_service.start_daemon(proxy_daemon)
    return store.save_user(user)


# {'Id': '3f48386700dba07fccf609a79502fc3215881275842433716bd77c9cc972ccc8', 'Created': '2022-05-24T10:52:01.782494064Z', 'Path': 'node', 'Args': ['dist/main.js'], 'State': {'Status': 'running', 'Running': True, 'Paused': False, 'Restarting': False, 'OOMKilled': False, 'Dead': False, 'Pid': 490643, 'ExitCode': 0, 'Error': '', 'StartedAt': '2022-05-24T10:52:04.667986443Z', 'FinishedAt': '0001-01-01T00:00:00Z'}, 'Image': 'sha256:6461bca235c12b44a368d6f8b512c705e1b485478187c416994937fa272b3d4d', 'ResolvConfPath': '/var/lib/docker/containers/3f48386700dba07fccf609a79502fc3215881275842433716bd77c9cc972ccc8/resolv.conf', 'HostnamePath': '/var/lib/docker/containers/3f48386700dba07fccf609a79502fc3215881275842433716bd77c9cc972ccc8/hostname', 'HostsPath': '/var/lib/docker/containers/3f48386700dba07fccf609a79502fc3215881275842433716bd77c9cc972ccc8/hosts', 'LogPath': '/var/lib/docker/containers/3f48386700dba07fccf609a79502fc3215881275842433716bd77c9cc972ccc8/3f48386700dba07fccf609a79502fc3215881275842433716bd77c9cc972ccc8-json.log', 'Name': '/godraadam-origin', 'RestartCount': 0, 'Driver': 'overlay2', 'Platform': 'linux', 'MountLabel': '', 'ProcessLabel': '', 'AppArmorProfile': 'docker-default', 'ExecIDs': None, 'HostConfig': {'Binds': None, 'ContainerIDFile': '', 'LogConfig': {'Type': 'json-file', 'Config': {}}, 'NetworkMode': 'default', 'PortBindings': {'6131/tcp': [{'HostIp': '', 'HostPort': '6131/tcp'}]}, 'RestartPolicy': {'Name': '', 'MaximumRetryCount': 0}, 'AutoRemove': False, 'VolumeDriver': '', 'VolumesFrom': None, 'CapAdd': None, 'CapDrop': None, 'CgroupnsMode': 'host', 'Dns': None, 'DnsOptions': None, 'DnsSearch': None, 'ExtraHosts': None, 'GroupAdd': None, 'IpcMode': 'private', 'Cgroup': '', 'Links': None, 'OomScoreAdj': 0, 'PidMode': '', 'Privileged': False, 'PublishAllPorts': False, 'ReadonlyRootfs': False, 'SecurityOpt': None, 'UTSMode': '', 'UsernsMode': '', 'ShmSize': 67108864, 'Runtime': 'runc', 'ConsoleSize': [0, 0], 'Isolation': '', 'CpuShares': 0, 'Memory': 0, 'NanoCpus': 0, 'CgroupParent': '', 'BlkioWeight': 0, 'BlkioWeightDevice': None, 'BlkioDeviceReadBps': None, 'BlkioDeviceWriteBps': None, 'BlkioDeviceReadIOps': None, 'BlkioDeviceWriteIOps': None, 'CpuPeriod': 0, 'CpuQuota': 0, 'CpuRealtimePeriod': 0, 'CpuRealtimeRuntime': 0, 'CpusetCpus': '', 'CpusetMems': '', 'Devices': None, 'DeviceCgroupRules': None, 'DeviceRequests': None, 'KernelMemory': 0, 'KernelMemoryTCP': 0, 'MemoryReservation': 0, 'MemorySwap': 0, 'MemorySwappiness': None, 'OomKillDisable': False, 'PidsLimit': None, 'Ulimits': None, 'CpuCount': 0, 'CpuPercent': 0, 'IOMaximumIOps': 0, 'IOMaximumBandwidth': 0, 'MaskedPaths': ['/proc/asound', '/proc/acpi', '/proc/kcore', '/proc/keys', '/proc/latency_stats', '/proc/timer_list', '/proc/timer_stats', '/proc/sched_debug', '/proc/scsi', '/sys/firmware'], 'ReadonlyPaths': ['/proc/bus', '/proc/fs', '/proc/irq', '/proc/sys', '/proc/sysrq-trigger']}, 'GraphDriver': {'Data': {'LowerDir': '/var/lib/docker/overlay2/4952e74cdac175c35ad2ab33a9aad4a2da1e6dbaaf81ba315ba1167884c07673-init/diff:/var/lib/docker/overlay2/f863315689e516c6c16b91f3e436d91c121295515a799519f29a81fdb3f3340b/diff:/var/lib/docker/overlay2/2e9db06caf6599d67e703e00704d04b8c47b7a03ee5db9fb7afef8322c931d5f/diff:/var/lib/docker/overlay2/2123dc89086fa7dad2bea8775d8c26853b07826feaebd34eee586bc04cad7e6d/diff:/var/lib/docker/overlay2/2764c56c1b3269fe5274d079b401f221de94c5954fbe4c096e3793d79a52e3a4/diff:/var/lib/docker/overlay2/b070038c98db02126576d88d60e9e994281190cda062edf6f4d81647ada54760/diff:/var/lib/docker/overlay2/07903ceaef3f6053321c66a56eee1d2aa84f1f5018db389e056cb2c84f14f8ab/diff:/var/lib/docker/overlay2/f1f3ef46a2fe372550bbdbbf0b7c892a2ce6e6b74254ba90ac04abc31153e6cd/diff:/var/lib/docker/overlay2/af3c641f7d7991e51390043a920a9492215cf984aa960332b0cedb85a7a0d4c6/diff:/var/lib/docker/overlay2/71f3ca8d6c15b95141834d15e48b0eb6af21eb397915ffacf5fdda9f4957c540/diff:/var/lib/docker/overlay2/d4a70844f027c435fdfdd9d9958ee30dfca55c0a2398e4a3efe32ee33117e309/diff:/var/lib/docker/overlay2/cf3e3e21654677855b34b666fd7f784861b6c990346e916a823af090e3d0fb7a/diff:/var/lib/docker/overlay2/2803f763441b4fe260643317d286159a83cda159de8ea429d66eed97f9cc8901/diff:/var/lib/docker/overlay2/f22fcf590b4d853a842325d899db3ab3d8f875199c0678230ebbab52a88d3c48/diff:/var/lib/docker/overlay2/63391aada42b3988632c872688e3a1c14d9c359c59a853001b0dd40881529431/diff:/var/lib/docker/overlay2/78a9f79ab341c8cb60aa42fb2e9e26860a08dbafd985c9d5696d059610a30722/diff', 'MergedDir': '/var/lib/docker/overlay2/4952e74cdac175c35ad2ab33a9aad4a2da1e6dbaaf81ba315ba1167884c07673/merged', 'UpperDir': '/var/lib/docker/overlay2/4952e74cdac175c35ad2ab33a9aad4a2da1e6dbaaf81ba315ba1167884c07673/diff', 'WorkDir': '/var/lib/docker/overlay2/4952e74cdac175c35ad2ab33a9aad4a2da1e6dbaaf81ba315ba1167884c07673/work'}, 'Name': 'overlay2'}, 'Mounts': [], 'Config': {'Hostname': '3f48386700db', 'Domainname': '', 'User': '', 'AttachStdin': False, 'AttachStdout': True, 'AttachStderr': True, 'ExposedPorts': {'6131/tcp': {}}, 'Tty': False, 'OpenStdin': False, 'StdinOnce': False, 'Env': ['SEED=y8sBrc/SD2EqqU4/Pw79/9Vw4MOEUeneUgOuks/JhPuEyRwjIC9UW7zR2WHhKn4LFGZTgOOW7sAZWP43qB6Xvg==', 'NODE_TYPE=origin', 'REPO=8b7c125ea28c4d4f8e414c25178ddb3d', 'PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'NODE_VERSION=16.13.2', 'YARN_VERSION=1.22.15'], 'Cmd': None, 'Image': 'godraadam/privyd:alpha', 'Volumes': None, 'WorkingDir': '/privy-daemon', 'Entrypoint': ['node', 'dist/main.js'], 'OnBuild': None, 'Labels': {}}, 'NetworkSettings': {'Bridge': '', 'SandboxID': 'd56d0f7a1f790b6005ad8d72d04dd6f7ae1ff603b8ca2f90af303c66b8c680a2', 'HairpinMode': False, 'LinkLocalIPv6Address': '', 'LinkLocalIPv6PrefixLen': 0, 'Ports': {'6131/tcp': [{'HostIp': '0.0.0.0', 'HostPort': '6131'}, {'HostIp': '::', 'HostPort': '6131'}]}, 'SandboxKey': '/var/run/docker/netns/d56d0f7a1f79', 'SecondaryIPAddresses': None, 'SecondaryIPv6Addresses': None, 'EndpointID': '2b2a996cc861f2275e56a4b074b67ace63f193ee136847e3fdcc2ac1746f45f7', 'Gateway': '172.17.0.1', 'GlobalIPv6Address': '', 'GlobalIPv6PrefixLen': 0, 'IPAddress': '172.17.0.2', 'IPPrefixLen': 16, 'IPv6Gateway': '', 'MacAddress': '02:42:ac:11:00:02', 'Networks': {'bridge': {'IPAMConfig': None, 'Links': None, 'Aliases': None, 'NetworkID': '8507a391c1d0f6bf37cd90696e6d26d51f349d8e803c258471929d12718a4564', 'EndpointID': '2b2a996cc861f2275e56a4b074b67ace63f193ee136847e3fdcc2ac1746f45f7', 'Gateway': '172.17.0.1', 'IPAddress': '172.17.0.2', 'IPPrefixLen': 16, 'IPv6Gateway': '', 'GlobalIPv6Address': '', 'GlobalIPv6PrefixLen': 0, 'MacAddress': '02:42:ac:11:00:02', 'DriverOpts': None}}}}