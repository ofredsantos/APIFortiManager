```
```
# 6. FortiGuard Management
```

}

RESPONSE
```
## 6.3. How to get the FMG upstream servers list?

It’s quite easy to expose the FortiManager JSON RPC API endpoints by debugging the fdssvrd process while issuing the FortiManager CLI command:

diagnose fmupdate view-serverlist <fgd|fds>


To debug the fdssvrd process:

```
diagnose debug application fdssvrd 255
diagnose debug enable
diagnose debug timestamp enable
```


Then we can ask for the upstream FDS servers using the following command:

diagnose fmupdate view-serverlist fds


Following output should be displayed:

2022-03-22 23:06:12 Request:
2022-03-22 23:06:12 { "client": "-newcli:22493", "id": 4, "method": "get", "params": [{ "data": { "flags": 0}, "target start": 1, "url": "misc\/server_list"}], "root": "um"}
2022-03-22 23:06:12 Response:
2022-03-22 23:06:12 { "id": 4, "result": [{ "data": { "loose_mode": 1, "public_network": 1, "server_list": [{ "0": { "addr": "208.184.237.67", "distance": 1, "port": 443, "src": 4, "timezone": 0}, "1": { "addr": "12.34.97.16", "distance": 6, "port": 443, "src": 4, "timezone": -5}, "2": { "addr": "208.184.237.68", "distance": 8, "port": 443, "src": 4, "timezone": 9}, "3": { "addr": "208.184.237.66", "distance": 9, "port": 443, "src": 4, "timezone": -8}, "4": { "addr": "usfds1.fortinet.com", "distance": 0, "port": 443, "src": 2, "timezone": 1}, "count": 5, "curr_svr_index": 3, "service_type": "fds"}, { "0": { "addr": "208.184.237.75", "distance": 9, "port": 443, "src": 4, "timezone": -8}, "1": { "addr": "usforticlient.fortinet.net", "distance": 0, "port": 443, "src": 2, "timezone": 1}, "count": 2, "curr_svr_index": 0, "service_type": "fct"}, { "0": { "addr": "65.210.95.253", "distance": 6, "port": 443, "src": 4, "timezone": -5}, "1": { "addr": "usfqsvr.fortinet.net", "distance": 0, "port": 443, "src": 2, "timezone": 1}, "count": 2, "curr_svr_index": 1, "service_type": "geoip"}]}, "status": { "code": 0, "message": "OK"}, "url": "misc\/server_list"}]}
2022-03-22 23:06:12
Fortiguard Server Comm : Enabled
Server Override Mode   : Loose
FDS   server list      :
Index   Address                    Port            TimeZone        Distance        Source
------------------------------------------------------------------------------------------------------
 0      208.184.237.67             443             0               1               FDNI
 1      12.34.97.16                443             -5              6               FDNI
 2      208.184.237.68             443             9               8               FDNI
*3      208.184.237.66             443             -8              9               FDNI
 4      usfds1.fortinet.com        443             1               0               DEFAULT

FCT   server list      :
Index   Address                    Port            TimeZone        Distance        Source
------------------------------------------------------------------------------------------------------
*0      208.184.237.75             443             -8              9               FDNI
 1      usforticlient.fortinet.net 443             1               0               DEFAULT

GEOIP server list      :
Index   Address                    Port            TimeZone        Distance        Source
------------------------------------------------------------------------------------------------------
 0      65.210.95.253              443             -5              6               FDNI
*1      usfqsvr.fortinet.net       443             1               0               DEFAULT


When formatted and cleaned a bit, we can see the following FortiManager JSON RPC API exchange:

