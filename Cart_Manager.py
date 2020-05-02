#Cart manager for wraith
import discord, time, threading
from discord.ext import commands
from datetime import datetime
from datetime import timedelta
from collections import Counter

try:
    with open("cart_manager_settings.txt","r") as r:
        settings=r.read().splitlines()
    wraith_channel_id=int(settings[0])
    cart_channel_id=int(settings[1])
    admin_role_id=int(settings[2])
    bot_token=settings[3]
except:
    print("Failed to import settings, error occured please check.")
    time.sleep(10)
    quit()

client=commands.Bot(command_prefix="")
amount_type="run"
amount_per="0"
time_claimed={}
already_claimed=[]
channel_embed=discord.Embed(title='__CART__', description="React to claim", colour=46336 )
channel_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/703941655992205342/703941970900287538/4UMcNdRKUMuYVANXtHmUVFVMI6hiIdLfd4lNSS-SE-rLFb1XpfnBC8ReI9CoNJwyvUhWBabzvWPUpPW7O0U4IB0EpIZnpx4-_77S.png")
channel_embed_claimed=discord.Embed(title='__CLAIMED__', colour=16711680)
channel_embed_timeout=discord.Embed(title='__TIMED OUT/ERROR__', colour=16711680)

def no():
    if amount_type =="t":
        return discord.Embed(title='__NO__',description="YOU CAN ONLY CLAIM A CART EVERY "+str(time_out)+" SECONDS", colour=0)
    elif amount_type =="a":
        return discord.Embed(title='__NO__',description="YOU CAN NOT CLAIM ANY MORE CARTS FOR THIS DROP", colour=0)
    elif amount_type =="l":
        return discord.Embed(title='__NO__',description="YOU HAVE RAN OUT OF CARTS ON YOUR ACCOUNT", colour=0)


def cooldown_monitor():
    while True:
        now = datetime.now()
        time_now=now.strftime("%H:%M:%S")
        try:
            timeout_now=time_claimed[str(time_now)]
        except KeyError:
            timeout_now=None
        if timeout_now==None:
            time.sleep(0.9)
        else:
            for i in timeout_now:
                time_claimed[str(time_now)]=None
                already_claimed.remove(i)
            time.sleep(0.98)




#Startup program
@client.event
async def on_ready():
    global amount_type
    await client.change_presence(activity=discord.Game("with modes"))
    global Bots_id
    Bots_id=client.user.id


