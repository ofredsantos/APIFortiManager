The following example shows how to delete the md_001 metadata in the demo ADOM:

```
REQUEST
{
  "id": 3,
  "method": "delete",
  "params": [
    {
      "url": "/pm/config/adom/demo/obj/fmg/variable/md_001"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
# 1.1.3. How to rename a metadata?
```

The following example shows how to rename the md_001 metadata to md_002 in the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "set",
  "params": [
    {
      "data": {
        "name": "md_002"
      },
      "url": "/pm/config/adom/demo/obj/fmg/variable/md_001"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
### 1.1.4. How to assign a metadata to devices?
#### 1.1.4.1. For a single device
```

The following example shows how to add a per-device mapping to the md_001 metadata for the dev_001 device in the demo ADOM; its value will be 1.

```
```
REQUEST
{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": [
        {
          "_scope": [
            {
              "name": "dev_001",
              "vdom": "global"
            }
          ],
          "value": "1"
        }
      ],
      "url": "/pm/config/adom/demo/obj/fmg/variable/md_001/dynamic_mapping"
    }
  ],
  "session": "{{session}}"
}
```


> **Warning:**

The value attribute has to be set with a string!

RESPONSE
```
```
#### 1.1.4.2. For multiple devices
```

The following example shows how to add per-device mapping to the md_001 metadata for the dev_001 and dev_002 devices in the demo ADOM; its value will be 1 and 2 respectively:

```
```
REQUEST
{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": [
        {
          "_scope": [
            {
              "name": "dev_001",
              "vdom": "global"
            }
          ],
          "value": "1"
        },
        {
          "_scope": [
            {
              "name": "dev_002",
              "vdom": "global"
            }
          ],
          "value": "2"
        }
      ],
      "url": "/pm/config/adom/demo/obj/fmg/variable/site_id/dynamic_mapping"
    }
  ],
  "session": "{{session}}"
}
```


> **Warning:**

The value attribute has to be set with a string!

RESPONSE
```
```
### 1.1.5. How to assign metadatas at Model Device creation time?
```

It can be exposed by using the following FortiManager CLI debug command:

```
```
diagnose debug service dvmcmd 255
diagnose debug

REQUEST
{
  "client": "gui json:23235",
  "id": "57337fc8-5029-4458-b100-18cddddb707b",
  "keep_session_idle": 1,
  "method": "exec",
  "params": [
    {
      "data": {
        "add-dev-list": [
          {
            "_platform": "FortiGate-VM64-KVM",
            "adm_pass": "******",
            "adm_usr": "admin",
            "desc": "Model device",
            "device action": "add_model",
            "device blueprint": "BRANCHES",
            "extra commands": [
              {
                "id": 1,
                "method": "set",
                "params": [
                  {
                    "data": {
                      "_scope": {
                        "name": "BRANCH_03",
                        "vdom": "global",
                        "vdom_oid": 1
                      },
                      "value": "10.200.1.3"
                    },
                    "url": "pm/config/adom/DEMO/obj/fmg/variable/BGP_LOOPBACK/dynamic_mapping"
                  }
                ]
              },
              {
                "id": 1,
                "method": "set",
                "params": [
                  {
                    "data": {
                      "_scope": {
                        "name": "BRANCH_03",
                        "vdom": "global",
                        "vdom_oid": 1
                      },
                      "value": ""
                    },
                    "url": "pm/config/adom/DEMO/obj/fmg/variable/INET1_IP/dynamic_mapping"
                  }
                ]
              },
              {
                "id": 1,
                "method": "set",
                "params": [
                  {
                    "data": {
                      "_scope": {
                        "name": "BRANCH_03",
                        "vdom": "global",
                        "vdom_oid": 1
                      },
                      "value": ""
                    },
                    "url": "pm/config/adom/DEMO/obj/fmg/variable/INET2_IP/dynamic_mapping"
                  }
                ]
              },
              {
                "id": 1,
                "method": "set",
                "params": [
                  {
                    "data": {
                      "_scope": {
                        "name": "BRANCH_03",
                        "vdom": "global",
                        "vdom_oid": 1
                      },
                      "value": "10.71.144.1/24"
                    },
                    "url": "pm/config/adom/DEMO/obj/fmg/variable/MPLS_IP/dynamic_mapping"
                  }
                ]
              },
              {
                "id": 1,
                "method": "set",
                "params": [
                  {
                    "data": {
                      "_scope": {
                        "name": "BRANCH_03",
                        "vdom": "global",
                        "vdom_oid": 1
                      },
                      "value": "10.0.3.1/24"
                    },
                    "url": "pm/config/adom/DEMO/obj/fmg/variable/LAN_IP/dynamic_mapping"
                  }
                ]
              },
              {
                "id": 1,
                "method": "set",
                "params": [
                  {
                    "data": {
                      "_scope": {
                        "name": "BRANCH_03",
                        "vdom": "global",
                        "vdom_oid": 1
                      },
                      "value": "10.0.31.1/24"
                    },
                    "url": "pm/config/adom/DEMO/obj/fmg/variable/VLAN1_IP/dynamic_mapping"
                  }
                ]
              },
              {
                "id": 1,
                "method": "set",
                "params": [
                  {
                    "data": {
                      "_scope": {
                        "name": "BRANCH_03",
                        "vdom": "global",
                        "vdom_oid": 1
                      },
                      "value": "10.0.32.1/24"
                    },
                    "url": "pm/config/adom/DEMO/obj/fmg/variable/VLAN2_IP/dynamic_mapping"
                  }
                ]
              },
              {
                "id": 1,
                "method": "set",
                "params": [
                  {
                    "data": {
                      "_scope": {
                        "name": "BRANCH_03",
                        "vdom": "global",
                        "vdom_oid": 1
                      },
                      "value": "10.0.33.1/24"
                    },
                    "url": "pm/config/adom/DEMO/obj/fmg/variable/VLAN3_IP/dynamic_mapping"
                  }
                ]
              },
              {
                "id": 1,
                "method": "set",
                "params": [
                  {
                    "data": {
                      "_scope": {
                        "name": "BRANCH_03",
                        "vdom": "global",
                        "vdom_oid": 1
                      },
                      "value": "172.16.31.42/24"
                    },
                    "url": "pm/config/adom/DEMO/obj/fmg/variable/OOB/dynamic_mapping"
                  }
                ]
              },
              {
                "id": 1,
                "method": "set",
                "params": [
                  {
                    "data": {
                      "_scope": {
                        "name": "BRANCH_03",
                        "vdom": "global",
                        "vdom_oid": 1
                      },
                      "value": "140"
                    },
                    "url": "pm/config/adom/DEMO/obj/fmg/variable/VLAN_BASE/dynamic_mapping"
                  }
                ]
              }
            ],
            "faz.perm": 15,
            "faz.quota": 0,
            "groups": [
              "BRANCHES"
            ],
            "is_vm": true,
            "mgmt_mode": 3,
            "mr": 2,
            "name": "BRANCH_03",
            "os_type": 0,
            "os_ver": 7,
            "sn": "FGVM08TM23000464"
          }
        ],
        "adom": "DEMO",
        "flags": [
          "create_task",
          "nonblocking",
          "log_dev"
        ]
      },
      "target start": 2,
      "url": "/dvm/cmd/add/dev-list"
    }
  ],
  "session": 52098
}
```


You’ll find additional details along with another alternative in section How to add a Model HA Cluster with Device Blueprint and Metadata?.

```
### 1.1.6. How to unassign a metadata?
```

The following example shows how to delete per-device mapping of the md_001 metadata for the dev_001 device in the demo ADOM:

```
REQUEST
{
  "id": 3,
  "method": "delete",
  "params": [
    {
      "url": "/pm/config/adom/demo/obj/fmg/variable/md_001/dynamic_mapping/dev_001/global"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
### 1.1.7. How to replace assigned device with another one?
```

The demo ADOM has the md_001 metadata assigned to the dev_001 device with value 1:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/demo/obj/fmg/variable/md_001/dynamic_mapping/dev_001/global"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```

The following example shows how to replace this per-device mapping with a new one for the dev_002 device:

```
REQUEST
{
  "id": 3,
  "method": "set",
  "params": [
    {
      "data": [
        {
          "name": "dev_002",
          "vdom": "global"
        }
      ],
      "url": "/pm/config/adom/demo/obj/fmg/variable/md_001/dynamic_mapping/dev_001/global/_scope"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```

You can double check: both value and oid are still with same value as before the replace operation:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/demo/obj/fmg/variable/md_001/dynamic_mapping/dev_002/root"
    }
  ],
  "session": "{{session}}"
}

REQUEST
```
### 1.1.8. How to get the metadata mapped to a specific managed device?
```

The following example shows how to get all the metadata mapped to the dev_001 managed device in the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "fields": [
        "name"
      ],
      "sub fetch": {
        "dynamic_mapping": {
          "fields": [
            "value"
          ],
          "scope member": [
            {
              "name": "dev_001",
              "vdom": "global"
            }
          ],
          "subfetch count": [
            "==",
            1
          ]
        }
      },
      "subfetch filter": 1,
      "url": "/pm/config/adom/demo/obj/fmg/variable"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
### 1.1.9. How to get the value of a metadata for a specific device/vdom?
```

The following example shows how to get the value of the var_001 metadata for the dev_001 mnanaged device and its global scope, from the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/demo/obj/fmg/variable/var_001/dynamic_mapping/dev_001/global"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```

