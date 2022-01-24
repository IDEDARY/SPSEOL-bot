import discord
import datetime
from discord.ext import commands
import os

TOKEN = os.environ["TOKEN"]

bot = commands.Bot(command_prefix='?',intents=discord.Intents.all())

@bot.command()
async def cmd(ctx):
    await ctx.send("```---< List of commands >--- \n - ?cmd = this \n - ?ping = pingni tvou třídu \n - ?group 'name' = vytvoř skupinu \n - ?group_add @honza 'name' = přidej člena \n - ?group_delete 'name' = odstraň skupinu```")

@bot.command()
async def ping(ctx,):
    channels = ["1L","2L","3L","4L","1A","2A","3A","4A","1B","2B","3B","4B","Učitel"]
    for x in channels:
        ROLE = discord.utils.get(ctx.guild.roles, name=x)
        if ROLE.id in [y.id for y in ctx.author.roles]:
            await ctx.send("<@&"+str(ROLE.id)+">")

@bot.command()
async def konec_roku(ctx):
    ROLE = discord.utils.get(ctx.guild.roles, name="Administrátor")
    if ROLE.id in [y.id for y in ctx.author.roles]:

        #Get current year
        _year = datetime.datetime.now().year
        _month = datetime.datetime.now().month
        if(_month >= 8):
            _schoolyear = str(_year)+"/"+str(_year+1)
        else:
            _schoolyear = str(_year-1)+"/"+str(_year)

        await ctx.send("```Ročník "+str(_schoolyear)+" zjištěn ...```")

        #Generate roles if they don't exist
        await ctx.send("```Kontrola rolí ...```")
        guild = ctx.guild

        channels = ["1L","2L","3L","4L","1A","2A","3A","4A","1B","2B","3B","4B"]
        channels_color = [0xB4C25E,0xE4C565,0xFFC67C,0xFFC89E,0xC25E7B,0xDE80B7,0xECA8F6,0xEBD5FF,0x5E8DC2,0x1EB4DD,0x00DADD,0x76FAC7]
        
        
        i = -1
        calc = 0
        #Generace class rolí
        for x in channels:
            i += 1
            if discord.utils.get(ctx.guild.roles, name=x) == None:
                await guild.create_role(name=x,colour=discord.Colour(channels_color[i]),permissions=discord.Permissions.none())
                calc += 1
        
        #Generace ABL rolí
        gen = "Lyceum"
        if discord.utils.get(ctx.guild.roles, name=gen) == None:
            await guild.create_role(name=gen,colour=discord.Colour(channels_color[3]),permissions=discord.Permissions.none())
            calc += 1
        
        gen = "Elektrotechnika"
        if discord.utils.get(ctx.guild.roles, name=gen) == None:
            await guild.create_role(name=gen,colour=discord.Colour(channels_color[7]),permissions=discord.Permissions.none())
            calc += 1
        
        gen = "Absolvent "+_schoolyear
        if discord.utils.get(ctx.guild.roles, name=gen) == None:
            await guild.create_role(name=gen,colour=discord.Colour(channels_color[11]),permissions=discord.Permissions.none())
            calc += 1



        await ctx.send("```Vytvořeno "+str(calc)+" rolí...```")



        i = 0
        _sorted_users = []
        for x in channels: #Loop through all classes role

            ROLE = discord.utils.get(ctx.guild.roles, name=x) #get role name
            _sorted_users.append([]) #Create an empty list inside a list

            for xx in guild.members: #Loop through players
                if ROLE.id in [y.id for y in xx.roles]: #If Role ID is inside player's list
                    _sorted_users[i].append(xx)
                
            i += 1

        await ctx.send("```Uživatelé sorted...```")



        calc = 0
        i = 0
        for x in _sorted_users: #X = classroom[i]
            if((i >= 0 and i <= 2) or (i >= 4 and i <= 6) or (i >= 8 and i <= 10)):
                for xx in x: #xx = user in that classroom [i]
                    oldclass = discord.utils.get(ctx.guild.roles, name=channels[i])
                    newclass = discord.utils.get(ctx.guild.roles, name=channels[i+1])
                    print("Uživatel "+str(xx.name)+" přesunut z třídy "+str(oldclass.name)+" do třídy "+str(newclass.name))
                    calc += 1
                    await xx.remove_roles(oldclass)
                    await xx.add_roles(newclass)
            elif(i == 3):
                for xx in x: #xx = user in that classroom [i]
                    oldclass = discord.utils.get(ctx.guild.roles, name=channels[i])
                    newclass = discord.utils.get(ctx.guild.roles, name="Lyceum")
                    newclass2 = discord.utils.get(ctx.guild.roles, name="Absolvent "+_schoolyear)
                    print("Uživatel "+str(xx.name)+" z třídy "+str(oldclass.name)+" ukončil vzdělání "+str(newclass.name)+" v roce "+_schoolyear)
                    calc += 1
                    await xx.remove_roles(oldclass)
                    await xx.add_roles(newclass)
                    await xx.add_roles(newclass2)
            elif(i == 7 or i == 11):
                for xx in x: #xx = user in that classroom [i]
                    oldclass = discord.utils.get(ctx.guild.roles, name=channels[i])
                    newclass = discord.utils.get(ctx.guild.roles, name="Elektrotechnika")
                    newclass2 = discord.utils.get(ctx.guild.roles, name="Absolvent "+_schoolyear)
                    print("Uživatel "+str(xx.name)+" z třídy "+str(oldclass.name)+" ukončil vzdělání "+str(newclass.name)+" v roce "+_schoolyear)
                    calc += 1
                    await xx.remove_roles(oldclass)
                    await xx.add_roles(newclass)
                    await xx.add_roles(newclass2)

            i += 1

        await ctx.send("```Posunuto "+str(calc)+" uživatelů do vyšších ročníků!```")
    else:
        await ctx.send("```Přístup odmítnut!```")


