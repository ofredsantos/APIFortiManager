# 5. Connector Management

## 5.1. JSON API Connector

### 5.1.1. How to create a new JSON API Connector?

It’s a two steps process:

```
```
# 1. Create the JSON API connector without tags
```

```
# 2. Create the tags

#### 5.1.1.1. Create the JSON API connector without tags

```
REQUEST

{
 "id": 3,
 "method": "add",
 "params": [
 {
 "data": {
 "name": "json_api_connector_001",
 "status": "enable"
 },
 "url": "/pm/config/adom/adom_70_001/obj/user/json"
 }
 ],
 "session": "{{session}}"
}

RESPONSE

{
 "id": 3,
 "result": [
 {
 "data": {
 "name": "json_api_connector_001"
 },
 "status": {
 "code": 0,
 "message": "OK"
 },
 "url": "/pm/config/adom/adom_70_001/obj/user/json"
 }
 ]
}
```

#### 5.1.1.2. Create the tags

Adding tags is very straightforward.

It is just about adding new entries in table `user adgrp` with a name matching the following format:

js_<json_api_connector_name>_<tag_name>

For instance, considering the above created JSON API connector `json_api_connector_001` (i.e., `json_api_connector_name`), if you want to add `tag_001` (i.e., `tag_name`), then the name of the `user adgrp` entry will be:

js_json_api_connector_001_tag_001

```
REQUEST

{
 "id": 3,
 "method": "add",
 "params": [
 {
 "data": [
 {
 "name": "js_json_api_connector_001_tag_001",
 "connector-source": "FMG JSON",
 "server-name": "FortiManager"
 },
 {
 "name": "js_json_api_connector_001_tag_002",
 "connector-source": "FMG JSON",
 "server-name": "FortiManager"
 },
 {
 "name": "js_json_api_connector_001_tag_003",
 "connector-source": "FMG JSON",
 "server-name": "FortiManager"
 }
 ],
 "url": "/pm/config/adom/adom_70_001/obj/user/adgrp"
 }
 ],
 "session": "{{session}}"
}
```

> **Note:**

*   You have to use specific a value for `server-name``; it has to be `FortiManager`.

*   However, you can use any string value for `connector-source` but better to keep the one used by FortiManager GUI which is `FMG JSON`.

```
RESPONSE

{
 "id": 3,
 "result": [
 {
 "status": {
 "code": 0,
 "message": "OK"
 },
 "url": "/pm/config/adom/adom_70_001/obj/user/adgrp"
 }
 ]
}
```

#### 5.1.1.3. Create both using a single API request

If you like multiplexing API calls:

```
REQUEST

{
 "id": 1,
 "method": "add",
 "params": [
 {
 "data": {
 "name": "json_api_connector_001",
 "status": "enable"
 },
 "url": "/pm/config/adom/adom_70_001/obj/user/json"
 },
 {
 "url": "/pm/config/adom/adom_70_001/obj/user/adgrp",
 "data": [
 {
 "name": "js_json_api_connector_001_tag_001",
 "server-name": "FortiManager",
 "connector-source": "FMG JSON"
 },
 {
 "name": "js_json_api_connector_001_tag_002",
 "server-name": "FortiManager",
 "connector-source": "FMG JSON"
 },
 {
 "name": "js_json_api_connector_001_tag_003",
 "server-name": "FortiManager",
 "connector-source": "FMG JSON"
 }
 ]
 }
 ],
 "session": "{{session}}"
}
```

> **Note:**

*   You have to use specific a value for `server-name`; it has to be `FortiManager`.

*   However, you can use any string value for `connector-source` but better to keep the one used by FortiManager GUI which is 
```
FMG
JSON
```
.

```
RESPONSE

