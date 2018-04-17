*** Settings ***
Library           Collections
Library           OperatingSystem

Variables   ${ProjectTarget}/resources/variables/VAR_COMMON.py
Library     api.ScgApi    ${SCG_MANAGEMENT_IP}    ${MODEL}    ${SCG_VERSION}   ${PUBLIC_API_VERSION}    WITH NAME    api
Library     ${RootTarget}/libs/python/lib/RWQAAPCLIKeywords.py
Library     ${RootTarget}/libs/python/lib/RWQALinuxPCKeywords.py
Library     ${RootTarget}/libs/python/lib/qa/Sniffer/RWMacSnifferTestAppliance.py

Resource    ${ProjectTarget}/resources/keywords/vsz_suite_keywords.robot
Resource    ${ProjectTarget}/resources/keywords/scg_pubapi_keywords.robot
Resource    ${ProjectTarget}/resources/keywords/scg_pubapi_mesh_keywords.robot
Resource    ${RootTarget}/resources/keywords/qa/apcli_keywords.robot
Resource    ${RootTarget}/resources/keywords/sta_keywords.robot


Suite Setup    AVC Suite Setup
Suite Teardown    AVC Suite Teardown

*** Variables ***
${user_app_name}=    user_app_ap134
${app_policy_name}=     app_policy_ap134
${utp_name}=    utp_ap134
${wifi_channel}=   6

*** Test Cases ***
VERIFY USER DEFINED APP WITH IP AND PORT 
    [Tags]    TLID-116135 
    [Setup]   Run Keywords    Login SCG Public API   AND
    ...   APCLI User Login OK     ip addr=${AP_1_IP_ADDR}  username=${AP_LOGIN_USERNAME}  password=${AP_LOGIN_PASSWORD}   AND
    ...   Create User Defined APP and Associate with Wlan  zone_name=${APZONE_NAME}  wlan_name=${WLAN_NAME}  
    ...   app_name=${user_app_name}  app_policy_name=${app_policy_name}    type=PORT_ONLY  utp_name=${utp_name}
    
    Wait Until Keyword Succeeds  5 min  5 sec
    ...   Modify User Defined APP and Verify   app_id=${app_id}   name=${user_app_name}  type=IP_WITH_PORT    dest_ip=${TEST_ENGINE_IPV4_ADDR}    dest_netmask=255.255.255.0
    Get Avc User App
    List Not Should Contain Value    ${res}    application name: ${user_app_name}
    List Should Contain Value    ${res}    port: 6000
    List Should Contain Value    ${res}    protocol: udp
    Should Contain Match    ${res}    regexp=App_Id: \\d+
    Should Contain Match    ${res}    regexp=Cat_Id: \\d+

    [Teardown]    Run Keywords    Run Keyword and Ignore Error    
    ...    Remove User Defined APP from Wlan and Delete    zone_name=${APZONE_NAME}    wlan_name=${WLAN_NAME}    
    ...    app_name=${user_app_name}    app_policy_name=${app_policy_name}    utp_name=${utp_name}   AND
    ...    Logout SCG Public API    AND
    ...    APCLI User Logout OK

ARC:Func-Default-UserDefinedAPP-All Combinations
    [Tags]    TLID-116134 
    [Setup]   Run Keywords    Login SCG Public API   AND
    ...   APCLI User Login OK     ip addr=${AP_1_IP_ADDR}  username=${AP_LOGIN_USERNAME}  password=${AP_LOGIN_PASSWORD}   AND
    ...   Create User Defined APP and Associate with Wlan  zone_name=${APZONE_NAME}  wlan_name=${WLAN_NAME}  
    ...   app_name=${user_app_name}  app_policy_name=${app_policy_name}    type=PORT_ONLY  utp_name=${utp_name}

    #VERIFY USER DEFINED APP  WITH PORT ONLY
    Wait Until Keyword Succeeds  5 min  5 sec
    ...   Modify User Defined APP and Verify   app_id= ${app_id}   name=${user_app_name}    type=PORT_ONLY
    Get User Defined Profile Details    profile_id=${app_id}
    ${res}=    Get Avc Port Mapping 
    List Should Contain Value    ${res}    application name: ${user_app_name}
    List Should Contain Value    ${res}    port: 6000
    List Should Contain Value    ${res}    protocol: udp
    Should Contain Match    ${res}    regexp=App_Id: \\d+
    Should Contain Match    ${res}    regexp=Cat_Id: \\d+

    [Teardown]    Run Keywords    Run Keyword and Ignore Error    
    ...    Remove User Defined APP from Wlan and Delete    zone_name=${APZONE_NAME}    wlan_name=${WLAN_NAME}    
    ...    app_name=${user_app_name}    app_policy_name=${app_policy_name}    utp_name=${utp_name}   AND
    ...    Logout SCG Public API    AND
    ...    APCLI User Logout OK
    

