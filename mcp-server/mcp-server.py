import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
from mcp.server.fastmcp import FastMCP
import os
from pathlib import Path

mcp = FastMCP("OS-Agent-MCP-Server", host="0.0.0.0", port=8001)

@mcp.tool()
def list_directory(dir_path: str) -> list[str]:
    dir_path = Path(dir_path)
    if not dir_path.is_dir():
        return [f"Error: No such file or directory: '{dir_path}'"]
    try:
        return [item.name for item in dir_path.iterdir()]
    except Exception as e:
        return f"Error: {e}"
    
@mcp.tool()
def get_file_content(file_path: str) -> str:
    file_path = Path(file_path)
    if not file_path.is_file():
        return f"Error: No such file: '{file_path}'"
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error: {e}"

def getFilesAndDirs(path: Path, files: list[str], dirs: list[str]) -> tuple[list[str], list[str]]:
    if path.is_file():
        files.append(str(path))
    elif path.is_dir():
        dirs.append(str(path))
        for entry in path.iterdir():
            getFilesAndDirs(entry, files, dirs)
    return files, dirs

@mcp.tool()
def list_directory_recursive(dir_path: str) -> tuple[list[str], list[str]]:
    dir_path = Path(dir_path)
    if not dir_path.is_dir():
        return [f"Error: No such file or directory: '{dir_path}'"]
    try:
        files, dirs = getFilesAndDirs(dir_path, [], [])
        result = (dirs, files)
        return result
    except Exception as e:
        return f"Error: {e}"
    
@mcp.tool()
def read_files_in_directory(dir_path: str) -> dict[str, str]:
    dir_path = Path(dir_path)
    if not dir_path.is_dir():
        return { "Error": f"No such file or directory: '{dir_path}'" }
    file_contents = {}
    try:
        for entry in dir_path.iterdir():
            if entry.is_file():
                try:
                    with open(entry, 'r', encoding='utf-8') as file:
                        file_contents[str(entry)] = file.read()
                except Exception as e:
                    file_contents[str(entry)] = f"Error: {e}"
        return file_contents
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def read_files_recursively(dir_path: str) -> dict[str, str]:
    dir_path = Path(dir_path)
    if not dir_path.is_dir():
        return { "Error": f"No such file or directory: '{dir_path}'" }
    file_contents = {}
    try:
        for root, _, files in os.walk(dir_path):
            for file_name in files:
                file_path = Path(root) / file_name
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        file_contents[str(file_path)] = file.read()
                except Exception as e:
                    file_contents[str(file_path)] = f"Error: {e}"
        return file_contents
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def delete_file(file_path: str) -> str:
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return f"Error: No such file: '{file_path}'"
    try:
        os.remove(file_path)
        return f"File '{file_path}' deleted successfully."
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def delete_folder(folder_path: str) -> str:
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return f"Error: No such directory: '{folder_path}'"
    try:
        os.rmdir(folder_path)
        return f"Directory '{folder_path}' deleted successfully."
    except Exception as e:
        return f"Error: {e}"
    
if __name__ == "__main__":
    try:
        mcp.run(transport="streamable-http", mount_path="/mcp")
    except ConnectionResetError:
        pass