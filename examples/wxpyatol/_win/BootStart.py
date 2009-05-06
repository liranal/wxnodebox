'''
#include <windows.h>
#include <tchar.h>

// Register program to be started at BOOT time!
//
//PARAMETERS:
// LPCTSTR lpValueName  // name of the value to set (can be anything, but must be unique for this app)
// LPCTSTR lpAppPath    // FULL PATH to APP
//
//RETURNS: TRUE on success

BOOL IsBootKeySet(LPCTSTR lpValueName);
BOOL RunProgramAtBoot(LPCTSTR lpValueName, LPCTSTR lpAppPath, BOOL bSet=TRUE);
#include 'bootstart.h'

BOOL RunProgramAtBoot(LPCTSTR lpValueName, LPCTSTR lpAppPath, BOOL bSet)
{
	HKEY keyRun = NULL;

	//open registry key with read/write access
	LONG lRes=RegOpenKeyEx( HKEY_LOCAL_MACHINE,
        'Software\\Microsoft\\Windows\\CurrentVersion\\Run',
		(DWORD) 0, KEY_ALL_ACCESS, &keyRun);

	if(ERROR_SUCCESS==lRes)
	{
		if(bSet){
			//register for boot startup
			lRes=RegSetValueEx(keyRun,
				lpValueName, (DWORD) 0, REG_SZ,
				(CONST BYTE *) lpAppPath, (DWORD) (_tcslen(lpAppPath)+1)*sizeof(TCHAR) );
		}
		else{
			//unregister boot startup (remove registry key)
			lRes=RegDeleteValue(keyRun, lpValueName);
		}
	}
	RegCloseKey(keyRun);
	return (ERROR_SUCCESS==lRes);
}

BOOL IsBootKeySet(LPCTSTR lpValueName)
{
	HKEY keyRun = NULL;

	//open registry key with read/write access
    LONG lRes=RegOpenKeyEx( HKEY_VFS_LOCAL_MACHINE,
        'Software\\Microsoft\\Windows\\CurrentVersion\\Run',
		(DWORD) 0, KEY_ALL_ACCESS, &keyRun);

	if(ERROR_SUCCESS==lRes)
	{
		DWORD dwValueSize = 0;
		lRes=RegQueryValueEx(keyRun, lpValueName,
				NULL, NULL,	NULL, &dwValueSize);
		//TOFIX could check if the the value matches app path
	}
	RegCloseKey(keyRun);
	return (ERROR_SUCCESS==lRes);
}

'''
