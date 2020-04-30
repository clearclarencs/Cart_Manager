# Cart_Manager
Discord Cart Manager

This program is a discord bot which allows webhook carts such as the ones from wraith and phasma to be distributed to a group. 
When a webhook is sent to the specified channel this bot will send a cart message to the cart channel, the first to react to this message without being blocked by the mode will be messaged the cart webhook for them to purchase.

Settings are stored in cart_manager_settings.txt in the form:
* Bot_webhook_channel_id
* Cart_channel_id
* Manager_ser_id(your user id)
* Discord_bot_token

Modes:
* Time - Sets a cooldown for users to claim carts
* Amount - Amount of carts a user can claim, resets once program closes
* List - Users.txt is used to store users ids and for each instance their id is there is a cart, this can be managed through dming the bot   and a "run" mode was created for you to edit this file through discord without the cart manager running.

Discord commands:
* !addlist x user_id - adds user_id x times to users.txt for list mode\n
* !purgelist - Purges users.txt
* !showlist - prints dictionary of users in user.txt
* !removelist - removes userid form list x times format: !removelist x userid

Dependencies:
Discord.py
Request