*** Keywords ***
AVC Suite Setup
    AP Suite Setup
    Login SCG Public API
    Modify 2G Radio Configuration in Zone    zone_name=${APZONE_NAME}   channel=${wifi_channel}
    Disable AP 5G Radio    ${AP_1_MAC}
    Logout SCG Public API

AVC Suite Teardown
    AP Suite Teardown
    

Create User Defined APP and Associate with Wlan
    [Arguments]    ${zone_name}   ${wlan_name}  ${app_name}   ${app_policy_name}   ${utp_name} 
    ...    ${type}=PORT_ONLY    ${dest_ip}=None    ${dest_netmask}=None    
    ...    ${dest_port}=${6000}   ${dest_protocol}=UDP    ${rule_type}=DENY    ${rule_number}=1   
    ...    ${uplink_marking_priority}=None  ${uplink_marking_type}=None  ${downlink_classication_type}=None
    ...    ${uplink_rate_limit}=None    ${downlink_rate_limit}=None 
    ${zone_id}=    SCG Get Zone ID By Zone Name    ${zone_name}
    ${wlan_id}=    SCG Get WLAN ID    ${zone_name}    ${wlan_name}
    ${app_id}  ${app_cat}=  Create User Defined Application Profile  name=${app_name}  type=${type}  dest_port=${dest_port}
    ...   dest_protocol=${dest_protocol}  dest_ip=${dest_ip}  dest_netmask=${dest_netmask}
    Set Test Variable    ${app_id}    ${app_id}
    Set Test Variable    ${app_cat}   ${app_cat}
    ${rule}=    Construct User Defined Application Policy Rule    rule_number=${rule_number}    rule_type=${rule_type}    user_app_id=${app_cat}
    ...    uplink_marking_priority=${uplink_marking_priority}   uplink_marking_type=${uplink_marking_type}   downlink_classication_type=${downlink_classication_type}
    ...    uplink_rate_limit=${uplink_rate_limit}    downlink_rate_limit=${downlink_rate_limit}
    ${app_policy_id}=    Create Application Policy Profile    name=${app_policy_name}    rules_list=${rule}
    Set Test Variable    ${app_policy_id}   ${app_policy_id}
    ${utp_id}=    Create User Traffic Profile    name=${utp_name}    app_policy_id=${app_policy_id}
    Set Test Variable    ${utp_id}   ${utp_id}
    Configure Advanced Options in WLAN    ${zone_name}    ${wlan_name}    arc_enable=${True}
    SCG Update Wlan with User Traffic Profile    ${zone_id}    ${wlan_id}  user_traffic_profile_id=${utp_id}    user_traffic_profile_name=${utp_name}

Remove User Defined APP from Wlan and Delete
    [Arguments]    ${zone_name}    ${wlan_name}   ${app_name}    ${app_policy_name}    ${utp_name}
    ${zone_id}=    SCG Get Zone ID By Zone Name    ${zone_name}
    ${wlan_id}=    SCG Get WLAN ID    ${zone_name}    ${wlan_name}
    Configure Advanced Options in WLAN    ${zone_name}  ${wlan_name}  arc_enable=${False}
    SCG Update Wlan with User Traffic Profile    ${zone_id}    ${wlan_id}    user_traffic_profile_name=System Default 
    SCG Delete User Traffic Profile    name=${utp_name}
    ${app_policy_id}    Get Application Policy ID by Name    name=${app_policy_name}
    Delete Application Policy Profile    id=${app_policy_id}
    Delete User Defined Application Profile    ${app_id}