{
 "id": 1,
 "result": [
 {
 "data": {
 "name": "json_api_connector_001"
 },
 "status": {
 "code": 0,
 "message": "OK"
 },
 "url": "/pm/config/adom/adom_70_001/obj/user/json"
 },
 {
 "status": {
 "code": 0,
 "message": "OK"
 },
 "url": "/pm/config/adom/adom_70_001/obj/user/adgrp"
 }
 ]
}
```

### 5.1.2. How to delete a JSON API Connector?

To delete JSON API Connector `json_api_connector_001` from ADOM `dc_amer`:

```
REQUEST

{
 "id": 1,
 "method": "delete",
 "params": [
 {
 "url": "/pm/config/adom/dc_amer/obj/user/json/json_api_connector_001"
 }
 ],
 "session": "{{session}}"
}

RESPONSE

{
 "id": 1,
 "result": [
 {
 "status": {
 "code": 0,
 "message": "OK"
 },
 "url": "/pm/config/adom/dc_amer/obj/user/json/json_api_connector_001"
 }
 ]
}
```

### 5.1.3. Managing JSON API Connector tags?

#### 5.1.3.1. Add IP addresses to a single tag

This request adds IPv4 addresses `10.1.0.{1,2,3}` and IPv6 addresses `2001:DB8::{1,2,3}` to the `tag_001` tag which has been declared within the `json_api_connector_001` JSON API Connector:

```
REQUEST

{
 "id": 3,
 "method": "exec",
 "params": [
 {
 "data": {
 "command": "add",
 "group": "tag_001",
 "ip-addr": [
 "10.1.0.1",
 "10.1.0.2",
 "10.1.0.3",
 "10.2.0.1",
 "2001:DB8::1",
 "2001:DB8::2",
 "2001:DB8::3"
 ],
 "path": "{{adom}}/json_api_connector_001"
 },
 "url": "/connector/user/manage"
 }
 ]
}

RESPONSE

{
 "result": [
 {
 "status": {
 "code": 0,
 "message": "OK"
 },
 "url": "/connector/user/manage"
 }
 ],
 "id": 3
}
```

#### 5.1.3.2. Add IP addresses to multiple tags

Caught in #1027981 (FMG 7.4.4/7.6.0).

The following example shows how to add IP address to the `tag_001`, `tag_002` and `tag_002` tags for the `json_api_connector_001` JSON API Connector in the `demo` ADOM:

```
REQUEST

{
 "id": 3,
 "method": "exec",
 "params": [
 {
 "data": [
 {
 "command": "add",
 "group": "tag_001",
 "ip-addr": [
 "10.1.0.1",
 "10.1.0.2",
 "10.1.0.3"
 ],
 "path": "demo/json_api_connector_001"
 },
 {
 "command": "add",
 "group": "tag_002",
 "ip-addr": [
 "10.2.0.1",
 "10.2.0.2",
 "10.2.0.3",
 "10.2.0.4",
 "10.2.0.5",
 "10.2.0.6"
 ],
 "path": "demo/json_api_connector_001"
 },
 {
 "command": "add",
 "group": "tag_003",
 "ip-addr": [
 "10.3.0.1",
 "10.3.0.2",
 "10.3.0.3",
 "10.3.0.4",
 "10.3.0.5",
 "10.3.0.6"
 ],
 "path": "demo/json_api_connector_001"
 }
 ],
 "url": "/connector/user/manage"
 }
 ],
 "session": "{{session}}"
}

RESPONSE

{
 "id": 3,
 "result": [
 {
 "status": {
 "code": 0,
 "message": "OK"
 },
 "url": "/connector/user/manage"
 }
 ]
}
```

#### 5.1.3.3. Get IP addresses

This request retrieves IP addresses corresponding to the `tag_001` tag which has been declared within the `json_api_connector_001` JSON API Connector:

```
REQUEST

{
 "method": "exec",
 "params": [
 {
 "data": {
 "adom": "{{adom}}",
 "connector": "json_api_connector_001",
 "server_type": "json",
 "type": "connector",
 "group":"tag_001"
 },
 "url": "/connector/get/user"
 }
 ]
}