The following example shows how to the value of the var_001 metadata for the dev_002 managed device and, this time, its root VDOM, from the demo ADOM:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/demo/obj/fmg/variable/var_001/dynamic_mapping/dev_002/root"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
### 1.1.10. How to set multiple metadatas for one device?
```

It is possible to use a single FortiManager JSON RPC API request.

The following example set the var_001 and var_002 metadata variables from the demo ADOM for the dev_001 managed device:

```
```
REQUEST
{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": {
        "_scope": [
          {
            "name": "dev_001",
            "vdom": "global"
          }
        ],
        "value": "var_001_dev_001"
      },
      "url": "/pm/config/adom/demo/obj/fmg/variable/var_001/dynamic_mapping"
    },
    {
      "data": {
        "_scope": [
          {
            "name": "dev_001",
            "vdom": "global"
          }
        ],
        "value": "var_002_dev_001"
      },
      "url": "/pm/config/adom/demo/obj/fmg/variable/var_002/dynamic_mapping"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
### 1.1.11. How to assign a global metadata?
```

Here the assign is in the sense to copy the global metadatas defined in the Global ADOM into specific normal ADOMs.

Global ADOM is having the global metadata g_hostname.

The following example shows how to assign the g_hostname global metadata to the root, adom_001 and adom_002 ADOMs:

```
```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "data": {
        "adom": "global",
        "category": 3200,
        "flags": "none",
        "objs": [
          "g_hostname"
        ],
        "scope": [
          {
            "adom": "root"
          },
          {
            "adom": "adom_001"
          },
          {
            "adom": "adom_002"
          }
        ],
        "target": [
          {
            "adom": "root"
          },
          {
            "adom": "adom_001"
          },
          {
            "adom": "adom_002"
          }
        ]
      },
      "url": "/securityconsole/assign/objs"
    }
  ],
  "session": "{{session}}"
}
```


> **Note:**

The category attribute is the number of the table fmg variable

You can get this number by issuing following command:

execute fmpolicy print-adom-object Global ?


In the output, you will see this line:

```
[...]
3200      "fmg variable"
[...]

RESPONSE
```
### 1.1.12. How to get the assignement status for global metadatas?
```

Caught in #1123231.

The following example shows how to get the assignment status for the global metadatas in the Global ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/global/_objstatus/fmg/variable"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}
```


> **Note:**

_objstatus keyword in the url attribute is the method to object assignement status for the global metadatas.

RESPONSE
```
```
### 1.1.13. How to Export/Import metadatas?
```

The FortiManager GUI allows you to export and import metadatas in either CSV or JSON format.

However, the CSV export/import process still relies on JSON format:

During CSV export, FortiManager first generates the data in JSON format, then it converts it to CSV before saving the file to your disk

During CSV import, FortiManager reads your CSV file, converts it to JSON format, and then adds the metadatas to the ADOM database

Direct CSV export/import cannot be performed via the FortiManager API. You will need to handle the conversion between CSV and JSON formats manually for both the export and import operations.

In the two next sections, you will export/import the following CSV file:

variable_name,default_value,description,device,VDOM,mapped_value
var_001,1,Variable #001,dev_001,,1_1
var_001,1,Variable #001,dev_002,root,1_2
var_002,2,Variable #002,,,


Where in the case of the import operation:

Metadata var_001 will be created with 1 as default value and will have two per-device mappings:

1_1 value will be set to the global scope of the dev_001 device because the vdom value is empty

However, 1_2 value will be set to the root VDOM of the dev_002 device

Metadata var_002 will be created with 2 as default value

```
#### 1.1.13.1. Export

The following example shows how to export in JSON format all your metadatas for the demo ADOM:

```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "url": "/pm/config/adom/demo/_fmgvar/export"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
#### 1.1.13.2. Import
```

Caught in #1032303.

The following example shows how to import metadatas in the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "data": "{'adom': 'dc_jani', 'variables': [{'name': 'var_001', 'description': 'Variable #001', 'value': '1', 'mapping': [{'value': '1_1', 'device': 'dev_001', 'vdom': ''}, {'value': '1_2', 'device': 'dev_002', 'vdom': 'root'}]}, {'name': 'var_002', 'description': 'Variable #002', 'value': '2'}]}",
      "url": "/pm/config/adom/demo/_fmgvar/import"
    }
  ],
  "session": "{{session}}"
}
```


> **Note:**

the data attribute has to be a string!

RESPONSE
```
```
## 1.2. Firewall Address
```
```
### 1.2.1. How to add a IP Range firewall address?

The following example shows how to add the iprange_001 firewall address in the demo ADOM:

```
REQUEST
{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": {
        "color": 4,
        "comment": "IP range #001",
        "end-ip": "10.0.0.100",
        "name": "iprange_001",
        "start-ip": "10.0.0.1",
        "type": "iprange"
      },
      "url": "/pm/config/adom/demo/obj/firewall/address"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
### 1.2.2. How to add a FQDN firewall address?
```

To add FQDN www.foobar.com in ADOM adom_70_001:

```
```
REQUEST:

{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": {
        "color": 2,
        "fqdn": "www.foobar.com",
        "name": "fqdn_001",
        "type": "fqdn"
      },
      "url": "/pm/config/adom/adom_70_001/obj/firewall/address"
    }
  ],
  "session": "FhdDcem5V4cjJZeGggJ36dn5fME4nxr4rkA0zojtu+c31+wGhWl2zhhhE2hyP/MAXWQQzNE1yUgQOrJ3eTH7SQ=="
}


RESPONSE:

{
  "id": 3,
  "result": [
    {
      "data": {
        "name": "fqdn_001"
      },
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/adom_70_001/obj/firewall/address"
    }
  ]
}
```

```
```
## 1.3. Firewall Address Groups
```
```
### 1.3.1. How to add a single member?

We add firewall address host_004 in the existing address group foobar from ADOM adom_dc2:

```
REQUEST:

{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": [
        "host_004"
      ],
      "url": "/pm/config/adom/adom_dc2/obj/firewall/addrgrp/foobar/member"
    }
  ],
  "session": "mZMkY72ZIYcs8QInB0h5CUILmCKWCesbvxXJ3P/t+JSrzBh32BV/HvCU7BNMp4GLe8/5vO1qNAoRlsSytXUlTw=="
}


RESPONSE:

{
  "id": 3,
  "result": [
    {
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/adom_dc2/obj/firewall/addrgrp/foobar/member"
    }
  ]
}
```

### 1.3.2. How to delete a single member?

We delete firewall address host_004 from the existing address group foobar from ADOM adom_dc2:

```
REQUEST:

{
  "id": 3,
  "method": "delete",
  "params": [
    {
      "data": [
        "host_004"
      ],
      "url": "/pm/config/adom/adom_dc2/obj/firewall/addrgrp/foobar/member"
    }
  ],
  "session": "5uNGBXEMc+cNXjSlx6RuyxE623Nul3hGTCEgeA7pONsNhMMEL1lxCUG7q2TVfnhD0BZiwMg+CgKpWuVY2k0oew=="
}


RESPONSE:

