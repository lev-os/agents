# macOS Accessibility - Threat Model

## Threat Model Overview

**Domain Risk Level**: HIGH
**Attack Surface**: System-wide accessibility access, TCC bypass potential

### Assets to Protect

1. **TCC Permissions** - CRITICAL - Gate to system-wide access
2. **User Credentials** - CRITICAL - Keychain, password fields
3. **System Integrity** - HIGH - Prevention of unauthorized automation
4. **User Privacy** - HIGH - Screen content, application data

---

## Attack Scenario 1: TCC Bypass

**Threat Category**: OWASP A01:2025 - Broken Access Control
**Threat Level**: CRITICAL

**Attack Flow**:
```
1. Attacker exploits TCC bypass vulnerability
2. Gains accessibility permission without user consent
3. Automates any application on system
4. Exfiltrates sensitive data
```

**Mitigation**: Keep macOS updated, monitor TCC database for anomalies

---

## Attack Scenario 2: Keychain Access

**Threat Category**: OWASP A07:2025 - Authentication Failures
**Threat Level**: CRITICAL

**Attack Flow**:
```
1. Automation targets Keychain Access
2. Uses AX to read password entries
3. Automates unlock if password cached
4. Exfiltrates all credentials
```

**Mitigation**: Block Keychain Access in automation, never store master password

---

## Attack Scenario 3: Code Signature Bypass

**Threat Category**: OWASP A05:2025 - Injection
**Threat Level**: HIGH

**Attack Flow**:
```
1. Malicious app spoofs trusted bundle ID
2. Automation trusts app based on bundle ID
3. Attacker injects malicious automation
4. System compromised
```

**Mitigation**: Verify code signature, not just bundle ID

---

## Attack Scenario 4: Security Dialog Automation

**Threat Category**: OWASP A01:2025 - Broken Access Control
**Threat Level**: CRITICAL

**Attack Flow**:
```
1. Trigger authentication dialog
2. Use AX to find password field
3. Inject known password or brute force
4. Bypass authentication
```

**Mitigation**: Block SecurityAgent bundle ID, never automate auth dialogs

---

## STRIDE Analysis

| Category | Threats | Mitigations | Priority |
|----------|---------|-------------|----------|
| **Spoofing** | Bundle ID spoofing | Code signature verification | CRITICAL |
| **Tampering** | Modify automation targets | Hardened runtime check | HIGH |
| **Repudiation** | Deny automation actions | Immutable audit logs | HIGH |
| **Information Disclosure** | Read sensitive AX attributes | Attribute filtering | CRITICAL |
| **Denial of Service** | Hang via slow AX calls | Timeouts | MEDIUM |
| **Elevation of Privilege** | TCC bypass | Keep macOS updated | CRITICAL |