#when a cart is recieved
@client.event
async def on_message(message):
    user=message.author
    global amount_type, authorised_list, already_claimed, time_claimed, time_out, amount_per
    try:
        #ensure cart is in correct channel
        try:
            role = discord.utils.get(message.guild.roles, id=int(admin_role_id))
        except:
            print("Couldnt get roles (error or dmed)")
        if message.content.startswith("help") and role in message.author.roles:
            await message.channel.send("Commands:\n!changemode\n!addlist\n!purgelist\n!showlist\n!removelist\nhelp\nmodes")
        elif message.content.startswith("modes") and role in message.author.roles:
            await message.channel.send("Modes:\nt - Timer mode for a cooldown of claiming carts with a specified time in seconds\na - Amount mode for max number of carts, resets when you change mode\nl - List mode using list edited using commands or Users.txt\nrun - Simply runs the bot without managing carts for you to manage the list between drops")
        elif message.content.startswith("!addlist") and role in message.author.roles:
            try:
                msglist=str(message.content).split(" ")
                if len(msglist)!=3:
                    raise
                int(msglist[2])
                with open("users.txt","a") as r:
                    for i in range(0,int(msglist[1])):
                        r.write(str(msglist[2])+"\n")
                await message.channel.send("Added "+str(msglist[2])+" "+str(msglist[1])+" times.\n*Created by Clearclarencs#5659    Not for resale*")
            except:
                await message.channel.send("Incorrect format, send !add [amount] [user id]\n*Created by Clearclarencs#5659    Not for resale*")
        elif message.content.startswith("!purgelist") and role in message.author.roles:
            try:
                with open("users.txt","w") as r:
                    r.write("")
                await message.channel.send("Purged\n*Created by Clearclarencs#5659    Not for resale*")
            except:
                await message.channel.send("Error\n*Created by Clearclarencs#5659    Not for resale*")
        elif message.content.startswith("!changemode") and role in message.author.roles:
            try:
                msglist=str(message.content).split(" ")
                if msglist[1] in ["t","a","l","run"]:
                    time_claimed={}
                    already_claimed=[]
                    if msglist[1]=="t":
                        amount_type="t"
                        time_out=int(msglist[2])
                        x = threading.Thread(target=cooldown_monitor, args=())
                        x.start()
                        await message.channel.send("Mode changed to: Time\n*Created by Clearclarencs#5659    Not for resale*")
                        await client.change_presence(activity=discord.Game("in timer mode"))
                    elif msglist[1]=="a":
                        amount_type="a"
                        amount_per=int(msglist[2])
                        await message.channel.send("Mode changed to: Amount\n*Created by Clearclarencs#5659    Not for resale*")
                        await client.change_presence(activity=discord.Game("in amount mode"))
                    elif msglist[1]=="l":
                        amount_type="l"
                        with open ("users.txt","r") as r:
                            authorised_list=r.read().splitlines()
                        await message.channel.send("Mode changed to: List\n*Created by Clearclarencs#5659    Not for resale*")
                        await client.change_presence(activity=discord.Game("in list mode"))
                    elif msglist[1]=="run":
                        amount_type="run"
                        await message.channel.send("Mode changed to: Run")
                        await client.change_presence(activity=discord.Game("with modes"))
                    else:
                        raise
                else:
                    raise
            except:
                await message.channel.send("Error, type !changelist [t or a or l or run] [setting if applicable\n*Created by Clearclarencs#5659    Not for resale*")
                print("Error")
        elif message.content.startswith("!showlist") and role in message.author.roles:
            try:
                with open("users.txt","r") as r:
                    usrs=Counter(r.read().splitlines())
                await message.channel.send(str(usrs)+"\n*Created by Clearclarencs#5659    Not for resale*")
            except:
                await message.channel.send("Error\n*Created by Clearclarencs#5659    Not for resale*")
        elif message.content.startswith("!removelist") and role in message.author.roles:
            try:
                msglist=str(message.content).split(" ")
                with open("users.txt","r") as r:
                    usrs=r.read().splitlines()
                for i in range(int(msglist[1])):
                    usrs.remove(str(msglist[2]))
                with open("users.txt","w") as r:
                    r.write("")
                with open("users.txt","a+") as r:
                    for i in usrs:
                        r.write(i+"\n")
                await message.channel.send("Removed "+msglist[2]+" "+msglist[1]+" times.\n*Created by Clearclarencs#5659    Not for resale*")
            except:
                await message.channel.send("Error, try !removelist [amount] [userid]\n*Created by Clearclarencs#5659    Not for resale*")
        elif message.channel.id == wraith_channel_id and amount_type!="run":
            #get the channel
            cart_channel=client.get_channel(cart_channel_id)
            #Send the cart claimer
            cart_message = await cart_channel.send("", embed=channel_embed)
            cart_message_id=str(cart_message).split("Message id=")[1][0:18]
            #print(str(instance)+"-message="+cart_message_id)
            #Add cart reaction
            await cart_message.add_reaction("\U0001F6D2")
            #first 19 may have already claimed
            #function is for the wait_for to ensure reaction is on the correct message
            def check(reaction, user):
                return str(reaction.message.id)==cart_message_id
            for i in range(20):
                #waits for a reaction
                msg, usr = await client.wait_for('reaction_add', check=check, timeout=None)
                userid=usr.id
                print("Inting")
                int(userid)
                print("Inted")
                if int(userid)==int(Bots_id):
                    None
                #Cooldown mode
                elif amount_type=="t":
                    if str(userid) not in already_claimed:
                        try:
                            await cart_message.edit(embed=channel_embed_claimed)
                            dm=client.get_user(userid)
                            await dm.send(embed=message.embeds[0])
                            worked= True
                        except:
                            worked= False
                        if worked:
                            await message.add_reaction("\U00002705")
                            now = datetime.now()
                            now=now + timedelta(seconds=time_out)
                            time_future= now.strftime("%H:%M:%S")
                            try:
                                time_set=time_claimed[str(time_future)]
                            except KeyError:
                                time_set=None
                            if time_set==None:
                                time_claimed[str(time_future)]=[str(userid)]
                            else:
                                time_claimed[time_future].append(str(userid))
                            already_claimed.append(str(userid))
                            i=20
                        break
                    else:
                        #message telling them they need to wait
                        try:
                            dm=client.get_user(userid)
                            await dm.send(embed=no())
                        except:
                            None
                #Amount mode
                elif amount_type=="a":
                    try:
                        time_claimed[userid]
                    except:
                        time_claimed[userid]=0
                    if time_claimed[userid] != amount_per:
                        try:
                            dm=client.get_user(userid)
                            await dm.send(embed=message.embeds[0])
                            await cart_message.edit(embed=channel_embed_claimed)
                            worked= True
                        except:
                            worked= False
                        if worked:
                            await message.add_reaction("\U00002705")
                            try:
                                number_so_far=time_claimed[userid]
                                time_claimed[userid]=number_so_far+1
                            except:
                                time_claimed[userid]=1
                            i=20
                        break
                    else:
                        #message telling them they need to wait
                        try:
                            dm=client.get_user(userid)
                            await dm.send(embed=no())
                        except:
                            None
                elif amount_type=="l":
                    if str(userid) in authorised_list:
                        try:
                            await cart_message.edit(embed=channel_embed_claimed)
                            dm=client.get_user(userid)
                            await dm.send(embed=message.embeds[0])
                            worked= True
                        except:
                            worked= False
                        if worked:
                            await message.add_reaction("\U00002705")
                            authorised_list.remove(str(userid))
                            with open("users.txt","w") as r:
                                r.write("")
                            with open("users.txt","a+") as r:
                                r.write("")
                                for i in authorised_list:
                                    r.write(i+"\n")
                            i=20
                        break
                    else:
                        #message telling them they need to wait
                        try:
                            dm=client.get_user(userid)
                            await dm.send(embed=no())
                        except:
                            print("Could not dm")
                elif amount_type=="run":
                    try:
                        await cart_message.edit(embed=channel_embed_claimed)
                        dm=client.get_user(userid)
                        await dm.send(embed=message.embeds[0])
                        worked= True
                    except:
                        worked= False
                    if worked:
                        await message.add_reaction("\U00002705")
                        i=20
                    break
                else:
                    while True:
                        print("Error")
                        time.sleep(10)
                        quit()
            ow = datetime.now()
            print("Finished"+str(now.strftime("%H:%M:%S")))
    except:
        try:
            await cart_message.edit(embed=channel_embed_timeout)
            print("Errrrrr")
        except:
            print("Error")

client.run(bot_token)
