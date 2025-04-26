import json
# chart = "Turning POINT"
chart = "win10"
with open(f'resources/chart/{chart}.json', 'r', encoding='utf-8') as file:
# with open('D:\\rpe\\PhiEdit\\Resources\\2335887341837385\\2335887341837385.json', 'r', encoding='utf-8') as file:
    chartFiles = file.read()
    chartFiles = json.loads(chartFiles)

NumberOfLines = len(chartFiles['judgeLineList'])
bpm = chartFiles["BPMList"][0]["bpm"]