@bot.command()
async def integrity(ctx):
    ROLE = discord.utils.get(ctx.guild.roles, name="Administrátor")
    if ROLE.id in [y.id for y in ctx.author.roles]:

        await ctx.send("```Pokus o opravení integrity ...```")

        classes = ["1","2","3","4"]
        oldname = ["-all","-private","a","a-materiály","b","b-materiály","l","l-materiály"]
        newname = ["-all","-private","-acko","a-materiály","-becko","b-materiály","-lyceum","l-materiály"]
        #EDIT CHANNELS NAME
        '''
        i = 0
        for x in oldname:
            for xx in classes:
                print("Přejmenování kanálu "+xx+x)
                if (discord.utils.get(ctx.guild.text_channels, name=xx+x) == None):
                    continue
                else:
                    channel = discord.utils.get(ctx.guild.text_channels, name=xx+x)
                    new_name = xx+newname[i]
                    await channel.edit(name=new_name)
            i += 1
        await ctx.send("```Kanály přejmenovány ...```")

        '''
        #EDIT CLASSES PERMISSIONS
        category = ["A","B","L"]
        i = 0
        '''
        for x in newname:
            for xx in classes:
                print("Úprava kanálu "+xx+x)
                await ctx.send("```Úprava kanálu "+xx+x+"```")
                if (discord.utils.get(ctx.guild.text_channels, name=xx+x) == None):
                    continue
                else:
                    #Získej aktuální channel
                    channel = discord.utils.get(ctx.guild.text_channels, name=xx+x)
                    #Resetuj všechna povolení
                    for y in channel.changed_roles:
                        await channel.set_permissions(y, overwrite=None)
                    #Zakaž everyone
                    await channel.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False)
                    #Iteruj přes třídy
                    if (x == "-all" and xx != "absolvent"):
                        for xxx in category:
                            ROLE = discord.utils.get(ctx.guild.roles, name=xx+xxx)
                            await channel.set_permissions(ROLE, send_messages=True, read_messages=True)
                        ROLE = discord.utils.get(ctx.guild.roles, name="Učitel")
                        channel.set_permissions(ROLE, overwrite=None)
                        await channel.set_permissions(ROLE, send_messages=True, read_messages=True)
                    elif (x == "-private" and xx != "absolvent"):
                        for xxx in category:
                            ROLE = discord.utils.get(ctx.guild.roles, name=xx+xxx)
                            await channel.set_permissions(ROLE, send_messages=True, read_messages=True)
                    elif ((x == "-acko" or x == "a-materiály") and xx != "absolvent"):
                        if(x == "a-materiály"):
                            for yy in range(4):
                                if(int(xx)<(yy+1)):
                                    ROLE = discord.utils.get(ctx.guild.roles, name=str(yy+1)+category[0])
                                    await channel.set_permissions(ROLE, read_messages=True)
                        ROLE = discord.utils.get(ctx.guild.roles, name=xx+category[0])
                        await channel.set_permissions(ROLE, send_messages=True, read_messages=True)
                    elif ((x == "-becko" or x == "b-materiály") and xx != "absolvent"):
                        if(x == "b-materiály"):
                            for yy in range(4):
                                if(int(xx)<(yy+1)):
                                    ROLE = discord.utils.get(ctx.guild.roles, name=str(yy+1)+category[1])
                                    await channel.set_permissions(ROLE, read_messages=True)
                        ROLE = discord.utils.get(ctx.guild.roles, name=xx+category[1])
                        await channel.set_permissions(ROLE, send_messages=True, read_messages=True)
                    elif ((x == "-lyceum" or x == "l-materiály") and xx != "absolvent"):
                        if(x == "l-materiály"):
                            for yy in range(4):
                                if(int(xx)<(yy+1)):
                                    ROLE = discord.utils.get(ctx.guild.roles, name=str(yy+1)+category[2])
                                    await channel.set_permissions(ROLE, read_messages=True)
                        ROLE = discord.utils.get(ctx.guild.roles, name=xx+category[2])
                        await channel.set_permissions(ROLE, send_messages=True, read_messages=True)
            i += 1
        '''
        '''
        for x in classes:
            if(x != "absolvent"):
                print(x)
                channel = discord.utils.get(ctx.guild.categories, name=x+". Ročník")
                for y in channel.changed_roles:
                        await channel.set_permissions(y, overwrite=None)
            else:
                print(x)
                channel = discord.utils.get(ctx.guild.categories, name="Absolvent")
                for y in channel.changed_roles:
                        await channel.set_permissions(y, overwrite=None)
        '''
        await ctx.send("```Integrita kanálů dokončena!```")

        channels = ["1L","2L","3L","4L","1A","2A","3A","4A","1B","2B","3B","4B"]
        channels_color = [0xB4C25E,0xE4C565,0xFFC67C,0xFFC89E,0xC25E7B,0xDE80B7,0xECA8F6,0xEBD5FF,0x5E8DC2,0x1EB4DD,0x00DADD,0x76FAC7]
        
        
        i = -1
        calc = 0
        #Change color rolí
        for x in channels:
            i += 1
            if (discord.utils.get(ctx.guild.roles, name=x) == None):
                continue
            else:
                role = discord.utils.get(ctx.guild.roles, name=x)
                await role.edit(colour=discord.Colour(channels_color[i]))
                calc += 1

        await ctx.send("```Integrita opravena!```")
    else:
        await ctx.send("```Přístup odmítnut!```")

