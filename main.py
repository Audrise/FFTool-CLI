"""
Developed by   : Audrise
Version        : 1.0.0
GitHub         : https://github.com//Audrise/audiotool
Status         : Launched
"""

try:
    from time import sleep
    from pystyle import System
    from tool.audio import AudioProcessor
    from tool.metadata import MetadataEditor
    from pystyle import Colorate, Col, System, Cursor, Center
    from subprocess import CalledProcessError
    from tool.cover import CoverArtEditor
    from os.path import basename
    from sys import stdout
    from os import getcwd

except Exception as e:
    print(f"Error: {e}")
    exit(0)

icon = r"""
                   ████████             
              ██████████████████        
           ████████████████████████     
          ██  ██████████████████████    
         ███ █  █████████████████████   
        ███████   ████████████████████  
       ██████████ ██      █████████████ 
       ███████████          ███████████ 
      ███████████     ██      ██████████
      ███████████     ██     ███████████
       ███████████          ███████████ 
       █████████████      ██ ██████████ 
        ████████████████████   ███████  
         █████████████████████  █ ███   
          ██████████████████████  ██    
           ████████████████████████     
              ██████████████████        
                   ████████             

▄▄   ▄▄ ▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄▄  ▄▄▄▄▄ ▄▄▄▄  ▄▄ ▄▄▄▄▄▄ 
██▀▄▀██ ██▄▄    ██  ██▀██ ██▄▄  ██▀██ ██   ██   
██   ██ ██▄▄▄   ██  ██▀██ ██▄▄▄ ████▀ ██   ██   """

black = Col.black
green = Col.green
res = Col.reset
red = Col.red

lightb = Col.StaticMIX((Col.light_blue, Col.blue, Col.light_blue))
purple = Col.StaticMIX((Col.purple, Col.blue, Col.purple))
blued = Col.StaticMIX((Col.black, Col.blue, Col.dark_gray))