{
  "id": 3,
  "result": [
    {
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/adom_dc2/obj/firewall/addrgrp/foobar/member"
    }
  ]
}
```

### 1.3.3. How to delete all members?

> **Note:**

You can delete all members because since FortiOS 7.2.0 (Internal Reference #0769154), you can operate an empty firewall addrgrp object

#### 1.3.3.1. Using the unset method

The following example shows how to delete all members from othe grp_001 firewall addrgrp in the demo ADOM using the unset method:

```
REQUEST
{
  "id": 3,
  "method": "unset",
  "params": [
    {
      "url": "/pm/config/adom/demo/obj/firewall/addrgrp/grp_001/member"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
#### 1.3.3.2. Using the unset attrs
```

The following example shows how to delete all members from othe grp_001 firewall addrgrp in the demo ADOM using the unset attrs described in How to unset a specific attribute?:

```
```
REQUEST
{
  "id": 3,
  "method": "set",
  "params": [
    {
      "data": {
        "unset attrs": [
          "member"
        ]
      },
      "url": "/pm/config/adom/demo/obj/firewall/addrgrp/grp_001"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
### 1.3.4. How to get firewall addrgrp members along with their details?
```

The following example demonstrates how to use the expand datasrc attribute to obtain the full details of the members of the addrgrp_001 address group in the demo ADOM:

We’re getting the member elements of our addrgrp_001 address group:

```
```
REQUEST
{
  "id": 1,
  "params": [
    {
      "expand datasrc": [
        {
          "datasrc": [
            {
              "fields": [
                "name",
                "subnet"
              ],
              "obj type": "firewall address"
            },
            {
              "fields": [
                "name",
                "member"
              ],
              "obj type": "firewall addrgrp"
            }
          ],
          "name": "member"
        }
      ],
      "filter": [
        "name",
        "==",
        "addrgrp_001"
      ],
      "url": "/pm/config/adom/demo/obj/firewall/addrgrp"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
## 1.4. Firewall VIP
### 1.4.1. How to add a new Firewall VIP?
```

The following example shows how to add a new Firewall VIP named vip_001 in the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": {
        "extintf": [
          "any"
        ],
        "extip": [
          "20.0.0.1-20.0.0.10"
        ],
        "mappedip": [
          "10.0.0.11-10.0.0.20"
        ],
        "name": "vip_001",
        "status": "enable"
      },
      "url": "/pm/config/adom/demo/obj/firewall/vip"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
### 1.4.2. How to add a new Firewall VIP Group?
```

The following example shows how to add a new Firewall VIP Group named vipgrp_001 in the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": {
        "interface": [
          "any"
        ],
        "member": [
          "vip_001",
          "vip_002"
        ],
        "name": "vipgrp_001"
      },
      "url": "/pm/config/adom/demo/obj/firewall/vipgrp"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
## 1.5. Wildcard FQDN
### 1.5.1. How to add a wildcard FQDN?
```

To add wilcard FQDN *.foobar.* to ADOM adom_70_001:

```
```
REQUEST:

{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": {
        "color": 3,
        "name": "w_fqdn_001",
        "wildcard-fqdn": "*.foobar.*",
      },
      "url": "/pm/config/adom/adom_70_001/obj/firewall/wildcard-fqdn/custom"
    }
  ],
  "session": "/CPDFD77zdvbfmX5tI0OwZ6mEha6Zcfsn1qPaITMmr43uysUgPlNBK5TgUIXFYQcoQXwF0w2oh1XcKRUnB2BMg=="
}


RESPONSE:

{
  "id": 3,
  "result": [
    {
      "data": {
        "name": "w_fqdn_001"
      },
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/adom_70_001/obj/firewall/wildcard-fqdn/custom"
    }
  ]
}
```

```
```
## 1.6. Normalized Interfaces
```
```
### 1.6.1. How to create a normalized interface?

```
REQUEST:

{
  "id": 1,
  "jsonrpc": "1.0",
  "method": "add",
  "params": [
    {
        "data": {
            "color": 2,
            "default-mapping": "enable",
            "defmap-intf": "ul_isp1",
            "description": "Underlay over ISP #1",
            "dynamic_mapping": [
                {
                    "_scope": [
                        {
                            "name": "dut_fgt_2",
                            "vdom": "root"
                        }
                    ],
                    "local-intf": [
                        "port1"
                    ]
                }
            ],
            "name": "ul_isp1",
            "platform_mapping": [
                {
                    "intf-zone": "ul_isp1",
                    "name": "FortiGate-100F"
                }
            ]
        },
        "url": "/pm/config/adom/{{adom}}/obj/dynamic/interface/ul_isp1"
    }
  ],
  "session": "{{session_id}}",
  "verbose": 1
}


RESPONSE:

{
  "id": 1,
  "result": [
    {
      "data": {
        "name": "ul_isp1"
      },
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/knock_06999/obj/dynamic/interface/ul_isp1"
    }
  ]
}
```

### 1.6.2. How to add a new per-platform mapping to an existing Normalized Interface?

```
REQUEST:

{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": {
        "intf-zone": "ol_isp2",
        "name": "FortiGate-40F"
      },
      "url": "/pm/config/adom/root/obj/dynamic/interface/ol_isp2/platform_mapping"
    }
  ],
  "session": "6hngsu9e2X+JBkpzxVIdWYPqLeYactJjmyyXeGkpkB/BlzGI8R9ynUPSP2wKFH5rTcijjR4+XBXWfliD7ichEg=="
}


RESPONSE:

{
  "id": 3,
  "result": [
    {
      "data": {
        "name": "FortiGate-40F"
      },
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/root/obj/dynamic/interface/ol_isp2/platform_mapping"
    }
  ]
}
```

### 1.6.3. How to get the normalized interfaces mapped to a specific managed device?

The following example shows how to get the list of normalized interfaces with a per-device mapping for the dev_001 device and its root VDOM in the demo ADOM:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "fields": [
        "name"
      ],
      "sub fetch": {
        "dynamic_mapping": {
          "fields": [
            "local-intf"
          ],
          "scope member": [
            {
              "name": "dev_001",
              "vdom": "root"
            }
          ],
          "subfetch count": [
            "==",
            1
          ]
        },
        "platform_mapping": {
          "subfetch hidden": 1
        }
      },
      "subfetch filter": 1,
      "url": "/pm/config/adom/demo/obj/dynamic/interface"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
### 1.6.4. How to delete an existing per-platform mapping?

```
REQUEST:

{
  "id": 3,
  "method": "delete",
  "params": [
    {
      "url": "/pm/config/adom/root/obj/dynamic/interface/ol_isp2/platform_mapping/FortiGate-40F"
    }
  ],
  "session": "vfIpN+LiUYGkHWcdTYcEe5RtIhDuIlw/42o9EsZ1KwNCHmSnytwa+cmTHGSJwEyYtencb3kLmFdq6AX5PK2FxQ=="
}


RESPONSE:

{
  "id": 3,
  "result": [
    {
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/root/obj/dynamic/interface/ol_isp2/platform_mapping/FortiGate-40F"
    }
  ]
}
```

```
```
## 1.7. Internet Service Objects
```
```
### 1.7.1. How to get the regions that can be used in a Geographic Based Internet Service object?

The following example shows how to get the regions that could be used to define a geographic based internet service object:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/root/_fdsdb/internet-service/region"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
### 1.7.2. How to get the countries that can be used in a Geographic Based Internet Service object?
```

The following example shows how to get the countries that could be used to define a geographic based internet service object:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/root/_fdsdb/internet-service/country"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
### 1.7.3. How to get the cities that can be used in a Geographic Based Internet Service object?
```

The following example shows how to get the cities that could be used to define a geographic based internet service object:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/demo/_fdsdb/internet-service/city"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
### 1.7.4. How to get the list of Internet Service objects?
```

The following example shows how to get the list of Internet Service objects from the demo ADOM:

```
```
REQUEST
    {
      "id": 3,
      "method": "get",
      "params": [
        {
          "url": "pm/config/adom/demo/_fdsdb/internet-service",
        }
      ],
"session": "{{session}}",
"verbose": 1
    }

RESPONSE
```

> **Note:**

Following method is only working with old FortiManager 6.4.X

Caught in Mantis #0622870.

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "pm/config/adom/demo/obj/firewall/internet-service-name",
      "option": [
        "get used",
              "get flags",
              "get devobj mapping",
              "get meta",
              "extra info",
              "no loadsub"
      ]
    }
  ]
}
```


But according to the #0622870, it is better to consider the datasrc method explained in section [TODO] (datasrc).

```
```
### 1.7.5. How to get the entries of an Internet Service object?
```

The following example shows how to get the entries of the Internet Service object with ID 327886 (Microsoft-Intune) in the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/demo/_fdsdb/internet-service/327886/entry"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
```
```
### 1.7.6. How to get the list of Internet Service FQDN objects?
```

Caught in #1156791.

The following shows how to get the list of Internet Service FQDN objects for the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/demo/_fdsdb/firewall/internet-service-fortiguard"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
```
```
## 1.8. Replacement Message Group
### 1.8.1. How to get the default Replacement Message Groups?
```

Caught in #1040582.

The following example shows how to get the default Replacement Message Group for the demo ADOM:

```
```
REQUEST
{
  "id": 2,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/demo/obj/_system/replacemsg"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
## 1.9. Objects Operations
### 1.9.1. How to reference objects when names have special characters?
```

It is required to escape the special character using the \\ (double back-slash) notation.

For instance to update the Net_10.0.0.0/18 (where / is the special character) located in the root ADOM:

```
```
REQUEST
{
  "id": 4,
  "method": "update",
  "params": [
    {
      "url": "pm/config/adom/root/obj/firewall/address/Net_10.0.0.0\\/18",
      "data": {
        "subnet": "10.0.0.0/255.255.255.0",
      }
    }
  ],
  "session": "{{session}}",
}
```

```
```
### 1.9.2. Objects default values
```
```
#### 1.9.2.1. How to get the default values for a firewall address?

```
REQUEST:

{
  "id": 1,
  "jsonrpc": "1.0",
  "method": "get",
  "params": [
    {
      "object template": 1,
      "url": "/pm/config/adom/DB/obj/firewall/address"
    }
  ],
  "session": "HKERCCqx6ximKXlkWN7lxWIgqagVqpj0xXiJtFtYrpiLIL7X3nCuIdlnZw83N+N3JO95oUOOCIwE+emXMuLvcPvKXNHsVYSN",
  "verbose": 1
}
```

### 1.9.3. How to bulk add objects?

You have two methods:

params multi-plexing

data multi-plexing

#### 1.9.3.1. params multi-plexing

```
REQUEST:

{
  "id": 1,
  "jsonrpc": "1.0",
  "method": "add",
  "params": [
    {
      "data": {
        "name": "test_004",
        "subnet": [
          "10.0.0.4",
          "255.255.255.0"
        ]
      },
      "url": "/pm/config/adom/DEMO_008/obj/firewall/address"
    },
    {
      "data": {
        "name": "test_005",
        "subnet": [
          "10.0.0.5",
          "255.255.255.0"
        ]
      },
      "url": "/pm/config/adom/DEMO_008/obj/firewall/address"
    },
    {
      "data": {
        "name": "test_006",
        "subnet": [
          "10.0.0.6",
          "255.255.255.0"
        ]
      },
      "url": "/pm/config/adom/DEMO_008/obj/firewall/address"
    }
  ],
  "session": "H4bqANWVw4+9ChxkRYdNfdtu4kE+5emeSojgay0fOghSwAPaFuzoBSZHjcvWc6l3TanYih4q9QktzVvLNTdpzA==",
  "verbose": 1
}


RESPONSE:

{
  "id": 1,
  "result": [
    {
      "data": {
        "name": "test_004"
      },
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/DEMO_008/obj/firewall/address"
    },
    {
      "data": {
        "name": "test_005"
      },
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/DEMO_008/obj/firewall/address"
    },
    {
      "data": {
        "name": "test_006"
      },
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/DEMO_008/obj/firewall/address"
    }
  ]
}
```

#### 1.9.3.2. data multi-plexing

```
REQUEST:

{
  "id": 1,
  "jsonrpc": "1.0",
  "method": "add",
  "params": [
    {
      "data": [
        {
          "name": "test_001",
          "subnet": [
            "10.0.0.1",
            "255.255.255.0"
          ]
        },
        {
          "name": "test_002",
          "subnet": [
            "10.0.0.2",
            "255.255.255.0"
          ]
        },
        {
          "name": "test_003",
          "subnet": [
            "10.0.0.3",
            "255.255.255.0"
          ]
        }
      ],
      "url": "/pm/config/adom/DEMO_008/obj/firewall/address"
    }
  ],
  "session": "31rAPPvgsYtaqwXnlwKZJrJQHff1V5hbfwj9lB62868KC1n73fF739Z+wTP+J5CoTxjKSWE8TqY7mTHyFovW7w==",
  "verbose": 1
}


RESPONSE:

{
  "id": 1,
  "result": [
    {
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/DEMO_008/obj/firewall/address"
    }
  ]
}
```

### 1.9.4. How to get CLI configuration of a new object?

This is a new feature from FortiManager 7.6.0 (#0954842).

The following example shows how to get the CLI configuration for the host_001 firewall address which is going to be created in the demo ADOM:

```
REQUEST
{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": {
        "color": 4,
        "name": "host_001",
        "subnet": "10.0.0.1/32"
      },
      "option": [
        "cli config"
      ],
      "url": "/pm/config/adom/demo/obj/firewall/address"
    }
  ],
  "session": "{{seession}}"
}
```


> **Note:**

The cli config is asking FortiManager to just generate the CLI configuration that could have been used to create this object

RESPONSE
### 1.9.5. How to get the full ADOM database objects syntax?

Caught in #0607071.

```
REQUEST:

{
  "id": 1,
  "method": "get",
  "params": [
    {
      "url": "pm/config/adom/root/obj",
      "option": "syntax"
    }
  ]
}
```


> **Note:**

Option syntax is described in section [TODO].

### 1.9.6. Cloning objects
#### 1.9.6.1. How to clone a firewall address?

```
REQUEST:

{
  "id": 1,
  "jsonrpc": "1.0",
  "method": "clone",
  "params": [
    {
      "data": {
        "name": "clone_host_001"
      },
      "url": "/pm/config/adom/DEMO_013/obj/firewall/address/host_001"
    }
  ],
  "session": "/FPLhY0rgXbpuZYz3TpcGtHQirT0ZHF09ILBV0ZrsWs2Knebq+5+CZ0fXejmyNWVqUm9Aftknb1biLL2JwiyXw==",
  "verbose": 1
}


RESPONSE:

{
  "id": 1,
  "result": [
    {
      "data": {
        "name": "clone_host_001"
      },
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/DEMO_013/obj/firewall/address/host_001"
    }
  ]
}
```

### 1.9.7. How to copy objects?

Here the word copy refers to the action of copying an object from ADOM DB to Device DB.

The target object isn’t push down to the managed devices.

A proper install operation should be triggered.

The FortiManager JSON RPC API endpoint used to trigger this copy operation isn’t documented hence we used the output of the following FortiManager debug command compile the information shared in this section:

diagnose debug service main 255


When we issue the following FortiManager CLI command to trigger a copy operation, we’re getting the following output:

```
```
# execute fmpolicy copy-adom-object dc_helsinki "firewall address" foo_002 france
Do you want to continue? (y/n)y
```

Request [/bin/newcli:14057:3]:
{ "client": "\/bin\/newcli:14057", "id": 3, "method": "exec", "params": [{ "data": { "adom": 3273, "category": 140, "override_conflict": 1, "query_only": 0, "scope": [{ "oid": 3569}], "src_list": [{ "oid": 4827}]}, "url": "install\/global"}], "root": "securityconsole", "session": 12207}
Waiting for task 1347...
Task completed


In the following example, we copy the foo_002 firewall address from the dc_helsinki ADOM to the devices belonging to the france device group:

```
```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "data": {
        "adom": "dc_helsinki",
        "category": 140,
        "override_conflict": 1,
        "query_only": 0,
        "scope": [
          {
            "name": "france"
          }
        ],
        "src_list": [
          {
            "oid": 4827
          }
        ]
      },
      "url": "/securityconsole/install/global"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```

FortiManager will return a task ID (task attribute) but won’t run it in the background. We have to wait for the end of the request.

The request is having a lot of numerical information:

The category attribute

140 is the category ID for the firewall address table

Unfortunately, we cannot use the string "firewall address" as shown below:

```
{
  "category": "firewall address"
}
```


We have to use an id

How to get it?

To get the category ID of the firewall address table:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "option": [
        "syntax"
      ],
      "url": "/pm/config/adom/dc_helsinki/obj/firewall/address"
    }
  ],
  "session": "{{session}}"
}
```


In the response, you have to get:

.result[0]["data"]["firewall address"]["category"]


src_list attribute

This list contains the OID of the objects to copy

For the 140 category (firewall address) the src_list list contain OID of firewall address objects

How to get the OID of a firewall address?

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "fields": [
        "name"
      ],
      "loadsub": 0,
      "url": "/pm/config/adom/dc_helsinki/obj/firewall/address/foo_002"
    }
  ],
  "session": "7bQB94D0zHu7I9EGtwIbQJEbrcH7qRBI/hwWbqrP/RVUWLd8h1PiFyTD+brojmELiV/rVHcSdYX2CqTAtEcmhg=="
}

RESPONSE
```

You can use the usual scope:

```
{
  "scope": [
     {
       "name": "device_group_001",
     },
     {
       "name": "device_group_002",
     },
     {
       "name": "device_001",
       "vdom": "vd_001"
     },
     {
       "name": "device_001",
       "vdom": "vd_002"
     },
     {
        "...": "..."
     }
  ]
}
```

```
```
### 1.9.8. Filtering objects
```

Getting an object table could generate a lot of output data.

Furthermore, most of the time, you’re only interested by a sub-part of that table if not by a single entry.

This is what you can achieve by filtering objects.

```
#### 1.9.8.1. The contain operator

To get firewall address groups containing member host_001:

```
REQUESTRESPONSE
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "fields": [
        "name",
        "member"
      ],
      "filter": [
        "member",
        "contain",
        "host_001"
      ],
      "loadsub": 0,
      "url": "/pm/config/adom/dc_amer/obj/firewall/addrgrp"
    }
  ],
  "session": "{{ session }}"
}
```

#### 1.9.8.2. How to filter firewall address according to their IPs?

Most of the examples provided in this section are inspired by #0363496.

##### 1.9.8.2.1. Retrieve all firewall address objects matching a specific IP subnet

The following example demonstrates how to use the <= (in) comparison operator to retrieve all firewall address objects that match the specified 10.0.0.0/16 subnet within the demo ADOM:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "fields": [
        "name",
        "type",
        "subnet"
      ],
      "filter": [
        [
          "type",
          "==",
          "ipmask"
        ],
        "&&",
        [
          "subnet",
          "<=",
          [
            "10.0.0.0",
            "255.255.0.0"
          ]
        ]
      ],
      "loadsub": 0,
      "url": "/pm/config/adom/demo/obj/firewall/address"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
##### 1.9.8.2.2. Retrieve all firewall address objects that strictly match an IP address or subnet
```

The following example demonstrates how to use the == (exact match) comparison operator to retrieve all firewall address objects that exactly match the specified 10.0.0.111/32 IP address within the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "fields": [
        "name",
        "type",
        "subnet"
      ],
      "filter": [
        [
          "type",
          "==",
          "ipmask"
        ],
        "&&",
        [
          "subnet",
          "==",
          [
            "10.0.0.111",
            "255.255.255.255"
          ]
        ]
      ],
      "loadsub": 0,
      "url": "/pm/config/adom/demo/obj/firewall/address"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
##### 1.9.8.2.3. Retrieve all firewall address subnets matching a specific IP address
```

The following example demonstrates how to use the >= (greater than or equal) comparison operator to retrieve all firewall address objects that include the specified 10.0.0.111/32 IP address in the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "fields": [
        "name",
        "type",
        "subnet"
      ],
      "filter": [
        [
          "type",
          "==",
          "ipmask"
        ],
        "&&",
        [
          "subnet",
          ">=",
          [
            "10.0.0.111",
            "255.255.255.255"
          ]
        ]
      ],
      "loadsub": 0,
      "url": "/pm/config/adom/demo/obj/firewall/address"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```

The response contains objects like all, FABRIC_DEVICE or FIREWALL_AUTH_PORTAL_ADDRESS which do not strict match. If a strict match is required replace the >= operator with == in the block filtering objects matching the ipmask type.

```
```
##### 1.9.8.2.4. Retrieve all firewall address ranges containing a specific IP address
```

The following example demonstrates how to use the <= (in) and >= (contain) operators together to identify firewall address ranges that include the 10.0.0.111 IP address within the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "fields": [
        "name",
        "type",
        "start-ip",
        "end-ip"
      ],
      "filter": [
        [
          "type",
          "==",
          "iprange"
        ],
        "&&",
        [
          [
            "start-ip",
            "<=",
            "10.0.0.111"
          ],
          "&&",
          [
            "end-ip",
            ">=",
            "10.0.0.111"
          ]
        ]
      ],
      "loadsub": 0,
      "url": "/pm/config/adom/demo/obj/firewall/address"
    }
  ],
  "session": "{{session}}"
  "verbose": 1
}

