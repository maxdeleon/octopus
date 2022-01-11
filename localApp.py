import datetime as dt
import os
import os.path
from os import path
import botPlugins.rss.rss as rss
import time 
from rich import print
from rich.console import Console



command_file = 'commands.txt'


# async method to handle commands passed in by the user

def on_message(message):
    global command_file
    command_dict = parseCommands()#parseCommands(commandFile=command_file)
    command_list = command_dict.keys()

    content = message.split(' ')
    #print(content)
    #content = message.content.strip('!')
    #content = content.split(' ')
    #print(message.author,content)

    if content[0] == 'help':
        if len (content) == 2:
            if content[1] in command_list:
                command = content[1]
                if path.exists(command_dict[command]['helpPath']):
                    with open(command_dict[command]['helpPath'],'r') as f:
                        help_text = ''
                        for line in f:
                            help_text += line
                        
                    #await message.channel.send(help_text)
                    fancyPrint(help_text)

                else:
                    help_message='Help file not found... Manually listing command parameters\n'
                    for parameter in command_dict[command]['parameters']:
                        help_message += parameter +'\n'
                    
                    #await message.channel.send(help_message)
                    fancyPrint(help_message)
            else:
                #await message.channel.send('```The command {} does not exist therefore there is not help for it```'.format(content[1]))
                fancyPrint('The command {} does not exist therefore there is not help for it'.format(content[1]))
        else:
            command_string = '\n [bold orange]Available Commands[/bold orange] \n'
            for command in command_list:
                command_string += command + '\n'
            
            #await message.channel.send(command_string)
            fancyPrint(command_string)
    elif content[0] in command_list:
        command = content[0]
        content.pop(0)
        if (len(content) == len(command_dict[command]['parameters']) and command_dict[command]['is_strict']) or (len(content) != len(command_dict[command]['parameters']) and not command_dict[command]['is_strict']): # if len(content) == len(command_dict[command]['parameters']) and command_dict[command]['is_strict']
            if path.exists(command_dict[command]['path']):
                command_parameters = ''
                for parameter in content:
                    command_parameters += parameter+ ' '
                system_command = 'python3 ' + command_dict[command]['path'] + ' ' + command_parameters
                fancyPrint('{}'.format(command))
                
                output  = os.popen(system_command).readlines()
                # add command characters so program switches to return image mode
                # output 0 is the control command for the image or not
                # if outputting image the plutgin file will return the image filename as a seperate line aka output[1]
                try:
                    if output[0].strip('\n') == 'type=FILE':
                        # does images stuff
                        file_to_send = output[1].strip('\n')
                        if path.exists(file_to_send):
                            #await message.channel.send(file=discord.File(file_to_send))
                            fancyPrint('Opening file at: {}'.format(file_to_send))
                            output  = os.popen('code {}'.format(file_to_send)).readlines()
                            if 'command not found: code' not in output[0]:
                                fancyPrint('Open the Command Palette (Cmd+Shift+P) and type "shell command" to find the Shell Command: Install "code" command in PATH command')
                            else: pass
                        else:
                            #await message.channel.send('```{} not found in directory.```'.format(file_to_send))
                            fancyPrint('{} not found in directory.'.format(file_to_send))
                    else:
                        output_string = ''
                        for line in output:
                            output_string += line
                        #await message.channel.send('```{}```'.format(output_string))
                        fancyPrint(output_string)
                except Exception as e:
                    #await message.channel.send('```Damn either you or one of the quants made a mistake with this tool...\n This is the error: {}```'.format(e))
                    fancyPrint('Developer error: {}'.format(e))
            else:
                #await message.channel.send('```Program not in directory.```')
                fancyPrint('Program not in directory.')
        else: 
            #await message.channel.send('```Number of given parameters do not match required amount.```')
            fancyPrint('Number of given parameters do not match required amount.')
    else:
        #await message.channel.send('```Unkown command. Type !help to see commands```')
        fancyPrint('Unkown command. Type !help to see commands')


def fancyPrint(message):
    print('[bold red]{}[/bold red] | [grey]{}'.format(time.asctime(time.localtime(time.time())),message))


def splashScreen():
    message = '''
   _                    _   _           
  /_\\   __ _  __ _ _ __| |_| |__   __ _ 
 //_\\\\ / _` |/ _` | '__| __| '_ \\ / _` |
/  _  \\ (_| | (_| | |  | |_| | | | (_| |
\\_/ \\_\\/\__ |\\__,_|_|   \\__|_| |_|\\__,_|
       |___/  
    '''
    print('[bold blue]{}'.format(message))



def parseCommands():
    commands = {}
    cwd = os.getcwd()
    plugin_folder = 'botPlugins'
    plugins_path = cwd +'/'+plugin_folder
    #print(os.listdir(plugins_path))
    plugin_directory_list = os.listdir(plugins_path)
    plugin_list = []
    command_paths = []
    for item in plugin_directory_list:
        path_to_plugin = plugins_path + '/'+item
        path_to_command_file = plugins_path + '/'+item +'/plugincommand.txt'

        if os.path.isdir(path_to_plugin) and os.path.exists(path_to_command_file):
            plugin_list.append(item)
            command_paths.append(path_to_command_file)

            with open(path_to_command_file,'r') as f:
                for line in f:
                    line = line.strip('\n')
                    line = line.split(' ')
                    command = line[0].strip('!')
                    parameters = line[1].split(',') if line[1] != 'null' else ''
                    path = line[2]
                    help_file = line[3]
                    strict = False if 'STRICT' not in line[4] else True

                    commands[command] = {'parameters':parameters,
                                         'path':'./'+plugin_folder + '/'+item+ '/'+path,
                                         'helpPath':'./'+plugin_folder + '/'+item+ '/'+help_file,
                                         'is_strict': strict}
        else:
            pass
    
    '''print('Available Plugin Data')
    for line in commands.keys():
        print(line,commands[line])'''
    return commands


def main():
    version = 0.01
    runtime = 1
    splashScreen()
    fancyPrint('Agartha Client v.{}'.format(version))
    while runtime == 1:
        print('[bold green]>',end='')
        message = input('')
        if message == 'kill':
            break
        if message == 'clear':
            os.system('clear')
            fancyPrint('Agartha Client v.{}'.format(version))
        else:
            on_message(message)
    fancyPrint('Exiting Agartha Client, goodbye!')


if __name__ == '__main__':
    main()