RESPONSE

{
 "result": [
 {
 "data": [
 {
 "grpname": "js_json_api_connector_001_tag_001",
 "ip_addr": "10.1.0.1",
 "ip_addr6": "::-::",
 "name": "",
 "state": 1
 },
 {
 "grpname": "js_json_api_connector_001_tag_001",
 "ip_addr": "10.1.0.2",
 "ip_addr6": "::-::",
 "name": "",
 "state": 1
 },
 {
 "grpname": "js_json_api_connector_001_tag_001",
 "ip_addr": "10.1.0.3",
 "ip_addr6": "::-::",
 "name": "",
 "state": 1
 },
 {
 "grpname": "js_json_api_connector_001_tag_001",
 "ip_addr6": "2001:db8::1-2001:db8::1",
 "name": "",
 "state": 1
 },
 {
 "grpname": "js_json_api_connector_001_tag_001",
 "ip_addr6": "2001:db8::2-2001:db8::2",
 "name": "",
 "state": 1
 },
 {
 "grpname": "js_json_api_connector_001_tag_001",
 "ip_addr6": "2001:db8::3-2001:db8::3",
 "name": "",
 "state": 1
 }
 ],
 "status": {
 "code": 0,
 "message": "OK"
 },
 "url": "/connector/get/user"
 }
 ]
}
```

#### 5.1.3.4. Delete IP addresses

To delete `10.1.0.1`, `10.1.0.3` and `10.1.0.5` IP addresses from tag `tag_001` declared within the `json_api_connector_001` JSON API Connector:

```
REQUEST

{
 "id": 3,
 "method": "exec",
 "params": [
 {
 "data": {
 "command": "delete",
 "group": "tag_001",
 "ip-addr": [
 "10.1.0.1",
 "10.1.0.3",
 "10.1.0.5"
 ],
 "path": "{{adom}}/json_api_connector_001"
 },
 "url": "/connector/user/manage"
 }
 ],
 "session": "{{session}"
}

RESPONSE

{
 "id": 3,
 "result": [
 {
 "status": {
 "code": 0,
 "message": "OK"
 },
 "url": "/connector/user/manage"
 }
 ]
}
```

## 5.2. ClearPass

### 5.2.1. TODO: How to simulate

diagnose system print connector DEMO clearpass cp-10.210.34.247
2020-04-20 17:57:30 Request:
2020-04-20 17:57:30 { "client": "-newcli:24885", "id": 2, "method": "exec", "params": [{ "data": { "adom": "DEMO", "connector": "cp-10.210.34.247", "server_type": "clearpass"}, "target start": 1, "url": "debug"}], "root": "connector"}
2020-04-20 17:57:30 __get_user_list : no user info obtained from server cp-10.210.34.247
2020-04-20 17:57:30 __get_cuser_list : no user info obtained from server cp-10.210.34.247
2020-04-20 17:57:30 __get_adgrp_list : no adgrp info obtained from server cp-10.210.34.247
2020-04-20 17:57:30 Response:
2020-04-20 17:57:30 { "id": 2, "result": [{ "status": { "code": 0, "message": "OK"}, "url": "debug"}]}2020-04-20 17:57:30

### 5.2.2. How to get a defined ClearPass connector?

```
REQUEST

{
 "id": 1,
 "method": "get",
 "params": [
 {
 "object template": 0,
 "option": ["get used", "get flags", "get devobj mapping", "get meta", "loadsub", "extra info"],
 "url": "/pm/config/adom/ClearPass/obj/user/clearpass/cp-001"
 }
 ],
 "session": 41581
}
```

### 5.2.3. How to get users?

This request is retrieving the user which are considered as authenticated at the ClearPass level.

```
REQUEST

{
 "id": 1,
 "method": "exec",
 "params": [
 {
 "data": {
 "adom": "ClearPass",
 "connector": "cp-001",
 "domid": "user-v-tree",
 "if_all_user": 0,
 "server_type": "clearpass",
 "type": "clearpass"
 },
 "url": "/connector/get/user"
 }
 ],
 "session": 35742
}