```
REQUEST:

{
  "id": 4,
  "method": "get",
  "params": [
    {
      "data": {
        "flags": 0
      },
      "url": "/um/misc/server_list"
    }
  ],
}


RESPONSE:

{
  "id": 4,
  "result": [
    {
      "data": {
        "loose_mode": 1,
        "public_network": 1,
        "server_list": [
          {
            "0": {
              "addr": "208.184.237.67",
              "distance": 1,
              "port": 443,
              "src": 4,
              "timezone": 0
            },
            "1": {
              "addr": "12.34.97.16",
              "distance": 6,
              "port": 443,
              "src": 4,
              "timezone": -5
            },
            "2": {
              "addr": "208.184.237.68",
              "distance": 8,
              "port": 443,
              "src": 4,
              "timezone": 9
            },
            "3": {
              "addr": "208.184.237.66",
              "distance": 9,
              "port": 443,
              "src": 4,
              "timezone": -8
            },
            "4": {
              "addr": "usfds1.fortinet.com",
              "distance": 0,
              "port": 443,
              "src": 2,
              "timezone": 1
            },
            "count": 5,
            "curr_svr_index": 3,
            "service_type": "fds"
          },
          {
            "0": {
              "addr": "208.184.237.75",
              "distance": 9,
              "port": 443,
              "src": 4,
              "timezone": -8
            },
            "1": {
              "addr": "usforticlient.fortinet.net",
              "distance": 0,
              "port": 443,
              "src": 2,
              "timezone": 1
            },
            "count": 2,
            "curr_svr_index": 0,
            "service_type": "fct"
          },
          {
            "0": {
              "addr": "65.210.95.253",
              "distance": 6,
              "port": 443,
              "src": 4,
              "timezone": -5
            },
            "1": {
              "addr": "usfqsvr.fortinet.net",
              "distance": 0,
              "port": 443,
              "src": 2,
              "timezone": 1
            },
            "count": 2,
            "curr_svr_index": 1,
            "service_type": "geoip"
          }
        ]
      },
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "misc/server_list"
    }
  ]
}


REQUEST:


RESPONSE:
```


## 6.4. Firmware Management
### 6.4.1. How to get the list of firmware images for FortiGate device?

It is to get the same list as the one you get when visiting the FortiGuard > Firmware Images:

Following example shows how to get the list of fimware images for the FortiGate-60F platform:

```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "data": {
        "flags": 1,
        "platform": "FortiGate-60F",
        "product": "FGT"
      },
      "url": "/um/image/version/list"
    }
  ],
  "session": "{{session}}",
}

RESPONSE
```

Should you want to get the firmware images for all FortiGate device? Just omit the platform attribute and keep the product one set with FGT:

```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "data": {
        "flags": 1,
        "product": "FGT"
      },
      "url": "/um/image/version/list"
    }
  ],
  "session": "{{session}}",
}
```


You can also get the firmware images for the following procuct:

Name

	

product


FortiGate

	

FGT


FortiAnalyzer

	

FAZ


FortiManager

	

FMG


FortiAP

	

FAP


FortiExtender

	

FXT


FortiSwitch

	

FSW


FortiProxy

	

FPX

If you omit both the platform and the product attributes, then you will get the firmware images list for all platforms/products!

> **Note:**

FortiManager indicates in the output when the firmware image has been already downloaded:

```
RESPONSE
{
  "bdate": "2304132147",
  "image_type": "NA",
  "objid": "06002000FIMG00259-00002.00014-2304132147",
  "type": "GA",
  "version": "6.2.14-b1364"
},
{
  "bdate": "2312230056",
  "image_path": "/var/fwm/image/FGT40F_7.4.2_b2571_FORTINET.out",
  "image_size": 81475306,
  "image_type": "F",
  "objid": "07004000FIMG00259-00004.00002-2312230056",
  "type": "GA",
  "version": "7.4.2-b2571"
},
```


> **Note:**

In the above response snipet, you can see that build 6.2.14 is still in the public FortiGuard servers while the build 7.4.2 has already been download in FortiManager.

### 6.4.2. How to download a firmware image?

The following example shows hot to download the firmware image for the FortiOS version 7.0.1 build 0489 and the FortiGate-100F platform:

```
REQUEST
{
  "id": 1,
  "method": "exec",
  "params": [
    {
      "data": {
        "create_task": "enable",
        "platform": "FortiGate-100F",
        "version": "7.0.11-b0489-GA"
      },
      "url": "/um/image/download"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
## 6.5. How to get contracts for managed devices?
```

There are multiple ways to obtain more or less the same thing: the list of contracts or entitlements associated with the managed devices.

```
### 6.5.1. Using /um/device/list

The following example shows how to get the contracts for all managed devices:

```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "url": "/um/device/list"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```

For instance, the following example shows how to get the contracts for the managed device with the FG421F0000000001 Serial Number:

```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "data": {
        "serial": "FG421F0000000001"
      },
      "url": "/um/device/list"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```

Or the following example shows how to get the contracts for all managed FortiGate units (i.e., the ones with the FortiOS operating system type os_type is 0):

```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "data": {
        "os_type": 0,
      },
      "url": "/um/device/list"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```

> **Tip:**

Where is the 0 value from for the os_type?

It’s in the file /var/dm/syntax/dvmcmd_syntax.json

Existing values are:

```
"OS_TYPE_OPTIONS": {
  "unknown": -1,
  "fos": 0,
  "fsw": 1,
  "foc": 2,
  "fml": 3,
  "faz": 4,
  "fwb": 5,
  "fch": 6,
  "fct": 7,
  "log": 8,
  "fmg": 9,
  "fsa": 10,
  "fdd": 11,
  "fac": 12,
  "fpx": 13,
  "fna": 14
}
```


You cannot use the symbolic form: for instance you can’t use fos instead of 0

### 6.5.2. Using /um/misc/dump_contract

The following example shows how to get the contracts for all managed devices:

```
REQUEST
{
  "id": 1,
  "method": "exec",
  "params": [
    {
      "data": {
        "flags": 0,
      },
      "url": "/um/misc/dump_contract"
    }
  ],
}

RESPONSE
```

The following example shows how to get the contracts for the managed device with the FG421F0000000001 Serial Number:

```
REQUEST
{
  "id": 1,
  "method": "exec",
  "params": [
    {
      "data": {
        "flags": 0,
        "serial": "FG421F0000000001"
      },
      "url": "/um/misc/dump_contract"
    }
  ],
}

RESPONSE
Click here to interpret a different but similar output
```
## 6.6. How to get the package versions for your managed devices?
```

Here package means IPS, AV, Applications, etc. databases that are used by your managed devices.

The following example shows how to get the package versions for all your managed devices:

```
```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "data": {
        "flags": 0
      },
      "url": "/um/device/object"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```

The following example shows how to get the package versions for the managed device with the FG421F0000000001 Serial Number:

```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "data": {
        "flags": 0,
        "serial": "FG421F0000000001"
      },
      "url": "/um/device/object"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
## 6.7. How to get the license status for managed devices?
```

This is more or less what you’re trying to achieve in How to get contracts for managed devices? or in How to get the package versions for your managed devices? by using data collected by the FortiManager.

However, it doesn’t seem to giver you the full list of contracts, packages name and versions.

The following example is getting the license status from the managed devices themselves:

```
```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "data": {
        "action": "get",
        "resource": "/api/v2/monitor/license/status",
        "target": [
          "adom/demo/group/All_FortiGate"
        ]
      },
      "url": "sys/proxy/json"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
## 6.8. How to get the update history for a specific FortiGuard objects?
```

The update history gives you how many time and which database versions a FortiGuard object has been downloaded by FortiManager.


In this case, you get this:

The following shows the corresponding API request:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "data": {
        "category": {
          "fds": {
            "objid": [
              "05000000FAPV00000"
            ]
          }
        }
      },
      "url": "/um/misc/update_history"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