Modify User Defined APP and Verify
    [Arguments]    ${app_id}   ${name}=None  ${type}=None  ${dest_port}=None  ${dest_protocol}=None  ${dest_ip}=None  ${dest_netmask}=None
    Modify User Defined Application Profile   app_id=${app_id}   name=${name}    type=${type}   dest_port=${dest_port}   dest_protocol=${dest_protocol}   dest_ip=${dest_ip}   dest_netmask=${dest_netmask}
    ${res}=    Get User Defined Profile Details    profile_id=${app_id}
    Run Keyword IF    "${name}" != "None"   Dictionary Should Contain item    ${res}   key=name    value=${name}
    Run Keyword IF    "${type}" != "None"   Dictionary Should Contain item    ${res}   key=type    value=${type}
    Run Keyword IF    "${dest_port}" != "None"   Dictionary Should Contain item    ${res}   key=destPort    value=${dest_port}
    Run Keyword IF    "${dest_protocol}" != "None"   Dictionary Should Contain item    ${res}   key=protocol    value=${dest_protocol}
    Run Keyword IF    "${dest_ip}" != "None"   Dictionary Should Contain item    ${res}   key=destIp    value=${dest_ip}
    Run Keyword IF    "${dest_netmask}" != "None"   Dictionary Should Contain item    ${res}   key=netmask    value=${dest_netmask}

Modify Application Policy Profile and Verify
    [Documentation]   Used to update the application policy rules for a particular application and to verify the changes in rules
    ...    app_type (string) : USER_DEFINED | SYSTEM 
    ...    app_policy_name (string) : name of the application policy rule
    ...    app_name (string) : name of the application for with the rules should be changed
    ...    
    ...    param string rule_number       - Rule number or priority of the rule (1 to 128)
    ...    param string rule_type         - Type of Rule (DENY | QOS | RATE_LIMITING)
    ...    param string user_app_id       - User Defined Profile AppId
    ...    param string user_app_category - User Defined Profile Category (Default - 32768)
    ...
    ...    Applicable when rule_type is "QOS":
    ...    param string uplink_marking_priority     - QoS Uplink marking Priority (IEEE802_1p | DSCP | BOTH)
    ...    param string uplink_marking_type         - QoS Uplink marking type (VOICE | VIDEO | BEST_EFFORT | BACKGROUND)
    ...    param string downlink_classication_type  - QoS Downlink classification type (VOICE | VIDEO | BEST_EFFORT | BACKGROUND)
    ...
    ...    Applicable when rule_type is "RATE_LIMITING":
    ...    param int    uplink_rate_limit           - Uplink rate-limiting in Kbps (250 - 2000)
    ...    param int    downlink_rate_limit         - Downlink rate-limiting in Kbps (250 - 2000)
    [Arguments]    ${app_type}   ${app_policy_name}    ${app_name} 
    ...    ${rule_type}=None    ${priority}=None    ${app_id}=None    ${cat_id}=None
    ...    ${marking_priority}=None  ${marking_type}=None  ${classification_type}=None
    ...    ${uplink_rate_limit}=None    ${downlink_rate_limit}=None 

    ${priority}=    Run Keyword IF    "${priority}" != "None"   Convert To Integer    ${priority}
    ${cat_id}=    Run Keyword IF   "${cat_id}" != "None"   Convert To String    ${cat_id}
    ${app_id}=    Run Keyword IF   "${app_id}" != "None"   Convert To String    ${app_id}

    ${cat_id_1}  ${app_id_1}=   Run Keyword IF   "${app_name}" != "None" and "${app_type}" != "USER_DEFINED"    Get IDs by Application Name    ${app_name}   
    ...   ELSE   Set Variable   None    None

    ${rule}=    Create Dictionary    
    Run Keyword IF   "${priority}" != "None"    Set to Dictionary    ${rule}    priority=${priority}
    Run Keyword IF   "${rule_type}" != "None"    Set to Dictionary    ${rule}    ruleType=${rule_type}
    Run Keyword IF   "${app_type}" == "USER_DEFINED"    Set to Dictionary    ${rule}    applicationType=USER_DEFINED
    Run Keyword IF   "${app_type}" == "SYSTEM"    Set to Dictionary    ${rule}    applicationType=SIGNATURE
    Run Keyword IF   "${app_id}" != "None"    Set to Dictionary   ${rule}    appId=${app_id}
    ...    ELSE IF   "${app_id_1}" != "None"  Set To Dictionary   ${rule}    appId=${app_id_1}
    Run Keyword IF   "${cat_id}" != "None"    Set to Dictionary   ${rule}    catId=${cat_id}
    ...    ELSE IF   "${cat_id_1}" != "None"  Set To Dictionary   ${rule}    catId=${cat_id_1}
    Run Keyword IF   "${app_name}" != "None"    Set To Dictionary    ${rule}    appName=${app_name}
    Run Keyword IF   "${marking_priority}" != "None"    Set To Dictionary   ${rule}    markingPriority=${marking_priority}
    Run Keyword IF   "${marking_type}" != "None"    Set To Dictionary      ${rule}    markingType=${marking_type}
    Run Keyword IF   "${classification_type}" != "None"    Set To Dictionary    ${rule}    classificationType=${classification_type}
    Run Keyword IF   "${downlink_rate_limit}" != "None"    Set To Dictionary    ${rule}    downlink=${downlink_rate_limit}
    Run Keyword IF   "${uplink_rate_limit}" != "None"    Set To Dictionary     ${rule}   uplink=${uplink_rate_limit}
    ${rule_list}=    Create List    ${rule}
    Log     ${rule_list}   
    Modify Application Policy Profile   name=${app_policy_name}   rules_list=${rule_list}
    
    ${res}=    Get Application Policy Rules by Name    ${app_name}
    Run Keyword IF    "${priority}" != "None"   Dictionary Should Contain item    ${res}   key=priority    value=${priority}
    Run Keyword IF    "${rule_type}" != "None"   Dictionary Should Contain item    ${res}   key=ruleType    value=${rule_type}
    Run Keyword IF    "${app_id}" != "None"   Dictionary Should Contain item    ${res}   key=appId    value=${app_id}
    Run Keyword IF    "${cat_id}" != "None"   Dictionary Should Contain item    ${res}   key=catId    value=${cat_id}
    Run Keyword IF    "${marking_priority}" != "None"   Dictionary Should Contain item    ${res}   key=markingPriority    value=${marking_priority}
    Run Keyword IF    "${marking_type}" != "None"   Dictionary Should Contain item    ${res}   key=markingType    value=${marking_type}
    Run Keyword IF    "${classification_type}" != "None"   Dictionary Should Contain item    ${res}   key=classificationType    value=${classification_type}
    Run Keyword IF    "${uplink_rate_limit}" != "None"   Dictionary Should Contain item    ${res}   key=uplink    value=${uplink_rate_limit}
    Run Keyword IF    "${downlink_rate_limit}" != "None"   Dictionary Should Contain item    ${res}   key=downlink    value=${downlink_rate_limit}

