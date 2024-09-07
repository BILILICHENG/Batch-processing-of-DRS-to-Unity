@echo off
setlocal enabledelayedexpansion

echo ---------------------------------------------------------------
echo https://github.com/BILILICHENG/Batch-processing-of-DRS-to-Unity
echo ---------------------------------------------------------------
echo ---------------------------------------------------------------
echo 请将音乐文件夹【music】拖放至这里并且按下回车
echo ---------------------------------------------------------------
set /p name=

echo ---------------------------------------------------------------
echo 请将Python脚本【drs_parse_000001.py】拖放至这里并且按下回车
echo 注意注意！最终转换的文本文件将放置在与【drs_parse_000001.py】的Python脚本同目录！
echo 因此请您提前将【drs_parse_000001.py】的Python脚本放好后再拖到这里！！
echo ---------------------------------------------------------------
echo 请注意！由于是批处理！并且由于【LI_CHENG】对于该代码写的很烂
echo 因此最终执行所需要的时间取决于歌曲的多少
echo 请您耐心等待！！！完成后将自动关闭该窗口！
echo ---------------------------------------------------------------

set /p pyname=

for /d %%i in ("%name%\*") do (
    for %%j in ("%%i\*.xml") do (
        echo Processing: %%j
        python "%pyname%" "%%j"
    )
)
 
endlocal
echo ---------------------------------------------------------------
echo 已全部执行成功！如果没问题的话请按下回车结束！
echo ---------------------------------------------------------------
pause