@bot.command()
async def group(ctx, *, namee: str = None):
    ROLE = discord.utils.get(ctx.guild.roles, name="Učitel")
    if ROLE.id in [y.id for y in ctx.author.roles]:
        if namee is None:
            await ctx.send("```Zadejte nazev př. ?group '3D tisk'```")
        else:
            namee = namee.lower()

            if discord.utils.get(ctx.guild.categories, name=namee) != None:
                await ctx.send("```Skupina již existuje!```")
            else:
                await ctx.send("```Vytvářím skupinu!```")

                guild = ctx.guild
                await guild.create_category(namee)
                cate = discord.utils.get(ctx.guild.categories, name=namee)

                await guild.create_role(name=namee,permissions=discord.Permissions.none())

                await guild.create_text_channel(namee+"-general", category=cate)
                await guild.create_voice_channel(namee+" Room", category=cate)

                ROLE = discord.utils.get(ctx.guild.roles, name=namee)
                await ctx.author.add_roles(ROLE)

                channel = discord.utils.get(ctx.guild.text_channels, name=namee+"-general")
                await channel.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False)
                await channel.set_permissions(ROLE, send_messages=True, read_messages=True)

                channel = discord.utils.get(ctx.guild.voice_channels, name=namee+" Room")
                await channel.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False)
                await channel.set_permissions(ROLE, send_messages=True, read_messages=True)

                channel = discord.utils.get(ctx.guild.categories, name=namee)
                await channel.set_permissions(ctx.guild.default_role, send_messages=False, read_messages=False)
                await channel.set_permissions(ROLE, send_messages=True, read_messages=True)

                await ctx.send("```Skupina vytvořena!```")
    else:
        await ctx.send("```Přístup odmítnut!```")

@bot.command()
async def group_add(ctx, member: discord.Member = None, namee: str = None):
    print(namee)
    print(member)
    if (namee is None or member is None):
            await ctx.send("```Zadejte nazev př. ?group_add '@honza' '3D tisk'```")
    else:
        namee = namee.lower()
        ROLE = discord.utils.get(ctx.guild.roles, name=namee)
        if ROLE.id in [y.id for y in ctx.author.roles]:
            await member.add_roles(ROLE)
            await ctx.send("```Uživatel přidán!```")
        else:
            await ctx.send("```Pouze členové skupiny mohou přidat členy!```")

@bot.command()
async def group_delete(ctx, *, namee: str = None):
    if (namee is None):
            await ctx.send("```Zadejte nazev př. ?group_delete '3D tisk'```")
    else:
        namee = namee.lower()
        ROLE = discord.utils.get(ctx.guild.roles, name=namee)
        if ROLE.id in [y.id for y in ctx.author.roles]:
            
            channel = discord.utils.get(ctx.guild.text_channels, name=namee+"-general")
            await channel.delete()
            channel = discord.utils.get(ctx.guild.voice_channels, name=namee+" Room")
            await channel.delete()
            channel = discord.utils.get(ctx.guild.categories, name=namee)
            await channel.delete()
            await ROLE.delete()

            await ctx.send("```Skupina smazána!```")
        else:
            await ctx.send("```Pouze členové skupiny mohou skupinu smazat!```")

bot.run(TOKEN)