Create System Defined APP Policy and Associate with Wlan
    [Arguments]    ${zone_name}   ${wlan_name}   ${app_name}   ${app_policy_name}   ${utp_name}   ${app_category}=None  
    ...    ${rule_type}=DENY    ${rule_number}=1   
    ...    ${uplink_marking_priority}=None  ${uplink_marking_type}=None  ${downlink_classication_type}=None
    ...    ${uplink_rate_limit}=None    ${downlink_rate_limit}=None 
    ${zone_id}=    SCG Get Zone ID By Zone Name    ${zone_name}
    ${wlan_id}=    SCG Get WLAN ID    ${zone_name}    ${wlan_name}
    ${app_id}  ${app_cat}=   Get IDs by Application Name    ${app_name}
    ${rule}=    Construct System Defined Application Policy Rule    rule_number=${rule_number}    rule_type=${rule_type}    
    ...    app_category=${app_category}  app_name=${app_name}   app_cat_id=${app_id}   app_id=${app_cat}
    ...    uplink_marking_priority=${uplink_marking_priority}   uplink_marking_type=${uplink_marking_type}   downlink_classication_type=${downlink_classication_type}
    ...    uplink_rate_limit=${uplink_rate_limit}    downlink_rate_limit=${downlink_rate_limit}
    ${app_policy_id}=    Create Application Policy Profile    name=${app_policy_name}    rules_list=${rule}
    ${utp_id}=    Create User Traffic Profile    name=${utp_name}    app_policy_id=${app_policy_id}
    Configure Advanced Options in WLAN    ${zone_name}    ${wlan_name}    arc_enable=${True}
    SCG Update Wlan with User Traffic Profile    ${zone_id}    ${wlan_id}  user_traffic_profile_id=${utp_id}    user_traffic_profile_name=${utp_name}

