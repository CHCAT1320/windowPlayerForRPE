import json
chart = "chart1"
with open(f'resources/chart/{chart}.json', 'r', encoding='utf-8') as file:
# with open('D:\\rpe\\PhiEdit\\Resources\\4203267478680411\\4203267478680411.json', 'r', encoding='utf-8') as file:
    chartFiles = file.read()
    chartFiles = json.loads(chartFiles)

NumberOfLines = len(chartFiles['judgeLineList'])
bpm = chartFiles["BPMList"][0]["bpm"]

