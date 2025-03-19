# utils.py

import requests
import json

def translate_text(text, target_language):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "deepseek/deepseek-r1-distill-qwen-32b:free",
            "messages": [
                {
                    "role": "user",
                    "content": f"Translate the following text to {target_language}: {text}"
                }
            ],
        })
    )
    return response.json()['choices'][0]['message']['content']

def parse_srt(file_content):
    subtitles = []
    for block in file_content.split('\n\n'):
        if block.strip():
            lines = block.split('\n')
            subtitles.append({
                'index': lines[0],
                'time': lines[1],
                'text': ' '.join(lines[2:])
            })
    return subtitles

def generate_srt(subtitles):
    srt_content = ""
    for sub in subtitles:
        srt_content += f"{sub['index']}\n{sub['time']}\n{sub['text']}\n\n"
    return srt_content
