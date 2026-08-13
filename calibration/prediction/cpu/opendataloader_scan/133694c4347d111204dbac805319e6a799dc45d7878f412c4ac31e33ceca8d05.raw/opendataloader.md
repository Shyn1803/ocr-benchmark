Network: Use the Network pane to manage the management IP addresses for the system, service IP addresses for the nodes, and iSCSI and Fibre Channel configurations. The system must support Fibre Channel or Fibre Channel over Ethernet connections to your storage area network (SAN).

Security: Use the Security pane to configure and manage remote authentication services.

System: Navigate to the System menu item to manage overall system configuration options, such as licenses, updates, and date and time settings.

the support center.

GUI Preferences: Configure welcome message after login, refresh internals and GUI logout timeouts.

These options are described next.

# 5.10.1 Notifications menu

IBM Storwize V7000 can use SNMP traps, syslog messages, and Call Home email to notify you and the IBM Support Center when significant events are detected. Any combination of these notification methods can be used simultaneously.

Notifications are normally sent immediately after an event is raised. However, events can occur because of service actions that are performed. If a recommended service action is active, notifications about these events are sent only if the events are still unfixed when the service action completes.

# SNMP notifications

can send SNMP messages that notify personnel about an event. You can use an SNMP manager to view the SNMP messages that are sent by IBM Storwize V7000.

To view the SNMP configuration, use the System window. Point to the Settings   icon   and click Notification → SNMP (see Figure 5-54).

![](<133694c4347d111204dbac805319e6a799dc45d7878f412c4ac31e33ceca8d05_images/imageFile1.png>)

SNMP

SNMP

Download MIB

MIB:

Syslog

Actions

Filter

Warning

Server IP

Info

Error

10.11.11.11

Showing

Selecting

1 server

servers

Figure 5-54 Setting SNMP server and traps