## 6.9. How to get the list of FortiGuard objects downloaded by FortiManager?
```

Goal is to produce the same listing as the one available in FortiManager GUI when visiting the FortiGuard > Package Management > Receive Status page.

We need to use the following method and url:

Method

	

get


URL

	

/um/object/list

We need to specify the Fortinet product of interest by using the system attribute with one of the following values:

Attribute

	

Product


FGT

	

FortiGate


FML

	

FortiMail


FAZ

	

FortiAnalyzer


FWB

	

FortiWeb


FCT

	

FortiClient

We also need to specify whether we want to get all objects related to a product or only the used objects by setting the attribute used_only to 0 or 1 respectively.

The FortiManager JSON API request/response:

```
```
REQUEST:

{
  "id": 1,
  "jsonrpc": "1.0",
  "method": "get",
  "params": [
    {
      "data": {
        "system": "FGT",
        "used_only": 0
      },
      "url": "/um/object/list"
    }
  ],
  "session": "hdRJAukKyAHEw+I6bZcn0wxxeWWBYDSOU6kq2aYvMgWOQJMBvo+YwdRonWgie93RF/80VgAUcTMNp7nLPIO/FVOCg3J7QFF8",
  "verbose": 1
}


RESPONSE:

            {
              "id": 1,
              "result": [
                {
                  "data": {
                    "object_list": {
                      "05000000IPGE00000": {
                        "latest_verdate": "2002080500",
                        "latest_version": 131120,
                        "latest_versize": 1080752,
                        "obj_desc": "IP Geo DB",
                        "obj_used": 0,
                        "objid": "05000000IPGE00000",
                        "prefer_version": 0,
                        "version_list": {
                          "00002.00048": {
                            "date": "2002080500",
                            "size": 1080752,
                            "version": 131120
                          }
                        }
                      },
                      "05004000NIDS02200": {
                        "latest_verdate": "2003102346",
                        "latest_version": 983833,
                        "latest_versize": 369848,
                        "obj_desc": "IPS Meta-Data",
                        "obj_used": 0,
                        "objid": "05004000NIDS02200",
                        "prefer_version": 0,
                        "version_list": {
                          "00015.00793": {
                            "date": "2003102346",
                            "size": 369848,
                            "version": 983833
                          }
                        }
                      },
                      "05004000NIDS02300": {
                        "latest_verdate": "2003102346",
                        "latest_version": 983833,
                        "latest_versize": 78128,
                        "obj_desc": "AppCat Meta-Data",
                        "obj_used": 0,
                        "objid": "05004000NIDS02300",
                        "prefer_version": 0,
                        "version_list": {
                          "00015.00793": {
                            "date": "2003102346",
                            "size": 78128,
                            "version": 983833
                          }
                        }
                      }
                    },
                    "system": "FGT",
                    "used_only": 0
                  },
                  "status": {
                    "code": 0,
                    "message": "OK"
                  },
                  "url": "/um/object/list"
                }
              ]
}
```

```
```
## 6.10. How to export/import FortiGuard objects?
```

Caught in #077802 (FortiManager 7.2.2).

These export/import operations were implemented to enable an air-gapped FortiManager to receive FortiGuard updates automatically.

For example, they can be used in a typical data-diode (OT environment) scenario:

INTERNET + FMG1 + DEVOPS ---- [data-diode >>>] ---- FMG2 + managed devices


where:

INTERNET represents the public FortiGuard servers.

FMG1 is the FortiManager instance connected to the Internet to retrieve FortiGuard objects.

DEVOPS is an external system capable of triggering FortiManager JSON RPC API operations.

The data-diode allows traffic to flow only from left to right.

FMG2 is the air-gapped FortiManager that cannot access public FortiGuard servers and manages FortiGate devices internally.

In this setup, the DEVOPS system can:

Use the FortiManager API to export FortiGuard objects from FMG1.

Use the FortiManager API to import FortiGuard objects into FMG2.

Traffic from DEVOPS to FMG2 is permitted by the data-diode since it flows in the allowed left-to-right direction.

```
### 6.10.1. How to export a FortiGuard Object?

