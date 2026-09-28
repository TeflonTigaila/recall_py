from pathlib import Path
import os , sys, shutil

#path to the dir where chapters and conf file are stored
action_dir:Path = Path("~/.py_recap/").expanduser()

#chapter structure 
class Chapter:
    def __init__(self,chapter:str)->None:
        chapter_dir:Path=action_dir/chapter
        self.exercises:list = [f for f in chapter_dir.iterdir() if f.is_file()]

#function responsabile for enviorment setup
def builder() -> None:
    home_dir = action_dir/"init.conf"
    home_dir.parent.mkdir(parents=True, exist_ok=True)
    home_dir.touch(mode=0o664)

### HOME SPECIFIC FUNCTIONS ###

##THIS function creates a dir. specifit to eatch chapter 
def newchap(chap_name:list ) -> str:
    if len(chap_name) == 1 :
        #if the user lives the chap_name atribut free it wil asign the name Cn
        chapters:list =  [f for f in action_dir.iterdir() if f.is_dir()]    
        new_chapter_name =  f"C{len(chapters)}"
    else:
        new_chapter_name = chap_name[1]
    new_chapter = action_dir/new_chapter_name
    while(new_chapter.is_dir()):
        try:
            new_chapter_name = input("You have a chapter with this name enter another name: ").strip()
        #forced exit error handler
        except (EOFError , KeyboardInterrupt):
            return ''
        if not new_chapter_name :
            continue
        new_chapter = action_dir/new_chapter_name
    new_chapter.mkdir(parents=True, exist_ok=True)
    return new_chapter_name

##this functions removes a specific chapter
def delchap(chap_name:list) -> str:
    if len(chap_name) != 1:
        chapter:Path = action_dir/chap_name[1]
        try:
            shutil.rmtree(chapter)
        except FileNotFoundError :
            print("The chapter you selected doesen't exist")
    return "HOME"

##this function lists all the chapters
def shwchap(chap_name:list) -> str:
    chapters:list =  [f for f in action_dir.iterdir() if f.is_dir()]
    for chapter in sorted(chapters):
        print(chapter.name)
    return "HOME"

##this functions opens the chapter you selected
def opnchap(chap_name:list) -> str:
    chapters:list =  [f.name for f in action_dir.iterdir() if f.is_dir()]
    print(chapters)
    if chap_name[1] in chapters:
        return chap_name[1]
    print(f"There is no chapter with the name {chap_name[1]}")
    return "HOME"

###Functions that apply on the chapter side

##Function for adding new text
def newtest(cmd:list , chapter:str) ->None:
    chapter_path:Path = action_dir/chapter
    text_files = [f for f in chapter_path.iterdir() if f.is_file()]
    if len(cmd) < 2:
        new_text_path = chapter_path/f"{len(text_files)}.test"
    else:
        new_text_path = chapter_path/f"{cmd[1]}.test"
    new_text_path.touch(mode=0o664)
    i_mode = input("Do you want to enter manual the text or with a file?[m/f]")
    while(i_mode != "m" and i_mode != "f"):
        i_mode = input("There is not sutch an option [m/f]")
    if i_mode == "f":
        i_file_name = input("What is the file path? :")
        i_file=Path(i_file_name.strip())
        while not Path(i_file).is_file():
            print("ERROR: There is not sutch a file ")
            i_file_name = input("What is the corect file path?:")
            i_file=Path(i_file_name)
        shutil.copyfile(i_file,new_text_path)
    if i_mode == "m":
        print("When you finish with the commands you can write END_OF_SCRIPT")
        i:int=0
        file = new_text_path.open("a" , encoding="utf-8" , buffering=1)
        i_file = input(f"{i}")
        print(i_file,file=file)
        while(i_file != "EOS"):
            i_file = input(f"{i}")
            print(i_file,file=file)
            i+=1
        file.close()

            

#dict with the active home space comands 
home_com:dict = {
    "cr":newchap ,
    "rm":delchap ,
    "ls":shwchap ,
    "op":opnchap
}
#dict with the active chaoter space comands
chap_com:dict = {
    "cr":newtest
}


def send_cmd(cmd:str, chapter:str) ->str:
    cmd_comps:list = cmd.split()
    if chapter == "HOME" and cmd_comps[0] in home_com:
        return home_com[cmd_comps[0]](cmd_comps)
    if chapter != "HOME" and cmd_comps[0] in chap_com:
        chap_com[cmd_comps[0]](cmd_comps , chapter)
        return chapter
    return "HOME"
    


if __name__ == "__main__":
    if not Path("~/.py_recap").expanduser().is_dir():
        builder()
    else:
        print(f"Happy to see you {os.getenv("USER")}")
        cmd:str = "HELP"  
        loc_chap:str =  "HOME"
        while cmd != "EXIT":
            loc_chap = send_cmd(cmd , loc_chap)
            cmd=input(f"[{loc_chap}]=>")
    sys.exit(0)
