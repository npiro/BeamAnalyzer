<?xml version='1.0'?>
<Project Type="Project" LVVersion="8208000">
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
      <Item Name="lensCluster.vi" Type="VI" URL="lensCluster.vi"/>
      <Item Name="BeamAnalyzer.vi" Type="VI" URL="BeamAnalyzer.vi"/>
      <Item Name="PlotControl.ctl" Type="VI" URL="PlotControl.ctl"/>
      <Item Name="PropagateBeam.vi" Type="VI" URL="PropagateBeam.vi"/>
      <Item Name="MultiplyMatrixRows.vi" Type="VI" URL="MultiplyMatrixRows.vi"/>
      <Item Name="MultiplyMatrices.vi" Type="VI" URL="MultiplyMatrices.vi"/>
      <Item Name="MultiplyMatrixElements.vi" Type="VI" URL="MultiplyMatrixElements.vi"/>
      <Item Name="PropagateBeamNumeric.vi" Type="VI" URL="PropagateBeamNumeric.vi"/>
      <Item Name="QtoBeamDiameter.vi" Type="VI" URL="QtoBeamDiameter.vi"/>
      <Item Name="Dependencies" Type="Dependencies"/>
      <Item Name="Build Specifications" Type="Build">
         <Item Name="BeamAnalyzer" Type="EXE">
            <Property Name="Absolute[0]" Type="Bool">false</Property>
            <Property Name="Absolute[1]" Type="Bool">false</Property>
            <Property Name="Absolute[2]" Type="Bool">false</Property>
            <Property Name="ActiveXServerName" Type="Str"></Property>
            <Property Name="AliasID" Type="Str">{C8A10449-A0F8-4BE3-980C-B0BAF3054AF6}</Property>
            <Property Name="AliasName" Type="Str">Project.aliases</Property>
            <Property Name="ApplicationID" Type="Str">{7B24AD39-E546-49CB-9386-48549D1A6ED1}</Property>
            <Property Name="ApplicationName" Type="Str">BeamAnalyzer.exe</Property>
            <Property Name="AutoIncrement" Type="Bool">false</Property>
            <Property Name="BuildName" Type="Str">BeamAnalyzer</Property>
            <Property Name="CommandLineArguments" Type="Bool">false</Property>
            <Property Name="CopyErrors" Type="Bool">false</Property>
            <Property Name="DebuggingEXE" Type="Bool">false</Property>
            <Property Name="DebugServerWaitOnLaunch" Type="Bool">false</Property>
            <Property Name="DefaultLanguage" Type="Str">English</Property>
            <Property Name="DependencyApplyDestination" Type="Bool">true</Property>
            <Property Name="DependencyApplyInclusion" Type="Bool">true</Property>
            <Property Name="DependencyApplyProperties" Type="Bool">true</Property>
            <Property Name="DependencyFolderDestination" Type="Int">0</Property>
            <Property Name="DependencyFolderInclusion" Type="Str">As needed</Property>
            <Property Name="DependencyFolderPropertiesItemCount" Type="Int">0</Property>
            <Property Name="DestinationID[0]" Type="Str">{B22F75F9-12FF-43FF-97BA-75900C80B679}</Property>
            <Property Name="DestinationID[1]" Type="Str">{B22F75F9-12FF-43FF-97BA-75900C80B679}</Property>
            <Property Name="DestinationID[2]" Type="Str">{0F7E1BB0-75CB-4DA5-96B1-484C989EB91F}</Property>
            <Property Name="DestinationItemCount" Type="Int">3</Property>
            <Property Name="DestinationName[0]" Type="Str">BeamAnalyzer.exe</Property>
            <Property Name="DestinationName[1]" Type="Str">Destination Directory</Property>
            <Property Name="DestinationName[2]" Type="Str">Support Directory</Property>
            <Property Name="Disconnect" Type="Bool">true</Property>
            <Property Name="IncludeHWConfig" Type="Bool">false</Property>
            <Property Name="IncludeSCC" Type="Bool">true</Property>
            <Property Name="INIID" Type="Str">{1FBF8295-7FAF-46F6-AFA3-E578206C49CC}</Property>
            <Property Name="ININame" Type="Str">LabVIEW.ini</Property>
            <Property Name="LOGID" Type="Str">{A3FE70BC-12EC-42CD-B7BC-E108EEDBFBD9}</Property>
            <Property Name="MathScript" Type="Bool">false</Property>
            <Property Name="Path[0]" Type="Path">../../builds/BeamAnalyzer/BeamAnalyzer/internal.llb</Property>
            <Property Name="Path[1]" Type="Path">../../builds/BeamAnalyzer/BeamAnalyzer</Property>
            <Property Name="Path[2]" Type="Path">../../builds/BeamAnalyzer/BeamAnalyzer/data</Property>
            <Property Name="ShowHWConfig" Type="Bool">false</Property>
            <Property Name="SourceInfoItemCount" Type="Int">5</Property>
            <Property Name="SourceItem[0].Inclusion" Type="Str">Startup VI</Property>
            <Property Name="SourceItem[0].ItemID" Type="Ref">/My Computer/BeamAnalyzer.vi</Property>
            <Property Name="SourceItem[1].Inclusion" Type="Str">Always Included</Property>
            <Property Name="SourceItem[1].ItemID" Type="Ref">/My Computer/PropagateBeam.vi</Property>
            <Property Name="SourceItem[2].Inclusion" Type="Str">Always Included</Property>
            <Property Name="SourceItem[2].ItemID" Type="Ref">/My Computer/MultiplyMatrixRows.vi</Property>
            <Property Name="SourceItem[3].Inclusion" Type="Str">Always Included</Property>
            <Property Name="SourceItem[3].ItemID" Type="Ref">/My Computer/MultiplyMatrices.vi</Property>
            <Property Name="SourceItem[4].Inclusion" Type="Str">Always Included</Property>
            <Property Name="SourceItem[4].ItemID" Type="Ref">/My Computer/MultiplyMatrixElements.vi</Property>
            <Property Name="StripLib" Type="Bool">true</Property>
            <Property Name="SupportedLanguageCount" Type="Int">0</Property>
            <Property Name="TLBID" Type="Str">{1DF6DC30-CBBA-42AA-8DCD-D451089E18D3}</Property>
            <Property Name="UseFFRTE" Type="Bool">false</Property>
            <Property Name="VersionInfoCompanyName" Type="Str">ICFO</Property>
            <Property Name="VersionInfoFileDescription" Type="Str"></Property>
            <Property Name="VersionInfoFileType" Type="Int">1</Property>
            <Property Name="VersionInfoFileVersionBuild" Type="Int">0</Property>
            <Property Name="VersionInfoFileVersionMajor" Type="Int">1</Property>
            <Property Name="VersionInfoFileVersionMinor" Type="Int">0</Property>
            <Property Name="VersionInfoFileVersionPatch" Type="Int">0</Property>
            <Property Name="VersionInfoInternalName" Type="Str">Beam Analyzer</Property>
            <Property Name="VersionInfoLegalCopyright" Type="Str">Copyright © 2007 ICFO</Property>
            <Property Name="VersionInfoProductName" Type="Str">Beam Analyzer</Property>
         </Item>
      </Item>
   </Item>
</Project>