class Audiotool:
    def __init__(self, current_directory, set_directory, tracklist):
        self.current_directory = current_directory
        self.set_directory = set_directory
        self.tracklist = tracklist

    def show_menu(self):
        print(normal("Main menu", '#'))
        print(normal_sub("Metadata", '1'))
        print(normal_sub("Audio convert", '2'))
        print(normal_sub("Change Directory", '3'))
        print(normal_sub("Cancel and exit", '0'))
        print()

    def show_metadata(self, data):
        for file, tags in data.items():
            print(normal(f"List of {purple}'{file}'{res} Metadata:"))

            if not tags:
                animation(error(f"{red}No Metadata found!!{res}\n"), 0.006)

            for k, v in tags.items():
                v_filtered = str(v).replace("[", "").replace("]", "")
                print(normal_sub(f": {purple}{v_filtered}{res}", k))
            print()

    def song_list(self):
        System.Clear()
        logo()

        if self.set_directory == "":
            self.current_directory = basename(getcwd())

        else:
           self.current_directory = self.set_directory

        if not self.tracklist.files:
            System.Clear()
            logo()
            print(normal(f"Songs list from {purple}'{self.current_directory}'{res}:", '#'))
            animation(error(f"{red}No audio found!{res}\n"), 0.004)
            sleep(0.3)
            animation(error(f"{red}Make sure you input the correct directory!{res}\n"), 0.003)
            sleep(1)
            return False

        else:
            print(normal(f"Songs list from {purple}'{self.current_directory}'{res}:", '#'))

        for i, file in enumerate(self.tracklist.files, start=1):
            print(normal_sub(f"{file.name}{res}", f'{i}'))
        return True

    def metadata_menu(self):
        System.Clear()
        logo()
        while True:
            print(normal("Metadata Menu", '#'))
            print(normal_sub("View song metadata", '1'))
            print(normal_sub("Add or Edit tags", '2'))
            print(normal_sub("Remove tags", '3'))
            print(normal_sub("Add or Edit cover", '4'))
            print(normal_sub("Remove cover", '5'))
            print(normal_sub("Back to main menu\n", '0'))

            choice = input(animation(normal(f"Select an option {purple}->{lightb} ", '?'), 0.003))

            if choice == "1":
                if not self.song_list():
                    System.Clear()
                    logo()
                    continue

                print(normal_sub(f"Back\n", '0'))
                idx = input(animation(normal(f"Select song number {purple}[{lightb}Press enter for all{purple}] ->{lightb} ", '?'), 0.003))

                if idx == "0":
                    System.Clear()
                    logo()
                    continue

                elif idx != "":
                    try:
                        data = self.tracklist.list_metadata(index=int(idx) - 1)
                    except IndexError:
                        animation(error(f"{red}Invalid index number!{res}\n"), 0.003)
                        continue
                else:
                    data = self.tracklist.list_metadata()

                System.Clear()
                self.show_metadata(data)

            elif choice == "2":
                if not self.song_list():
                    System.Clear()
                    logo()
                    continue

                print(normal_sub(f"Back\n", '0'))
                idx = input(animation(normal(f"Select song number {purple}[{lightb}Press enter for all songs{purple}] ->{lightb} ", '?'), 0.003))

                if idx.lower() == "0":
                    System.Clear()
                    logo()
                    continue

                elif idx != "":
                    try:
                        data = self.tracklist.list_metadata(index=int(idx) - 1)
                    except IndexError:
                        animation(error(f"{red}Invalid index number!{res}\n"), 0.003)
                        continue

                else:
                    data = self.tracklist.list_metadata()

                System.Clear()
                self.show_metadata(data)

                try:
                    key = input(animation(normal(f"Enter the tag key {purple}->{lightb} ", '?'), 0.003))
                    value = input(animation(normal(f"Enter the tag value {purple}->{lightb} ", '?'), 0.003))

                except KeyboardInterrupt:
                    System.Clear()
                    logo()
                    continue

                try:
                    if idx:
                        self.tracklist.set_tag(key, value, int(idx) - 1)
                    else:
                        self.tracklist.set_tag(key, value)

                    animation(success(f"{green}Editing success!{res}\n"), 0.003)
                    sleep(1)
                    System.Clear()
                    logo()

                except IndexError:
                    animation(error(f"{red}Invalid index number!{res}\n"), 0.003)

                except Exception as e:
                    animation(error(f"{red}An error occured: {e}{res}\n"), 0.003)
                    exit()

            elif choice == "3":
                if not self.song_list():
                    System.Clear()
                    logo()
                    continue

                print(normal_sub(f"Back\n", '0'))
                idx = input(animation(normal(f"Select song number {purple}[{lightb}Press enter for all{purple}] ->{lightb} ", '?'), 0.003))

                if idx == "0":
                    System.Clear()
                    logo()
                    continue

                elif idx != "":
                    try:
                        data = self.tracklist.list_metadata(index=int(idx) - 1)
                    except IndexError:
                        animation(error(f"{red}Index tidak valid!{res}\n"), 0.003)
                        continue
                else:
                    data = self.tracklist.list_metadata()

                System.Clear()
                self.show_metadata(data)

                key = input(animation(normal(f"Enter the tag key {purple}[{lightb}Press enter to cancel{purple}] ->{lightb} ", '?'), 0.003))
                if key == "":
                    System.Clear()
                    logo()
                    continue

                else:
                    self.tracklist.delete_tag(key)
                    animation(success(f"{green}Deleting '{key}' success!{res}\n"), 0.003)
                    sleep(1)
                    System.Clear()
                    logo()

            elif choice == "4":
                if not self.song_list():
                    System.Clear()
                    logo()
                    continue

                print(normal_sub(f"Back\n", '0'))
                idx = input(animation(normal(f"Select song number {purple}[{lightb}Press enter for all{purple}] ->{lightb} ", '?'), 0.003))

                if idx.lower() == "0":
                    System.Clear()
                    logo()
                    continue

                try:
                    if idx != "":
                        data_list = [self.tracklist.files[int(idx)-1]]
                    else:
                        data_list = self.tracklist.files
                except (IndexError, ValueError):
                    animation(error(f"{red}Invalid index number!{res}\n"), 0.003)
                    continue

                for data in data_list:
                    file_path = str(data)  # Direct to path object
                    try:
                        cover = CoverArtEditor(file_path)
                    except Exception as e:
                        animation(error(f"{red}Cannot open file: {e}{res}\n"), 0.003)
                        continue

                    img = input(animation(normal(f"Enter the cover path{purple} ->{lightb} ", '?'), 0.003))

                    if img == "0":
                        System.Clear()
                        logo()
                        break

                    else:
                        mime = "image/jpeg"
                        if img.lower().endswith(".png"):
                            mime = "image/png"

                        try:
                            cover.add_cover(img, mime=mime)
                            animation(success(f"{green}Success adding cover!{res}\n"), 0.003)
                            sleep(1)
                            System.Clear()
                            logo()

                        except Exception as e:
                            animation(error(f"{red}Failed add cover: {e}{res}\n"), 0.003)
                            sleep(1)
                            System.Clear()
                            logo()

            elif choice == "5":
                if not self.song_list():
                    System.Clear()
                    logo()
                    continue

                print(normal_sub(f"Back\n", '0'))
                idx = input(animation(normal(f"Select song number {purple}[{lightb}Press enter for all{purple}] ->{lightb} ", '?'), 0.003))

                if idx.lower() == "0":
                    System.Clear()
                    logo()
                    continue

                try:
                    if idx != "":
                        data_list = [self.tracklist.files[int(idx)-1]]
                    else:
                        data_list = self.tracklist.files

                except (IndexError, ValueError):
                    animation(error(f"{red}Invalid index number!{res}\n"), 0.003)
                    continue

                for data in data_list:
                    file_path = str(data) # Direct to object path
                    try:
                        cover = CoverArtEditor(file_path)
                    except Exception as e:
                        animation(error(f"{red}Cannot open file: {e}{res}\n"), 0.003)
                        continue

                if idx == "":
                    confirm = input(animation(normal(f"Do you sure want to delete all songs cover {purple}[{lightb}Press enter for yes{purple}] ->{lightb} ", '?'), 0.003))

                    try:
                        if confirm == "":
                            cover.remove_cover()
                            animation(success(f"{green}Deleting all cover success!{res}\n"), 0.003)

                        else:
                            System.Clear()
                            logo()
                            continue

                    except Exception as e:
                        animation(error(f"{red}Failed to deleting cover: {e}{res}\n"), 0.003)

                else:
                    confirm = input(animation(normal(f"Do you sure want to deleting the cover {purple}[{lightb}Press enter for yes{purple}] ->{lightb} ", '?'), 0.003))

                    try:
                        if confirm == "":
                            cover.remove_cover()
                            animation(success(f"{green}Deleting cover success!{res}\n"), 0.003)

                        else:
                            System.Clear()
                            logo()
                            continue

                    except Exception as e:
                        animation(error(f"{red}Failed to deleting cover: {e}{res}\n"), 0.003)

            elif choice == "0":
                System.Clear()
                break

            else:
                print(error(f"{red}Invalid option!{res}\n"))
                sleep(1)
                System.Clear()
                logo()

    def audio_menu(self):
        audio = AudioProcessor()
        sample_rate = bit_depth = codec = file_to_convert = None

        while True:
            System.Clear()
            logo()
            print(normal(f"Current settings", '#'))
            print(normal_sub(f"Audio file    {purple}-> [{lightb}{file_to_convert.name if file_to_convert else None}{purple}]", '!'))
            print(normal_sub(f"Sampling rate {purple}-> [{lightb}{sample_rate}{' Hz' if sample_rate is not None else ''}{purple}]", '!'))
            print(normal_sub(f"Bit depth     {purple}-> [{lightb}{bit_depth}{' bits' if bit_depth is not None else ''}{purple}]", '!'))
            print(normal_sub(f"Output format {purple}-> [{lightb}{codec}{purple}]", '!'))
            print()
            print(normal(f"Audio Processing Menu", '#'))
            print(normal_sub("Set Audio", '1'))
            print(normal_sub("Convert settings", '2'))
            print(normal_sub("Start Converting", '3'))
            print(normal_sub("Reset all settings", '4'))
            print(normal_sub("Back to main menu\n", '0'))


            choice = input(animation(normal(f"Select an option {purple}->{lightb} ", '?'), 0.003))
            # set the file of audio
            if choice == "1":
                while True:
                    # System.Clear()
                    if not self.song_list():
                        System.Clear()
                        logo()
                        break

                    print(normal_sub(f"Back\n", '0'))

                    idx = input(animation(normal(f"Select song number {purple}->{lightb} ", '?'), 0.003))

                    if idx == "0":
                        break

                    try:
                        idx = int(idx) - 1
                        if idx < 0 or idx >= len(self.tracklist.files):
                            print(error(f"{red}Invalid index!{res}"))
                            sleep(0.8)
                            System.Clear()
                            continue
                        file_to_convert = self.tracklist.files[idx]
                        break
                    except ValueError:
                        print(error(f"{red}Please enter an integer!{res}"))
                        sleep(0.8)
                        System.Clear()
                        continue

            # sampling rate
            elif choice == "2":
                if not file_to_convert:
                    print(error(f"{red}Please select a file first{res}\n"))
                    sleep(0.8)
                    System.Clear()
                    continue

                while True:
                    System.Clear()
                    logo()
                    print(normal("Sampling rate Menu:", '#'))
                    print(normal_sub(f"192000 Hz {purple}[{lightb}High Resolution{purple}]{res}", '1'))
                    print(normal_sub(f"176400 Hz {purple}[{lightb}High Resolution{purple}]{res}", '2'))
                    print(normal_sub(f"96000 Hz  {purple}[{lightb}High Resolution{purple}]{res}", '3'))
                    print(normal_sub(f"88200 Hz  {purple}[{lightb}High Resolution{purple}]{res}", '4'))
                    print(normal_sub(f"48000 Hz  {purple}[{lightb}Studio Quailty{purple}]{res}", '5'))
                    print(normal_sub(f"44100 Hz  {purple}[{lightb}Standard Quality{purple}]{res}", '6'))
                    print(normal_sub("Back to Audio Menu\n", '0'))

                    sr = input(animation(normal(f"Select Sample rate {purple}[{lightb}Press enter for 44100 Hz{purple}] ->{lightb} ", '?'), 0.003))

                    if sr == "":
                        sample_rate = 44100
                        break
                    elif sr == "1":
                        sample_rate = 192000
                        break
                    elif sr == "2":
                        sample_rate = 176400
                        break
                    elif sr == "3":
                        sample_rate = 96000
                        break
                    elif sr == "4":
                        sample_rate = 88200
                        break
                    elif sr == "5":
                        sample_rate = 48000
                        break
                    elif sr == "6":
                        sample_rate = 44100
                        break
                    elif sr == "0":
                        break
                    else:
                        try:
                            sample_rate = int(sr)
                            break
                        except ValueError:
                            print(error(f"{red}Please enter an integer!{res}"))
                            sleep(0.8)
                            System.Clear()
                            continue

                while True:
                    System.Clear()
                    logo()
                    print(normal("Bitrate Menu:", '#'))
                    print(normal_sub(f"32 Bits {purple}[{lightb}Studio Quality{purple}]{res}", '1'))
                    print(normal_sub(f"24 Bits {purple}[{lightb}Studio Quality{purple}]{res}", '2'))
                    print(normal_sub(f"16 Bits {purple}[{lightb}Standard Quality{purple}]{res}", '3'))
                    print(normal_sub("Back to Audio Menu\n", '0'))

                    bit_select = input(animation(normal(f"Select Bitrate {purple}[{lightb}Press enter for 16 Bits{purple}] ->{lightb} ", '?'), 0.003))

                    if bit_select == "":
                        bit_depth = 16
                        break
                    elif bit_select == "1":
                        bit_depth = 32
                        break
                    elif bit_select == "2":
                        bit_depth = 24
                        break
                    elif bit_select == "3":
                        bit_depth = 16
                        break
                    elif bit_select == "0":
                        break
                    else:
                        try:
                            bit_depth = int(bit_select)
                            break
                        except ValueError:
                            print(error(f"{red}Please enter an integer!{res}"))
                            sleep(0.8)
                            System.Clear()
                            continue

                while True:
                    System.Clear()
                    logo()
                    print(normal("Output format Menu:", '#'))
                    print(normal_sub(f"FLAC {purple}[{lightb}Lossless{purple}]{res}", '1'))
                    print(normal_sub(f"MP3  {purple}[{lightb}Lossy{purple}]{res}", '2'))
                    print(normal_sub(f"AAC  {purple}[{lightb}Lossy{purple}]{res}", '3'))
                    print(normal_sub(f"OGG  {purple}[{lightb}Lossy{purple}]{res}", '4'))
                    print(normal_sub("Back to Audio Menu\n", '0'))

                    codec_select = input(animation(normal(f"Select format {purple}[{lightb}Press enter for MP3{purple}] ->{lightb} ", '?'), 0.003))

                    if codec_select == "":
                        codec = "mp3"
                        break
                    elif codec_select == "1":
                        codec = "flac"
                        break
                    elif codec_select == "2":
                        codec = "mp3"
                        break
                    elif codec_select == "3":
                        codec = "aac"
                        break
                    elif codec_select == "4":
                        codec = "ogg"
                        break
                    else:
                        codec = codec
                        break

            # start converting
            elif choice == "3":
                if not file_to_convert:
                    print(error(f"{red}Please select a file first{res}\n"))
                    sleep(0.8)
                    # System.Clear()
                    continue

                if codec == None:
                    print(error(f"{red}Please set all settings first!{res}\n"))
                    sleep(0.8)
                    # System.Clear()
                    continue


                System.Clear()
                logo()
                print(normal(f"Current settings:", '#'))
                print(normal_sub(f"Audio file    {purple}-> [{lightb}{file_to_convert.name if file_to_convert else None}{purple}]", '1'))
                print(normal_sub(f"Sampling rate {purple}-> [{lightb}{sample_rate}{' Hz' if sample_rate is not None else ''}{purple}]", '2'))
                print(normal_sub(f"Bits depth    {purple}-> [{lightb}{bit_depth}{' bits' if bit_depth is not None else ''}{purple}]", '3'))
                print(normal_sub(f"Output format {purple}-> [{lightb}{codec}{purple}]", '4'))
                print(normal_sub("Back to Audio Menu\n", '0'))

                output_file = input(animation(normal(f"Enter output file name {purple}[{lightb}Press enter for default{purple}] ->{lightb} ", '?'), 0.003))

                if output_file == "0":
                    continue

                if output_file == "":
                    output_file = f"resampled_song.{codec}"

                if "." not in output_file:
                    output_file = f"{output_file}.{codec}"

                try:
                    System.Clear()
                    logo()
                    print(normal(f"Resampling info:", '#'))
                    print(normal_sub(f"Audio file    {purple}-> [{lightb}{file_to_convert.name if file_to_convert else None}{purple}]", '1'))
                    print(normal_sub(f"Sampling rate {purple}-> [{lightb}{sample_rate}{' Hz' if sample_rate is not None else ''}{purple}]", '2'))
                    print(normal_sub(f"Bits depth    {purple}-> [{lightb}{bit_depth}{' bits' if bit_depth is not None else ''}{purple}]", '3'))
                    print(normal_sub(f"Output format {purple}-> [{lightb}{codec}{purple}]\n", '4'))

                    animation(normal(f"Starting resampling from {lightb}'{file_to_convert}'{purple} to {lightb}'{output_file}'{res}"), 0.003)
                    sleep(1)
                    audio.convert(input_file=file_to_convert, output_file=output_file, sample_rate=sample_rate, bit_depth=bit_depth, codec=codec)
                    sleep(0.5)
                    animation(success(f"{green}Resampling from '{file_to_convert}' to '{output_file}' success!{res}\n\n"), 0.006)
                    sleep(0.5)

                    rep = input(animation(normal(f"Want to converting again {purple}[{lightb}Press enter to continue{purple}] ->{lightb} ", '?'), 0.003))
                    if rep != "":
                        System.Clear()
                        animation(success(f"{green}Thanks for using the tool!{res}"), 0.003)
                        sleep(1)
                        exit(0)

                    sample_rate = None
                    bit_depth = None
                    codec = None
                    file_to_convert = None

                except CalledProcessError as e:
                    print(error(f"{red}An error occured: {e}{res}\n"), 0.003)
                    exit(0)

            elif choice == "4":
                sample_rate = bit_depth = codec = file_to_convert = None

            elif choice == "0":
                System.Clear()
                break

            else:
                print(error(f"{red}Invalid selection!{res}"))
                sleep(0.8)
                System.Clear()

