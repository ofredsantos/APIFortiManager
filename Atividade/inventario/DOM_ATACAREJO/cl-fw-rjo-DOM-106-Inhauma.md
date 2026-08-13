# Inventário de Padronização - cl-fw-rjo-DOM-106-Inhauma

**Device:** cl-fw-rjo-DOM-106-Inhauma
**Serial:** FGT40FTK2209HHJ7
**ADOM:** DOM_ATACAREJO
**Plataforma:** FortiGate-40F
**Versão:** 7.0

---
## Resumo dos Requisitos

| # | Requisito | Status |
|---|-----------|--------|
| 1 | VPN IPsec (Túneis Dedicados) | ❌ Ausente |
| 2 | Rotas Estáticas | ✅ OK |
| 3 | Accprofile 'API' | ❌ Ausente |
| 4 | Contas Admin Padrão | ❌ Ausente |
| 5 | Interface Loopback | ✅ OK |
| 6 | Nomenclatura de Túneis | ✅ OK |
| 7 | Zone SOC | ❌ Ausente |
| 8 | Address Objects Gerenciamento | ✅ OK |
| 9 | Firewall Policies SOC | ❌ Ausente |
| 10 | Servidor RADIUS | ❌ Ausente |
| 11 | User Groups RADIUS | ❌ Ausente |
| 12 | admintimeout | ✅ OK |
| 13 | Sync Status | ❌ Ausente |

---
## Detalhamento por Requisito

### 1. VPN IPsec (Túneis Dedicados)

**Status:** ❌ Ausente

**Configuração Atual:**

```
Nenhum túnel IPsec encontrado ou erro na consulta.
```

**Sugestão:**

Criar 2 túneis VPN IPsec (um por link WAN) entre o FortiGate e o SOC. Utilizar nomenclatura padrão: to_soc_wan1, to_soc_wan2.

---

### 2. Rotas Estáticas

**Status:** ✅ OK

**Configuração Atual:**

```
2 rotas de gerenciamento encontradas:
  - ['198.19.0.0', '255.255.255.192'] → ['VPN.MGMT.01'] (GW: N/A)
  - ['198.19.0.0', '255.255.255.192'] → ['VPN.MGMT.02'] (GW: N/A)
```

**Sugestão:**

Nenhuma ação necessária. Rotas estáticas já configuradas.

---

### 3. Accprofile 'API'

**Status:** ❌ Ausente

**Configuração Atual:**

```
Nenhum perfil de administrador encontrado.
```

**Sugestão:**

Criar accprofile 'API' com permissões de leitura/escrita via RPC: config system accprofile
  edit API
    set adomprlv custom
    set fmgprlv custom
    set rpc-permit read-write
  next
end

---

### 4. Contas Admin Padrão

**Status:** ❌ Ausente

**Configuração Atual:**

```
Nenhum administrador encontrado.
```

**Sugestão:**

Criar contas administrativas padrão: api_soc, api_nava, algar_soc, algar_atv, operacao_soc.

---

### 5. Interface Loopback

**Status:** ✅ OK

**Configuração Atual:**

```
Loopback(s) encontrado(s):
  - loopback: ['198.19.1.106', '255.255.255.255']
  - loopback_dom: ['198.18.1.106', '255.255.255.255']
  - mgmt.algar: ['198.19.14.210', '255.255.255.255']
```

**Sugestão:**

Nenhuma ação necessária. Loopback já configurada.

---

### 6. Nomenclatura de Túneis

**Status:** ✅ OK

**Configuração Atual:**

```
Túneis no padrão de gerência: VPN.MGMT.01, VPN.MGMT.02
```

**Sugestão:**

Nenhuma ação necessária. Nomenclatura já padronizada.

---

### 7. Zone SOC

**Status:** ❌ Ausente

**Configuração Atual:**

```
Nenhuma zone encontrada.
```

**Sugestão:**

Criar zone 'SOC' e associar os túneis IPsec:
config system zone
  edit SOC
    set interface to_soc_wan1 to_soc_wan2
  next
end

---

### 8. Address Objects Gerenciamento

**Status:** ✅ OK

**Configuração Atual:**

```
Address objects de gerenciamento encontrados:
  - MGMT.DC: ['198.19.0.0', '255.255.255.192']
  - MGMT.SPOKE: ['198.19.14.126', '255.255.255.255']
```

**Sugestão:**

Nenhuma ação necessária. Address objects já existem.

---

### 9. Firewall Policies SOC

**Status:** ❌ Ausente

**Configuração Atual:**

```
Nenhuma firewall policy encontrada.
```

**Sugestão:**

Criar firewall policies para permitir tráfego de gerenciamento entre a zone SOC e a interface loopback_mgmt.

---

### 10. Servidor RADIUS

**Status:** ❌ Ausente

**Configuração Atual:**

```
Nenhum servidor RADIUS configurado.
```

**Sugestão:**

Configurar servidor RADIUS para autenticação administrativa:
config user radius
  edit SOC_RADIUS
    set server <ip_radius>
    set secret <secret>
    set auth-type pap
  next
end

---

### 11. User Groups RADIUS

**Status:** ❌ Ausente

**Configuração Atual:**

```
Nenhum user group encontrado.
```

**Sugestão:**

Criar user group para autenticação RADIUS:
config user group
  edit SOC_Admins
    set member SOC_RADIUS
  next
end

---

### 12. admintimeout

**Status:** ✅ OK

**Configuração Atual:**

```
admintimeout = 31 minutos (padrão Algar)
```

**Sugestão:**

Nenhuma ação necessária.

---

### 13. Sync Status

**Status:** ❌ Ausente

**Configuração Atual:**

```
Device fora de sincronia (db_status=nomod, mgmt_mode=fmgfaz)
```

**Sugestão:**

Sincronizar device com o FMG:
1. Revisar configurações pendentes no FMG
2. Executar install para sincronizar

---