RESPONSE

{
 "id": 1,
 "result": [
 {
 "data": [
 {
 "grpname": "cp_cp-001_Support",
 "ip_addr": "10.210.34.185",
 "name": "user1",
 "state": 1
 },
 {
 "grpname": "cp_cp-001_Marketing",
 "ip_addr": "10.210.34.186",
 "name": "user2",
 "state": 1
 },
 {
 "grpname": "cp_cp-001_Sales",
 "ip_addr": "10.210.34.187",
 "name": "user3",
 "state": 1
 }
 ],
 "status": {
 "code": 0,
 "message": "OK"
 },
 "url": "/connector/get/user"
 }
 ]
}
```

### 5.2.4. H ow to get address groups?

```
REQUEST

{
 "id": 1,
 "method": "exec",
 "params": [
 {
 "data": {
 "adom": "ClearPass",
 "connector": "cp-001",
 "server_type":
 "clearpass"
 },
 "url": "/connector/get/adgrp"
 }
 ],
 "session": 35742
}
```

### 5.2.5. Update connector (ie. retrieve logged in users)

```
REQUEST

{
 "id": 1,
 "method": "exec",
 "params": [
 {
 "data": {
 "adom": "ClearPass",
 "connector": "cp-001",
 "server_type": "clearpass",
 "service_type": 0
 },
 "url": "/connector/update"
 }
 ],
 "session": 35742
}
```

Response is having a `taskid`

### 5.2.6. How to simulate a user login via FMG JSON API?

The end result will be that FMG will see an authenticated clearpass user, and will send it to the managed devices.

```
REQUEST

{
 "id": 1,
 "method": "exec",
 "params": [
 {
 "data": {
 "adom": "ClearPass",
 "connector": "cp-001",
 "ip-addr": "10.0.0.100",
 "role": "Marketing, [User Authenticated]",
 "user": "user100"
 },
 "url": "/connector/user/login"
 }
 ],
 "session": "Nsr3neywQlAxPXm+IHNhsjGr0bzzD4SRXSP8Q7zuBiwMpT+1yFrISKBvIdJBokSxL15X9OLr6HZPH4BpU3FmTQ==",
 "verbose": 1
}
```

> **Note:**

`Marketing` has to be mapped to an existing `user.group` used in a firewall policy. Or `user.adgrp` object named `cp_<connector>_Marketing` has to be used by a firewal policy

```
RESPONSE

{
 "id": 1,
 "result": [
 {
 "status": {
 "code": 0,
 "message": "OK"
 },
 "url": "/connector/user/login"
 }
 ]
}
```

### 5.2.7. How to simulate a user logout via FMG JSON API?

The end result will be that FMG will see an authenticated clearpass user, and will send it to the managed devices.

```
REQUEST

{
 "id": 1,
 "method": "exec",
 "params": [
 {
 "data": {
 "adom": "ClearPass",
 "connector": "cp-001",
 "ip-addr": "10.0.0.100",
 "role": "Marketing, [User Authenticated]",
 "user": "user100"
 },
 "url": "/connector/user/logout"
 }
 ],
 "session": "y1S9rwduTi71hMjLsur1P4vQ5ZbnX6aMpjBsSVfYLtVyeXGM0Srg1hbyIx6jLqcxWJ4h1gxp02BLBITWE5DGMg==",
 "verbose": 1
}

RESPONSE

{
 "id": 1,
 "result": [
 {
 "status": {
 "code": 0,
 "message": "OK"
 },
 "url": "/connector/user/logout"
 }
 ]
}
```

## 5.3. Cisco ACI

### 5.3.1. How to get all tenants?

```
REQUEST