RESPONSE
```
```
```
##### 1.9.8.2.5. Retrieve all firewall address subnets or ranges matching an IP address
```

The following example demonstrates how to build a complex filter expression to search for objects based on various criteria. In this case, the objective is to retrieve all firewall address ranges or subnets that match the 10.0.0.111/32 IP address within the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "fields": [
        "name",
        "type",
        "subnet",
        "start-ip",
        "end-ip"
      ],
      "filter": [
        [
          [
            "type",
            "==",
            "iprange"
          ],
          "&&",
          [
            [
              "start-ip",
              "<=",
              "10.0.0.111"
            ],
            "&&",
            [
              "end-ip",
              ">=",
              "10.0.0.111"
            ]
          ]
        ],
        "||",
        [
          [
            "type",
            "==",
            "ipmask"
          ],
          "&&",
          [
            "subnet",
            ">=",
            [
              "10.0.0.111",
              "255.255.255.255"
            ]
          ]
        ]
      ],
      "loadsub": 0,
      "url": "/pm/config/adom/demo/obj/firewall/address"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
```

The response contains objects like all, FABRIC_DEVICE or FIREWALL_AUTH_PORTAL_ADDRESS which do not strict match. If a strict match is required replace the >= operator with == in the block filtering objects matching the ipmask type.

```
```
```
##### 1.9.8.2.6. Retrieve all firewall addresses with a per-device mapping, where the subnet or range matches a specific IP address
```

The following example demonstrates how to create a complex filter expression to search for objects based on multiple criteria. In this example, the goal is to retrieve all firewall address objects within the demo ADOM that have a per-device mapping subnet or range matching the IP address 10.0.0.111/32:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "fields": [
        "name",
        "type",
        "subnet",
        "start-ip",
        "end-ip"
      ],
      "sub fetch": {
        "dynamic_mapping": {
          "fields": [
            "name",
            "type",
            "subnet",
            "start-ip",
            "end-ip"
          ],
          "filter": [
            [
              [
                "type",
                "==",
                "iprange"
              ],
              "&&",
              [
                [
                  "start-ip",
                  "<=",
                  "10.0.0.111"
                ],
                "&&",
                [
                  "end-ip",
                  ">=",
                  "10.0.0.111"
                ]
              ]
            ],
            "||",
            [
              [
                "type",
                "==",
                "ipmask"
              ],
              "&&",
              [
                "subnet",
                ">=",
                [
                  "10.0.0.111",
                  "255.255.255.255"
                ]
              ]
            ]
          ]
        },
        "list": {
          "subfetch hidden": 1
        },
        "tagging": {
          "subfetch hidden": 1
        }
      },
      "url": "/pm/config/adom/demo/obj/firewall/address"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}
```