To export a FortiGuard object, you need to know its objid.

This is what is showing up in the FortiManager GUI when you navigate to FortiGuard > Package > Receive Status:

> **Note:**

You can also obtain a list of available FortGuard objects via the FortiManager JSON RPC API (see section How to get the list of FortiGuard objects downloaded by FortiManager?).

To export 06002000NIDS02400 (Signature Meta Data (IPS Regular)) FortiGuard Object:

```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "data": {
        "category": {
          "fds": {
            "objid": [
              "06002000NIDS02400"
            ]
          }
        },
        "flags": "base64"
      },
      "url": "/um/object/export"
    }
  ],
  "session": "{{session}}"
}
```


> **Note:**

The objid attribute is a list; you could pass muliple FortiGuard objects

The base64 value for the flags attribute is required if you want to get the requested FortiGuard objects returned in base64 format in the API response.

If the flags attribute is omitted, FortiGuard objects will be placed in the FortiManager filesystem (in folder /var/tmp/um/export)

RESPONSE

Starting with FortiManager 8.0.0 (#1125122), the export has been improved in term of flexibility with the addition of the filter attribute. You can now export specific FortiGuard objects based on different criteria: by system (e.g. FGT, FCT, etc) or by version.

For instance, if you want to export all FortiGuard objects, you can use following example:

```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "data": {
        "category": {
          "fds": {
            "filter": {
              "export-all": 1
            }
          }
        },
        "flags": "base64"
      },
      "url": "/um/object/export"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```

You can also export FortiGuard objects based on their system and version. The following example exports all FortiGuard objects for FortiGate systems with version 7.6 and 7.4 and for FortiClient systems regardless of their version:

```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "data": {
        "category": {
          "fds": {
            "filter": {
              "system": {
                "FCT": [],
                "FGT": [
                  "7.6",
                  "7.4"
                ]
              }
            }
          }
        },
        "flags": "base64"
      },
      "url": "/um/object/export"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```

You can also export FortiGuard objects based on their object type and version as shown in the below example:

```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "data": {
        "category": {
          "fds": {
            "filter": {
              "object": [
                {
                  "objid": "07002000NIDS02600",
                  "version": [
                    "34.89",
                    "34.90"
                  ]
                },
                {
                  "objid": "07004000APDB00100",
                  "version": [
                    "all"
                  ]
                },
                {
                  "objid": "07004000SFAS00000"
                }
              ]
            }
          }
        },
        "flags": "base64"
      },
      "url": "/um/object/export"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```

You can also explore the other flags delta and only that you can see as available options when using:

fmupdate ftp fds-export ?


and shows their corresponding API form by enabling debug in FortiManager:

```
diagnose debug application fdssvrd 255
diagnose debug enable
```

### 6.10.2. How to import a FortiGuard Object?

To import a FortiGuard object, you need to pass the base64 output you obtain at the time your exported it (see section How to export a FortiGuard Object?):

```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "data": {
        "base64": "UFVURjA0MDAwMDAwAwAAAHiZEABAAAAAMj[...]",
      }
      },
      "url": "/um/object/import"
    }
  ],
  "session": "{{session}}"
}
```


> **Note:**

The base64 attribute is set with the base64 output of one or multiple FortiGuard objects

RESPONSE

> **Hint:**

If you want to control the effectiveness of the import operation for the FortiGuard Object with objid 06002000NIDS02400, you can perform the following operation:

Check this FortiGuard object exists using FortiManager CLI

Enter:

diagnose fmupdate list-object fds 06002000/NIDS02400


You should get this output:

06002000/NIDS02400
06002000/NIDS02400/00026.00713-2401110136


Export the FortiGuard object to save it in an external system

See How to export a FortiGuard Object?

Delete the FortiGuard object using FortiManager CLI

Enter:

fmupdate del-object fds 06002000/NIDS02400


You should get this output:

06002000/NIDS02400
06002000/NIDS02400/00026.00713-2401110136

This operation will delete all fds 06002000/NIDS02400 objects.
Do you want to continue? (y/n)


Enter y then ENTER to confirm the delete operation

Check this FortiGuard object does no longer exist using FortiManager CLI

Enter:

diagnose fmupdate list-object fds 06002000/NIDS02400


You should get this output:

no object was found for service "fds" by type "06002000/NIDS02400".
Command fail. Return code -9999


Import the FortiGuard Object as described in this section

Check this FortiGuard object is back using FortiManager CLI

Enter:

diagnose fmupdate list-object fds 06002000/NIDS02400


You should get this output:

06002000/NIDS02400
06002000/NIDS02400/00026.00713-2401110136

## 6.11. How to export/import Entitlement?

Caught in #0778029.

TBD.

## 6.12. Local External Resources

Starting with FortiManager 7.4.1 and 7.2.5 (#0934664), it is possible to manage External Threat Feeds using Local External Resources files hosted by FortiManager.

> **Note:**

The following url is used in this section:

/pm/config/global/_external/resource


This refers to the Global ADOM for convenience. Alternatively, you can use:

/pm/config/adom/<adom>/_external/resource


Both forms yield the same result. External resource files are accessible to all ADOMs.

### 6.12.1. How to add a local external resource?
#### 6.12.1.1. Using FortiManager JSON RPC API for adding a local external resource

The following example shows how to add the local_external_resource_001.txt local external resource:

```
REQUEST
{
  "method": "set",
  "params": [
    {
      "url": "/pm/config/global/_external/resource/local_external_resource_001.txt",
      "data": {
        "content": "10.0.0.1\n10.0.0.2\n10.0.0.3\n"
      },
      "session": "{{session}}"
    }
  ]
}

RESPONSE
```
#### 6.12.1.2. Using REST API for adding a local external resource
```

The following example shows how to add the local_external_resource_002.txt local external resource file:

```
```
REQUEST
curl -sk -u devops:fortinet -X PUT \
https://10.210.35.112/jsonrpc/pm/config/global/_external/resource/local_external_resource_002.txt \
--data-binary @local_external_resource_002.txt | jq
```


> **Note:**

File local_external_resource_002.txt is with following content:

10.0.0.1
10.0.0.2
10.0.0.3
10.0.0.4
10.0.0.5

RESPONSE
```
```
### 6.12.2. How to get the list of local external resources?
```

Caught in #0953203 (7.2.5/7.4.2).

```
#### 6.12.2.1. Using FortiManager JSON RPC API for getting the list of local external resources

The following example shows how to get the list of local external resources:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "pm/config/global/_external/resource"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
#### 6.12.2.2. Using REST API for getting the list of local external resources
```

The following example shows how to get the list of local external resources:

```
```
REQUEST
curl -sk -u devops:fortinet -X GET \
https://10.210.35.112/jsonrpc/pm/config/global/_external/resource | jq

REQUEST
```
### 6.12.3. How to get the content of a local external resource?
#### 6.12.3.1. Using FortiManager JSON RPC API for getting the content of a local external resource
```

The following example shows how to retrieve the content of the local_external_resource_001.txt local external resource:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "pm/config/global/_external/resource/local_external_resource_001.txt"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
#### 6.12.3.2. Using REST API for getting the content of a local external resource
```

The following example shows how to retrieve the content of the local_external_resource_002.txt local external resource:

```
```
REQUEST
curl -sk -u devops:fortinet -X GET \
https://10.210.35.112/jsonrpc/pm/config/global/_external/resource/local_external_resource_002.txt

REQUEST
```
### 6.12.4. How to replace the entire content of a local external resource?
#### 6.12.4.1. Using FortiManager JSON RPC API for replacing the content of a local external resource
```

The example below shows how to replace the content of the local_external_resource_001 local external resource:

```
```
REQUEST
{
  "id": 3,
  "method": "set",
  "params": [
    {
      "data": {
        "content": "10.1.0.1\n10.1.0.2\n10.1.0.3\n"
      },
      "url": "pm/config/global/_external/resource/local_external_resource_001.txt"
    }
  ],
  "session": "{{session}}"
}
```


> **Note:**

You just need to reapply the API call used when you created that local external resource (see How to add a local external resource?) but with a new content block.

RESPONSE
```
```
#### 6.12.4.2. Using REST API for replacing the content of a local external resource
```

The example below shows how to replace the content of the local_external_resource_002 local external resource:

```
```
REQUEST
curl -sk -u devops:fortinet -X PUT \
https://10.210.34.120/jsonrpc/pm/config/global/_external/resource/local_external_resource_002.txt \
--data-binary @local_external_resource_002.txt | jq
```


> **Note:**

You just need to reapply the API call used when you created that local external resource (see How to add a local external resource?) but with a new content block.

RESPONSE
```
```
### 6.12.5. How to delete a local external resource?
```
```
#### 6.12.5.1. Using FortiManager JSON RPC API for deleting a local external resource

The example below shows how to replace the content of the local_external_resource_002.txt local external resource:

```
REQUEST
curl -sk -u devops:fortinet -X DELETE \
https://10.210.35.112/jsonrpc/pm/config/global/_external/resource/local_external_resource_002.txt \
| jq

RESPONSE
```

The following example shows how to delete the local external resource named local_external_resource_001.txt:

```
REQUEST
{
  "method": "delete",
  "params": [
    {
      "url": "/pm/config/global/_external/resource/local_external_resource_001.txt",
      "session": "{{session}}"
    }
  ]
}

RESPONSE
```
#### 6.12.5.2. Using REST API for deleting a local external resource
```

The following example shows how to delete the local external resource named local_external_resource_002.txt:

```
```
REQUEST
curl -sk -u devops:fortinet -X DELETE \
https://10.210.35.112/jsonrpc/pm/config/global/_external/resource/local_external_resource_002.txt \
| jq

RESPONSE
```
## 6.13. Remote External Resources
```

Starting in version 7.6.3 (#1039834), FortiManager supports downloading external resources from a web server.

Once downloaded by FortiManager, the file becomes a local external resource.

```
### 6.13.1. How to add a remote external resource?

The following example shows how to add a remote external resource file named remote_external_resource_001:

```
REQUEST
{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": {
        "http_auth": 0,
        "name": "remote_external_resource_001",
        "refresh_rate": 5,
        "status": 1,
        "url": "http://www.url-001.com/filename_001.txt",
        "use_web_proxy": 0
      },
      "url": "/um/external_resource"
    }
  ],
  "session": "{{session}}",
}
```


> **Note:**

http_auth: 0: No authentication is required to access the URL.

refresh_rate: 5: FortiManager will check the URL and refresh the file every 5 minutes.

use_web_proxy: 0: FortiManager will access the URL directly, without using a proxy.

RESPONSE
### 6.13.2. How to get the existing remote external resources?

The following example shows how to get the list of existing remote external resources:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/um/external_resource"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
### 6.13.3. How to delete a remote external resource?
```

The following example shows how to delete the remote_external_resource_001:

```
```
REQUEST
{
  "id": 3,
  "method": "delete",
  "params": [
    {
      "data": {
        "name": "foobar"
      },
      "url": "/um/external_resource"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
### 6.13.4. How to check for an external resource?
```

Caught in #1140702.

The capability of FortiManager to fetch a remote external resource can be validated using the FortiManager API to check the corresponding URL.

The example below describes how to check for an URL prior to set it in a remote external resource:

```
```
REQUEST
{
  "id": 3,
  "method": "exec",
  "params": [
    {
      "data": {
        "opt": "check_url",
        "url": "http:/www.url-003.com"
      },
      "url": "/um/external_resource"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```


```
```
# 5. Connector Management
```


```
# 1. FortiManager operations