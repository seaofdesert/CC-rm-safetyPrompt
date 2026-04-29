@echo off
setlocal

@rem 将这段代码放在需要获取uac权限的bat前面
@echo off
NET SESSION >nul 2>&1 && goto noUAC
title.
set n=%0 %*
set n=%n:"=" ^& Chr(34) ^& "%
echo Set objShell = CreateObject("Shell.Application")>"%tmp%\cmdUAC.vbs"
echo objShell.ShellExecute "cmd.exe", "/c start " ^& Chr(34) ^& "." ^& Chr(34) ^& " /d " ^& Chr(34) ^& "%CD%" ^& Chr(34) ^& " cmd /c %n%", "", "runas", ^1>>"%tmp%\cmdUAC.vbs"
echo Not Admin, Attempting to elevate...
cscript "%tmp%\cmdUAC.vbs" //Nologo
del "%tmp%\cmdUAC.vbs"
exit /b
:noUAC

::-----Normal Batch Starts Here---------------------
:: 获取脚本所在目录
set "SCRIPT_DIR=%~dp0"
:: 去除末尾反斜杠
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

:: 转义路径中的反斜杠（注册表需要双反斜杠）
set "REG_SCRIPT_DIR=%SCRIPT_DIR:\=\\%"

:: 图标路径：脚本目录下的 Claude.ico
set "REG_ICON_PATH=%REG_SCRIPT_DIR%\\Claude.ico"

:: bat 脚本路径
set "REG_BAT_PATH=%REG_SCRIPT_DIR%\\start_with_dir.bat"

:: 创建临时注册表文件
set "REG_FILE=%TEMP%\claude_context_menu_%RANDOM%.reg"

(
echo Windows Registry Editor Version 5.00
echo.
echo [HKEY_CLASSES_ROOT\Directory\shell\Claude_Crack]
echo @="Claude破解版"
echo "Icon"="%REG_ICON_PATH%"
echo.
echo [HKEY_CLASSES_ROOT\Directory\shell\Claude_Crack\command]
echo @="C:\\Windows\\System32\\cmd.exe /c call "%REG_BAT_PATH%" "%%1""
echo.
echo [HKEY_CLASSES_ROOT\Directory\Background\shell\Claude_Crack]
echo @="Claude破解版"
echo "Icon"="%REG_ICON_PATH%"
echo.
echo [HKEY_CLASSES_ROOT\Directory\Background\shell\Claude_Crack\command]
echo @="C:\\Windows\\System32\\cmd.exe /c call "%REG_BAT_PATH%" "%%V""
) > "%REG_FILE%"

:: 导入注册表
reg import "%REG_FILE%" >nul 2>&1
if %errorLevel% equ 0 (
    echo 右键菜单添加成功！
) else (
    echo 添加失败，请检查是否以管理员权限运行。
)

:: 清理临时文件
del "%REG_FILE%" >nul 2>&1

pause
