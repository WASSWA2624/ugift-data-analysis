Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
using System.Collections.Generic;
public static class FileLock {
  [StructLayout(LayoutKind.Sequential)]
  public struct RM_UNIQUE_PROCESS {
    public int dwProcessId;
    public System.Runtime.InteropServices.ComTypes.FILETIME ProcessStartTime;
  }
  [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
  public struct RM_PROCESS_INFO {
    public RM_UNIQUE_PROCESS Process;
    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 256)]
    public string strAppName;
    [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 64)]
    public string strServiceShortName;
    public int ApplicationType;
    public uint AppStatus;
    public uint TSSessionId;
    [MarshalAs(UnmanagedType.Bool)]
    public bool bRestartable;
  }
  [DllImport("rstrtmgr.dll", CharSet = CharSet.Unicode)]
  public static extern int RmStartSession(out uint pSessionHandle, int dwSessionFlags, string strSessionKey);
  [DllImport("rstrtmgr.dll")]
  public static extern int RmEndSession(uint pSessionHandle);
  [DllImport("rstrtmgr.dll", CharSet = CharSet.Unicode)]
  public static extern int RmRegisterResources(uint pSessionHandle, uint nFiles, string[] rgsFilenames, uint nApplications, IntPtr rgApplications, uint nServices, IntPtr rgsServiceNames);
  [DllImport("rstrtmgr.dll")]
  public static extern int RmGetList(uint dwSessionHandle, out uint pnProcInfoNeeded, ref uint pnProcInfo, [In, Out] RM_PROCESS_INFO[] rgAffectedApps, ref uint lpdwRebootReasons);
  public static string[] Who(string path) {
    uint handle;
    string key = Guid.NewGuid().ToString();
    int rc = RmStartSession(out handle, 0, key);
    if (rc != 0) return new string[] { "start " + rc };
    try {
      rc = RmRegisterResources(handle, 1, new string[] { path }, 0, IntPtr.Zero, 0, IntPtr.Zero);
      if (rc != 0) return new string[] { "reg " + rc };
      uint needed = 0, count = 0, reboot = 0;
      rc = RmGetList(handle, out needed, ref count, null, ref reboot);
      if (needed == 0) return new string[] { "none" };
      var arr = new RM_PROCESS_INFO[needed];
      count = needed;
      rc = RmGetList(handle, out needed, ref count, arr, ref reboot);
      var lines = new List<string>();
      for (int i = 0; i < count; i++) lines.Add(arr[i].Process.dwProcessId + " " + arr[i].strAppName);
      return lines.ToArray();
    } finally { RmEndSession(handle); }
  }
}
"@
$path = "D:\coding\ugift-data-analysis\outputs\narrative-report\UgIFT Asset Verification Report.pdf"
[FileLock]::Who($path)