Remove System Defined APP Policy from Wlan and Delete 
    [Arguments]    ${zone_name}    ${wlan_name}    ${app_policy_name}    ${utp_name}
    ${zone_id}=    SCG Get Zone ID By Zone Name    ${zone_name}
    ${wlan_id}=    SCG Get WLAN ID    ${zone_name}    ${wlan_name}
    Configure Advanced Options in WLAN    ${zone_name}  ${wlan_name}  arc_enable=${False}
    SCG Update Wlan with User Traffic Profile    ${zone_id}    ${wlan_id}    user_traffic_profile_name=System Default
    SCG Delete User Traffic Profile    name=${utp_name}
    ${app_policy_id}    Get Application Policy ID by Name    name=${app_policy_name}
    Delete Application Policy Profile    id=${app_policy_id}

Send Iperf Traffic from Test Engine to Windows Client Station
    [Arguments]    ${port}    ${test_udp}
    Linux Login With Telnet    ip_addr=${TEST_ENGINE_IPV4_ADDR}  user=${TEST_ENGINE_USERNAME}  password=${TEST_ENGINE_PASSWORD}  as_root=${true}   root_password=${TEST_ENGINE_ROOT_PASSWORD} 
    Associate Client With Open WLAN    ${WIFI_WIN_STA1_ETH_IPV4_ADDR}  ${AP_1_IP_ADDR}  ${WLAN_SSID}
    ${address}=       Get Addresses
    ${iperf_server_ip}=    Get From Dictionary    ${address}    IP
    Client Start Iperf    test_udp=${test_udp}    timeout=0   port=${port}  save_res=yes  nonblock=yes
    Linux Start Iperf Client     stream_srv=${iperf_server_ip}    test_udp=${test_udp}    timeout=30    port=${port} 
    Sleep   60 s
    Linux Stop Iperf
    Client Stop Iperf
    Remove all WLAN profiles and check

Send Iperf Traffic from Test Engine to Windows Client Station And Verify Fragmentation on Test Engine
    [Arguments]    ${test_udp}    ${port}    ${packet_length}=2000
    Linux Login With Telnet    ip_addr=${TEST_ENGINE_IPV4_ADDR}  user=${TEST_ENGINE_USERNAME}  password=${TEST_ENGINE_PASSWORD}  as_root=${true}   root_password=${TEST_ENGINE_ROOT_PASSWORD} 
    Linux Set Tshark File   tshark_file=/tmp/tshark1.pcap
    Linux Start Tshark    count=0   iface=any
    Associate Client With Open WLAN    ${WIFI_WIN_STA1_ETH_IPV4_ADDR}  ${AP_1_IP_ADDR}  ${WLAN_SSID}
    ${address}=       Get Addresses
    ${iperf_server_ip}=    Get From Dictionary    ${address}    IP
    Client Start Iperf    test_udp=${test_udp}    timeout=0   port=${port}   save_res=yes   nonblock=yes
    Run Keyword If    ${test_udp}==${true} 
    ...   Linux Start Iperf Client     stream_srv=${iperf_server_ip}    test_udp=${test_udp}    timeout=30    port=${port}   packet_len=${packet_length}
    Run Keyword If    ${test_udp}==${false} 
    ...   Linux Start Iperf Client     stream_srv=${iperf_server_ip}    test_udp=${test_udp}    timeout=30    port=${port}   tcp_len=${packet_length}
    sleep    60s
    Linux Stop Iperf
    Client Stop Iperf
    Remove all WLAN profiles and check
    Linux Stop Tshark
    ${len}=   Run Keyword If   ${test_udp}==${true} 
    ...    Linux Get Tshark File Length   tshark_file=/tmp/tshark1.pcap   filter_str=udp && ip.fragments && ip.src==${TEST_ENGINE_IPV4_ADDR} && ip.dst==${iperf_server_ip}
    ...    ELSE IF   ${test_udp}==${false} 
    ...    Linux Get Tshark File Length   tshark_file=/tmp/tshark1.pcap   filter_str=tcp && ip.fragments && ip.src==${TEST_ENGINE_IPV4_ADDR} && ip.dst==${iperf_server_ip}
    Run Keyword If    ${len} <= ${0}    Fail

