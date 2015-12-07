to_icinga2
==========

a simple filter to convert ansible vars (more precisely dictionaries) to icinga2 host-attributes expression.

i.e. if you define the following var e.g. in your *host_vars/** files

```yaml
icinga_host_attributes:
  http_vhosts:
    Syncthing https redirect:
      http_port: 8384
      http_expect: 302
    Syncthing:
      http_port: 8384
      http_ssl: 1
      http_expect: 401
```

you can use ```{{ hostvars[item].icinga_host_attributes|to_icinga2 }}``` in your icinga2-templates, yielding

    vars.http_vhosts["Syncthing https redirect"] = {
        http_port = 8384
        http_expect = 302
    }
    vars.http_vhosts["Syncthing"] = {
        http_port = 8384
        http_expect = 401
        http_ssl = 1
    }
