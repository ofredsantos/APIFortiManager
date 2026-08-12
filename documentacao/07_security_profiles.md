```
```
# 2. Security Profiles

```
"params": [
    {
      "data": [
        {
          "url": "www.url-002.com"
        },
        {
          "url": "www.url-003.com"
        },
        {
          "url": "www.url-004.com"
        }
      ],
      "url": "/pm/config/adom/demo/obj/webfilter/urlfilter/1/entries"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
#### 2.1.1.3. How to replace the entire list of webfilter.urlfilter.entries?
```

Sometimes, you receive a new list of URLs and don’t want to go through the tedious process of comparing which ones are present or missing from your existing webfilter.urlfilter.entries, then updating accordingly.

It is much simpler and faster to just ignore the existing webfilter.urlfilter.entries list and replace it with the new one.

The example below shows how to replace the contents of the webfilter.urlfilter.entries sub-table of the URL Filter with ID 1 in the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "set",
  "params": [
    {
      "data": {
        "entries": [
          {
            "action": "block",
            "url": "www.host-001.com"
          },
          {
            "action": "block",
            "url": "www.host-002.com"
          },
          {
            "action": "block",
            "url": "www.host-003.com"
          },
          {
            "action": "block",
            "url": "www.host-004.com"
          },
          {
            "action": "block",
            "url": "www.host-005.com"
          },
          {
            "action": "block",
            "url": "www.host-006.com"
          }
        ]
      },
      "revision note": "URL List v20250607-002.",
      "url": "pm/config/adom/demo/obj/webfilter/urlfilter/1"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
#### 2.1.1.4. How to delete an entry in a webfilter.urlfilter.entries?
```

Goal is to delete an existing entry without overwritting the existing ones.

To delete entry www.url-003.com with ID 4, in the webfilter.urlfilter named urlfilter_001, with ID 1, in ADOM dc_emea:

```
```
REQUEST:

{
  "id": 3,
  "method": "delete",
  "params": [
    {
      "url": "/pm/config/adom/dc_emea/obj/webfilter/urlfilter/1/entries/4"
    }
  ],
  "session": "GcpTJdkN8A0VwkAQF+zBA70wdh7B+Qe3tZoGil4lR+rQlrUhy0nOjNeoJLKyQb/CgdXmuA8i5omm4WV/dE7cQw=="
}
```


> **Note:**

The webfilter.urlfilter urlfilter_001 cannot be used as master key; its ID 1 has to be used instead

The webfilter.urlfilter.entries www.url-003.com cannot be used as a master key; its ID 4 has to be used instead.

```
RESPONSE:

{
  "id": 3,
  "result": [
    {
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/dc_emea/obj/webfilter/urlfilter/1/entries/3"
    }
  ]
}
```

```
```
### 2.1.2. Web rating overrides
```

This section is for the webfilter.ftgd-local-rating objects.

```
#### 2.1.2.1. How to add a new web rating override?

To add a new web rating override in ADOM dc_amer:

```
REQUEST:

{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": {
        "comment": "Test #003",
        "rating": [
          "96"
        ],
        "status": "enable",
        "url": "www.url-003.com"
      },
      "url": "/pm/config/adom/dc_amer/obj/webfilter/ftgd-local-rating"
    }
  ],
  "session": "6vRSrzLBbOj1JB0thRDB1/dzUETGtibb3oohHEPXs+ppbcq99CkWp33QZLWPwd9rmYgeRXYozeXNSLjUIb6pjQ=="
}


RESPONSE:

{
  "id": 3,
  "result": [
    {
      "data": {
        "url": "www.url-003.com"
      },
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/pm/config/adom/dc_amer/obj/webfilter/ftgd-local-rating"
    }
  ]
}
```

### 2.1.3. Webfilter profile

This section is for operating the webfilter profile object.

#### 2.1.3.1. How to add a new filter in a webfilter profile?

filter wording is used because of the CLI syntax used to add a new category and its corresponding action. You have to update a table named filters as shown below:

CLI syntax for a webfilter profile filter
```
config webfilter profile
    edit <wfp_name>
        config ftgd-wf

            config filters

                edit <filter>

                    set category <id>

                    set action <action>

                next

            end

        end
    next
end
```


The following example shows how to add the wfp_001 webfilter profile in the demo ADOM. It will block web traffic to URLs categorized as Web-based Applications (i.e. category ID is 84):

```
REQUEST
{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": {
        "action": "block",
        "category": 84
      },
      "url": "/pm/config/adom/demo/obj/webfilter/profile/wfp_001/ftgd-wf/filters"
    }
  ],
  "session": "{{session}}"
}
```


> **Note:**

See section How to get the webfilter categories? for how to get the category ID used in the attribute category

RESPONSE
pyFMG
#### 2.1.3.2. How to get existing filters in a webfilter profile?

The following example shows how to get the configured filters for the wfp_001 in the demo ADOM:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/demo/obj/webfilter/profile/wfp_001/ftgd-wf/filters"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
pyFMG
```

In the above example, the information you’re getting from the existing filters isn’t very meaningful: action is quite explicit, but you don’t get the symbolic name associated with the returned category…

The following example shows how to obtain a more meaningful output by leveraging the expand datasrc mechaism:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "expand datasrc": [
        {
          "datasrc": [
            {
              "obj type": "webfilter categories"
            }
          ],
          "name": "category"
        }
      ],
      "url": "/pm/config/adom/demo/obj/webfilter/profile/wfp_001/ftgd-wf/filters"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
pyFMG
```
#### 2.1.3.3. How to update an existing filter in a webfilter profile?
```

Goal is to change the action attribute value of an webfilter profile filter.

The following example shows how to update the action, for the Potentially Unwanted Program category, from block to warning in the wfp_001 webfilter profile of the demo ADOM:

Current action is block:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "expand datasrc": [
        {
          "datasrc": [
            {
              "obj type": "webfilter categories"
            }
          ],
          "name": "category"
        }
      ],
      "url": "/pm/config/adom/demo/obj/webfilter/profile/wfp_001/ftgd-wf/filters/33"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}
```


> **Note:**

How do you know that you have to use the 33 ID for the filter entry? See ref:How to get existing filters in a webfilter profile?

RESPONSE
pyFMG

Change it to warning:

```
REQUEST
{
  "id": 3,
  "method": "set",
  "params": [
    {
      "data": {
        "action": "warning"
      },
      "url": "/pm/config/adom/demo/obj/webfilter/profile/wfp_001/ftgd-wf/filters/33"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
pyFMG
```

After the change, action is warning:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "expand datasrc": [
        {
          "datasrc": [
            {
              "obj type": "webfilter categories"
            }
          ],
          "name": "category"
        }
      ],
      "url": "/pm/config/adom/demo/obj/webfilter/profile/wfp_001/ftgd-wf/filters/33"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
#### 2.1.3.4. How to update multiple filters in a webfilter profile?
```

Goal is to change the action attribute values of multiple webfilter profile filters.

The following example shows how to set the action, for the Potentially Unwanted Program and Web-based Applications categories, to monitor in the wfp_001 webfilter profile of the demo ADOM:

Current action are warning and block respectively:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "expand datasrc": [
        {
          "datasrc": [
            {
              "obj type": "webfilter categories"
            }
          ],
          "name": "category"
        }
      ],
      "filter": [
        "id",
        "in",
        33,
        34
      ],
      "url": "/pm/config/adom/demo/obj/webfilter/profile/wfp_001/ftgd-wf/filters"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
pyFMG
```

Change them to warning:

```
REQUEST
{
  "id": 3,
  "method": "set",
  "params": [
    {
      "data": [
        {
          "action": "monitor",
          "id": 33
        },
        {
          "action": "monitor",
          "id": 34
        }
      ],
      "url": "/pm/config/adom/demo/obj/webfilter/profile/wfp_001/ftgd-wf/filters"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
pyFMG
```

After the change, action is monitor for both filter entries:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "expand datasrc": [
        {
          "datasrc": [
            {
              "obj type": "webfilter categories"
            }
          ],
          "name": "category"
        }
      ],
      "filter": [
        "id",
        "in",
        33,
        34
      ],
      "url": "/pm/config/adom/demo/obj/webfilter/profile/wfp_001/ftgd-wf/filters"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
#### 2.1.3.5. How to get the webfilter categories?
```

Caught in #0227646.

It is about describing how to obtain a category ID along with its corresponding symbolic name.

The following example shows how to get the categories ID along with their symbolic names, by combining the datasrc option with the attr attribute:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "attr": "rating",
      "option": "datasrc",
      "url": "/pm/config/adom/demo/obj/webfilter/ftgd-local-rating"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
pyFMG
```

You could leverage the datasrc option and the attr attribute for all url leading to a configuration element referencing a category ID.

The following example will produce a similar output but with a different url and attr values:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "attr": "ftgd-wf/filters/category",
      "option": "datasrc",
      "url": "/pm/config/adom/demo/obj/webfilter/profile"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
pyFMG
```

There is a second alternative which consists in using the get reserved option as shown below:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "option": "get reserved",
      "url": "/pm/config/adom/demo/obj/webfilter/categories"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
pyFMG
```
## 2.2. DNS Filtering
```

The dnsfilter.domain-filter used by the dnsfilter.profile is the counterpart of the webfilter.urlfilter used by the webfilter.profile.

```
### 2.2.1. How to empty the dnsfilter.domain-filter.entries table?

You can use the JSON RPC method update or set as shown below:

```
REQUESTRESPONSE
{
  "id": 3,
  "method": "update",
  "params": [
    {
      "data": {
        "entries": []
      },
      "url": "/pm/config/adom/dc_amer/obj/dnsfilter/domain-filter/2"
    }
  ],
  "session": "{{ session }}"
}
```

## 2.3. Application Control Management
### 2.3.1. How to get the list of all applications?

We can use any of those URL

pm/config/global/_application/list
pm/config/global/obj/_application/list
pm/config/adom/<adom>/_application/list
pm/config/adom/<adom>/obj/_application/list
pm/config/device/<device>/global/_application/list
pm/config/device/<device>/_application/list
pm/config/device/<device>/vdom/<vdom>/_application/list


For instance:

```
REQUEST:

{
  "id": 1,
  "jsonrpc": "1.0",
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/CM-LAB-001/_application/list"
    }
  ],
  "session": "NFqDRmsSz8tdxPZ7TPLdPCewoXS8Tz/vvZyOXera6CVntGsNHbElddvtyW/gAdmacfrYsoyaQsAaIktFwQm2dmRfUocs1u4B",
  "verbose": 1
}


RESPONSE:

{
  "id": 1,
  "result": [
    {
      "data": [
        {
          "behavior": "",
          "cat-id": "21",
          "category": "Email",
          "id": "16554",
          "language": "Chinese",
          "name": "126.Mail",
          "parameter": "",
          "popularity": "4.low",
          "protocol": "1.TCP, 9.HTTP, 26.SSL",
          "require_ssl_di": "No",
          "risk": "3.low",
          "shaping": "0",
          "sub-cat-id": "0",
          "sub-category": "(null)",
          "technology": "1.Browser-Based",
          "vendor": "9.Netease",
          "weight": "10"
        },
[...]
```

### 2.3.2. How to get the list of Application Categories?

Caught in #0278734.

We can use either of those URLs:

pm/config/adom/<adom>/_category/list

pm/config/adom/<adom>/obj/_category/list

To get some output, the ADOM has to contains a real device.

If your ADOM doesn’t have yet any real devices or only has Model Devices, the output will be null.

```
REQUEST:

{
  "id": 1,
  "method": "get",
  "params": [
    {
      "url": "pm/config/adom/ADOM_54_001/obj/_category/list"
    }
  ],
  "session": "xkULr1ot8oq+HnVLlrxVC9KafsiO+ZvtU0Uot+LlueIqDegtqIw9W0lYSF1YkyUgCHLH/PxwnSmCjnfuLPoZrQ==",
  "verbose": 1
}


RESPONSE:

{
  "id": 1,
  "result": [
    {
      "data": [
        {
          "id": 19,
          "name": "\"Botnet\""
        },
        {
          "id": 29,
          "name": "\"Business\""
        },
        {
          "id": 30,
          "name": "\"Cloud.IT\""
        },
        {
          "id": 5,
          "name": "\"Video/Audio\""
        },
        {
          "id": 3,
          "name": "\"VoIP\""
        },
        {
          "id": 25,
          "name": "\"Web.Client\""
        }
      ],
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "pm/config/adom/ADOM_54_001/_category/list"
    }
  ]
}
```


Please also consider the new information from #0370036.

1) JSON API changes:
a) The following 3 JSON API:
firewall/service/predefined (this one should be deleted)
ips/sensor/entries/protocol
ips/sensor/entries/application
Will merge into one:
_data/reserved/<mapping_name>
b) New category: application/categories,
also "webfilter/categories", etc...
can be get by the new JSON API:
_data/reserved/application/categories
_data/reserved/webfilter/categories
c) The old JSON API:
_category/list
will be kept which will return the DB calculated category list.