> **Note:**

For the sub fetch and subfetch hidden instructions, review the Sub fetch operations section.

RESPONSE
```
```
##### 1.9.8.2.7. Retrieve all firewall address subnets or ranges matching a specific IP address including in their per-device mapping entries
```

This describes how to obtain the combined results from the API calls in the following two sections:

Retrieve all firewall address subnets or ranges matching an IP address

Retrieve all firewall addresses with a per-device mapping, where the subnet or range matches a specific IP address

This can be accomplished by multiplexing at the params block level.

The example below demonstrates how to retrieve all firewall address objects that match the IP address 10.0.0.111/32 (by subnet, range, and per-device mapping subnet and range as well). This time, a strict match is used for the ipmask case to reduce the amount of returned data.

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "fields": [
        "name",
        "type",
        "subnet",
        "start-ip",
        "end-ip"
      ],
      "filter": [
        [
          [
            "type",
            "==",
            "iprange"
          ],
          "&&",
          [
            [
              "start-ip",
              "<=",
              "10.0.0.111"
            ],
            "&&",
            [
              "end-ip",
              ">=",
              "10.0.0.111"
            ]
          ]
        ],
        "||",
        [
          [
            "type",
            "==",
            "ipmask"
          ],
          "&&",
          [
            "subnet",
            "==",
            [
              "10.0.0.111",
              "255.255.255.255"
            ]
          ]
        ]
      ],
      "loadsub": 0,
      "url": "/pm/config/adom/demo/obj/firewall/address"
    },
    {
      "fields": [
        "name",
        "type",
        "subnet",
        "start-ip",
        "end-ip"
      ],
      "sub fetch": {
        "dynamic_mapping": {
          "fields": [
            "name",
            "type",
            "subnet",
            "start-ip",
            "end-ip"
          ],
          "filter": [
            [
              [
                "type",
                "==",
                "iprange"
              ],
              "&&",
              [
                [
                  "start-ip",
                  "<=",
                  "10.0.0.111"
                ],
                "&&",
                [
                  "end-ip",
                  ">=",
                  "10.0.0.111"
                ]
              ]
            ],
            "||",
            [
              [
                "type",
                "==",
                "ipmask"
              ],
              "&&",
              [
                "subnet",
                "==",
                [
                  "10.0.0.111",
                  "255.255.255.255"
                ]
              ]
            ]
          ]
        },
        "list": {
          "subfetch hidden": 1
        },
        "tagging": {
          "subfetch hidden": 1
        }
      },
      "url": "/pm/config/adom/demo/obj/firewall/address"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
```
#### 1.9.8.3. How to get the Last Modified timestamp?
```

The following example will get the Last Modified timestamp (i.e., _modified timestamp) for the firewall address groups declared in the dc_amer ADOM:

```
```
REQUEST:
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "fields": [
        "name",
        "_modified timestamp"
      ],
      "option": [
        "extra info",
        "no loadsub"
      ],
      "url": "/pm/config/adom/dc_amer/obj/firewall/addrgrp"
    }
  ],
  "session": "PT2or1RfAXowIdjpnhHiEx4W6p12Hx3AkWE5RK9noPTLN5gKy79kywOSYEL5P5vjAc2Ymvt7Zo9OoXV8TndYfQ=="
}

RESPONSE
```
```
#### 1.9.8.4. How to filter on the Last Modified timestamp?
```

Idea is to retrieve the list of objects more recent that a specific timestamp.

Caught in #0539624.

```
```
REQUEST
{
  "id": 1,
  "method": "get",
  "params": [
    {
      "url": "pm/config/adom/FortiOS-54/obj/firewall/address",
      "option": [
        "get used",
        "get flags",
        "get devobj mapping",
        "get meta",
        "extra info",
        "no loadsub"
      ],
      "filter": [
        "_modified timestamp",
        ">=",
        1549412522
      ]
    }
  ]
            }
```


> **Note:**

The option of interest is extra info.

```
```
#### 1.9.8.5. The like operator
```

What if goal is to retrieve all firewall addresses whose name start with host_?

```
```
REQUESTRESPONSE
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "fields": [
        "name",
        "subnet"
      ],
      "filter": [
        "name",
        "like",
        "host_%"
      ],
      "loadsub": 0,
      "url": "/pm/config/adom/demo/obj/firewall/address"
    }
  ],
  "session": "Wvq6WltRC50vmipqJhAacFrS0RAr/sxQGdrr3NaT2SbAdcz8XzyPbZTd98ewBhiFtMmWLDLkUrSQWCVGhqzvZA==",
  "verbose": 1
}
```

```
```
#### 1.9.8.6. How to delete multiple objects?
```

The filter operator can also be very useful to delete multiple objects with a single FortiManager JSON RPC API request.

For instance to delete all firewall addresses starting with host_:

```
```
REQUEST:

{
  "id": 1,
  "create task": {
    "adom": "dc_amer"
  },
  "method": "delete",
  "params": [
    {
      "filter": [
          "name",
          "like",
          "host_%"
      ],
      "url": "/pm/config/adom/dc_amer/obj/firewall/address"
    }
  ],
  "session": "{{session}}"
}
```


> **Note:**

We’re using the create task to get a sucessful response!

In this case, we will just receive a task ID and we will have to review the task output.

The filter operator is for all name starting with host_.

```
RESPONSE:

{
  "id": 1,
  "result": [
    {
      "data": {
        "task": 7
      },
      "status": {
        "code": 0,
        "message": "OK"
      }
    }
  ]
}
```


Task failed!

Message (captured from the FortiManager GUI) is:

The command is invalid for selected url


OK…

In fact, an yes message is really not meaningful, we need to confirm such dangerous delete form.

We could place the wrong filter and delete a lot of objects!

Let’s retry by confirming the operation:

```
REQUEST:

{
  "id": 1,
  "create task": {
    "adom": "dc_amer"
  },
  "method": "delete",
  "params": [
    {
      "confirm": 1,
      "filter": [
          "name",
          "like",
          "host_%"
      ],
      "url": "/pm/config/adom/dc_amer/obj/firewall/address"
    }
  ],
  "session": "{{session}}"
}
```


> **Note:**

To confirm, you just need to use the confirm attribute.

But… Wait. The task failed again!

used


Of course, our objects are used in some firewall policies.

Let’s force the delete operation!

```
REQUEST:

{
  "id": 1,
  "create task": {
    "adom": "dc_amer"
  },
  "method": "delete",
  "params": [
    {
      "confirm": 1,
      "option": "force",
      "filter": [
          "name",
          "like",
          "host_%"
      ],
      "url": "/pm/config/adom/dc_amer/obj/firewall/address"
    }
  ],
  "session": "{{session}}"
}
```


> **Note:**

To force the requested operation, you have to use the option attribute set with the force keyword.

This time the task is succeeded.

> **Warning:**

The operation is succeeded even if you have the following FortiManager CLI setting disabled:

```
config system admin setting
    set objects-force-deletion disable
end
```


As a last word, on this particular exemple, to delete just the list of objects (and not more matching the previous used filter value) you could have used the following filter:

```
"filter": [
  "name",
  "in",
  "host_001",
  "host_002",
  "host_003",
]
```

```
### 1.9.9. Used/Unused objects
```

> **Note:**

This section will take the firewall address table as example, but you can apply it to all other tables.

#### 1.9.9.1. How to know whether a specific object is used?

We can use the option get used and observe the returned obj flags.

Our firewall address foo_host_001 is member of a firewall address group. It is only used in this firewall address group.

If we get it with the option get used, we can see a returned obj flags:

```
REQUEST:

{
  "id": 1,
  "jsonrpc": "1.0",
  "method": "get",
  "params": [
    {
      "fields": [
        "name",
        "obj flags"
      ],
      "loadsub": 0,
      "option": [
        "get used"
      ],
      "url": "/pm/config/adom/production_001/obj/firewall/address/foo_host_001"
    }
  ],
  "session": "oc+DBEboJovBLDkoYqyFkB3dnhoazTP1fbVTRIi1XbVHmVTvuL2A+lUxuYnhjk3L9Sdd74g/SqaOGFQO1saVB2aouTDXWgQg",
  "verbose": 1
}


RESPONSE:

{
  "id": 1,
  "result": [
    {
      "data": {
        "name": "foo_host_001",
        "obj flags": 1
      },
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/production_001/obj/firewall/address/foo_host_001"
    }
  ]
}
```


When obj flags is equal to 1 it means the object is used.

If we remove firewall address foo_host_001 from the group it was belonging to, the same request now gives:

```
RESPONSE:

{
  "id": 1,
  "result": [
    {
      "data": {
        "name": "foo_host_001"
      },
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/production_001/obj/firewall/address/foo_host_001"
    }
  ]
}
```


The obj flags is no longer returned meaning the object isn’t used.

#### 1.9.9.2. How to get the list of used objects?

You can get the list of used objects by getting the table only using the get used option as seen in section How to know whether a specific object is used?

For instance:

```
REQUEST:

{
  "id": 3,
  "method": "get",
  "params": [
    {
      "fields": [
        "name"
      ],
      "option": [
        "no loadsub",
        "get used"
      ],
      "url": "/pm/config/adom/production_001/obj/firewall/address"
    }
  ],
  "session": "Shc2xxYYd6Q0apcJAYewlcFxv/pgyCg/ADzB0hC187N1i70lzP9v2808/D2F89JhRFKPbxVAv0XiiK8SUAjrPQ==",
  "verbose": 1
}


RESPONSE:

{
  "id": 3,
  "result": [
    {
      "data": [
        {
          "name": "FABRIC_DEVICE",
          "oid": 2644
        },
        {
          "name": "FIREWALL_AUTH_PORTAL_ADDRESS",
          "oid": 2643
        },
        {
          "name": "RFC1918-10",
          "obj flags": 1,
          "oid": 2646
        },
        {
          "name": "RFC1918-172",
          "obj flags": 1,
          "oid": 2647
        },
        "...": "...",
        {
          "name": "metadata-server",
          "oid": 2645
        },
        {
          "name": "none",
          "oid": 2634
        },
        {
          "name": "wildcard.dropbox.com",
          "oid": 2640
        },
        {
          "name": "wildcard.google.com",
          "obj flags": 1,
          "oid": 2639
        }
      ],
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/knock_45329/obj/firewall/address"
    }
  ]
}
```


However, as you can see, FortiManager is still returning all firewall addresses!

You have to filter by yourself and isolate the returned objects which are using the obj flags.

You can try to add a filter block:

```
"filter": [
  "obj flags",
  "==",
  1
]
```


but it won’t work.

Fortunately, we can ask FortiManager to only return used objects using the following request:

```
REQUEST:

{
  "id": 3,
  "method": "get",
  "params": [
    {
      "fields": [
        "name"
      ],
      "filter": [
        [
          "object used",
          "==",
          1
        ],
        "&&",
        [
          "name",
          "like",
          "host_%"
        ]
      ],
      "option": [
        "no loadsub",
        "get used"
      ],
      "url": "/pm/config/adom/knock_45329/obj/firewall/address"
    }
  ],
  "session": "tdGYyiDdeDNhiaGmXCJShCAnWS+N5AIeWcb1bMtccP3xNmG6bGONVWUZkU5j+fpTAR48BlvGDfrebJdAcZGQBg==",
  "verbose": 1
}


RESPONSE:

{
  "id": 3,
  "result": [
    {
      "data": [
        {
          "name": "host_001",
          "obj flags": 1,
          "oid": 4156
        },
        {
          "name": "host_002",
          "obj flags": 1,
          "oid": 4157
        },
        {
          "name": "host_003",
          "obj flags": 1,
          "oid": 4158
        },
        "...": "...",
        {
          "name": "host_198",
          "obj flags": 1,
          "oid": 4353
        },
        {
          "name": "host_199",
          "obj flags": 1,
          "oid": 4354
        },
        {
          "name": "host_200",
          "obj flags": 1,
          "oid": 4355
        }
      ],
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/knock_45329/obj/firewall/address"
    }
  ]
}
```


> **Note:**

You can keep using the get used option just to confirm that all returned objects have the flag obj flags set to 1.

#### 1.9.9.3. How to get unused objects?

To get all unused firewall addresses from ADOM demo and matching a specific name:

```
REQUEST:

{
  "id": 3,
  "method": "get",
  "params": [
    {
      "fields": [
        "name"
      ],
      "filter": [
        [
          "object used",
          "==",
          0
        ],
        "&&",
        [
          "name",
          "like",
          "host_%"
        ]
      ],
      "option": [
        "search all adoms",
        "no loadsub"
      ],
      "url": "/pm/config/adom/knock_45329/obj/firewall/address"
    }
  ],
  "session": "Iu1Msbu+H9FQO/IjfnpRMI96BfCoASYDwzizRfmx6Th6xcMWmCuERL4KYmej7vTRfR58KTYKNqRMbxa25l0vMg==",
  "verbose": 1
}


RESPONSE:

