Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "D:\Projects\FengVoice"
WshShell.Run "python -m uvicorn main:app --host 0.0.0.0 --port 8000", 0, False
WScript.Sleep 2000
WshShell.Run "npm run dev -- --host 0.0.0.0 --port 3000", 0, False
