# 🔐 Security Policy & Vulnerability Management

## Vulnerability Scanning
This project uses Trivy for container image scanning.

## Known Vulnerabilities (Accepted Risks)

### CVE-2026-0861 (glibc)
- **Severity:** HIGH
- **Package:** libc6, libc-bin (Debian 13.3)
- **Status:** ⚠️ No fix available yet
- **Risk Assessment:** 
  - Low exploitation likelihood for this use case
  - Application does not directly interact with affected glibc functions
  - Container runs as non-root user (reduces impact)
- **Mitigation:**
  - Running as non-root user (appuser)
  - Minimal base image (slim variant)
  - Monitoring Debian security announcements
- **Remediation Plan:** 
  - Will patch when Debian releases updated glibc package
  - Automated scan in CI/CD will alert when fix is available

## Last Scan
- Date: 2026-03-02
- Tool: Trivy v0.49
- Result: 0 CRITICAL, 2 HIGH (OS-level, accepted), 3 HIGH (Python, fixed in newer deps)