Send Iperf Traffic From Test Engine to Windows Client Station and Capture Packets On Windows Client
    [Arguments]    ${test_udp}    ${port}
    Set Target   host=${WIFI_WIN_STA1_ETH_IPV4_ADDR}
    Linux Login With Telnet    ip_addr=${TEST_ENGINE_IPV4_ADDR}  user=${TEST_ENGINE_USERNAME}  password=${TEST_ENGINE_PASSWORD}  as_root=${true}   root_password=${TEST_ENGINE_ROOT_PASSWORD}
    Associate Client With Open WLAN    ${WIFI_WIN_STA1_ETH_IPV4_ADDR}  ${AP_1_IP_ADDR}  ${WLAN_SSID}
    ${address}=       Get Addresses
    ${iperf_server_ip}=    Get From Dictionary    ${address}    IP
    Client Start Tshark1    interface=Wireless 
    Client Start Iperf    test_udp=${test_udp}    timeout=0   port=${port}   save_res=yes   nonblock=yes
    Linux Start Iperf Client     stream_srv=${iperf_server_ip}    test_udp=${test_udp}    timeout=30    port=${port}  
    sleep    60s
    Linux Stop Iperf
    Client Stop Iperf
    Remove all WLAN profiles and check
    Client Stop Tshark
    #client_tshark_read_cap_file    cap_file_name=tshark_capture.pcap   tshark_params=-Y 'tcp.len > 0'
    ${file}=  Copy Tshark File from Windows Client

Stop Iperf On Test Engine and Windows Station
    Set Target   host=${WIFI_WIN_STA1_ETH_IPV4_ADDR}
    Linux Stop Iperf
    Client Stop Iperf
    Remove all WLAN profiles and check

Copy Iperf Server Report from Windows Client 
    [Arguments]    ${client_ip}=${WIFI_WIN_STA1_ETH_IPV4_ADDR}   ${dest_ip}=${TFTP_SERVER_IP}
    Set Target   host=${client_ip}
    ${username}=   Get Station Username
    ${report_path}=    Catenate    SEPARATOR=    c:/\Users/\   ${username}   /\Downloads/\srv.txt
    ${file_config}=    Create Dictionary    ip_address=${dest_ip}    filepath=${report_path}
    Transfer File To Remote Server    ${file_config}
    ${file}=   OperatingSystem.Get File    path=${TEST_ENGINE_TFTP_BOOT}/srv.txt
    Log    ${file}
    [return]   ${file}

Copy Tshark File from Windows Client
    [Arguments]    ${client_ip}=${WIFI_WIN_STA1_ETH_IPV4_ADDR}   ${dest_ip}=${TFTP_SERVER_IP}
    Set Target   host=${client_ip}
    ${file_config}=    Create Dictionary    ip_address=${dest_ip}    filepath=C:\rwqaauto\elements\rat22cs\tshark_capture.pcap
    Transfer File To Remote Server    ${file_config}
    ${file}=   OperatingSystem.Get File    path=${TEST_ENGINE_TFTP_BOOT}/tshark_capture.pcap
    Log    ${file}
    [return]   ${file}

Start Mac Sniffer On Channel
    [Arguments]    ${mac_ip}=${MAC_SNIFFER_HOST}    ${mac_username}=${MAC_USERNAME}    ${mac_password}=${MAC_PASSWORD}    ${channel}=6   ${filename}=capture.pcap
    Ssh Connection Mac Sniffer      mac_ipaddr=${mac_ip}     username=${mac_username}  password=${mac_password}
    set_sniffer_channel  channel=${channel}
    start_sniffer    filename=/tmp/${filename}

Stop Mac Sniffer    
    [Arguments]    ${mac_ip}=${MAC_SNIFFER_HOST}    ${mac_username}=${MAC_USERNAME}    ${mac_password}=${MAC_PASSWORD}    ${filename}=capture.pcap
    #Ssh Connection Mac Sniffer      mac_ipaddr=${mac_ip}     username=${mac_username}  password=${mac_password}
    stop_sniffer
    get_captured_file    filename=/tmp/${filename}   localfile=/opt/tftpboot/${filename}
    OperatingSystem.File Should Exist     /opt/tftpboot/${filename}
    Ssh Close Connection

Get Pcap Entry Length   
    [Arguments]    ${filter}    ${filename}=capture.pcap
    ${res}=    linux_get_tshark_file_length    /opt/tftpboot/${filename}   filter_str=(${filter})
    [Return]    ${res}
    
Check If Rule is Applied in AP
    [Arguments]    ${user_app_name}   ${app_policy_name}    ${utp_name}
    ${policy_info}=    Get Arc App Policy    2
    Should Contain Match    ${policy_info}    regexp=UTP Name\\s*:\\s*${utp_name}\\s*ID\\s*:\\s*\\d+
    Should Contain Match    ${policy_info}    regexp=Policy Name\\s*:\\s*${app_policy_name}
    Should Contain Match    ${policy_info}    regexp=App Name\\s*:\\s*${user_app_name}
