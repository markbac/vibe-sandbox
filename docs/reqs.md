<!-- filepath: docs/reqs.md -->
# Requiremenst

## Reqs Mermaid

```mermaid
requirementDiagram
requirement "REQ_001" {
  id: REQ_001
  text: "Temperature Control"
}
requirement "REQ_008" {
  id: REQ_008
  text: "Temperature Accuracy"
}
"REQ_001" -contains-> "REQ_008"
requirement "REQ_009" {
  id: REQ_009
  text: "Scheduled Profiles"
}
"REQ_001" -contains-> "REQ_009"
"REQ_009" -traces-> "REQ_013"
requirement "REQ_010" {
  id: REQ_010
  text: "Manual Override"
}
"REQ_001" -contains-> "REQ_010"
requirement "REQ_002" {
  id: REQ_002
  text: "User Interface"
}
requirement "REQ_011" {
  id: REQ_011
  text: "Local Touchscreen UI"
}
"REQ_002" -contains-> "REQ_011"
requirement "REQ_012" {
  id: REQ_012
  text: "Remote Web UI"
}
"REQ_002" -contains-> "REQ_012"
"REQ_012" -traces-> "REQ_014"
"REQ_012" -satisfies-> "REQ_022"
requirement "REQ_013" {
  id: REQ_013
  text: "Safe UI Constraints"
}
"REQ_002" -contains-> "REQ_013"
"REQ_013" -refines-> "REQ_011"
requirement "REQ_003" {
  id: REQ_003
  text: "Connectivity"
}
requirement "REQ_014" {
  id: REQ_014
  text: "Wi-Fi Support"
}
"REQ_003" -contains-> "REQ_014"
requirement "REQ_015" {
  id: REQ_015
  text: "Matter Support"
}
"REQ_003" -contains-> "REQ_015"
requirement "REQ_016" {
  id: REQ_016
  text: "Bluetooth Support"
}
"REQ_003" -contains-> "REQ_016"
requirement "REQ_004" {
  id: REQ_004
  text: "Safety & Compliance"
}
requirement "REQ_017" {
  id: REQ_017
  text: "Overtemperature Shutdown"
}
"REQ_004" -contains-> "REQ_017"
"REQ_017" -refines-> "REQ_008"
requirement "REQ_018" {
  id: REQ_018
  text: "EN60730 Compliance"
}
"REQ_004" -contains-> "REQ_018"
requirement "REQ_019" {
  id: REQ_019
  text: "Watchdog Support"
}
"REQ_004" -contains-> "REQ_019"
"REQ_019" -derives-> "REQ_018"
requirement "REQ_005" {
  id: REQ_005
  text: "Security & Access Control"
}
requirement "REQ_020" {
  id: REQ_020
  text: "User Roles"
}
"REQ_005" -contains-> "REQ_020"
requirement "REQ_021" {
  id: REQ_021
  text: "PIN Protection"
}
"REQ_005" -contains-> "REQ_021"
"REQ_021" -refines-> "REQ_020"
requirement "REQ_022" {
  id: REQ_022
  text: "TLS for Remote Access"
}
"REQ_005" -contains-> "REQ_022"
requirement "REQ_006" {
  id: REQ_006
  text: "System Configuration & Storage"
}
requirement "REQ_023" {
  id: REQ_023
  text: "Store Settings in NVM"
}
"REQ_006" -contains-> "REQ_023"
requirement "REQ_024" {
  id: REQ_024
  text: "Import/Export Support"
}
"REQ_006" -contains-> "REQ_024"
"REQ_024" -traces-> "REQ_023"
requirement "REQ_027" {
  id: REQ_027
  text: "Firmware Update Mechanism"
}
"REQ_006" -contains-> "REQ_027"
"REQ_027" -satisfies-> "REQ_022"
requirement "REQ_007" {
  id: REQ_007
  text: "External API Support"
}
requirement "REQ_025" {
  id: REQ_025
  text: "Local REST API"
}
"REQ_007" -contains-> "REQ_025"
"REQ_025" -traces-> "REQ_011"
requirement "REQ_026" {
  id: REQ_026
  text: "MQTT Integration"
}
"REQ_007" -contains-> "REQ_026"
"REQ_026" -satisfies-> "REQ_015"
```

## reqs yaml

``` yaml
requirements:
- id: REQ_001
  title: Temperature Control
  description: 'The system **shall** control room temperature based on:\n\n    Accuracy and responsiveness are critical to user comfort.'
  tags:
  - core
  - control
  status:
    implemented: true
    verified: false
  children:
  - id: REQ_008
    title: Temperature Accuracy
  - id: REQ_009
    title: Scheduled Profiles
  - id: REQ_010
    title: Manual Override
- id: REQ_002
  title: User Interface
  description: 'Users shall be able to interact with the system via:\n\n    - A simplified fallback control method'
  tags:
  - ui
  - usability
  children:
  - id: REQ_011
    title: Local Touchscreen UI
    - hmi
  - id: REQ_012
    title: Remote Web UI
  - id: REQ_013
    title: Safe UI Constraints
- id: REQ_003
  title: Connectivity
  description: The device must support **multiple communication paths** for both user access and smart home integration.
  tags:
  - iot
  - integration
  children:
  - id: REQ_014
- id: REQ_004
  title: Safety & Compliance
- id: REQ_005
  title: Security & Access Control
- id: REQ_006
  title: System Configuration & Storage
- id: REQ_007
  title: External API Support

```
