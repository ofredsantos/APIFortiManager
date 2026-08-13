# Inventário de Padronização - cl-fw-ula-MartMinas-246

**Device:** cl-fw-ula-MartMinas-246
**Serial:** FGT40FTK21024569
**ADOM:** MART_MINAS
**Plataforma:** FortiGate-40F
**Versão:** 7.0

---
## Resumo dos Requisitos

| # | Requisito | Status |
|---|-----------|--------|
| 1 | VPN IPsec (Túneis Dedicados) | ❌ Ausente |
| 2 | Rotas Estáticas | ❌ Ausente |
| 3 | Accprofile 'API' | ❌ Ausente |
| 4 | Contas Admin Padrão | ❌ Ausente |
| 5 | Interface Loopback | ✅ OK |
| 6 | Nomenclatura de Túneis | ❌ Ausente |
| 7 | Zone SOC | ❌ Ausente |
| 8 | Address Objects SOC | ✅ OK |
| 9 | Firewall Policies SOC | ❌ Ausente |
| 10 | Servidor RADIUS | ❌ Ausente |
| 11 | User Groups RADIUS | ❌ Ausente |
| 12 | admintimeout | ❌ Ausente |
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

**Status:** ❌ Ausente

**Configuração Atual:**

```
Nenhuma rota para túneis SOC encontrada.
```

**Sugestão:**

Criar rotas estáticas para as redes do SOC (ex: 10.10.0.0/16) apontando para os túneis IPsec to_soc_wan1 e to_soc_wan2.

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

Criar contas administrativas padrão: algar_ops (super_admin) e algar_soc (read_only).

---

### 5. Interface Loopback

**Status:** ✅ OK

**Configuração Atual:**

```
Loopback(s) encontrado(s):
  - loopback: ['198.19.1.46', '255.255.255.255']
  - loopback_DR: ['198.19.100.46', '255.255.255.255']
```

**Sugestão:**

Nenhuma ação necessária. Loopback já configurada.

---

### 6. Nomenclatura de Túneis

**Status:** ❌ Ausente

**Configuração Atual:**

```
Túneis atuais: naf.root, l2t.root, ssl.root, SPK-OCI-Wan1, SPK-OCI-Wan2, SPK-OCIDR-Wan1, SPK-OCIDR-Wan2
```

**Sugestão:**

Renomear túneis para o padrão: to_soc_wan1, to_soc_wan2.

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

### 8. Address Objects SOC

**Status:** ✅ OK

**Configuração Atual:**

```
Address objects SOC encontrados:
  - sistema.soc.com.br: N/A
  - socged.soc.com.br: N/A
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

**Status:** ❌ Ausente

**Configuração Atual:**

```
admintimeout = 31 minutos (esperado: 480)
```

**Sugestão:**

Ajustar admintimeout para 480 minutos:
config system global
  set admintimeout 480
end

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
