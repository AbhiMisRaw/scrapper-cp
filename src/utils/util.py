import asyncio
import json
import aiofiles

INDENT = 4

async def write_json_async(filename, data):
    # Convert Python dictionary to a JSON string first
    json_string = json.dumps(data, indent=INDENT)
    
    # Open and write to the file asynchronously
    async with aiofiles.open(filename, mode='w') as f:
        await f.write(json_string)


def print_hiring_lens():
    print("="*40)
    print("--"*20)
    print("")
    print(" ","="*6, "HIRING LENS IS STARTING","="*6)
    print("")
    print("-"*40)
    print("="*40)