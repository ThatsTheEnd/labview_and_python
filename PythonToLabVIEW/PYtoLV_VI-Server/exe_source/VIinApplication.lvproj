<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="25008000">
	<Property Name="NI.LV.All.SaveVersion" Type="Str">25.0</Property>
	<Property Name="NI.LV.All.SourceOnly" Type="Bool">true</Property>
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Python" Type="Folder">
			<Item Name="Send-To-Queue.py" Type="Document" URL="../Send-To-Queue.py"/>
		</Item>
		<Item Name="main.vi" Type="VI" URL="../main.vi"/>
		<Item Name="sendqueue.vi" Type="VI" URL="../sendqueue.vi"/>
		<Item Name="Dependencies" Type="Dependencies"/>
		<Item Name="Build Specifications" Type="Build">
			<Item Name="My Application" Type="EXE">
				<Property Name="App_copyErrors" Type="Bool">true</Property>
				<Property Name="App_INI_aliasGUID" Type="Str">{37E07243-565A-469E-A607-D2DF1DEEFCBE}</Property>
				<Property Name="App_INI_GUID" Type="Str">{69067D75-B4C9-4671-BF8E-55922F205BAE}</Property>
				<Property Name="App_serverConfig.httpPort" Type="Int">8002</Property>
				<Property Name="App_serverType" Type="Int">0</Property>
				<Property Name="App_winsec.description" Type="Str">http://www.Datatec.com</Property>
				<Property Name="Bld_autoIncrement" Type="Bool">true</Property>
				<Property Name="Bld_buildCacheID" Type="Str">{B67E7DF2-C4F4-44EF-8B44-D640F79E97EE}</Property>
				<Property Name="Bld_buildSpecName" Type="Str">My Application</Property>
				<Property Name="Bld_excludeInlineSubVIs" Type="Bool">true</Property>
				<Property Name="Bld_excludeLibraryItems" Type="Bool">true</Property>
				<Property Name="Bld_excludePolymorphicVIs" Type="Bool">true</Property>
				<Property Name="Bld_localDestDir" Type="Path">../executable</Property>
				<Property Name="Bld_localDestDirType" Type="Str">relativeToCommon</Property>
				<Property Name="Bld_modifyLibraryFile" Type="Bool">true</Property>
				<Property Name="Bld_previewCacheID" Type="Str">{B90B6C19-0312-4703-9F5E-C52EB3C46039}</Property>
				<Property Name="Bld_version.build" Type="Int">3</Property>
				<Property Name="Bld_version.major" Type="Int">1</Property>
				<Property Name="Destination[0].destName" Type="Str">Application.exe</Property>
				<Property Name="Destination[0].path" Type="Path">../executable/Application.exe</Property>
				<Property Name="Destination[0].preserveHierarchy" Type="Bool">true</Property>
				<Property Name="Destination[0].type" Type="Str">App</Property>
				<Property Name="Destination[1].destName" Type="Str">Support Directory</Property>
				<Property Name="Destination[1].path" Type="Path">../executable/data</Property>
				<Property Name="DestinationCount" Type="Int">2</Property>
				<Property Name="Exe_actXinfo_enumCLSID[0]" Type="Str">{6BFC0C0B-43F2-4F50-A891-2B28CA8D5C97}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[1]" Type="Str">{4FB18EAC-C85B-4700-9A68-21D99AC5A457}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[10]" Type="Str">{A337327E-3597-49A3-BD7A-E77EE8D051AA}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[11]" Type="Str">{F0340945-DAA8-4D45-8B25-DE5B5FA99378}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[12]" Type="Str">{0F3343B0-A12C-4A5D-8A22-BAAF091F99D9}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[13]" Type="Str">{A3FFEE02-32F9-463B-9B89-C92DA460ABCA}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[14]" Type="Str">{089DBB8F-9096-4363-BA30-3733F6C2796A}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[15]" Type="Str">{12BE3A2F-FB8E-4D8A-977E-F3C2AED9E9C8}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[16]" Type="Str">{0DD66DE0-6D3A-422F-A374-6B5CC54D79C2}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[2]" Type="Str">{18FE9102-E0D6-4157-802F-EAB2ADE87D50}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[3]" Type="Str">{EAB3F1F1-BB94-4335-A098-D0D0072A6380}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[4]" Type="Str">{BA6767A7-F378-4CC1-A639-F160A03B5EB2}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[5]" Type="Str">{501AD159-19C1-404D-A040-E7935F600A6E}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[6]" Type="Str">{A0412987-315C-4527-9FEA-42F017234FB4}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[7]" Type="Str">{DAB21DB5-97C3-4F1A-96E4-E15F057FC902}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[8]" Type="Str">{C0FB6A4B-7094-4E95-9B42-95341DE10D82}</Property>
				<Property Name="Exe_actXinfo_enumCLSID[9]" Type="Str">{04B9E6C3-4E60-42CC-9F54-D6C86EA23E9C}</Property>
				<Property Name="Exe_actXinfo_enumCLSIDsCount" Type="Int">17</Property>
				<Property Name="Exe_actXinfo_majorVersion" Type="Int">5</Property>
				<Property Name="Exe_actXinfo_minorVersion" Type="Int">5</Property>
				<Property Name="Exe_actXinfo_objCLSID[0]" Type="Str">{932D7418-D92B-4442-83C3-92F5D28F1FB8}</Property>
				<Property Name="Exe_actXinfo_objCLSID[1]" Type="Str">{0E69F37B-AA55-4AE6-A64A-E97AB7E9679A}</Property>
				<Property Name="Exe_actXinfo_objCLSID[10]" Type="Str">{ADBF579A-8FC2-4385-BAE2-E9368EC8C263}</Property>
				<Property Name="Exe_actXinfo_objCLSID[11]" Type="Str">{B8DC24E1-233F-481B-8676-16573BA77B8B}</Property>
				<Property Name="Exe_actXinfo_objCLSID[12]" Type="Str">{2B4E8999-1483-4C95-AD8D-B1B67964E0FA}</Property>
				<Property Name="Exe_actXinfo_objCLSID[13]" Type="Str">{76B5AB24-D54F-4482-BE38-19F60A490240}</Property>
				<Property Name="Exe_actXinfo_objCLSID[2]" Type="Str">{9C7513B9-EB23-4EEA-BBFC-F44A7EF1BCCC}</Property>
				<Property Name="Exe_actXinfo_objCLSID[3]" Type="Str">{140F2905-D147-4579-8284-CBA3F19138A9}</Property>
				<Property Name="Exe_actXinfo_objCLSID[4]" Type="Str">{8185C810-3454-4489-9847-5F3069E7E2E8}</Property>
				<Property Name="Exe_actXinfo_objCLSID[5]" Type="Str">{5A97E383-FC5A-4905-94D4-45622A40F715}</Property>
				<Property Name="Exe_actXinfo_objCLSID[6]" Type="Str">{41110812-BE48-4AED-A805-4C175ED80854}</Property>
				<Property Name="Exe_actXinfo_objCLSID[7]" Type="Str">{E0462E1E-2AD4-4CD1-9D77-C6241976DDC4}</Property>
				<Property Name="Exe_actXinfo_objCLSID[8]" Type="Str">{B40C16D1-50D2-4DD4-B1FC-ECEF2BCD525E}</Property>
				<Property Name="Exe_actXinfo_objCLSID[9]" Type="Str">{AE77A64F-6EF6-44AD-B2D7-B72000461ABB}</Property>
				<Property Name="Exe_actXinfo_objCLSIDsCount" Type="Int">14</Property>
				<Property Name="Exe_actXinfo_progIDPrefix" Type="Str">MyLvApp</Property>
				<Property Name="Exe_actXServerName" Type="Str">MyLvApp</Property>
				<Property Name="Exe_actXServerNameGUID" Type="Str">{6132DCEF-5619-4C1D-A1D2-06CF0FC5D451}</Property>
				<Property Name="Source[0].itemID" Type="Str">{CDC7407F-0433-4932-BB6E-72E885180DCE}</Property>
				<Property Name="Source[0].type" Type="Str">Container</Property>
				<Property Name="Source[1].destinationIndex" Type="Int">0</Property>
				<Property Name="Source[1].itemID" Type="Ref">/My Computer/main.vi</Property>
				<Property Name="Source[1].sourceInclusion" Type="Str">TopLevel</Property>
				<Property Name="Source[1].type" Type="Str">VI</Property>
				<Property Name="SourceCount" Type="Int">2</Property>
				<Property Name="TgtF_companyName" Type="Str">Datatec</Property>
				<Property Name="TgtF_fileDescription" Type="Str">My Application</Property>
				<Property Name="TgtF_internalName" Type="Str">My Application</Property>
				<Property Name="TgtF_legalCopyright" Type="Str">Copyright © 2025 Datatec</Property>
				<Property Name="TgtF_productName" Type="Str">My Application</Property>
				<Property Name="TgtF_targetfileGUID" Type="Str">{873C3D71-C9C3-4188-A922-B274F9DFF0E0}</Property>
				<Property Name="TgtF_targetfileName" Type="Str">Application.exe</Property>
				<Property Name="TgtF_versionIndependent" Type="Bool">true</Property>
			</Item>
		</Item>
	</Item>
</Project>
