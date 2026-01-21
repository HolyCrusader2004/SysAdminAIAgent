import sys
import asyncio

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from mcp.server.fastmcp import FastMCP
from mcp.server.auth.settings import AuthSettings
from pydantic import AnyHttpUrl
import os
from pathlib import Path

mcp = FastMCP("OS-Agent-MCP-Server", host="0.0.0.0", port=8001)

@mcp.tool()
def list_directory(dir_path: str) -> list[str]:
    dir_path = Path(dir_path)
    if not dir_path.is_dir():
        error_msg = f"Error: No such file or directory: '{dir_path}'"
        return [error_msg]
    try:
        items = [item.name for item in dir_path.iterdir()]
        return items
    except Exception as e:
        error_msg = f"Error: {e}"
        return [error_msg]

@mcp.tool()
def get_file_content(file_path: str) -> str:
    file_path = Path(file_path)
    if file_path.name == "flag.txt":
        return "Error: Access to 'flag.txt' is restricted."
    
    if not file_path.is_file():
        error_msg = f"Error: No such file: '{file_path}'"
        return error_msg
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except Exception as e:
        error_msg = f"Error: {e}"
        return error_msg

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
        error_msg = f"Error: No such file or directory: '{dir_path}'"
        return ([error_msg], [])
    try:
        files, dirs = getFilesAndDirs(dir_path, [], [])
        return (dirs, files)
    except Exception as e:
        error_msg = f"Error: {e}"
        return ([error_msg], [])

@mcp.tool()
def read_files_in_directory(dir_path: str) -> dict[str, str]:
    dir_path = Path(dir_path)
    if not dir_path.is_dir():
        return {"Error": f"No such file or directory: '{dir_path}'"}
    
    file_contents = {}
    try:
        for entry in dir_path.iterdir():
            if entry.is_file():
                if entry.name == "flag.txt":
                    continue
                try:
                    with open(entry, 'r', encoding='utf-8') as file:
                        file_contents[str(entry)] = file.read()
                except Exception as e:
                    file_contents[str(entry)] = f"Error: {e}"
        return file_contents
    except Exception as e:
        return {"Error": f"{e}"}

@mcp.tool()
def read_files_recursively(dir_path: str) -> dict[str, str]:
    dir_path = Path(dir_path)
    if not dir_path.is_dir():
        return {"Error": f"No such file or directory: '{dir_path}'"}
    
    file_contents = {}
    try:
        for root, _, files in os.walk(dir_path):
            for file_name in files:
                file_path = Path(root) / file_name
                if file_path.name == "flag.txt":
                    continue
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        file_contents[str(file_path)] = file.read()
                except Exception as e:
                    file_contents[str(file_path)] = f"Error: {e}"
        return file_contents
    except Exception as e:
        return {"Error": f"{e}"}

@mcp.tool()
def delete_file(file_path: str) -> str:
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return f"Error: No such file: '{file_path}'"
    try:
        os.remove(file_path)
        msg = f"File '{file_path}' deleted successfully."
        return msg
    except Exception as e:
        error_msg = f"Error: {e}"
        return error_msg

@mcp.tool()
def delete_folder(folder_path: str) -> str:
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        return f"Error: No such directory: '{folder_path}'"
    try:
        os.rmdir(folder_path)
        msg = f"Directory '{folder_path}' deleted successfully."
        return msg
    except Exception as e:
        error_msg = f"Error: {e}"
        return error_msg

if __name__ == "__main__":
    try:
        mcp.run(transport=config.TRANSPORT, mount_path=config.MOUNT_PATH)
    except ConnectionResetError:
        pass
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.exit(1)