{
  "id": 3,
  "result": [
    {
      "data": [
        {
          "name": "host_201",
          "oid": 4489
        },
        {
          "name": "host_300",
          "oid": 4481
        }
      ],
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/knock_45329/obj/firewall/address"
    }
  ]
}
```

### 1.9.10. Where Used
#### 1.9.10.1. How to where used from the global adom?

First of all, you have to allow FortiManager to search in all ADOMs:

```
config system global
set search-all-adoms enable
end
```


Then it’s a three steps process:

Start a where used request

In this example, we have the global object g_host_001 in the Global ADOM. We want to see where this object is used in all ADOMs.

```
REQUEST
{
  "id": 1,
  "method": "exec",
  "params": [
    {
      "data": {
        "mkey": "g_host_001",
        "obj": "global/obj/firewall/address"
      },
      "url": "/cache/search/where/used/start"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```

Wait for the where used task to complete

```
REQUEST
{
  "id": 1,
  "method": "exec",
  "params": [
    {
      "token": "K11EnEPIkRUx23ws7sbm6A==",
      "url": "cache/search/where/used/get/summary"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```

We can now get the final result

```
REQUEST
{
  "id": 1,
  "method": "exec",
  "params": [
    {
      "token": "K11EnEPIkRUx23ws7sbm6A==",
      "url": "/cache/search/where/used/get/detail"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
#### 1.9.10.2. How to where used from within a normal ADOM?
```

Follow the same three steps process as the one describe in How to where used from the global adom?

You just need to replace the obj attribute’s value with something like:

adom/<adom>/obj/firewall/address


For instance, if you want to where used the host_001 firewall address from within the dc_emea ADOM, your step 1 request will be:

```
```
{
  "id": 1,
  "method": "exec",
  "params": [
    {
      "data": {
        "mkey": "host_001",
        "obj": "adom/dc_emea/obj/firewall/address"
      },
      "url": "/cache/search/where/used/start"
    }
  ],
  "session": "{{session}}"
}
```

```
```
#### 1.9.10.3. How to where used only for direct object usage?
```

Caught in #1094113.

To retrieve the list of objects that directly use a specific object within an ADOM, you can trigger a where used process with the flags set to include the direct used option.

What is the behavior without direct used flag? If host_001 (a firewall address object) is used in the following ways:

Directly in the address group grp_002

Indirectly in the address group grp_001, which includes grp_002

Directly as the source in the firewall policy Policy_001

Indirectly as the destination in Policy_002, via its inclusion in grp_002

then the where used query will report all of these usages above.

What is the behavior with direct used flag? When the direct used flag is enabled, only direct references are returned. For the same object host_001, this means:

It is reported as a direct member of grp_002

It is reported as a direct source in Policy_001

Indirect usages such as through nested groups or inherited references are excluded.

The following example shows how to start a where used operation for the host_001 firewall address object in the demo ADOM using the direct used option:

```
```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "data": {
        "flags": [
          "direct used"
        ],
        "mkey": "host_001",
        "obj": "adom/demo/obj/firewall/address"
      },
      "url": "/cache/search/where/used/start"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
```
```
### 1.9.11. Find duplicates objects
```

To get duplicates firewall addresses:

```
```
REQUEST:

{
  "id": 1,
  "jsonrpc": "1.0",
  "method": "get",
  "params": [
    {
      "fields": [
        "name",
        "type",
        "subnet",
        "duplicate enntries"
      ],
      "load assigned": 0,
      "loadsub": 0,
      "option": [
        "find duplicates"
      ],
      "url": "/pm/config/adom/demo_002/obj/firewall/address"
    }
  ],
  "session": "V3pHwSOgmHZEQoqJ4pVHJFQSCIiaXm0cOjvXp40JN1ps2FQWNwqMNz0jATnrQxGr2K78L6+mY9Os8WRVBRCxKw==",
  "verbose": 1
}


RESPONSE:

{
  "id": 1,
  "result": [
    {
      "data": [
        {
          "duplicate entries": [
            "login.microsoft.com",
            "login.microsoftonline.com",
            "login.windows.net",
            "wildcard.dropbox.com",
            "wildcard.google.com"
          ],
          "name": "gmail.com",
          "subnet": [
            "0.0.0.0",
            "0.0.0.0"
          ],
          "type": "fqdn"
        },
        {
          "duplicate entries": [
            "FIREWALL_AUTH_PORTAL_ADDRESS",
            "all"
          ],
          "name": "FABRIC_DEVICE",
          "subnet": [
            "0.0.0.0",
            "0.0.0.0"
          ],
          "type": "ipmask"
        },
        {
          "duplicate entries": [
            "host_001_002"
          ],
          "name": "host_001_001",
          "subnet": [
            "10.0.0.1",
            "255.255.255.255"
          ],
          "type": "ipmask"
        }
      ],
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/demo_002/obj/firewall/address"
    }
  ]
}
```
```


FortiManager is using the fields attribute to format the response logic. For instance, if we remove the type criteria we will obtain this output:

```
```
REQUEST:

{
  "id": 1,
  "jsonrpc": "1.0",
  "method": "get",
  "params": [
    {
      "fields": [
        "name",
        "subnet"
      ],
      "load assigned": 0,
      "loadsub": 0,
      "option": [
        "find duplicates"
      ],
      "url": "/pm/config/adom/demo_002/obj/firewall/address"
    }
  ],
  "session": "qpzdhu+2yDsbeuGJQB/OUGjnmIa+/35YCJrXTudpteCy2XnTgHPEeFZaYHs4sHq1yFQohl7NkpfVjkW7H1dUxF5/i1JnAyE+",
  "verbose": 1
}


RESPONSE:

{
  "id": 1,
  "result": [
    {
      "data": [
        {
          "duplicate entries": [
            "FCTEMS_ALL_FORTICLOUD_SERVERS",
            "FIREWALL_AUTH_PORTAL_ADDRESS",
            "SSLVPN_TUNNEL_ADDR1",
            "all",
            "gmail.com",
            "login.microsoft.com",
            "login.microsoftonline.com",
            "login.windows.net",
            "wildcard.dropbox.com",
            "wildcard.google.com"
          ],
          "name": "FABRIC_DEVICE",
          "subnet": [
            "0.0.0.0",
            "0.0.0.0"
          ]
        },
        {
          "duplicate entries": [
            "host_001_002"
          ],
          "name": "host_001_001",
          "subnet": [
            "10.0.0.1",
            "255.255.255.255"
          ]
        }
      ],
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/demo_002/obj/firewall/address"
    }
  ]
}
```


Observe where are now listed the firewall addresses FIREWALL_AUTH_PORTAL_ADDRESS and all.

The find duplicates option is working with other objects, like address groups, IPv6 firewall addresses, VIP, etc. You just have to replace the url parameter with the proper path.

```
```
```
### 1.9.12. Merge objects
```
```
```
#### 1.9.12.1. How to merge firewall addresses?

We want to merge firewall address host_001_001 and host_001_002. Destination firewall address name has to be one of them; we cannot merge for instance to firewall address name host_001_merged.

In below example, we will merge both firewall address in host_001_001:

```
REQUEST:

{
  "id": 1,
  "jsonrpc": "1.0",
  "method": "set",
  "params": [
    {
      "merge": [
        "host_001_001",
        "host_001_002"
      ],
      "url": "/pm/config/adom/demo_002/obj/firewall/address/host_001_001"
    }
  ],
  "session": "1PIOQRlz0dKA/xk8nUY1dsmOuiI7rHcjaAyiTjbaSzJVnpa8smZ8VSUAsWn7NWW/ZZWusUbbrNfte0RgNHdInGwTCiQICw3Y",
  "verbose": 1
}


RESPONSE:

{
  "id": 1,
  "result": [
    {
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/demo_002/obj/firewall/address/host_001_001"
    }
  ]
}
```


> **Note:**

Replacing firewall address host_001_002 with firewall address host_001_001 everywhere it was used (in firewall policy, in firewall address group, etc.)

Deleting firewall address host_001_002

The merge operation is working with other objects, like address groups, IPv6 firewall addresses, VIP, etc. You just have to replace the url parameter with the proper path.

### 1.9.13. Find and Replace

The example below shows how to find and replace the firewall address group grp_002 used by some of our firewall policies, with firewall address group grp_001 in the demo ADOM.

First you need to where used the firewall address group grp_002 object. As you know the where used is a three steps process (see How to where used from within a normal ADOM?).

Step #1: You need to start a new where used task

```
REQUEST
{
  "id": 1,
  "method": "exec",
  "params": [
    {
      "data": {
        "flags": [
         "direct used"
        ],
        "mkey": "grp_002",
        "obj": "adom/demo/obj/firewall/addrgrp"
      },
      "url": "cache/search/where/used/start"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```

Step #2: Monitor the task completion using the returned token

```
REQUEST
{
  "id": 1,
  "method": "exec",
  "params": [
    {
      "token": "ng9jCDhg9qZVmUt4oaYPZw==",
      "url": "cache/search/where/used/get/summary"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```

Step #3: Collect the where used result using the returned token

```
REQUEST
{
  "id": 1,
  "method": "exec",
  "params": [
    {
      "token": "ng9jCDhg9qZVmUt4oaYPZw==",
      "url": "cache/search/where/used/get/detail"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```

You can now proceed with the replace operation. To replace grp_002 with grp_001 for policy 3 of policy package pkg_002 in the demo ADOM, you can use the following request:

```
REQUEST
{
  "id": 3,
  "method": "update",
  "params": [
    {
      "url": "/pm/config/adom/demo/pkg/pkg_002/firewall/policy/3",
      "used objs": {
        "attr": [
          "dstaddr"
        ],
        "from": "obj/firewall/addrgrp/grp_002",
        "to": [
          "grp_001"
        ]
      }
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
#### 1.9.13.1. How to find and replace objects in firewall policy?
```

Caught in #0636807.

```
```
REQUEST:

{
  "method": "update",
  "params": [
{
      "target start": 2,
      "url": "pm/config/adom/BusySYSLabFG/pkg/BUSYSYSLABFG_Monitoring/firewall/policy/3",
      "used objs": {
                "from": "obj/firewall/address/192.168.215.157-VCenter",
        "to": [
                    "10.1.0.0/16-IT_BUSY"
                  ]
      }
    }
  ],
  "session": 4131
}
```

```
```
### 1.9.14. Partial installation
```

Caught in #0225600.

This is the template to install any objects:

```
```
REQUEST
{
  "id": 1,
  "method": "exec",
  "params": [
    {
      "data": {
        "adom": "{{adom}}>",
        "scope": [
          {
            "name": "{{device}}",
            "vdom": "{{vdom}}"
          },
          {"...", "..."}
        ],
        "target": [
          "{{target}}"
        ]
      },
      "url": "/securityconsole/install/objects"
    }
  ],
  "session": "{{session}}",
}
```


where:

scope could be omitted, in that case FortiManager will manage to find the devices/vdoms which are using the target object

target is the target object to be install

You declare a target using the usual format.

For instance:

```
```
```
```
# For any objects
/pm/config/adom/<adom>/obj/<fortios cli>
```

```
```
```
# For a firewall policyid
/pm/config/adom/<adom>/pkg/<pkg>/firewall/policy/<policyid>

etc.


More information about the partial install mechanism are given in section Partial Install

#### 1.9.14.1. How to partial install an IPS profile?
##### 1.9.14.1.1. Using the Legacy Partial Install API

See Legacy Partial Install API for more details about the Legacy Partial Install API.

The following example shows how to partial install the ips_sensor_001 IPS profile from the demo ADOM against the dev_001 and dev_002 managed device and their respective root VDOM:

```
REQUEST
{
  "id": 1,
  "method": "exec",
  "params": [
    {
      "data": {
        "adom": "demo",
        "scope": [
          {
            "name": "dev_001",
            "vdom": "root"
          },
          {
            "name": "dev_002",
            "vdom": "root"
          }
        ],
        "target": [
          "/pm/config/adom/demo/obj/ips/sensor/ips_sensor_001"
        ]
      },
      "url": "/securityconsole/install/objects"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
##### 1.9.14.1.2. Using the New Partial Install API
```

See New Partial Install API for more details about the New Partial Install API.

The following example shows how to partial install the ips_sensor_001 IPS profile from the demo ADOM against the dev_001 and dev_002 managed device and their respective root VDOM:

```
```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "data": {
        "adom": "demo",
        "flags": 0,
        "objects": [
          [
            "update",
            "obj/ips/sensor/ips_sensor_001",
            "",
            ""
          ]
        ],
        "scope": [
          {
            "name": "dev_001",
            "vdom": "root"
          },
          {
            "name": "dev_002",
            "vdom": "root"
          }
        ]
      },
      "url": "/securityconsole/install/objects/v2"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
### 1.9.15. How to check for a duplicate object name?
```

Caught in #893698

To check whether an object name is already used, you can use the option duplicate check:

```
"option": [
    "duplicate check"
]
```


For instance, to check whether a firewall address with name host_001 already exists in ADOM dc_amiens:

```
```
REQUEST
{
  "method": "add",
  "id": 1,
  "session": "{{session}}",
  "params": [
    {
      "data": {
```

      },
```
      "url": "/pm/config/adom/dc_amiens/obj/firewall/address/host_001",
      "option": ["duplicate check"]
    }
  ]
}
```


> **Note:**

The method attribute is add

RESPONSE
```
```
## 1.10. Object Revision
```
```
### 1.10.1. How to add an object with an object revision note?

Following example applies to firewall address object type.

It is showing how to add a new firewall address with an object revision note:

```
REQUEST
{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": {
        "color": 4,
        "name": "host_005",
        "subnet": "10.0.0.5/32"
      },
      "revision note": "Initial Revision",
      "url": "/pm/config/adom/dc_amer/obj/firewall/address"
    }
  ],
  "session": "{{ session }}"
}

RESPONSE
```
### 1.10.2. How to update an object with an object revision note?
```

Following example applies to firewall address object type.

It is showing how to update both an existing firewall address and its associated object revision note:

```
```
REQUEST
{
  "id": 3,
  "method": "update",
  "params": [
    {
      "data": {
        "color": 10
      },
      "revision note": "Color changed a second time",
      "url": "/pm/config/adom/dc_amer/obj/firewall/address/host_005"
    }
  ],
  "session": "{{ session }}"
}

RESPONSE
```
### 1.10.3. How to get the object revision notes for a specific object?
```

The following example demonstrates how to retrieve object revision notes for an existing firewall address object.

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/dc_amer/_objrev/obj/firewall/address/host_005"
    }
  ],
  "session": "{{ session }}",
  "verbose": 1
}

RESPONSE
```

This second example shows how to get the object revision notes for the system_template_001 System Template in the demo ADOM:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/demo/_objrev/devprof/system_template_001"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
### 1.10.4. How to delete an object revision?
```

The following example shows how to delete the object revision version 2 for the system_template_001 System Template in the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "delete",
  "params": [
    {
      "url": "/pm/config/adom/demo/_objrev/devprof/system_template_001/2"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
### 1.10.5. How to revert to a specific object revision?
```

The following example applies to the firewall address object type. It demonstrates how to revert an existing firewall address to a specific object revision.

> **Note:**

```
```
REQUEST
{
  "id": 3,
  "method": "replace",
  "params": [
    {
      "data": {
        "color": 4,
        "name": "host_005",
        "subnet": "10.0.0.5/32"
      },
      "revision note": "Reverted from revision 1",
      "url": "/pm/config/adom/dc_amer/obj/firewall/address/host_005"
    }
  ],
  "session": "{{ session }}"
}

RESPONSE
```
## 1.11. Per-device mapping
```

This is a mechanism where FortiManager can push the same object to multiple devices, but with different values.

For instance, you could have the net_branch_lan firewall address to represent the internal network of your remote sites and you would like it to be with the 10.0.1.0/24 for site #1, 10.0.2.0/24 for site #2, etc.

The per-device mapping feature isn’t available for all objects.

> **Note:**

CLI Template could be use to overcome the lack of per-device mapping support.

```
### 1.11.1. Per-device mapping for firewall.address
#### 1.11.1.1. How to get per-device mapping info for a firewall address obejct?

The following example shows how to get the per-device mapping info for the net_branch_lan firewall address from the demo ADOM:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/demo/obj/firewall/address/net_branch_lan/dynamic_mapping"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}
```


> **Note:**

To get the per-device mapping info, you just need to append the dynamic_mapping subtable in the url

RESPONSE
#### 1.11.1.2. How to add a per-device mapping to a firewall address object?

The following example shows how to add a new per-device mapping entry for the dev_002 device and its root VDOM, for the net_branch_lan firewall address from the demo ADOM:

```
REQUEST
{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": {
        "_scope": [
          {
            "name": "dev_002",
            "vdom": "root"
          }
        ],
        "subnet": [
          "10.0.2.0",
          "255.255.255.0"
        ]
      },
      "url": "/pm/config/adom/demo/obj/firewall/address/net_branch_lan/dynamic_mapping"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```

You can add multiple per-device mapping entries in a single request.

The following example add per-device mapping entries for the dev_003 and dev_004 devices and their root VDOM:

```
REQUEST
{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": [
        {
          "_scope": [
            {
              "name": "dev_003",
              "vdom": "root"
            }
          ],
          "subnet": [
            "10.0.3.0",
            "255.255.255.0"
          ]
        },
        {
          "_scope": [
            {
              "name": "dev_004",
              "vdom": "root"
            }
          ],
          "subnet": [
            "10.0.4.0",
            "255.255.255.0"
          ]
        }
      ],
      "url": "/pm/config/adom/demo/obj/firewall/address/net_branch_lan/dynamic_mapping"
    }
  ],
  "session": "{{session}}",
}

RESPONSE
```
#### 1.11.1.3. How to delete a per-device mapping from a firewall address object?
```

The following example shows how to delete the per-device mapping entry for the dev_004 device and its root VDOM, for the net_branch_lan firewall address from the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "delete",
  "params": [
    {
      "url": "/pm/config/adom/demo/obj/firewall/address/net_branch_lan/dynamic_mapping/dev_004/root"
    }
  ],
  "session": "{{session}}"
}

REQUEST
```

You can delete multiple per-device mapping entries in a single request.

The following example delete per-device mapping entries for the dev_003 and dev_002 devices and their root VDOM:

```
REQUEST
{
  "id": 3,
  "method": "delete",
  "params": [
    {
      "url": "/pm/config/adom/demo/obj/firewall/address/net_branch_lan/dynamic_mapping/dev_003/root"
    },
    {
      "url": "/pm/config/adom/demo/obj/firewall/address/net_branch_lan/dynamic_mapping/dev_002/root"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```


<no title>


```
```
# 2. Security Profiles
```

Contents
```
## 1.1. Metadata
### 1.1.1. How to add a metadata?
### 1.1.2. How to delete a metadata?
### 1.1.3. How to rename a metadata?
### 1.1.4. How to assign a metadata to devices?
#### 1.1.4.1. For a single device
#### 1.1.4.2. For multiple devices
### 1.1.5. How to assign metadatas at Model Device creation time?
### 1.1.6. How to unassign a metadata?
### 1.1.7. How to replace assigned device with another one?
### 1.1.8. How to get the metadata mapped to a specific managed device?
### 1.1.9. How to get the value of a metadata for a specific device/vdom?
### 1.1.10. How to set multiple metadatas for one device?
### 1.1.11. How to assign a global metadata?
### 1.1.12. How to get the assignement status for global metadatas?
### 1.1.13. How to Export/Import metadatas?
#### 1.1.13.1. Export
#### 1.1.13.2. Import
## 1.2. Firewall Address
### 1.2.1. How to add a IP Range firewall address?
### 1.2.2. How to add a FQDN firewall address?
## 1.3. Firewall Address Groups
### 1.3.1. How to add a single member?
### 1.3.2. How to delete a single member?
### 1.3.3. How to delete all members?
#### 1.3.3.1. Using the unset method
#### 1.3.3.2. Using the unset attrs
### 1.3.4. How to get firewall addrgrp members along with their details?
## 1.4. Firewall VIP
### 1.4.1. How to add a new Firewall VIP?
### 1.4.2. How to add a new Firewall VIP Group?
## 1.5. Wildcard FQDN
### 1.5.1. How to add a wildcard FQDN?
## 1.6. Normalized Interfaces
### 1.6.1. How to create a normalized interface?
### 1.6.2. How to add a new per-platform mapping to an existing Normalized Interface?
### 1.6.3. How to get the normalized interfaces mapped to a specific managed device?
### 1.6.4. How to delete an existing per-platform mapping?
## 1.7. Internet Service Objects
### 1.7.1. How to get the regions that can be used in a Geographic Based Internet Service object?
### 1.7.2. How to get the countries that can be used in a Geographic Based Internet Service object?
### 1.7.3. How to get the cities that can be used in a Geographic Based Internet Service object?
### 1.7.4. How to get the list of Internet Service objects?
### 1.7.5. How to get the entries of an Internet Service object?
### 1.7.6. How to get the list of Internet Service FQDN objects?
## 1.8. Replacement Message Group
### 1.8.1. How to get the default Replacement Message Groups?
## 1.9. Objects Operations
### 1.9.1. How to reference objects when names have special characters?
### 1.9.2. Objects default values
#### 1.9.2.1. How to get the default values for a firewall address?
### 1.9.3. How to bulk add objects?
#### 1.9.3.1. params multi-plexing
#### 1.9.3.2. data multi-plexing
### 1.9.4. How to get CLI configuration of a new object?
### 1.9.5. How to get the full ADOM database objects syntax?
### 1.9.6. Cloning objects
#### 1.9.6.1. How to clone a firewall address?
### 1.9.7. How to copy objects?
### 1.9.8. Filtering objects
#### 1.9.8.1. The contain operator
#### 1.9.8.2. How to filter firewall address according to their IPs?
##### 1.9.8.2.1. Retrieve all firewall address objects matching a specific IP subnet
##### 1.9.8.2.2. Retrieve all firewall address objects that strictly match an IP address or subnet
##### 1.9.8.2.3. Retrieve all firewall address subnets matching a specific IP address
##### 1.9.8.2.4. Retrieve all firewall address ranges containing a specific IP address
##### 1.9.8.2.5. Retrieve all firewall address subnets or ranges matching an IP address
##### 1.9.8.2.6. Retrieve all firewall addresses with a per-device mapping, where the subnet or range matches a specific IP address
##### 1.9.8.2.7. Retrieve all firewall address subnets or ranges matching a specific IP address including in their per-device mapping entries
#### 1.9.8.3. How to get the Last Modified timestamp?
#### 1.9.8.4. How to filter on the Last Modified timestamp?
#### 1.9.8.5. The like operator
#### 1.9.8.6. How to delete multiple objects?
### 1.9.9. Used/Unused objects
#### 1.9.9.1. How to know whether a specific object is used?
#### 1.9.9.2. How to get the list of used objects?
#### 1.9.9.3. How to get unused objects?
### 1.9.10. Where Used
#### 1.9.10.1. How to where used from the global adom?
#### 1.9.10.2. How to where used from within a normal ADOM?
#### 1.9.10.3. How to where used only for direct object usage?
### 1.9.11. Find duplicates objects
### 1.9.12. Merge objects
#### 1.9.12.1. How to merge firewall addresses?
### 1.9.13. Find and Replace
#### 1.9.13.1. How to find and replace objects in firewall policy?
### 1.9.14. Partial installation
#### 1.9.14.1. How to partial install an IPS profile?
##### 1.9.14.1.1. Using the Legacy Partial Install API
##### 1.9.14.1.2. Using the New Partial Install API
### 1.9.15. How to check for a duplicate object name?
## 1.10. Object Revision
### 1.10.1. How to add an object with an object revision note?
### 1.10.2. How to update an object with an object revision note?
### 1.10.3. How to get the object revision notes for a specific object?
### 1.10.4. How to delete an object revision?
### 1.10.5. How to revert to a specific object revision?
## 1.11. Per-device mapping
### 1.11.1. Per-device mapping for firewall.address
#### 1.11.1.1. How to get per-device mapping info for a firewall address obejct?
#### 1.11.1.2. How to add a per-device mapping to a firewall address object?
#### 1.11.1.3. How to delete a per-device mapping from a firewall address object?


ClickSend's MCP server now lets you trigger SMS with natural language. Find out more.
