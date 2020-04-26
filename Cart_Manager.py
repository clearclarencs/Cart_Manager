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
    admin_id=int(settings[2])
    bot_token=settings[3]
except:
    print("Failed to import settings, error occured please check.")
    time.sleep(10)
    quit()

client=commands.Bot(command_prefix="")
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

while True:
    amount_type=input("Type or enter \"help\" to learn about types: ")
    if amount_type=="help":
        print("TYPES\nt - Time(a cooldown for cart claiming)\na - Amount(Each member can only claim a set amount of carts per session)\nl - List(User ids go in users.txt and each time that id appears is 1 cart for that user)\nrun - Run without waiting for carts for adding users to users.txt remotely\n----------------------------------------------------------------")
    elif amount_type=="t":
        while True:
            try:
                time_out=int(input("User claim cooldown in seconds: "))
                break
            except:
                print("Not a valid number")
        print("Time Mode\n----------------------------------------------------------------")
        x = threading.Thread(target=cooldown_monitor)
        x.start()
        break
    elif amount_type=="a":
        while True:
            try:
                amount_per=int(input("Amount of carts per member: "))
                break
            except:
                print("Not a valid number")
        print("Amount Mode\n----------------------------------------------------------------")
        break
    elif amount_type=="l":
        try:
            with open("users.txt","r") as r:
                authorised_list=r.read().splitlines()
            #print("Amount of carts authorised: "+str(len(authorised_list)))
        except FileNotFoundError:
            print("No users file found")
        else:
            print("Error occured")
        print("List Mode\n----------------------------------------------------------------")
        break
    elif amount_type=="run":
        break
    else:
        print("Invalid response, retry.")




#Startup program
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game("with carts"))
    global Bots_id
    Bots_id=client.user.id
    if amount_type=="run":
        print("Running but not waiting for carts")
    else:  
        print("Waiting for carts")


#when a cart is recieved
@client.event
async def on_message(message):
    try:
        #ensure cart is in correct channel
        if message.content.startswith("!addlist") and message.author.id==admin_id:
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
        elif message.content.startswith("!purgelist") and message.author.id==admin_id:
            try:
                with open("users.txt","w") as r:
                    r.write("")
                await message.channel.send("Purged\n*Created by Clearclarencs#5659    Not for resale*")
            except:
                await message.channel.send("Error\n*Created by Clearclarencs#5659    Not for resale*")
        elif message.content.startswith("!showlist") and message.author.id==admin_id:
            try:
                with open("users.txt","r") as r:
                    usrs=Counter(r.read().splitlines())
                await message.channel.send(str(usrs)+"\n*Created by Clearclarencs#5659    Not for resale*")
            except:
                await message.channel.send("Error\n*Created by Clearclarencs#5659    Not for resale*")
        elif message.channel.id == wraith_channel_id:
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
                msg, usr = await client.wait_for('reaction_add', check=check)
                userid=usr.id
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
                else:
                    while True:
                        input("Running but not waiting for carts")
    except:
        await cart_message.edit(embed=channel_embed_timeout)
        print("Errrrrr")
        None

client.run(bot_token)