{
 "id": 1,
 "method": "exec",
 "params": [
 {
 "data": {
 "adom": "root",
 "command": "epgs",
 "connector_name": "APIC-MOW"
 },
 "url": "/sys/api/sdnconnector"
 }
 ],
 "session": 11221
}

RESPONSE

{
 "id": 1,
 "result": [
 {
 "data": "[{\"epgs\": [{\"name\": \"classic|VLAN_3102\", \"tags\": []}, {\"name\": \"classic|uAPP\", \"tags\": []}, {\"name\": \"classic|uWeb.test\", \"tags\": []}, {\"name\": \"classic|VLAN_3100\", \"tags\": []}, {\"name\": \"classic|uWEB\", \"tags\": []}, {\"name\": \"classic|uApp.test\", \"tags\": []}], \"tenant\": \"customer\"}, {\"epgs\": [{\"name\": \"K8sDemo_bd_kubernetes-service|ToOut-L3OUT\", \"tags\": [\"K8sDemo-8bb120060f0848e0280b450eeea23d95\"]}, {\"name\": \"K8sDemo_bd_kubernet[...]",
 }
 "[...]": "[...]"
}
```

> **Note:**

### 5.3.2. How to import a tenant?

First you need to get the available tenants by using the info [how_to_get_all_tenants].

Then you just have to pick one tenant from the outout, and create a Firewall Address.

```
REQUEST

{
 "id": 1,
 "method": "add",
 "params": [
 {
 "data": {
 "epg-name": "classic|VLAN_3100",
 "name": "customer-classic|VLAN_3100",
 "sdn": "AP IC-MOW",
 "tenant": "customer",
 "type": 15
 },
 "url": "pm/config/adom/root/obj/firewall/address"
 }
 ],
 "session": 11221
}
```

## 5.4. SSO Agent

### 5.4.1. How to retrieve new `user.agrp`?

The goal is to trigger the same operation as the _Apply&Refresh_ button present when editing a _Fortinet Single Sign-On Agent_.

```
REQUEST

{
 "id": "1",
 "method": "exec",
 "params": [
 {
 "url": "sys/api/fsso",
 "data": {
 "adom": "{{adom}}",
 "user_fsso": "fsso_agent_001"
 }
 }
 ],
 "session": "{{session}}"
}
```

## 5.5. Thread Feeds Connectors

### 5.5.1. How to define local or remote external resources hosted in FortiManager?

See sections [Local External Resources] and [Remote External Resources].

### 5.5.2. How to get resolved IP addresses for an IP Address Threat Feed?

The following example shows how to get the resolved IP addresses for the `malicicous_ip` IP Address Thread Feed defined in the `demo` ADOM and from the perspective of the `dev_001` managed device:

```
REQUEST

{
 "id": 3,
 "method": "exec",
 "params": [
 {
 "data": {
 "action": "get",
 "resource": "/api/v2/monitor/system/external-resource/entry-list?count=0&mkey=malicious_ip&vdom=root",
 "target": [
 "adom/demo/device/dev_001"
 ]
 },
 "url": "/sys/proxy/json"
 }
 ],
 "session": "{{session}}"
}

RESPONSE

{
 "id": 3,
 "result": [
 {
 "data": [
 {
 "response": {
 "action": "entry-list",
 "build": 2571,
 "http_method": "GET",
 "name": "external-resource",
 "path": "system",
 "results": {
 "conn_attempt_time": 1715356114,
 "entries": [
 {
 "entry": "192.168.2.100",
 "valid": true
 },
 {
 "entry": "172.200.1.4/16",
 "valid": true
 },
 {
 "entry": "172.16.1.2/24",
 "valid": true
 },
 {
 "entry": "172.16.8.1-172.16.8.100",
 "valid": true
 },
 {
 "entry": "2001:0db8::eade:27ff:fe04:9a01/120",
 "valid": true
 },
 {
 "entry": "2001:0db8::eade:27ff:fe04:aa01-2001:0db8::eade:27ff:fe04:ab01",
 "valid": true
 }
 ],
 "http_status_code": 304,
 "invalid_count": 0,
 "last_content_update_time": 1715355563,
 "overflow": false,
 "resource_file_status": "downloaded",
 "status": "success",
 "valid_count": 6
 },
 "serial": "FGVMMLREDACTED40",
 "status": "success",
 "vdom": "root",
 "version": "v7.4.2"
 },
 "status": {
 "code": 0,
 "message": "OK"
 },
 "target": "dev_001"
 }
 ],
 "status": {
 "code": 0,
 "message": "OK"
 },
 "url": "/sys/proxy/json"
 }
 ]
}
```

## 5.6. SASE Connector

### 5.6.1. How to add a SASE Connector?

```
REQUEST

{
 "id": 3,
 "method": "exec",
 "params": [
 {
 "data": {
 "adom": "demo"
 "flags": [
 "create-task"
 ],
 "key": "12345678901234567890123456789012",
 "name": "Connector_to_FortiSASE"
 },
 "url": "/dmsase/add/service"
 }
 ],
 "session": "{{session}}"
}

RESPONSE

{
 "cid": 68,
 "id": 3,
 "result": [
 {
 "data": {
 "task": 271
 },
 "status": {
 "code": 0,
 "message": "OK"
 },
 "url": "/dmsase/add/service"
 }
 ]
}
```

> **TODO::**
>
```
```
# Get SASE Controller status
Request [gui forward:23891:9aed47df-a7fd-4c2f-acdf-65c35e4756c4]:
```
{ "client": "gui forward:23891", "id": "9aed47df-a7fd-4c2f-acdf-65c35e4756c4", "keep_session_idle": 1, "method": "get", "params": [{ "scope member": { "name": "FFSASEREDACTED67", "vdom": "root"}, "target start": 2, "url": "pm\/config\/adom\/root\/obj\/fmg\/sase-manager\/status"}], "session": 3761}
Response [gui forward:23891:9aed47df-a7fd-4c2f-acdf-65c35e4756c4]:
{ "id": "9aed47df-a7fd-4c2f-acdf-65c35e4756c4", "result": [{ "data": { "forticlient-ver": "7.0.11", "forticloud-id": 1705791, "license-type": 0, "oid": 8283, "spa-hubs": 0}, "status": { "code": 0, "message": "OK"}, "url": "pm\/config\/adom\/root\/obj\/fmg\/sase-manager\/status"}]}
```

```
```
# Get SASE Controller settings
Request [gui forward:23894:0b253ff9-cfee-44e2-a066-fef040565032]:
```
{ "client": "gui forward:23894", "id": "0b253ff9-cfee-44e2-a066-fef040565032", "keep_session_idle": 1, "method": "get", "params": [{ "object template": 0, "option": ["get used", "get flags", "get devobj mapping", "get meta", "loadsub"], "scope member": { "name": "FFSASEREDACTED67", "vdom": "root"}, "target start": 2, "url": "pm\/config\/adom\/root\/obj\/fmg\/sase-manager\/settings"}], "session": 3761}
Response [gui forward:23894:0b253ff9-cfee-44e2-a066-fef040565032]:
{ "id": "0b253ff9-cfee-44e2-a066-fef040565032", "result": [{ "data": {   "address": ["BaaS_Backup_Clients_FAL", "ACE_Tacacs_Clients", "Bad_IPs_Group", "sase-BSA_Host_List", "AKLHYDRA1"], "oid": 8282, "profile-group": ["CMI Mandated", "DOE Mandated", "sase-security-group"], "sync-address": 5, "sync-profile-group": 5, "sync-user": 5, "user": ["sase-servers-group", "sase-groups", "sase-user2", "sase-user1", "sase-ldap-server", "sase-radius-server"]}, "status": { "code": 0, "message": "OK"}, "url": "pm\/config\/adom\/root\/obj\/fmg\/sase-manager\/settings"}]}
```
```