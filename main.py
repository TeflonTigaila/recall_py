from pathlib import Path
import sys
import os

class Chapter:
    def __init__(self,chapter:str)->None:
        chapter_dir:Path=Path(f"~/.py_recap/{$chapter}").expanduser()
        self.exercises:list = [f for f in chapter_dir.iterdir() if f.is_file()]

def builder() -> None:
    home_dir = Path("~/.py_recap/init.conf").expanduser()
    home_dir.parent.mkdir(parents=True)
    home_dir.touch(mode=0o664)

def send_cmd() ->None:


if __name__ == "__main__":
    if not Path("~/.py_recap").expanduser().is_dir():
        builder()
    else:
        print(f"Happy to see you{os.environ.get("USER")}")
        cmd:str , loc_chap:str = "HELP" , "HOME"
        while cmd != "EXIT":
            send_cmd(cmd , loc_chap)
            cmd=input(f"[{loc_chap}]=>")
    sys.exit(0)