def logo():
    print(Colorate.Vertical(Col.DynamicMIX((blued, purple)), Center.XCenter(icon)))
    print()

def animation(s, w):
    result = ""
    for c in s:
        stdout.write(c)
        stdout.flush()
        sleep(w)
    return result

def normal(text, symbol = '!'):
    col1 = purple
    col2 = res
    return f" {Col.Symbol(symbol, col2, col1, '[', ']')} {col2}{text}"

def normal_sub(text, symbol = '!'):
    col1 = purple
    col2 = res
    return f" {Col.Symbol(symbol, col2, col1, '  [', ']')} {col2}{text}"

def error(text, symbol = '!'):
    col1 = red
    col2 = res
    return f" {Col.Symbol(symbol, col2, col1, '[', ']')} {col2}{text}"

def success(text, symbol = '!'):
    col1 = green
    col2 = res
    return f" {Col.Symbol(symbol, col2, col1, '[', ']')} {col2}{text}"

def main():
    try:
        current_directory = set_directory = tracklist = None
        Cursor.HideCursor()
        System.Clear()
        logo()
        set_directory = input(animation(normal(f"Enter the path {purple}[{lightb}Press enter for current path{purple}] ->{lightb} ", '?'), 0.004))
        tracklist = MetadataEditor(set_directory)
        start_run = Audiotool(current_directory, set_directory, tracklist)
        System.Clear()

        while True:
            logo()
            start_run.show_menu()
            choice = input(animation(normal(f"Select an option {purple}->{lightb} ", '?'), 0.003))

            if choice == "1":
                start_run.metadata_menu()

            elif choice == "2":
                start_run.audio_menu()

            elif choice == "3":
                System.Clear()
                logo()
                set_directory = input(animation(normal(f"Enter the path {purple}[{lightb}Press enter for current path{purple}] ->{lightb} ", '?'), 0.004))
                tracklist = MetadataEditor(set_directory)
                start_run = Audiotool(current_directory, set_directory, tracklist)
                System.Clear()

            elif choice == "0":
                print(error(f"{red}Exitting{res}"))
                sleep(0.5)
                System.Clear()
                break

            else:
                print(error(f"{red}Invalid index!{res}"))
                sleep(0.5)
                System.Clear()

    except KeyboardInterrupt:
        System.Clear()
        print(error(f"{red}Stopping Success!{res}"))
        Cursor.ShowCursor()
        exit(0)

    except Exception as e:
        print(error(f"{red}{e}{res}\n"))
        Cursor.ShowCursor()
        exit(0)

if __name__ == '__main__':
    main()