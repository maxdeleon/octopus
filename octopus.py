import discord
from discord.ext import tasks
import matplotlib.dates as mpdates
import datetime as dt
import os
import os.path
from os import path
import botPlugins.rss.rss as rss
import sys
from KEYS import *

# discord token

command_file = 'commands.txt'
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    rssFeed.start()

# async method to handle commands passed in by the user
@client.event
async def on_message(message):
    if message.author == client.user:
        pass

    if message.content.startswith('!'): # checks if the message starts with an app header
        command_dict = parseCommands()#parseCommands(commandFile=command_file)
        command_list = command_dict.keys()
        content = message.content.strip('!')
        content = content.split(' ')
        print(message.author,content)

        if content[0] == 'help':
            if len (content) == 2:
                if content[1] in command_list:
                    command = content[1]
                    if path.exists(command_dict[command]['helpPath']):
                        with open(command_dict[command]['helpPath'],'r') as f:
                            help_text = '```'
                            for line in f:
                                help_text += line
                            help_text +='```'
                        await message.channel.send(help_text)
                    else:
                        help_message='```Help file not found... Manually listing command parameters\n'
                        for parameter in command_dict[command]['parameters']:
                            help_message += parameter +'\n'
                        help_message+='```'
                        await message.channel.send(help_message)
                else:
                    await message.channel.send('```The command {} does not exist therefore there is not help for it```'.format(content[1]))
            else:
                command_string = '```Available Commands:\n'
                for command in command_list:
                    command_string += command + '\n'
                command_string+= '```'
                await message.channel.send(command_string)
        elif content[0] in command_list:
            command = content[0]
            content.pop(0)
            if (len(content) == len(command_dict[command]['parameters']) and command_dict[command]['is_strict']) or (len(content) != len(command_dict[command]['parameters']) and not command_dict[command]['is_strict']): # if len(content) == len(command_dict[command]['parameters']) and command_dict[command]['is_strict']
                if path.exists(command_dict[command]['path']):
                    command_parameters = ''
                    for parameter in content:
                        command_parameters += parameter+ ' '
                    system_command = 'python3 ' + command_dict[command]['path'] + ' ' + command_parameters
                    await message.channel.send('```recieved {} command from @{}```'.format(command,message.author))
                    output  = os.popen(system_command).readlines()
                    # add command characters so program switches to return image mode
                    # output 0 is the control command for the image or not
                    # if outputting image the plutgin file will return the image filename as a seperate line aka output[1]
                    try:
                        if output[0].strip('\n') == 'type=FILE':
                            # does images stuff
                            file_to_send = output[1].strip('\n')
                            if path.exists(file_to_send):
                                await message.channel.send(file=discord.File(file_to_send))
                            else:
                                await message.channel.send('```{} not found in directory.```'.format(file_to_send))
                        else:
                            output.pop(0)
                            output_string = ''
                            for line in output:
                                output_string += line
                            await message.channel.send('```{}```'.format(output_string))
                    except Exception as e:
                        await message.channel.send('```Damn either you or one of the quants made a mistake with this tool...\n This is the error: {}```'.format(e))
                else:
                    await message.channel.send('```Program not in directory.```')
            else: 
                await message.channel.send('```Number of given parameters do not match required amount.```')
        elif content[0] == 'ping':
            await message.channel.send('```pong```')
        else:
            await message.channel.send('```Unkown command. Type !help to see commands```')

# method to parse plugins and link user input to programs
@tasks.loop(minutes=RSS_UPDATE_FREQUENCY)
async def rssFeed():
    if RSS_MODE:
        channel = client.get_channel(NEWS_CHANNEL)
        rss_data = rss.fetch()
        if len(rss_data) != 0:
            for item in rss_data:
                await channel.send("```{}```".format(item))
                pass
        else:
            pass
    else:
        pass
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
    
    print('Available Plugin Data')
    for line in commands.keys():
        print(line,commands[line])
    return commands


client.run(BOT_TOKEN)