### 2.3.3. How to create a new Custom Application Signature?

To add a new APP_SIG_002 Custom Application Signature in dc_africa ADOM:

```
REQUEST
{
  "id": 3,
  "method": "set",
  "params": [
    {
      "data": {
        "comment": null,
        "signature": "F-SBID (--app_cat 36; --name \"Front.FP30reg.Chunked.Overflow TEst\"; --protocol tcp; --service HTTP; --flow from_client; --parsed_type HTTP_POST; --pattern \"/vti_bin/_vti_aut/fp30reg.dll\"; --context uri; --no_case; --parsed_type HTTP_CHUNKED; )",
        "tag": "APP_SIG_002"
      },
      "url": "pm/config/adom/dc_africa/obj/application/custom"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
## 2.4. DLP Profile Management
### 2.4.1. How to add a new DLP File Pattern?
```

Caught in #594984.

```
```
REQUEST
{
  "id": 1,
  "method": "add",
  "params": [
    {
      "url": "pm/config/adom/root/obj/dlp/filepattern",
      "data": {
        "name": "test",
        "id": 0,
        "entries": [
          {
            "file-type": 64,
            "filter-type": 1,
            "pattern": "Test"
          }
        ]
      }
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
### 2.4.2. How to get DLP elements from FortiGuard DB?
```

Caught in #0966060.

```
#### 2.4.2.1. How to get DLP sensors from FortiGuard DB?
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "pm/config/adom/root/_fdsdb/dlp/sensor"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
#### 2.4.2.2. How to get DLP dictionnaries from FortiGuard DB?
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "pm/config/adom/root/_fdsdb/dlp/dictionary"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
#### 2.4.2.3. How to get DLP data-type from FortiGuard DB?
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "pm/config/adom/root/_fdsdb/dlp/data-type"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
## 2.5. IPS Sensors Management
### 2.5.1. How to add an IPS rule in an IPS sensor?
```

The following example shows how to add a new IPS rule in the ips_sensor_001 IPS sensor in the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": {
        "action": "default",
        "application": [
          "all"
        ],
        "cve": [],
        "default-action": "all",
        "default-status": "all",
        "exempt-ip": null,
        "last-modified": [],
        "location": [
          "all"
        ],
        "log": "disable",
        "log-attack-context": "disable",
        "log-packet": "disable",
        "os": [
          "all"
        ],
        "protocol": [
          "all"
        ],
        "quarantine": "none",
        "rule": [],
        "severity": [
          "info"
        ],
        "status": "default",
        "vuln-type": []
      },
      "url": "/pm/config/adom/demo/obj/ips/sensor/ips_sensor_001/entries"
    }
  ],
  "session": "{{session}}"
}
```


> **Note:**


New item is added at the end of the list of existing items

RESPONSE
```
```
### 2.5.2. How to insert an IPS rule in an IPS sensor?
```

The following example shows how to insert a new IPS rule in the ips_sensor_001 IPS sensor in the demo ADOM.

This new IPS rule will be inserted after the IPS rule with ID 1:

```
```
REQUEST
{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": {
        "action": "default",
        "application": [
          "all"
        ],
        "cve": [],
        "default-action": "all",
        "default-status": "all",
        "exempt-ip": null,
        "last-modified": [],
        "location": [
          "all"
        ],
        "log": "enable",
        "log-attack-context": "enable",
        "log-packet": "enable",
        "object position": [
          "after",
          "1"
        ],
        "os": [
          "all"
        ],
        "protocol": [
          "HTTP",
          "FTP"
        ],
        "quarantine": "none",
        "rule": [],
        "severity": [
          "high"
        ],
        "status": "default",
        "vuln-type": []
      },
      "url": "/pm/config/adom/demo/obj/ips/sensor/ips_sensor_001/entries"
    }
  ],
  "session": "{{session}}"
}
```


> **Note:**

object position mechanism seen in How to insert a policy? is used to insert the new IPS rule

RESPONSE
```
```
### 2.5.3. How to delete an IPS rule from an IPS sensor?
```

The following example shows how to delete the IPS rule with ID 5 from the ips_sensor_001 in the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "delete",
  "params": [
    {
      "url": "/pm/config/adom/demo/obj/ips/sensor/ips_sensor_001/entries/5"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
```
### 2.5.4. How to get list of IPS signatures?
```

The following example shows how to get the list of IPS signatures available in the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/demo/_rule/list"
    }
  ],
  "session": "{{session}}"
  "verbose": 1
}

RESPONSE
```
```

> **Note:**

The obtained signatures are from the IPS package version indicated in the output of this command:

diagnose dvm adom list demo


You should get an output similar to the following one:

OID      STATE    PRODUCT OSVER MR  LIC NAME MODE    VPN MANAGEMENT        IPS     ISDB
3        enabled  FOS     7.0   4       demo Normal  Policy & Device VPNs  26.740  7.3585
---End ADOM list---


In this above output, the IPS package version is given by the IPS column: 26.740

```
```
### 2.5.5. How to get list of IPS protocols?
```

The following example shows how to get the list of IPS protocols using the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/demo/_data/reserved/ips/sensor/entries/protocol"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
```
```
### 2.5.6. How to get list of IPS applications?
```

The following example shows how to get the list of IPS applications using the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/demo/_data/reserved/ips/sensor/entries/application"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
```
```
### 2.5.7. How to get IPS Profile Usage?
```

Caught in #0955276.

IPS Profile Usage is a tool that lets the FortiManager administror knows about global IPS sensor usage.

You trigger it using the More > IPS Profile Usages from the Intrusion Prevention page:

For each managed device using IPS sensors, You can review the Installed Timestamp, the Modified Timestamp and most importantly the IPS sensor Status (whether it is in sync with the one used by the managed device):

In the above example, the default IPS sensor was installed on the two site_1 and site_2 managed devices at the indicated Installed Timestamp. The example is also confirming that for the moment, the default IPS sensor is still in sync with the one currently enforced by the two managed devices since the Status is green for them.

You can trigger the IPS Profile Usages operation using the FortiManager JSON RPC API as shown below:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/production/_objstatus/ips/sensor"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
### 2.5.8. Global IPS sensor
```

The Global IPS Sensor allows you to create baseline IPS sensors composed of header and footer IPS rules.

In the FortiManager GUI, you can find it under Policy & Objects > Header/Footer IPS.

> **Note:**

The Global IPS sensor defining header/footer IPS rules has nothing to do with the normal Global IPS sensor that you can find under Policy & Objects > Security Profile > Intrusion Prevention

```
#### 2.5.8.1. How to create a Global IPS sensor

The following example shows how to add the g_ips_sensor_001 Global IPS sensor made of one header and one footer rules in the Global ADOM:

```
REQUEST
{
  "id": 3,
  "method": "add",
  "params": [
    {
      "data": {
        "block-malicious-url": 0,
        "entries": [
          {
            "action": 5,
            "application": ["all"],
            "default-action": 34,
            "default-status": 34,
            "exempt-ip": [],
            "last-modified": null,
            "location": ["all"],
            "log": true,
            "log-attack-context": 0,
            "log-packet": 0,
            "os": ["all"],
            "position": "header",
            "protocol": ["all"],
            "quarantine": 0,
            "quarantine-expiry": "5m",
            "quarantine-log": 1,
            "rate-count": 0,
            "rate-duration": 60,
            "rate-mode": 9,
            "rate-track": 0,
            "severity": ["all"],
            "status": 3
          },
          {
            "action": 5,
            "application": ["all"],
            "default-action": 34,
            "default-status": 34,
            "exempt-ip": [],
            "last-modified": null,
            "location": ["all"],
            "log": true,
            "log-attack-context": 0,
            "log-packet": 0,
            "os": ["all"],
            "position": "footer",
            "protocol": ["all"],
            "quarantine": 0,
            "quarantine-expiry": "5m",
            "quarantine-log": 1,
            "rate-count": 0,
            "rate-duration": 60,
            "rate-mode": 9,
            "rate-track": 0,
            "severity": ["all"],
            "status": 3
          }
        ],
        "extended-log": 0,
        "name": "g_ips_sensor_001",
        "scan-botnet-connections": 0
      },
      "url": "/pm/config/global/obj/global/ips/sensor"
    }
  ],
  "session": "{{session}}"
}
```


> **Note:**

The entries attribute contains the IPS header and footer rules

The position attribute determines whether the IPS rule is in the header (value is header) of footer (footer) rule block

RESPONSE
#### 2.5.8.2. How to delete a Global IPS sensor?

The following example shows how to delete the g_ips_sensor_001 Global IPS sensor from the Global ADOM:

```
REQUEST
{
  "id": 3,
  "method": "delete",
  "params": [
    {
      "url": "/pm/config/global/obj/global/ips/sensor/g_ips_sensor_001",
    }
  ]
}

RESPONSE
```
#### 2.5.8.3. How to add ADOMs to a Global IPS sensor?
```

The following example shows how to add the demo_001 and demo_002 to the g_ips_sensor_001 Global IPS sensor in the Global ADOM:

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
          "name": "demo_001"
        },
        {
          "name": "demo_002"
        }
      ],
      "url": "/pm/config/global/obj/global/ips/sensor/g_ips_sensor_001/scope member"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
#### 2.5.8.4. How to delete ADOMs from a Global IPS sensor?
```

The following example shows how to delete the demo_001 and demo_002 from the g_ips_sensor_001 Global IPS sensor in the Global ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "delete",
  "params": [
    {
      "data": [
        {
          "name": "demo_001"
        },
        {
          "name": "demo_002"
        }
      ],
      "url": "/pm/config/global/obj/global/ips/sensor/g_ips_sensor_001/scope member"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
#### 2.5.8.5. How to assign a Global IPS sensor?
```

The following example shows how to assign the g_ips_sensor_001 Global IPS sensor to the demo_001 and demo_002 ADOMs:

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
        "category": 1908,
        "flags": "none",
        "objs": [
          "g_ips_sensor_001"
        ],
        "target": [
          {
            "adom": "demo_001"
          },
          {
            "adom": "demo_002"
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

The category attribute is the number of the table global ips sensor

You can get this number by issuing following command:

execute fmpolicy print-adom-object Global ?


In the output, you will see this line:

```
[...]
1908      "global ips sensor"
[...]

RESPONSE
```
#### 2.5.8.6. How to unassign a Global IPS sensor?
```

The following example shows how to unassign the g_ips_sensor_001 Global IPS sensor from the demo_001 and demo_002 ADOMs:

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
        "category": 1908,
        "flags": "unassign",
        "objs": [
          "g_ips_sensor_001"
        ],
        "target": [
          {
            "adom": "demo_001"
          },
          {
            "adom": "demo_002"
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

The category attribute is the number of the table global ips sensor

You can get this number by issuing following command:

execute fmpolicy print-adom-object Global ?


In the output, you will see this line:

```
[...]
1908      "global ips sensor"
[...]

RESPONSE
```
#### 2.5.8.7. How to get the assign status for Global IPS sensors?
```

Caught in #1051174.

This is to get the information exposed in the following screenshot:

The screenshot above shows two global IPS sensor, g_ips_sensor_001 and g_ips_sensor_002, along with their assignement status.

You can see that:

The g_ips_sensor_001 global IPS sensor isn’t assigned to the dc_amer ADOM; its status is Never installed

The g_ips_sensor_001 global IPS sensor is assigned to the dc_africa ADOM but it has pending changes; its status is Modified

The g_ips_sensor_002 has been assigned to its dc_emea ADOM; its status is Synced

The following example shows how to get the same information using the FortiManager API:

```
```
REQUEST
{
  "id": 2,
  "method": "get",
  "params": [
    {
      "stype": "gl_ips_sensor",
      "type": "template",
      "url": "/pm/config/global/_package/status"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
### 2.5.9. IPS Package Management
```

The following capabilities are available for querying IPS signature and package information programmatically. They cover a range of use cases, from retrieving the details of an individual signature (How to get the detail of a specific IPS signature?) to inspecting the contents of a full package release (see How to fetch all signature IDs and details for a given package release version?).

You can look up a single signature by its ID (How to get the detail of a specific IPS signature?), or retrieve the complete set of signature IDs and details contained in a given package release version (How to fetch all signature IDs and details for a given package release version?). It is also possible to compare two versions and return only the delta - the signatures added between them (How to fetch delta signature IDs between two package versions?). All listing queries support pagination through offset and limit parameters, so large result sets can be retrieved in manageable chunks.

In addition to listing the signatures themselves, you can query counts directly: either the total number of signatures in a specific version (How to get total count of signatures for a given package version?), or the number of signatures introduced between two versions (How to get the total count of signatures between two package versions?). A summary query returns the most recent IPS package releases, which is useful for determining the latest available version (How to list the latest IPS packages?). Finally, change log information can be retrieved for an individual signature to track its history over time (How to get the changelog info for a specific IPS signature ID?).

Caught in #1271574 (FortiManager 8.0.1).

```
#### 2.5.9.1. How to get the detail of a specific IPS signature?

If you have a specific IPS signature ID, you can get its details using the following FortiManager API request:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "data": {
        "target": "/fgd/lookup/ency?source=ips&id=25536"
      },
      "url": "/um/query/productapi"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}
```


> **Note:**

The id attribute in the target attribute of the request is the IPS signature ID you want to query.

RESPONSE
#### 2.5.9.2. How to fetch all signature IDs and details for a given package release version?

If you have a specific package version, you can get its signature details using the following FortiManager API request:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "data": {
        "target": "/srvupd/detail/ips/34.089?detail=1&offset=0&limit=3"
      },
      "url": "/um/query/productapi"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}
```


> **Note:**

The target attribute in the request contains the package version you want to query (34.089 in this example).

The offset and limit attributes are used for pagination of the results. In this example, we are requesting the first 3 signatures of the package version 34.089.

RESPONSE
#### 2.5.9.3. How to fetch delta signature IDs between two package versions?

You can obtain the list of signature IDs that were added between two package versions using the following FortiManager API request:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "data": {
        "target": "/srvupd/detail/ips/34.085/34.089?detail=1&offset=0&limit=3"
      },
      "url": "/um/query/productapi"
    }
  ],
  "session": "{{version}}",
  "verbose": 1
}
```


> **Note:**

The target attribute in the request contains the two package versions you want to compare (34.085 and 34.089 in this example).

The offset and limit attributes are used for pagination of the results. In this example, we are requesting the first 3 signatures that were added between the two package versions.

RESPONSE
#### 2.5.9.4. How to get total count of signatures for a given package version?

You can obtain the total count of signature in a given package version using the following FortiManager API request:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "data": {
        "target": "/srvupd/count-detail/ips/34.089"
      },
      "url": "/um/query/productapi"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}
```


> **Note:**

The target attribute in the request contains the package version you want to get the total count of signatures from (34.089 in this example).

RESPONSE
#### 2.5.9.5. How to get the total count of signatures between two package versions?

You can obtain the total count of signature IDs that were added between two package versions using the following FortiManager API request:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "data": {
        "target": "/srvupd/count-detail/ips/34.080/34.089"
      },
      "url": "/um/query/productapi"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}
```


> **Note:**

The target attribute in the request contains the two package versions you want to compare (34.085 and 34.089 in this example).

RESPONSE
#### 2.5.9.6. How to list the latest IPS packages?

The example below shows how to get the last 10 IPS packages information:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "data": {
        "target": "/srvupd/summary?types=ips&limit=10"
      },
      "url": "/um/query/productapi"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
#### 2.5.9.7. How to get the changelog info for a specific IPS signature ID?
```

The example below shows how to get the changelog for a given IPS signature ID:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "data": {
        "target": "/srvupd/history/ips/56720"
      },
      "url": "/um/query/productapi"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```
## 2.6. Virtual Patching
### 2.6.1. How to get the Virtual Patching Signatures list?
```

Caught in #0983425 and #1103218

Following example shows how to get the Virtual Patching Signatures list using the demo ADOM:

```
```
REQUEST
{
  "id": 1,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/demo/_fdsdb/rule/otvp"
    }
  ],
  "session": "{{session}}"
}

RESPONSE
```
## 2.7. Inline CASB Profile
### 2.7.1. How to get list of SaaS Applications?
```

Caught in #1094160.

The following example shows how to get the list of SaaS applications using the demo ADOM:

```
```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "attr": "saas-application/name",
      "option": "datasrc",
      "url": "/pm/config/adom/demo/obj/casb/profile"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```

Alternatively, and starting with FortiManager 7.4.11, 7.6.7 or 8.0.0 (#1194560), you can use the following FortiManager API request:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "option": [
        "get reserved"
      ],
      "url": "/pm/config/adom/demo/obj/casb/saas-application"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```

Seen in #1281997, another alternative which seems to give more details:

```
REQUEST
{
  "id": 3,
  "method": "get",
  "params": [
    {
      "url": "/pm/config/adom/demo/_fdsdb/casb/saas-application"
    }
  ],
  "session": "{{session}}",
  "verbose": 1
}

RESPONSE
```


```
```
# 1. Objects Management
```


```
# 3. Policy Package Management

Contents
## 2.1. URL Filtering
### 2.1.1. Webfilter urlfilter
#### 2.1.1.1. How to add a new entry in a webfilter.urlfilter.entries?
#### 2.1.1.2. How to add multiple entries in a webfilter.urlfilter.entries?
#### 2.1.1.3. How to replace the entire list of webfilter.urlfilter.entries?
#### 2.1.1.4. How to delete an entry in a webfilter.urlfilter.entries?
### 2.1.2. Web rating overrides
#### 2.1.2.1. How to add a new web rating override?
### 2.1.3. Webfilter profile
#### 2.1.3.1. How to add a new filter in a webfilter profile?
#### 2.1.3.2. How to get existing filters in a webfilter profile?
#### 2.1.3.3. How to update an existing filter in a webfilter profile?
#### 2.1.3.4. How to update multiple filters in a webfilter profile?
#### 2.1.3.5. How to get the webfilter categories?
## 2.2. DNS Filtering
### 2.2.1. How to empty the dnsfilter.domain-filter.entries table?
## 2.3. Application Control Management
### 2.3.1. How to get the list of all applications?
### 2.3.2. How to get the list of Application Categories?
### 2.3.3. How to create a new Custom Application Signature?
## 2.4. DLP Profile Management
### 2.4.1. How to add a new DLP File Pattern?
### 2.4.2. How to get DLP elements from FortiGuard DB?
#### 2.4.2.1. How to get DLP sensors from FortiGuard DB?
#### 2.4.2.2. How to get DLP dictionnaries from FortiGuard DB?
#### 2.4.2.3. How to get DLP data-type from FortiGuard DB?
## 2.5. IPS Sensors Management
### 2.5.1. How to add an IPS rule in an IPS sensor?
### 2.5.2. How to insert an IPS rule in an IPS sensor?
### 2.5.3. How to delete an IPS rule from an IPS sensor?
### 2.5.4. How to get list of IPS signatures?
### 2.5.5. How to get list of IPS protocols?
### 2.5.6. How to get list of IPS applications?
### 2.5.7. How to get IPS Profile Usage?
### 2.5.8. Global IPS sensor
#### 2.5.8.1. How to create a Global IPS sensor
#### 2.5.8.2. How to delete a Global IPS sensor?
#### 2.5.8.3. How to add ADOMs to a Global IPS sensor?
#### 2.5.8.4. How to delete ADOMs from a Global IPS sensor?
#### 2.5.8.5. How to assign a Global IPS sensor?
#### 2.5.8.6. How to unassign a Global IPS sensor?
#### 2.5.8.7. How to get the assign status for Global IPS sensors?
### 2.5.9. IPS Package Management
#### 2.5.9.1. How to get the detail of a specific IPS signature?
#### 2.5.9.2. How to fetch all signature IDs and details for a given package release version?
#### 2.5.9.3. How to fetch delta signature IDs between two package versions?
#### 2.5.9.4. How to get total count of signatures for a given package version?
#### 2.5.9.5. How to get the total count of signatures between two package versions?
#### 2.5.9.6. How to list the latest IPS packages?
#### 2.5.9.7. How to get the changelog info for a specific IPS signature ID?
## 2.6. Virtual Patching
### 2.6.1. How to get the Virtual Patching Signatures list?
## 2.7. Inline CASB Profile
### 2.7.1. How to get list of SaaS Applications?


Protect your code and reputation. See why top mobile app developers trust Guardsquare for security.
